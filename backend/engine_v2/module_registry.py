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
        # 메모리 캐시 — DB 쿼리 병목 해소
        self._compat_cache: set[tuple[str, str]] | None = None
        self._bridge_cache: dict[tuple[str, str], list[str]] | None = None
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
            # Bridge 체이닝 연결 캐시
            # source → target 방향의 공유 bridge key를 JSON 배열로 저장
            conn.execute("""
                CREATE TABLE IF NOT EXISTS module_bridge_connections (
                    source_module_id TEXT NOT NULL,
                    target_module_id TEXT NOT NULL,
                    bridge_keys      TEXT NOT NULL DEFAULT '[]',  -- JSON 배열
                    updated_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (source_module_id, target_module_id)
                )
            """)
            # combination_metrics: 조합별 성과 이력 (자가 진화 피드백 루프)
            # CLAUDE.md Section 5의 Score 공식 데이터 소스
            conn.execute("""
                CREATE TABLE IF NOT EXISTS combination_metrics (
                    combo_key       TEXT NOT NULL,     -- 정렬된 module_id CSV (예: "mod_a,mod_b")
                    estimated_daps  REAL NOT NULL,
                    measured_daps   REAL,              -- NULL = 아직 BEq 미통과
                    daps_delta      REAL,              -- measured - estimated
                    verdict         TEXT NOT NULL,     -- 'PASS' | 'FAIL' | 'FIX_REQUIRED'
                    fail_reason     TEXT DEFAULT '',   -- 'MATH_ERROR' | 'AMBIGUITY' | 'WRITER_LOOP'
                    attempt_count   INTEGER DEFAULT 1,
                    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (combo_key, created_at)
                )
            """)
            conn.commit()

    # ── DB 초기화 ────────────────────────────────────────────────────────────

    def reset_db(self) -> None:
        """모든 등록 데이터를 삭제하고 클린 슬레이트로 초기화합니다."""
        with sqlite3.connect(self.db_path) as conn:
            for table in ["module_compatibility", "modules",
                          "module_bridge_connections", "combination_metrics"]:
                conn.execute(f"DELETE FROM {table}")
            conn.commit()
        self._modules.clear()

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

            # dict 반환 모듈 호환: 첫 번째 int 값을 정답으로 사용
            if isinstance(ans_a, dict):
                ans_a = next((v for v in ans_a.values() if isinstance(v, (int, float))), 0)
            if isinstance(ans_b, dict):
                ans_b = next((v for v in ans_b.values() if isinstance(v, (int, float))), 0)

            valid_a, reason_a = mod_a.validate_answer(int(ans_a))
            valid_b, reason_b = mod_b.validate_answer(int(ans_b))

            if not valid_a:
                return self._save_compat(a_id, b_id, "INCOMPATIBLE", f"모듈 A 정답 무효: {reason_a}")
            if not valid_b:
                return self._save_compat(a_id, b_id, "INCOMPATIBLE", f"모듈 B 정답 무효: {reason_b}")

        except Exception as e:
            reason = f"실행 오류: {traceback.format_exc(limit=2)}"
            return self._save_compat(a_id, b_id, "INCOMPATIBLE", reason)

        # 4단계: Bridge 연결 탐지 (구조적 검사 — 실행 불필요)
        import json as _json
        keys_a_to_b = list(set(mod_a.META.bridge_output_keys) & set(mod_b.META.bridge_input_accepts))
        keys_b_to_a = list(set(mod_b.META.bridge_output_keys) & set(mod_a.META.bridge_input_accepts))
        self._save_bridge(a_id, b_id, keys_a_to_b)
        self._save_bridge(b_id, a_id, keys_b_to_a)

        if keys_a_to_b or keys_b_to_a:
            direction = f"{a_id}→{b_id}: {keys_a_to_b}" if keys_a_to_b else ""
            rev = f"{b_id}→{a_id}: {keys_b_to_a}" if keys_b_to_a else ""
            bridge_str = " | ".join(filter(None, [direction, rev]))
            print(f"  🔗 Bridge 탐지: {bridge_str}")

        return self._save_compat(a_id, b_id, "COMPATIBLE", "")

    def _save_bridge(self, source_id: str, target_id: str, keys: list) -> None:
        """Bridge 연결 정보를 DB에 저장합니다. 키가 없으면 저장하지 않습니다."""
        if not keys:
            return
        import json as _json
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO module_bridge_connections
                (source_module_id, target_module_id, bridge_keys)
                VALUES (?, ?, ?)
            """, (source_id, target_id, _json.dumps(keys)))
            conn.commit()

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

        tolerance = 5.0  # target ± 5.0 범위 (MASTER 달성을 위해 확장)
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

        # 복합 정렬: Jaccard(기출 연관) + Bridge(구조)
        # History(이력)는 Cold Start에서 비용 대비 효과 없으므로 데이터 축적 후 활성화
        from engine_v2.co_occurrence_matrix import CoOccurrenceMatrix
        _matrix = CoOccurrenceMatrix(db_path=self.db_path)
        if not _matrix.load_from_db():
            _matrix.build_from_problem_map()

        self._load_caches()

        def composite_score(combo: list[str]) -> float:
            # Jaccard 기출 연관 점수 (0~100)
            jaccard = _matrix.combo_jaccard_score(combo) * 100
            # Bridge 구조 보너스 (캐시 사용)
            bridge = sum(
                1 for i in range(len(combo) - 1)
                if self._bridge_cache.get((combo[i], combo[i + 1]))
                or self._bridge_cache.get((combo[i + 1], combo[i]))
            )
            return jaccard * 0.60 + bridge * 40

        candidates.sort(key=composite_score, reverse=True)
        return candidates

    def _load_caches(self) -> None:
        """호환성 + Bridge 데이터를 메모리에 일괄 로드 (최초 1회)."""
        if self._compat_cache is not None:
            return
        self._compat_cache = set()
        self._bridge_cache = {}
        with sqlite3.connect(self.db_path) as conn:
            # 호환 쌍 캐시
            rows = conn.execute(
                "SELECT module_a_id, module_b_id FROM module_compatibility WHERE status='COMPATIBLE'"
            ).fetchall()
            for a, b in rows:
                self._compat_cache.add((a, b))
            # Bridge 캐시
            import json as _json
            rows = conn.execute(
                "SELECT source_module_id, target_module_id, bridge_keys FROM module_bridge_connections"
            ).fetchall()
            for s, t, keys in rows:
                parsed = _json.loads(keys)
                if parsed:
                    self._bridge_cache[(s, t)] = parsed

    def _all_compatible(self, module_ids: list[str]) -> bool:
        """모든 모듈 쌍이 COMPATIBLE인지 확인합니다 (메모리 캐시 사용)."""
        from itertools import combinations
        self._load_caches()
        for a, b in combinations(module_ids, 2):
            if (a, b) not in self._compat_cache and (b, a) not in self._compat_cache:
                return False
        return True

    # ── 피드백 루프: combination_metrics 기록 + Score 공식 ─────────────────

    @staticmethod
    def _combo_key(module_ids: list[str]) -> str:
        """조합의 정규화 키 (정렬된 CSV)."""
        return ",".join(sorted(module_ids))

    def record_outcome(
        self,
        module_ids: list[str],
        estimated_daps: float,
        measured_daps: float | None,
        verdict: str,
        fail_reason: str = "",
        attempt_count: int = 1,
    ) -> None:
        """
        파이프라인 실행 결과를 combination_metrics에 기록합니다.
        Pipeline에서 BEq 판정 후 호출됩니다.
        """
        key = self._combo_key(module_ids)
        delta = (measured_daps - estimated_daps) if measured_daps is not None else None
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO combination_metrics
                (combo_key, estimated_daps, measured_daps, daps_delta, verdict, fail_reason, attempt_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (key, estimated_daps, measured_daps, delta, verdict, fail_reason, attempt_count))
            conn.commit()

    def get_combo_score(
        self, module_ids: list[str], target_daps: float
    ) -> float:
        """
        CLAUDE.md Section 5의 Deterministic Score 공식:
        Score = (P_daps × S_coeff × R_pass) - W_fail

        모든 값은 combination_metrics 이력에서 자동 계산됩니다.
        이력이 없으면 Cold Start 기본값을 사용합니다.
        """
        key = self._combo_key(module_ids)

        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT estimated_daps, measured_daps, daps_delta, verdict, fail_reason
                FROM combination_metrics WHERE combo_key = ?
                ORDER BY created_at DESC
            """, (key,)).fetchall()

        if not rows:
            # Cold Start: 이력 없음 → META 합산으로 추정
            estimated = sum(
                self._modules[mid].META.daps_contribution
                for mid in module_ids if mid in self._modules
            )
            p_daps = max(0, 100 - abs(estimated - target_daps) * 10)
            return p_daps * 1.0 * 0.7  # S_coeff=1.0, R_pass=0.7 (Cold Start)

        # ── P_daps: measured_daps 기반 DAPS 근접도 (최근 5개 평균) ──
        recent_measured = [r[1] for r in rows[:5] if r[1] is not None]
        if recent_measured:
            avg_measured = sum(recent_measured) / len(recent_measured)
        else:
            avg_measured = rows[0][0]  # estimated fallback
        p_daps = max(0, 100 - abs(avg_measured - target_daps) * 10)

        # ── R_pass: historical pass rate ──
        total = len(rows)
        passes = sum(1 for r in rows if r[3] == "PASS")
        r_pass = passes / total if total > 0 else 0.7

        # ── S_coeff: 시너지 계수 (데이터 100개 이상 시 자동 보정) ──
        if total >= 100:
            s_coeff = 0.8 + (r_pass * 0.6)  # 범위: 0.8 ~ 1.4
        else:
            s_coeff = 1.0  # Cold Start

        # ── W_fail: 누적 감점 (상한 -40) ──
        penalty_map = {"MATH_ERROR": -30, "AMBIGUITY": -10, "WRITER_LOOP": -5}
        w_fail = 0
        for r in rows:
            reason = r[4]
            if reason in penalty_map:
                w_fail += penalty_map[reason]
        w_fail = max(w_fail, -40)  # 하한 캡

        score = (p_daps * s_coeff * r_pass) + w_fail
        return round(score, 2)

    def get_bridge_connection(self, source_id: str, target_id: str) -> list[str]:
        """
        source → target 방향으로 전달 가능한 bridge key 목록을 반환합니다.
        Bridge가 없으면 빈 리스트 반환 (메모리 캐시 사용).
        """
        self._load_caches()
        return self._bridge_cache.get((source_id, target_id), [])

    def find_best_chain(self, module_ids: list[str]) -> list[str]:
        """
        주어진 모듈 목록에서 Bridge 연결이 최대화되는 실행 순서를 반환합니다.
        2개 모듈: [A, B] → A→B 또는 B→A 중 bridge 있는 방향 선택
        3개 이상: 체인이 가장 긴 순열 선택 (브루트포스, 모듈 수 제한으로 안전)
        """
        from itertools import permutations
        if len(module_ids) <= 1:
            return module_ids

        best_order, best_score = module_ids, 0
        for perm in permutations(module_ids):
            score = sum(
                1 for i in range(len(perm) - 1)
                if self.get_bridge_connection(perm[i], perm[i + 1])
            )
            if score > best_score:
                best_score, best_order = score, list(perm)
        return best_order

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
