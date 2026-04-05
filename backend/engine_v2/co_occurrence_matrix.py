"""
AI_MathMate V2 -- Jaccard Co-Occurrence Transition Matrix

기출 AIME 1,065문제의 모듈 동시 출현 데이터로부터
Jaccard 연관 계수 + 전이 확률 행렬을 구축합니다.

2-Track 조합 샘플링:
  Track A (exploitation): Jaccard 강화 composite_score 정렬
  Track B (exploration): 마르코프 체인 Random Walk + DAPS 기각 샘플링
"""
from __future__ import annotations
import json
import math
import random
import sqlite3
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any

from engine_v2.config import DB, COMBINATION_SAMPLING

DATA_DIR = Path(__file__).parent / "data"
PROBLEM_MAP_PATH = DATA_DIR / "problem_module_map.json"


class CoOccurrenceMatrix:
    """Jaccard 동시 출현 행렬 + 마르코프 전이 확률."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or DB["v2_path"]
        # co_count[a][b] = 두 모듈이 같은 문제에 등장한 횟수
        self.co_count: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        # 각 모듈이 등장한 문제 수
        self.module_freq: dict[str, int] = defaultdict(int)
        # 전체 문제 수
        self.total_problems: int = 0
        # 등록된 모듈 ID 집합
        self.all_modules: set[str] = set()
        # Jaccard 캐시
        self._jaccard_cache: dict[tuple[str, str], float] = {}
        # 전이 확률 캐시
        self._transition_cache: dict[tuple[str, str], float] = {}

    # ── Phase 1-A: 기출 데이터에서 동시 출현 빈도 추출 ─────────────

    def build_from_problem_map(self, path: str | Path | None = None) -> None:
        """problem_module_map.json에서 행렬을 구축합니다."""
        path = Path(path) if path else PROBLEM_MAP_PATH
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        mappings = data.get("mappings", data if isinstance(data, list) else [])
        self.total_problems = len(mappings)

        # 모듈별 등장 문제 집합 (Jaccard 분모용)
        module_problems: dict[str, set[str]] = defaultdict(set)

        for entry in mappings:
            pid = entry["problem_id"]
            modules = entry.get("modules_used", [])

            for mid in modules:
                self.module_freq[mid] += 1
                self.all_modules.add(mid)
                module_problems[mid].add(pid)

            # 모든 2-쌍 조합의 동시 출현 카운트
            for a, b in combinations(sorted(set(modules)), 2):
                self.co_count[a][b] += 1
                self.co_count[b][a] += 1

        # Jaccard 계수 계산
        self._jaccard_cache.clear()
        self._transition_cache.clear()

        for a in self.all_modules:
            for b in self.all_modules:
                if a == b:
                    continue
                # Jaccard: |A ∩ B| / |A ∪ B|
                both = len(module_problems[a] & module_problems[b])
                either = len(module_problems[a] | module_problems[b])
                j = both / either if either > 0 else 0.0
                self._jaccard_cache[(a, b)] = j

        # 전이 확률 계산 (라플라스 스무딩)
        alpha = COMBINATION_SAMPLING.get("laplace_alpha", 0.01)
        n_modules = len(self.all_modules)

        for a in self.all_modules:
            row_sum = sum(self.co_count[a].values())
            denominator = row_sum + alpha * n_modules
            for b in self.all_modules:
                if a == b:
                    continue
                numerator = self.co_count[a].get(b, 0) + alpha
                self._transition_cache[(a, b)] = numerator / denominator

        # DB에 저장
        self._save_to_db()

    # ── Phase 1-D: DB 저장 ─────────────────────────────────────────

    def _save_to_db(self) -> None:
        """행렬을 SQLite에 캐시합니다."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS co_occurrence_matrix (
                    module_a_id      TEXT NOT NULL,
                    module_b_id      TEXT NOT NULL,
                    co_count         INTEGER DEFAULT 0,
                    jaccard          REAL,
                    transition_prob  REAL,
                    PRIMARY KEY (module_a_id, module_b_id)
                )
            """)
            conn.execute("DELETE FROM co_occurrence_matrix")

            rows = []
            for (a, b), j in self._jaccard_cache.items():
                tp = self._transition_cache.get((a, b), 0.0)
                cc = self.co_count[a].get(b, 0)
                rows.append((a, b, cc, j, tp))

            conn.executemany(
                "INSERT INTO co_occurrence_matrix VALUES (?, ?, ?, ?, ?)",
                rows,
            )
            conn.commit()

    def load_from_db(self) -> bool:
        """DB에서 캐시된 행렬을 로드합니다. 없으면 False."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                rows = conn.execute(
                    "SELECT module_a_id, module_b_id, co_count, jaccard, transition_prob "
                    "FROM co_occurrence_matrix"
                ).fetchall()
            if not rows:
                return False
            for a, b, cc, j, tp in rows:
                self.co_count[a][b] = cc
                self._jaccard_cache[(a, b)] = j
                self._transition_cache[(a, b)] = tp
                self.all_modules.add(a)
                self.all_modules.add(b)
            return True
        except Exception:
            return False

    # ── 조회 API ───────────────────────────────────────────────────

    def get_jaccard(self, a: str, b: str) -> float:
        """두 모듈의 Jaccard 연관 계수를 반환합니다."""
        if a == b:
            return 1.0
        key = (a, b)
        return self._jaccard_cache.get(key, 0.0)

    def get_transition_prob(self, a: str, b: str) -> float:
        """P(b|a) 전이 확률을 반환합니다."""
        return self._transition_cache.get((a, b), 0.0)

    def combo_jaccard_score(self, module_ids: list[str]) -> float:
        """조합 내 모든 인접 쌍의 평균 Jaccard (0~1)."""
        if len(module_ids) < 2:
            return 0.0
        pairs = list(combinations(module_ids, 2))
        total = sum(self.get_jaccard(a, b) for a, b in pairs)
        return total / len(pairs)

    def top_pairs(self, n: int = 10) -> list[tuple[tuple[str, str], float]]:
        """Jaccard 상위 N개 쌍을 반환합니다."""
        items = sorted(self._jaccard_cache.items(), key=lambda x: -x[1])
        # 중복 제거 (a,b)와 (b,a)
        seen = set()
        result = []
        for (a, b), j in items:
            key = tuple(sorted([a, b]))
            if key not in seen:
                seen.add(key)
                result.append(((a, b), j))
            if len(result) >= n:
                break
        return result

    @property
    def nonzero_count(self) -> int:
        """J > 0인 고유 쌍의 수."""
        seen = set()
        for (a, b), j in self._jaccard_cache.items():
            if j > 0:
                seen.add(tuple(sorted([a, b])))
        return len(seen)

    # ── Phase 3: 마르코프 체인 Random Walk (Track B) ────────────────

    def markov_sample(
        self,
        target_daps: float,
        combo_size: int = 2,
        temperature: float | None = None,
        n_samples: int = 10,
        module_daps: dict[str, float] | None = None,
    ) -> list[list[str]]:
        """
        전이 확률 행렬 위에서 마르코프 Random Walk로 조합을 샘플링합니다.

        Args:
            target_daps: 목표 DAPS 점수
            combo_size: 조합 크기 (2 또는 3)
            temperature: softmax 온도 (높을수록 탐색 강화)
            n_samples: 생성할 후보 수
            module_daps: 모듈별 daps_contribution (없으면 DB에서 조회)
        """
        if temperature is None:
            temperature = COMBINATION_SAMPLING.get("exploration_temperature", 1.5)
        tolerance = COMBINATION_SAMPLING.get("daps_rejection_tolerance", 3.0)
        max_attempts = COMBINATION_SAMPLING.get("max_exploration_attempts", 50)

        # 모듈 DAPS 정보 로드
        if module_daps is None:
            module_daps = self._load_module_daps()

        module_list = [m for m in self.all_modules if m in module_daps]
        if not module_list:
            return []

        results: list[list[str]] = []
        attempts = 0

        while len(results) < n_samples and attempts < max_attempts * n_samples:
            attempts += 1
            combo = self._random_walk(module_list, combo_size, temperature)

            # DAPS 기각 샘플링
            est_daps = sum(module_daps.get(m, 3.0) for m in combo)
            if abs(est_daps - target_daps) > tolerance:
                continue

            # 중복 방지
            combo_key = tuple(sorted(combo))
            if combo_key in {tuple(sorted(r)) for r in results}:
                continue

            results.append(combo)

        return results

    def _random_walk(
        self, module_list: list[str], steps: int, temperature: float
    ) -> list[str]:
        """마르코프 체인 1회 Random Walk."""
        # 시작점: 균등 분포
        current = random.choice(module_list)
        path = [current]

        for _ in range(steps - 1):
            # 전이 확률 + temperature softmax
            candidates = [m for m in module_list if m not in path]
            if not candidates:
                break

            probs = []
            for c in candidates:
                tp = self.get_transition_prob(current, c)
                probs.append(tp)

            # Temperature-scaled softmax
            if sum(probs) == 0:
                # 전이 확률이 모두 0이면 균등 분포
                chosen = random.choice(candidates)
            else:
                scaled = [p / temperature for p in probs]
                max_s = max(scaled)
                exp_probs = [math.exp(s - max_s) for s in scaled]
                total = sum(exp_probs)
                normalized = [e / total for e in exp_probs]

                # 가중 랜덤 선택
                r = random.random()
                cumulative = 0.0
                chosen = candidates[-1]
                for c, p in zip(candidates, normalized):
                    cumulative += p
                    if r <= cumulative:
                        chosen = c
                        break

            path.append(chosen)
            current = chosen

        return path

    def _load_module_daps(self) -> dict[str, float]:
        """DB에서 모듈별 daps_contribution을 로드합니다."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                rows = conn.execute(
                    "SELECT module_id, daps_contribution FROM modules"
                ).fetchall()
            return {mid: daps for mid, daps in rows}
        except Exception:
            return {}

    # ── Phase 4-C: 피드백 루프 ─────────────────────────────────────

    def record_new_combination(self, module_ids: list[str], passed: bool) -> None:
        """Track B에서 BEq 통과한 새 조합을 행렬에 반영합니다."""
        if not passed or len(module_ids) < 2:
            return
        # 동시 출현 카운트 +1 (가상 기출)
        for a, b in combinations(sorted(set(module_ids)), 2):
            self.co_count[a][b] += 1
            self.co_count[b][a] += 1
        # 전이 확률 재계산은 비용이 크므로 DB에 카운트만 업데이트
        with sqlite3.connect(self.db_path) as conn:
            for a, b in combinations(sorted(set(module_ids)), 2):
                conn.execute("""
                    UPDATE co_occurrence_matrix
                    SET co_count = co_count + 1
                    WHERE module_a_id = ? AND module_b_id = ?
                """, (a, b))
                conn.execute("""
                    UPDATE co_occurrence_matrix
                    SET co_count = co_count + 1
                    WHERE module_a_id = ? AND module_b_id = ?
                """, (b, a))
            conn.commit()
