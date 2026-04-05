"""
AI_MathMate V2 -- meta_anonymization (변수 익명화 전략)
문제의 변수명을 표준형(a, b, n)에서 익명형(x_1, alpha, mu)으로 치환하여
학생이 패턴 매칭으로 풀이 전략을 유추하는 것을 방지합니다.
DAPS의 delta(Heuristic/Trap) 성분을 직접 상승시킵니다.
"""
from __future__ import annotations
import random
import hashlib
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class MetaAnonymizationModule(AtomicModule):
    META = ModuleMeta(
        module_id="meta_anonymization",
        name="변수 익명화 전략 (Variable Anonymization)",
        domain="integer",
        namespace="meta_anon",
        input_schema={
            "target_vars": FieldSpec(dtype=list, domain="VarNames", description="익명화할 변수명 목록"),
            "anonymization_style": FieldSpec(dtype=str, domain=["greek", "subscript", "abstract"],
                                              description="익명화 스타일"),
        },
        output_schema={
            "var_mapping": FieldSpec(dtype=dict, domain="str->str", description="원래 변수명 -> 익명 변수명 매핑"),
            "daps_bonus": FieldSpec(dtype=float, domain="R+", description="익명화로 인한 DAPS 보너스"),
        },
        logic_depth=3,
        daps_contribution=2.5,
        min_difficulty=10,
        category="meta",
        tags=["anonymization", "variable_hiding", "pattern_break", "heuristic_trap"],
        v2_strategy_tags=["anonymize"],
    )

    # 익명 변수 풀
    _GREEK = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
              "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma", "tau"]
    _SUBSCRIPT = ["x_1", "x_2", "x_3", "y_1", "y_2", "y_3", "z_1", "z_2",
                  "w_1", "w_2", "u_1", "v_1"]
    _ABSTRACT = ["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                 "f(k)", "g(j)", "h(m)"]

    def generate_seed(self, difficulty_hint: float = 11.0) -> dict[str, Any]:
        styles = ["greek", "subscript", "abstract"]
        target_vars = random.sample(["a", "b", "c", "n", "m", "k", "p", "q", "r"], k=random.randint(2, 5))
        style = random.choice(styles)
        return {
            "target_vars": target_vars,
            "anonymization_style": style,
        }

    def execute(self, seed: dict[str, Any]) -> int:
        """변수 개수 × 스타일 가중치 기반 결정론적 전략 점수."""
        target_vars = seed["target_vars"]
        style = seed["anonymization_style"]
        style_weight = {"greek": 3, "subscript": 2, "abstract": 5}
        n = len(target_vars)
        # 변수명의 해시합으로 결정론적 값 생성
        var_hash = sum(ord(c) for v in target_vars for c in v)
        return (n * style_weight.get(style, 1) * 37 + var_hash) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        """전략 데이터를 bridge로 전달."""
        target_vars = seed["target_vars"]
        style = seed["anonymization_style"]
        pool = {"greek": self._GREEK, "subscript": self._SUBSCRIPT, "abstract": self._ABSTRACT}[style][:]
        mapping = {var: pool[i % len(pool)] for i, var in enumerate(target_vars)}
        return {"var_mapping": mapping, "daps_bonus": min(2.0, len(target_vars) * 0.4)}

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        bridge = self.get_bridge_output(seed)
        mapping = bridge.get("var_mapping", {})
        style = seed["anonymization_style"]
        return [
            f"1. 대상 변수 {seed['target_vars']}의 표준 이름에서 '{style}' 스타일로 치환합니다.",
            f"2. 매핑: {', '.join(f'{k}->{v}' for k, v in mapping.items())}.",
            f"3. 치환된 변수명으로 지문을 재구성하여 패턴 매칭 풀이를 차단합니다.",
        ]
