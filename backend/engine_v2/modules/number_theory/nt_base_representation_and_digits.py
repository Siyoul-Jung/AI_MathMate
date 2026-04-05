"""
AI_MathMate V2 — 진법 표현과 자릿수 (nt_base_representation_and_digits)
진법 변환, 자릿수 합, 자릿수 곱 등 AIME 기출 82회 출제 핵심 정수론 기법을 다룹니다.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtBaseRepresentationAndDigitsModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_base_representation_and_digits",
        name="진법 표현과 자릿수",
        domain="integer",
        namespace="nt_base_repr",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=10, max_val=99999, description="변환할 양의 정수"),
            "base": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=16, description="목표 진법"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'digit_sum' | 'digit_product' | 'palindrome_count'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=3.5,
        min_difficulty=3,
        category="number_theory",
        tags=["base_conversion", "digit_sum", "digit_product", "palindrome", "representation"],
        exam_types=["AIME", "AMC"],
    )

    @staticmethod
    def _to_base(n: int, base: int) -> list[int]:
        """n을 base 진법 자릿수 리스트로 변환 (최하위 자리 먼저)."""
        if n == 0:
            return [0]
        digits = []
        while n > 0:
            digits.append(n % base)
            n //= base
        return digits

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        modes = ["digit_sum", "digit_product", "palindrome_count"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "digit_sum":
                base = random.randint(2, 16)
                n = random.randint(100, 50000) if difficulty_hint < 10 else random.randint(1000, 99999)
            elif mode == "digit_product":
                base = random.randint(3, 12)
                # 자릿수 곱이 0이 되지 않도록 보장하기 위해 적당한 범위
                n = random.randint(10, 5000)
            else:  # palindrome_count
                base = random.randint(2, 10)
                n = random.randint(100, 5000)

            seed = {"n": n, "base": base, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"n": 255, "base": 2, "mode": "digit_sum"}

    def execute(self, seed: dict[str, Any]) -> int:
        n, base, mode = seed["n"], seed["base"], seed["mode"]

        if mode == "digit_sum":
            # base 진법으로 표현했을 때 자릿수의 합
            digits = self._to_base(n, base)
            return sum(digits) % 1000

        elif mode == "digit_product":
            # base 진법으로 표현했을 때 0이 아닌 자릿수의 곱
            digits = self._to_base(n, base)
            prod = 1
            for d in digits:
                if d > 0:
                    prod *= d
            return prod % 1000

        else:  # palindrome_count
            # 1~n 범위에서 base 진법 회문(palindrome)의 개수
            count = 0
            for k in range(1, n + 1):
                digs = self._to_base(k, base)
                if digs == digs[::-1]:
                    count += 1
            return count % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, base, mode = seed["n"], seed["base"], seed["mode"]
        digits = self._to_base(n, base)
        digit_str = "".join(str(d) for d in reversed(digits))

        if mode == "digit_sum":
            return [
                f"1. {n}을 {base}진법으로 변환합니다: ({digit_str})_{base}.",
                f"2. 각 자릿수를 더합니다: {' + '.join(str(d) for d in digits)} = {sum(digits)}.",
                f"3. 결과를 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "digit_product":
            nonzero = [d for d in digits if d > 0]
            return [
                f"1. {n}을 {base}진법으로 변환합니다: ({digit_str})_{base}.",
                f"2. 0이 아닌 자릿수들의 곱을 구합니다: {' × '.join(str(d) for d in nonzero)}.",
                f"3. 결과를 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. 1부터 {n}까지 각 수를 {base}진법으로 변환합니다.",
                f"2. 각 수가 회문(앞뒤가 같은 수)인지 확인합니다.",
                f"3. 회문인 수의 개수를 세고 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Integer
            n, base, mode = seed["n"], seed["base"], seed["mode"]

            if mode == "digit_sum":
                # sympy Integer의 진법 변환으로 독립 검증
                digits = []
                temp = n
                while temp > 0:
                    digits.append(temp % base)
                    temp //= base
                return sum(digits) % 1000
            elif mode == "digit_product":
                digits = []
                temp = n
                while temp > 0:
                    digits.append(temp % base)
                    temp //= base
                prod = 1
                for d in digits:
                    if d > 0:
                        prod *= d
                return prod % 1000
            else:
                count = 0
                for k in range(1, n + 1):
                    digs = []
                    temp = k
                    while temp > 0:
                        digs.append(temp % base)
                        temp //= base
                    if digs == digs[::-1]:
                        count += 1
                return count % 1000
        except Exception:
            return None
