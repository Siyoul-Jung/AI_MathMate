"""
AI_MathMate V2 — 삼각함수 대수 (algebra_trigonometry) [Bridge 소스]
sin/cos/tan 항등식, 합성각, 배각 공식을 다룹니다.
bridge_output_keys: ["trig_value", "angle_deg", "identity_type"]
기출 빈도: 72회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


# 정확한 삼각함수 값 테이블 (분모 제거를 위해 유리수 표현)
# (angle_deg, sin_num, sin_den, cos_num, cos_den) — sin = sin_num/sin_den
_EXACT_TABLE = [
    (30, 1, 2, 3, 4),    # sin30=1/2, cos^2=3/4
    (45, 1, 2, 1, 2),    # sin^2=1/2, cos^2=1/2
    (60, 3, 4, 1, 2),    # sin^2=3/4, cos30=1/2 → cos60=1/2
]


class AlgebraTrigonometryModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_trigonometry",
        name="삼각함수 대수",
        domain="integer",
        namespace="alg_trig",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str",
                              description="유형: 'double_angle' | 'sum_angle' | 'identity'"),
            "alpha_deg": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=89,
                                   description="각도 alpha (도)"),
            "beta_deg": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=89,
                                  description="각도 beta (도, sum_angle 모드)"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=20,
                           description="정수 배수 k (정수 변환용)"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=10,
                           description="거듭제곱 지수"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999,
                                description="삼각함수 값의 정수 변환 (mod 1000)"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=5,
        category="algebra",
        tags=["trigonometry", "double_angle", "sum_angle", "identity", "sin", "cos", "tan"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["trig_value", "angle_deg", "identity_type"],
    )

    # ── 핵심 연산 헬퍼 ──────────────────────────────────────────────────────
    @staticmethod
    def _sin(deg: float) -> float:
        return math.sin(math.radians(deg))

    @staticmethod
    def _cos(deg: float) -> float:
        return math.cos(math.radians(deg))

    @staticmethod
    def _tan(deg: float) -> float:
        return math.tan(math.radians(deg))

    # ── generate_seed ────────────────────────────────────────────────────────
    def generate_seed(self, difficulty_hint: float = 7.0) -> dict[str, Any]:
        modes = ["double_angle", "sum_angle", "identity"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "double_angle":
                # sin(2*alpha) 또는 cos(2*alpha) 기반 문제
                alpha = random.choice([15, 18, 20, 30, 36, 45, 54, 60, 72, 75])
                beta = 0
                k = random.randint(50, 500)
                n = random.randint(1, 4) if difficulty_hint >= 9 else random.randint(1, 2)
            elif mode == "sum_angle":
                # sin(alpha+beta) 또는 cos(alpha-beta)
                alpha = random.choice([15, 20, 30, 36, 45])
                beta = random.choice([15, 20, 30, 36, 45])
                if alpha == beta:
                    beta = random.choice([v for v in [15, 20, 30, 36, 45] if v != alpha])
                k = random.randint(50, 500)
                n = 1
            else:
                # sin^2 + cos^2 = 1 변형, tan^2 + 1 = sec^2 등
                alpha = random.choice([30, 45, 60])
                beta = 0
                k = random.randint(100, 800)
                n = random.randint(2, 6) if difficulty_hint >= 9 else random.randint(2, 4)

            seed = {"mode": mode, "alpha_deg": alpha, "beta_deg": beta, "k": k, "n": n}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"mode": "double_angle", "alpha_deg": 30, "beta_deg": 0, "k": 100, "n": 2}

    # ── execute ──────────────────────────────────────────────────────────────
    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]
        alpha = seed["alpha_deg"]
        beta = seed.get("beta_deg", 0)
        k = seed["k"]
        n = seed["n"]

        if mode == "double_angle":
            # 값 = k * sin(2*alpha)^n  (반올림 정수)
            val = k * (self._sin(2 * alpha) ** n)
            return round(abs(val)) % 1000

        elif mode == "sum_angle":
            # 값 = k * (sin(alpha+beta) + cos(alpha-beta))
            val = k * (self._sin(alpha + beta) + self._cos(alpha - beta))
            return round(abs(val)) % 1000

        else:  # identity
            # sin^n(alpha) + cos^n(alpha) 에 k 를 곱함
            val = k * (self._sin(alpha) ** n + self._cos(alpha) ** n)
            return round(abs(val)) % 1000

    # ── Bridge 인터페이스 ─────────────────────────────────────────────────────
    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        """대수적으로 계산된 삼각함수 값을 하류 기하 모듈에 전달합니다."""
        mode = seed["mode"]
        alpha = seed["alpha_deg"]
        beta = seed.get("beta_deg", 0)
        n = seed["n"]

        if mode == "double_angle":
            trig_value = round(self._sin(2 * alpha) ** n * 10000) / 10000
            angle = (2 * alpha) % 360
        elif mode == "sum_angle":
            trig_value = round((self._sin(alpha + beta) + self._cos(alpha - beta)) * 10000) / 10000
            angle = alpha + beta
        else:
            trig_value = round((self._sin(alpha) ** n + self._cos(alpha) ** n) * 10000) / 10000
            angle = alpha

        return {
            "trig_value": trig_value,
            "angle_deg": angle,
            "identity_type": mode,
        }

    # ── get_logic_steps ──────────────────────────────────────────────────────
    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]
        alpha = seed["alpha_deg"]
        beta = seed.get("beta_deg", 0)
        k = seed["k"]
        n = seed["n"]

        if mode == "double_angle":
            return [
                f"1. 배각 공식을 적용합니다: sin(2*{alpha}^\\circ) = 2 sin({alpha}^\\circ) cos({alpha}^\\circ).",
                f"2. sin(2*{alpha}^\\circ)의 정확한 값을 계산합니다.",
                f"3. 결과를 {n}제곱하고 {k}를 곱합니다.",
                f"4. 반올림한 절댓값을 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "sum_angle":
            return [
                f"1. 합성각 공식을 적용합니다: sin({alpha}^\\circ + {beta}^\\circ), cos({alpha}^\\circ - {beta}^\\circ).",
                f"2. sin({alpha + beta}^\\circ) + cos({alpha - beta}^\\circ)의 값을 계산합니다.",
                f"3. {k}를 곱하여 정수로 변환합니다.",
                f"4. 반올림한 절댓값을 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. 항등식 sin^{n}({alpha}^\\circ) + cos^{n}({alpha}^\\circ)을 구합니다.",
                f"2. sin({alpha}^\\circ), cos({alpha}^\\circ)의 정확한 값을 대입합니다.",
                f"3. 거듭제곱을 계산한 뒤 {k}를 곱합니다.",
                f"4. 반올림한 절댓값을 1000으로 나눈 나머지를 구합니다.",
            ]

    # ── verify_with_sympy ────────────────────────────────────────────────────
    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import sin, cos, pi, Rational, N
            mode = seed["mode"]
            alpha = Rational(seed["alpha_deg"]) * pi / 180
            beta = Rational(seed.get("beta_deg", 0)) * pi / 180
            k = seed["k"]
            n = seed["n"]

            if mode == "double_angle":
                val = k * float(N(sin(2 * alpha) ** n))
            elif mode == "sum_angle":
                val = k * float(N(sin(alpha + beta) + cos(alpha - beta)))
            else:
                val = k * float(N(sin(alpha) ** n + cos(alpha) ** n))

            return round(abs(val)) % 1000
        except Exception:
            return None
