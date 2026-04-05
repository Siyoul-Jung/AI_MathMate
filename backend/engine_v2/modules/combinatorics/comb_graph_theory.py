"""
AI_MathMate V2 — 그래프 이론 (comb_graph_theory)
AIME 기출 2회 UNMAPPED으로 발견된 기법.
완전 그래프의 오일러 경로, 토너먼트 해밀턴 경로, 삼각형(3-cycle) 카운팅을 다룹니다.
"""
from __future__ import annotations
import random
import math
from itertools import permutations
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombGraphTheoryModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_graph_theory",
        name="그래프 이론 (경로, 토너먼트, 오일러)",
        domain="integer",
        namespace="comb_graph",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=4, max_val=44, description="정점 수"),
            "mode": FieldSpec(dtype=str, domain="str", description="'euler_path' | 'tournament_count' | 'complete_graph'"),
            "adj": FieldSpec(dtype=list, domain="list", description="인접행렬 (tournament_count용)"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999),
        },
        logic_depth=4,
        daps_contribution=5.0,
        min_difficulty=8,
        category="combinatorics",
        tags=["graph_theory", "eulerian_path", "tournament", "directed_graph", "adjacency", "hamiltonian"],
        exam_types=["AIME"],
        bridge_output_keys=["vertex_count", "edge_count"],
        bridge_input_accepts=["n_sides", "n_elements"],
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["euler_path", "tournament_count", "complete_graph"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "euler_path":
                # K_n에 오일러 회로가 존재하려면 모든 정점 차수가 짝수 → n이 홀수
                n = random.choice([5, 7, 9, 11, 13, 15, 17, 19, 21])
                if difficulty_hint >= 12:
                    n = random.choice([23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43])
                adj = []
            elif mode == "tournament_count":
                # n팀 토너먼트에서 해밀턴 경로 수 (n <= 6으로 제한, 완전 열거 가능)
                n = random.randint(4, 6)
                # 랜덤 토너먼트 생성: adj[i][j] = 1이면 i가 j를 이김
                adj = [[0] * n for _ in range(n)]
                for i in range(n):
                    for j in range(i + 1, n):
                        if random.random() < 0.5:
                            adj[i][j] = 1
                        else:
                            adj[j][i] = 1
            else:  # complete_graph
                # K_n의 삼각형 수 = C(n, 3), n <= 18이면 C(18,3) = 816 < 999
                n = random.randint(4, 18) if difficulty_hint < 12 else random.randint(10, 18)
                adj = []

            seed = {"n": n, "mode": mode, "adj": adj}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"n": 5, "mode": "complete_graph", "adj": []}

    def execute(self, seed: dict[str, Any]) -> int:
        n, mode = seed["n"], seed["mode"]

        if mode == "euler_path":
            # K_n 간선 수 = n(n-1)/2, 홀수 n이면 오일러 회로 존재
            edges = n * (n - 1) // 2
            return edges % 1000

        elif mode == "tournament_count":
            # n팀 토너먼트에서 해밀턴 경로 수를 완전 열거
            adj = seed["adj"]
            count = 0
            for perm in permutations(range(n)):
                # perm[0] → perm[1] → ... → perm[n-1] 이 유효한 해밀턴 경로인지
                valid = True
                for i in range(len(perm) - 1):
                    if adj[perm[i]][perm[i + 1]] != 1:
                        valid = False
                        break
                if valid:
                    count += 1
            return count % 1000

        else:  # complete_graph
            # K_n의 삼각형(3-cycle) 수 = C(n, 3)
            return math.comb(n, 3) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        n = seed["n"]
        return {
            "vertex_count": n,
            "edge_count": n * (n - 1) // 2,
        }

    def generate_seed_with_bridge(
        self, bridge: dict[str, Any], difficulty_hint: float = 10.0
    ) -> dict[str, Any]:
        """상위 모듈의 n_sides 또는 n_elements를 정점 수로 활용."""
        n_candidate = bridge.get("n_sides") or bridge.get("n_elements")
        if n_candidate is not None and 4 <= int(n_candidate) <= 18:
            n = int(n_candidate)
            return {"n": n, "mode": "complete_graph", "adj": []}
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, mode = seed["n"], seed["mode"]

        if mode == "euler_path":
            return [
                f"1. 완전그래프 K_{n}의 각 정점의 차수는 {n - 1}입니다.",
                f"2. 모든 정점의 차수가 {'짝수' if (n - 1) % 2 == 0 else '홀수'}이므로 "
                f"오일러 {'회로가 존재합니다' if (n - 1) % 2 == 0 else '경로 조건을 확인합니다'}.",
                f"3. K_{n}의 간선 수 = {n}({n}-1)/2 = {n * (n - 1) // 2}를 구합니다.",
                f"4. 최종 답을 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "tournament_count":
            return [
                f"1. {n}팀 라운드로빈 토너먼트의 인접행렬을 분석합니다.",
                f"2. 해밀턴 경로: 모든 팀을 정확히 한 번씩 방문하는 경로를 찾습니다.",
                f"3. {n}! = {math.factorial(n)}개의 순열을 검사하여 유효한 해밀턴 경로 수를 셉니다.",
                f"4. 유효한 경로 수를 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. 완전그래프 K_{n}에서 3개의 정점을 선택하면 반드시 삼각형을 이룹니다.",
                f"2. 삼각형의 수 = C({n}, 3) = {n}!/(3!({n}-3)!)를 계산합니다.",
                f"3. C({n}, 3) = {math.comb(n, 3)}을 구합니다.",
                f"4. 최종 답을 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            n, mode = seed["n"], seed["mode"]

            if mode == "euler_path":
                from sympy import binomial
                return int(binomial(n, 2)) % 1000

            elif mode == "tournament_count":
                # 동일하게 완전 열거하되, 독립 구현
                adj = seed["adj"]
                count = 0
                for perm in permutations(range(n)):
                    if all(adj[perm[i]][perm[i + 1]] == 1 for i in range(n - 1)):
                        count += 1
                return count % 1000

            else:  # complete_graph
                from sympy import binomial
                return int(binomial(n, 3)) % 1000
        except Exception:
            return None
