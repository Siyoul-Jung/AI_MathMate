"""
AI_MathMate V2 — ModuleRegistry
원자 모듈의 등록, 호환성 자동 테스트, 조합 선택을 담당합니다.

[핵심 기능]
1. 모듈 등록 시 자동으로 기존 모든 모듈과 호환성 테스트 실행
2. DAPS 점수 기반 조합 후보 필터링
3. 테스트 결과를 DB에 캐싱하여 중복 테스트 방지
"""

from __future__ import annotations
import sqlite3
import traceback
from pathlib import Path
from typing import Optional

from engine_v2.modules.base_module import (
    AtomicModule,
    check_namespace_conflict,
    check_domain_compatibility,
    check_answer_scale_compatibility,
)
from engine_v2.config import DB, PIPELINE


# ─── ModuleRegistry ─────────────────────────────────────────────────────────

class ModuleRegistry:
    """
    모든 원자 모듈을 관리하는 중앙 레지스트리.
    싱글턴 패턴으로 사용합니다: registry = ModuleRegistry.get_instance()
    """

    _instance: Optional[ModuleRegistry] = None
    _modules: dict[str, AtomicModule] = {}

    def __init__(self, db_path: str = DB["v2_path"]):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._modules: dict[str, AtomicModule] = {}
        self._init_db()

    @classmethod
    def get_instance(cls) -> ModuleRegistry:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # ── DB 초기화 ────────────────────────────────────────────────────────────

    def _init_db(self):
        """호환성 캐시 테이블 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS module_compatibility (
                    module_a_id     TEXT NOT NULL,
                    module_b_id     TEXT NOT NULL,
                    status          TEXT NOT NULL,   -- 'COMPATIBLE' | 'INCOMPATIBLE'
                    conflict_reason TEXT DEFAULT '',
                    tested_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (module_a_id, module_b_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS modules (
                    module_id       TEXT PRIMARY KEY,
                    name            TEXT NOT NULL,
                    category        TEXT NOT NULL,
                    domain          TEXT NOT NULL,
                    namespace       TEXT NOT NULL UNIQUE,
                    logic_depth     INTEGER NOT NULL,
                    daps_contribution REAL NOT NULL,
                    min_difficulty  INTEGER NOT NULL,
                    exam_types      TEXT NOT NULL,   -- JSON 배열
                    registered_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    # ── 모듈 등록 ────────────────────────────────────────────────────────────

    def register(self, module: AtomicModule) -> dict:
        """
        모듈을 레지스트리에 등록하고, 기존 모든 모듈과 호환성 테스트를 실행합니다.
        :return: {"registered": bool, "compatibility_results": dict}
        """
        mid = module.META.module_id

        # 1. 모듈 DB에 저장
        import json
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO modules
                (module_id, name, category, domain, namespace, logic_depth,
                 daps_contribution, min_difficulty, exam_types)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mid,
                module.META.name,
                module.META.category,
                module.META.domain,
                module.META.namespace,
                module.META.logic_depth,
                module.META.daps_contribution,
                module.META.min_difficulty,
                json.dumps(module.META.exam_types),
            ))
            conn.commit()

        # 2. 기존 모든 모듈과 자동 호환성 테스트
        compat_results = {}
        for existing_id, existing_module in self._modules.items():
            result = self._run_compatibility_test(module, existing_module)
            compat_results[existing_id] = result

        # 3. 레지스트리에 추가
        self._modules[mid] = module
        print(f"✅ 모듈 등록: {mid} | 호환성 테스트: {len(compat_results)}개 완료")

        return {
            "registered": True,
            "module_id": mid,
            "compatibility_results": compat_results,
        }

    # ── 호환성 테스트 ────────────────────────────────────────────────────────

    def _run_compatibility_test(
        self, mod_a: AtomicModule, mod_b: AtomicModule
    ) -> dict:
        """
        두 모듈 간 3단계 호환성 테스트를 실행합니다.
        [3단계 타입 계약 — 실행 기반 검사]
        """
        a_id, b_id = mod_a.META.module_id, mod_b.META.module_id

        # 1단계: 네임스페이스 충돌 검사
        ok, reason = check_namespace_conflict(mod_a, mod_b)
        if not ok:
            return self._save_compat(a_id, b_id, "INCOMPATIBLE", reason)

        # 2단계: 도메인 호환성 검사 (integer ↔ real)
        ok, reason = check_domain_compatibility(mod_a, mod_b)
        if not ok:
            return self._save_compat(a_id, b_id, "INCOMPATIBLE", reason)

        # 3단계: 실행 기반 테스트 (실제 시드 생성 후 정답 계산)
        try:
            seed_a = mod_a.generate_seed(difficulty_hint=12.0)
            seed_b = mod_b.generate_seed(difficulty_hint=12.0)

            ans_a = mod_a.execute(seed_a)
            ans_b = mod_b.execute(seed_b)

            valid_a, reason_a = mod_a.validate_answer(ans_a)
            valid_b, reason_b = mod_b.validate_answer(ans_b)

            if not valid_a:
                return self._save_compat(a_id, b_id, "INCOMPATIBLE", f"모듈 A 정답 무효: {reason_a}")
            if not valid_b:
                return self._save_compat(a_id, b_id, "INCOMPATIBLE", f"모듈 B 정답 무효: {reason_b}")

            return self._save_compat(a_id, b_id, "COMPATIBLE", "")

        except Exception as e:
            reason = f"실행 오류: {traceback.format_exc(limit=2)}"
            return self._save_compat(a_id, b_id, "INCOMPATIBLE", reason)

    def _save_compat(self, a_id: str, b_id: str, status: str, reason: str) -> dict:
        """호환성 결과를 DB에 저장합니다."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO module_compatibility
                (module_a_id, module_b_id, status, conflict_reason)
                VALUES (?, ?, ?, ?)
            """, (a_id, b_id, status, reason))
            # 대칭 저장 (A↔B, B↔A 동일)
            conn.execute("""
                INSERT OR REPLACE INTO module_compatibility
                (module_a_id, module_b_id, status, conflict_reason)
                VALUES (?, ?, ?, ?)
            """, (b_id, a_id, status, reason))
            conn.commit()

        icon = "✅" if status == "COMPATIBLE" else "❌"
        print(f"  {icon} {a_id} ↔ {b_id}: {status}" + (f" ({reason[:60]})" if reason else ""))
        return {"status": status, "reason": reason}

    # ── 조합 후보 필터링 (Architect 에이전트용) ──────────────────────────────

    def get_compatible_combinations(
        self,
        target_daps: float,
        combination_size: int = 2,
        exam_type: str = "AIME",
    ) -> list[list[str]]:
        """
        DAPS 목표 점수에 맞는 호환 가능한 모듈 조합 후보를 반환합니다.
        Architect 에이전트가 이 후보 중 최종 1개를 선택합니다.

        :param target_daps: 목표 DAPS 점수
        :param combination_size: 조합할 모듈 수 (2 또는 3)
        :return: 호환 가능한 모듈 ID 조합 리스트
        """
        from itertools import combinations

        tolerance = 1.5  # target ± 1.5 범위
        eligible = [
            mid for mid, mod in self._modules.items()
            if exam_type in mod.META.exam_types
        ]

        candidates = []
        for combo in combinations(eligible, combination_size):
            # 1. 모든 쌍이 COMPATIBLE인지 확인
            all_compat = self._all_compatible(list(combo))
            if not all_compat:
                continue

            # 2. 예상 DAPS 점수 계산
            estimated_daps = sum(
                self._modules[mid].META.daps_contribution for mid in combo
            )
            if abs(estimated_daps - target_daps) > tolerance:
                continue

            candidates.append(list(combo))

        return candidates

    def _all_compatible(self, module_ids: list[str]) -> bool:
        """모든 모듈 쌍이 COMPATIBLE인지 확인합니다."""
        from itertools import combinations
        with sqlite3.connect(self.db_path) as conn:
            for a, b in combinations(module_ids, 2):
                row = conn.execute("""
                    SELECT status FROM module_compatibility
                    WHERE module_a_id = ? AND module_b_id = ?
                """, (a, b)).fetchone()
                if not row or row[0] != "COMPATIBLE":
                    return False
        return True

    # ── 조회 유틸 ────────────────────────────────────────────────────────────

    def get_module(self, module_id: str) -> Optional[AtomicModule]:
        return self._modules.get(module_id)

    def list_modules(self) -> list[str]:
        return list(self._modules.keys())

    def count(self) -> int:
        return len(self._modules)

    def print_summary(self):
        print(f"\n{'='*50}")
        print(f"ModuleRegistry: {self.count()}개 모듈 등록됨")
        for mid, mod in self._modules.items():
            print(f"  [{mod.META.category:12s}] {mid:35s} depth={mod.META.logic_depth} DAPS={mod.META.daps_contribution:.1f}")
        print(f"{'='*50}\n")
