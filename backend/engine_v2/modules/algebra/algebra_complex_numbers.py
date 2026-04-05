"""
AI_MathMate V2 — 복소수 연산 (algebra_complex_numbers)
z^n = w, 드무아브르 정리, 복소수 절대값, 편각, 단위근 등을 다룹니다.
기출 빈도: 58회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraComplexNumbersModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_complex_numbers",
        name="복소수 연산",
        domain="complex",
        namespace="alg_complex",
        input_schema={
            "re1": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20, description="첫 번째 복소수 실수부"),
            "im1": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20, description="첫 번째 복소수 허수부"),
            "re2": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20, description="두 번째 복소수 실수부"),
            "im2": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20, description="두 번째 복소수 허수부"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=12, description="거듭제곱 지수 또는 단위근 차수"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'power_mod' | 'unit_roots_sum' | 'product_abs'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답 mod 1000"),
        },
        logic_depth=5,
        daps_contribution=4.5,
        min_difficulty=5,
        category="algebra",
        tags=["complex_numbers", "de_moivre", "roots_of_unity", "modulus", "argument"],
        exam_types=["AIME"],
        bridge_output_keys=["modulus_squared", "argument_degrees"],
        bridge_input_accepts=["root_abs_sum", "polynomial_degree"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["power_mod", "unit_roots_sum", "product_abs"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "power_mod":
                # |z^n|^2 where z = re1 + im1*i
                re1 = random.randint(-10, 10)
                im1 = random.randint(-10, 10)
                if re1 == 0 and im1 == 0:
                    continue
                n = random.randint(2, 8) if difficulty_hint < 10 else random.randint(4, 12)
                re2, im2 = 0, 0
            elif mode == "unit_roots_sum":
                # n-th 단위근 중 실수부가 양수인 것들의 실수부 합 * 1000 반올림
                n = random.randint(3, 12)
                re1, im1, re2, im2 = 0, 0, 0, 0
            else:  # product_abs
                # |z1 * z2|^2 where z1 = re1+im1*i, z2 = re2+im2*i
                re1 = random.randint(-12, 12)
                im1 = random.randint(-12, 12)
                re2 = random.randint(-12, 12)
                im2 = random.randint(-12, 12)
                if (re1 == 0 and im1 == 0) or (re2 == 0 and im2 == 0):
                    continue
                n = 1

            seed = {"re1": re1, "im1": im1, "re2": re2, "im2": im2, "n": n, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"re1": 3, "im1": 4, "re2": 1, "im2": 2, "n": 2, "mode": "power_mod"}

    def execute(self, seed: dict[str, Any]) -> int:
        re1 = seed["re1"]
        im1 = seed["im1"]
        re2 = seed["re2"]
        im2 = seed["im2"]
        n = seed["n"]
        mode = seed["mode"]

        if mode == "power_mod":
            # |z^n|^2 = (|z|^2)^n = (re1^2 + im1^2)^n
            mod_sq = re1 * re1 + im1 * im1
            result = mod_sq ** n
            return result % 1000

        elif mode == "unit_roots_sum":
            # n-th 단위근: e^{2*pi*i*k/n} for k=0..n-1
            # 실수부가 양수인 단위근들의 실수부 합을 100배하여 반올림
            total = 0.0
            for k in range(n):
                cos_val = math.cos(2 * math.pi * k / n)
                if cos_val > 1e-9:
                    total += cos_val
            # 100을 곱하고 반올림하여 정수화
            result = round(total * 100)
            return abs(result) % 1000

        else:  # product_abs
            # |z1 * z2|^2 = |z1|^2 * |z2|^2
            mod1_sq = re1 * re1 + im1 * im1
            mod2_sq = re2 * re2 + im2 * im2
            result = mod1_sq * mod2_sq
            return result % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        re1, im1, n, mode = seed["re1"], seed["im1"], seed["n"], seed["mode"]
        mod_sq = re1 * re1 + im1 * im1
        if re1 == 0 and im1 == 0:
            arg_deg = 0
        else:
            arg_deg = round(math.degrees(math.atan2(im1, re1)))
        return {
            "modulus_squared": mod_sq,
            "argument_degrees": arg_deg,
        }

    def generate_seed_with_bridge(
        self, bridge: dict[str, Any], difficulty_hint: float = 8.0
    ) -> dict[str, Any]:
        """poly_complex_roots의 root_abs_sum을 re1^2+im1^2 힌트로 활용."""
        root_abs_sum = bridge.get("root_abs_sum")
        poly_degree = bridge.get("polynomial_degree")

        # root_abs_sum을 modulus_squared의 목표값으로 사용
        target_mod_sq = int(root_abs_sum) if root_abs_sum is not None else None
        n = int(poly_degree) if poly_degree is not None and 2 <= int(poly_degree) <= 12 else random.randint(2, 8)

        if target_mod_sq is not None and 2 <= target_mod_sq <= 400:
            # re1^2 + im1^2 = target_mod_sq가 되도록 (re1, im1) 탐색
            for re1 in range(0, int(target_mod_sq ** 0.5) + 1):
                rem = target_mod_sq - re1 * re1
                if rem < 0:
                    break
                im1_sq = rem
                im1 = int(im1_sq ** 0.5)
                if im1 * im1 == im1_sq and im1 > 0:
                    # 부호 랜덤화
                    re1 = re1 * random.choice([-1, 1]) if re1 != 0 else re1
                    im1 = im1 * random.choice([-1, 1])
                    seed = {"re1": re1, "im1": im1, "re2": 0, "im2": 0, "n": n, "mode": "power_mod"}
                    ans = self.execute(seed)
                    if 0 <= ans <= 999:
                        return seed

        # 폴백
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        re1, im1, re2, im2, n, mode = (
            seed["re1"], seed["im1"], seed["re2"], seed["im2"], seed["n"], seed["mode"],
        )
        if mode == "power_mod":
            mod_sq = re1 * re1 + im1 * im1
            return [
                f"1. z = {re1} + {im1}i의 절대값의 제곱 |z|^2 = {re1}^2 + {im1}^2 = {mod_sq}를 구합니다.",
                f"2. 드무아브르 정리에 의해 |z^{n}|^2 = (|z|^2)^{n} = {mod_sq}^{n}입니다.",
                f"3. {mod_sq}^{n}을 계산합니다.",
                f"4. 결과를 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "unit_roots_sum":
            return [
                f"1. {n}차 단위근 e^(2*pi*i*k/{n}) (k = 0, 1, ..., {n - 1})을 나열합니다.",
                f"2. 각 단위근의 실수부 cos(2*pi*k/{n})를 계산합니다.",
                f"3. 실수부가 양수인 단위근만 선별하여 실수부의 합을 구합니다.",
                f"4. 합에 100을 곱하고 반올림하여 정수화한 후 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            mod1_sq = re1 * re1 + im1 * im1
            mod2_sq = re2 * re2 + im2 * im2
            return [
                f"1. z1 = {re1} + {im1}i, z2 = {re2} + {im2}i를 정의합니다.",
                f"2. |z1|^2 = {mod1_sq}, |z2|^2 = {mod2_sq}를 계산합니다.",
                f"3. |z1 * z2|^2 = |z1|^2 * |z2|^2 = {mod1_sq} * {mod2_sq} = {mod1_sq * mod2_sq}입니다.",
                f"4. 결과를 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            re1, im1, re2, im2, n, mode = (
                seed["re1"], seed["im1"], seed["re2"], seed["im2"], seed["n"], seed["mode"],
            )

            if mode == "power_mod":
                mod_sq = re1 * re1 + im1 * im1
                return (mod_sq ** n) % 1000

            elif mode == "unit_roots_sum":
                from sympy import cos, pi, Rational, N
                total = 0.0
                for k in range(n):
                    cos_val = float(N(cos(2 * pi * k / n)))
                    if cos_val > 1e-9:
                        total += cos_val
                return abs(round(total * 100)) % 1000

            else:  # product_abs
                mod1_sq = re1 * re1 + im1 * im1
                mod2_sq = re2 * re2 + im2 * im2
                return (mod1_sq * mod2_sq) % 1000
        except Exception:
            return None
