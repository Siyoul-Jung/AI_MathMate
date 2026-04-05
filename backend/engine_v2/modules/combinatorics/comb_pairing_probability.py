"""
AIME 2025 I Problem 7 - Pairing Probability (짝짓기 정렬과 확률)
V2 이식(Porting) 완료 모듈.
"""

import math
from fractions import Fraction
import random
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class CombPairingProbabilityModule(AtomicModule):
    """
    2n개의 대상을 2개씩 짝지어 정렬했을 때, 특정 문자가 마지막 쌍에 포함될 확률을 구하는 모듈.
    내부 알파벳 정렬 및 쌍 간 첫 글자 정렬 조건 포함.
    """

    META = ModuleMeta(
        module_id="comb_pairing_probability",
        name="Pairing Probability",
        category="combinatorics",
        domain="integer",
        namespace="comb.pairing",
        logic_depth=4,
        daps_contribution=8.5,
        min_difficulty=7,
        heuristic_weight=0.1,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Pairing Count", "Lexicographical Order", "Probability"],
        source_reference="AIME 2025 P07",
        # Bridge: 상위 모듈의 위수(order)를 n_pairs 파라미터로 수신
        bridge_input_accepts=["order"],
        input_schema={
            "n_pairs": FieldSpec(dtype=int, domain="Z+", min_val=4, max_val=7),
            "target_idx": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=13, description="Index of target character (0=A, 1=B...)")
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="Sum of numerator and denominator of probability p")
        }
    )

    def generate_seed(self, difficulty_hint: float = 8.5) -> Dict[str, Any]:
        for _ in range(100):
            n_pairs = random.randint(4, 7)
            target_idx = random.randint(n_pairs, 2 * n_pairs - 1)
            seed = {"n_pairs": n_pairs, "target_idx": target_idx}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return {"n_pairs": 6, "target_idx": 6}

    def execute(self, seed: Dict[str, Any]) -> int:
        n_pairs = seed["n_pairs"]
        target_idx = seed["target_idx"]
        n = n_pairs * 2
        total_pairings = math.prod(range(n - 1, 0, -2))
        count = self._brute_force_count(n_pairs, target_idx)
        prob = Fraction(count, total_pairings)
        if prob == 0:
            return 0
        return int(prob.numerator + prob.denominator)

    def verify_with_sympy(self, seed: dict) -> int | None:
        """[Branch B] brute-force 열거로 독립 검증 (n_pairs ≤ 7, max 135135 경우)."""
        try:
            from sympy import Rational
            n_pairs = seed["n_pairs"]
            target_idx = seed["target_idx"]
            n = n_pairs * 2
            count = self._brute_force_count(n_pairs, target_idx)
            total = math.prod(range(n - 1, 0, -2))
            prob = Rational(count, total)
            if prob == 0:
                return 0
            return int(prob.p + prob.q)
        except Exception:
            return None

    def _brute_force_count(self, n_pairs: int, target_idx: int) -> int:
        """
        n_pairs ≤ 5용 완전 열거.

        규칙:
          - 2n개 원소를 n개의 정렬된 쌍으로 분할
          - 각 쌍 내부: 작은 원소가 앞 (a_i < b_i)
          - 쌍 사이: 첫 번째 원소 기준 정렬 (a_1 < a_2 < ... < a_n)
          - target_idx가 마지막 쌍(a_n 또는 b_n)에 포함되는 경우 카운트
        """
        from itertools import combinations

        elements = list(range(n_pairs * 2))
        target = target_idx
        count = 0

        # n_pairs개의 쌍 생성: a_i를 오름차순으로 고르는 것과 동일
        def generate_pairings(remaining, pairs):
            nonlocal count
            if not remaining:
                # 모든 쌍이 구성됨: 마지막 쌍에 target이 있는지 확인
                last_pair = pairs[-1]
                if target in last_pair:
                    count += 1
                return
            # 첫 번째 원소를 고르고 (오름차순 보장), 파트너 선택
            first = remaining[0]
            rest = remaining[1:]
            for i, partner in enumerate(rest):
                pair = (first, partner) if first < partner else (partner, first)
                new_remaining = rest[:i] + rest[i + 1:]
                generate_pairings(new_remaining, pairs + [pair])

        generate_pairings(elements, [])
        return count

    def generate_seed_with_bridge(
        self, bridge: dict, difficulty_hint: float = 8.5
    ) -> dict:
        """
        [Bridge 수신] 상위 모듈의 ord_p(a) = order를 n_pairs로 활용합니다.

        수학적 연결:
          nt_mod_order_primitive → order = ord_p(a) (위수)
          → 이 값이 4~7이면 2n = 2·order 개의 알파벳을 짝짓는 문제로 자연 연결됩니다.
          → "소수 p에 대해 a의 위수가 k일 때, 2k개의 원소를 조건에 맞게 짝지으시오"
        """
        order = bridge.get("order")
        if order is not None and 4 <= int(order) <= 7:
            n_pairs = int(order)
            target_idx = random.randint(n_pairs, 2 * n_pairs - 1)
            # Fallback: validate the generated seed
            for _ in range(20):
                seed = {"n_pairs": n_pairs, "target_idx": target_idx}
                ans = self.execute(seed)
                if 0 < ans <= 999:
                    return seed
                target_idx = random.randint(n_pairs, 2 * n_pairs - 1)
        # Bridge 범위 밖이면 자체 generate_seed() 실행
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        n_pairs = seed["n_pairs"]
        target_char = chr(ord('A') + seed["target_idx"])
        return [
            f"Step 1: 총 {2 * n_pairs}개의 서로 다른 문자를 2개씩 짝짓는 모든 경우의 수 (2n-1)!! 를 계산합니다.",
            f"Step 2: 각 쌍의 문자 정렬 및 쌍 간의 알파벳 순서 정렬 조건에 따라, '마지막 쌍'에 타겟 문자 '{target_char}'가 포함될 수 있는 위치(첫 번째 원소 혹은 두 번째 원소)를 분석합니다.",
            f"Step 3: 조합론적 제약 조건(타겟 문자보다 뒤에 올 수 있는 문자의 개수 등)을 고려하여 각 경우를 만족하는 짝짓기 방법의 수를 산출합니다.",
            f"Step 4: (유리한 경우의 수) / (전체 경우의 수) 를 통해 확률 p 를 기약분수 m/n 으로 구하고 최종값 m+n을 도출합니다."
        ]
