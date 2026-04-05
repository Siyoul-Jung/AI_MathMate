"""
AI_MathMate V2 — 위수와 원시근 (nt_mod_order_primitive)
모듈러 연산에서 원소의 위수(Order)와 원시근(Primitive Root) 존재성을 분석하며 고난도 이산 로그 문제를 위한 기반을 제공합니다.
기존 nt_order_and_primitive_roots 모듈의 기능을 통합하고 고난도 정수론 지능의 밀도를 높입니다.
"""
from __future__ import annotations
import random
import sympy as sp
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class NTModOrderPrimitiveModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_mod_order_primitive",
        name="위수와 원시근 (Advanced)",
        domain="integer",
        namespace="nt_mod_order",
        input_schema={
            "p": FieldSpec(dtype=int, domain="Primes", description="법 소수 p"),
            "a": FieldSpec(dtype=int, domain="[2, p-1]", description="위수를 구할 밑 a"),
            "is_primitive_root": FieldSpec(dtype=bool, domain="bool", description="원시근 판정 여부")
        },
        output_schema={
            "order": FieldSpec(dtype=int, domain="[1, p-1]", description="a의 모듈로 p에 대한 위수 ord_p(a)"),
            "primitive_roots_count": FieldSpec(dtype=int, domain="Z+", description="p의 원시근 개수 phi(phi(p))")
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=12,
        category="number_theory",
        tags=["modular_arithmetic", "order", "primitive_root", "euler_totient"],
        # Bridge: 이 모듈이 산출하는 위수(order)·소수(prime)를 하류 모듈에 전달
        bridge_output_keys=["order", "prime", "base", "primitive_roots_count"],
    )

    def generate_seed(self, difficulty_hint: float = 12.0) -> dict[str, Any]:
        p = sp.nextprime(random.randint(11, 101))
        # 난이도에 따라 법 p의 크기를 조절 (AIME급은 대개 작거나 특별한 성질을 가짐)
        if difficulty_hint >= 14:
            p = sp.nextprime(random.randint(103, 331))
            
        a = random.randint(2, p - 1)
        return {
            "p": int(p),
            "a": int(a),
            "is_primitive_root": random.choice([True, False])
        }

    def execute(self, seed: dict[str, Any]) -> int:
        p, a = seed["p"], seed["a"]

        # ord_p(a) + phi(phi(p)) 를 최종 답으로
        order = int(sp.ntheory.residue_ntheory.n_order(a, p))
        phi_phi_p = int(sp.totient(p - 1))

        return (order + phi_phi_p) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        """
        [Bridge 출력] 이 모듈이 산출한 위수·소수를 하류 모듈(예: comb_pairing_probability)에 전달합니다.

        전달 값:
          - order: ord_p(a) — 하류 모듈의 n_pairs 파라미터로 활용 가능 (4~7 범위 시)
          - prime: 법 소수 p
          - base: 밑 a
          - primitive_roots_count: φ(φ(p))
        """
        p, a = seed["p"], seed["a"]
        order = int(sp.ntheory.residue_ntheory.n_order(a, p))
        phi_phi_p = int(sp.totient(p - 1))
        return {
            "order": order,
            "prime": p,
            "base": a,
            "primitive_roots_count": phi_phi_p,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        p, a = seed["p"], seed["a"]
        return [
            f"1. 모듈로 {p}에 대한 오일러 피 함수 phi({p}) = {p-1}를 계산합니다.",
            f"2. {a}의 거듭제곱 중 1과 합동이 되는 최소의 지수 k (위수)를 찾습니다.",
            f"3. {a}^k ≡ 1 (mod {p})를 만족하는 k가 {p-1}의 약수임을 이용하여 위수를 확정합니다.",
            f"4. 만약 위수가 {p-1}과 같다면 {a}는 모듈로 {p}의 원시근입니다."
        ]
