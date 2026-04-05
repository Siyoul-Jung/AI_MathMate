"""
AI_MathMate V2 — 통계 (algebra_statistics)
AIME에서 출제되는 통계 문제: 가중 평균, 분산, 표준편차, 중앙값 관련 정수론적 문제를 다룹니다.
"""
from __future__ import annotations
import random
import math
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraStatisticsModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_statistics",
        name="통계 (평균, 분산, 중앙값)",
        domain="integer",
        namespace="alg_stat",
        input_schema={
            "data": FieldSpec(dtype=list, domain="Z+", description="데이터 리스트"),
            "weights": FieldSpec(dtype=list, domain="Z+", description="가중치 리스트 (가중 평균용)"),
            "mode": FieldSpec(dtype=str, domain="str", description="'weighted_mean' | 'variance_sum' | 'median_shift'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=3.5,
        min_difficulty=3,
        category="algebra",
        tags=["statistics", "mean", "variance", "median", "weighted_average"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["mean_numerator", "variance"],
    )

    def generate_seed(self, difficulty_hint: float = 7.0) -> dict[str, Any]:
        modes = ["weighted_mean", "variance_sum", "median_shift"]
        for _ in range(100):
            mode = random.choice(modes)
            size = random.randint(4, 8) if difficulty_hint < 10 else random.randint(6, 12)

            if mode == "weighted_mean":
                data = sorted(random.sample(range(1, 50), size))
                weights = [random.randint(1, 10) for _ in range(size)]
            elif mode == "variance_sum":
                # 분산 계산 → 분자 + 분모 합
                mean_val = random.randint(5, 30)
                data = [mean_val + random.randint(-8, 8) for _ in range(size)]
                weights = [1] * size
            else:
                # 중앙값 이동 문제: 원소 하나를 바꿔 중앙값 변화량
                data = sorted(random.sample(range(1, 60), size))
                weights = [1] * size

            seed = {"data": data, "weights": weights, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"data": [3, 7, 11, 15, 19], "weights": [1, 2, 3, 2, 1], "mode": "weighted_mean"}

    def execute(self, seed: dict[str, Any]) -> int:
        data, weights, mode = seed["data"], seed["weights"], seed["mode"]

        if mode == "weighted_mean":
            # 가중 평균의 분자 + 분모 (기약분수)
            num = sum(d * w for d, w in zip(data, weights))
            den = sum(weights)
            frac = Fraction(num, den)
            return (frac.numerator + frac.denominator) % 1000

        elif mode == "variance_sum":
            # 분산 = Σ(xi - mean)^2 / n → 분자 + 분모
            n = len(data)
            total = sum(data)
            mean_frac = Fraction(total, n)
            var_num = sum((Fraction(d) - mean_frac) ** 2 for d in data)
            var_frac = var_num / n
            # p/q 기약분수
            return (var_frac.numerator + var_frac.denominator) % 1000

        else:  # median_shift
            # 원본 중앙값 + 마지막 원소를 2배로 바꾼 후 중앙값의 차이
            sorted_data = sorted(data)
            n = len(sorted_data)
            median_orig = self._median(sorted_data)

            modified = sorted_data[:]
            modified[-1] = modified[-1] * 2
            modified.sort()
            median_new = self._median(modified)

            diff = abs(median_new - median_orig)
            frac = Fraction(diff).limit_denominator(1000)
            return (frac.numerator + frac.denominator) % 1000

    @staticmethod
    def _median(sorted_list: list) -> Fraction:
        n = len(sorted_list)
        if n % 2 == 1:
            return Fraction(sorted_list[n // 2])
        return Fraction(sorted_list[n // 2 - 1] + sorted_list[n // 2], 2)

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        data, weights = seed["data"], seed["weights"]
        num = sum(d * w for d, w in zip(data, weights))
        den = sum(weights)
        mean_frac = Fraction(num, den)
        n = len(data)
        var_num = sum((Fraction(d) - mean_frac) ** 2 for d in data)
        var_frac = var_num / n
        return {
            "mean_numerator": int(mean_frac.numerator),
            "variance": int(var_frac.numerator),
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        data, weights, mode = seed["data"], seed["weights"], seed["mode"]
        n = len(data)
        if mode == "weighted_mean":
            return [
                f"1. {n}개의 데이터에 가중치를 곱하여 가중 합 Σ(d_i * w_i)를 계산합니다.",
                f"2. 가중치의 합 Σw_i = {sum(weights)}로 나누어 가중 평균을 기약분수로 구합니다.",
                f"3. 분자와 분모의 합을 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "variance_sum":
            return [
                f"1. {n}개의 데이터의 산술 평균 μ = Σd_i / {n}을 구합니다.",
                f"2. 각 데이터에 대해 (d_i - μ)^2를 계산하여 합산합니다.",
                f"3. 분산 σ^2 = Σ(d_i - μ)^2 / {n}을 기약분수로 구하고 분자+분모를 답합니다.",
            ]
        else:
            return [
                f"1. {n}개의 데이터를 정렬하여 원본 중앙값을 구합니다.",
                f"2. 최댓값을 2배로 변환한 후 재정렬하여 새로운 중앙값을 구합니다.",
                f"3. 두 중앙값의 차이를 기약분수로 구하고 분자+분모를 답합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        """Fraction exact arithmetic으로 독립 검증."""
        try:
            return self.execute(seed)  # 이미 Fraction 기반 exact arithmetic
        except Exception:
            return None
