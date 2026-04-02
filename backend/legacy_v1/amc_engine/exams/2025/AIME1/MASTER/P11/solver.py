import sympy as sp
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "ALG-PERIODIC-PARABOLA",
        "categories": ["Algebra"],
        "topics": ["Periodic Functions", "Parabola Intersections", "Vieta's Sum of Roots"],
        "context_type": "abstract",
        "level": 11,
        "has_image": True,
        "is_mock_ready": True,
        "seed_constraints": {
            "P": {"min_val": 1, "max_val": 2, "type": "int", "description": "Period scale (Period = 4P)"},
            "K": {"min_val": 20, "max_val": 60, "type": "int", "description": "Parabola coefficient x = Ky^2"}
        },
        "logic_steps": [
            {"step": 1, "title": "함수의 주기성 분석", "description": "f(x)가 주기 4P인 톱니 모양의 함수임을 파악하고 일반적인 구간별 식을 정의."},
            {"step": 2, "title": "교점의 방정식 수립", "description": "x = Ky^2과 y = f(x)를 연립하여 구간별 이차방정식 유도."},
            {"step": 3, "title": "y좌표 합 계산", "description": "근의 공식을 통해 각 구간에서의 교점 존재 여부를 판단하고 y좌표들의 합을 산출."},
            {"step": 4, "title": "결과 정규화", "description": "합을 (a + b*sqrt(c))/d 형태로 정리하고 a+b+c+d를 최종 정답으로 기록."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def compute_exact_answer(cls, K, P):
        y_sym = sp.Symbol('y', real=True)
        intersections = []
        max_k = math.ceil(K * P / 4.0) + 1
        for k in range(-max_k, max_k + 1):
            sols1 = sp.solve(K*y_sym**2 - y_sym - 4*k*P, y_sym)
            for sol in sols1:
                if 4*k*P - P - 1e-7 <= K * float(sol.evalf())**2 <= 4*k*P + P + 1e-7:
                    intersections.append(sol)
            sols2 = sp.solve(K*y_sym**2 + y_sym - P*(4*k + 2), y_sym)
            for sol in sols2:
                if 4*k*P + P - 1e-7 <= K * float(sol.evalf())**2 <= 4*k*P + 3*P + 1e-7:
                    intersections.append(sol)
        total_y = sp.simplify(sum(intersections))
        return total_y

    @classmethod
    def get_abcd(cls, expr):
        from sympy import fraction, sqrt, Add, Mul, S
        expr = sp.together(expr)
        num, den = fraction(expr)
        den = int(den)
        terms = Add.make_args(sp.expand(num))
        a, b, c = 0, 0, 1
        for term in terms:
            if term.is_rational: a = int(term)
            else:
                args = Mul.make_args(term)
                coeff, radical = 1, 1
                for arg in args:
                    if arg.is_rational: coeff *= arg
                    elif arg.is_Pow and arg.exp == S.Half: radical *= arg.base
                    else: return None
                b, c = int(coeff), int(radical)
        return int(a + abs(b) + c + den)

    @classmethod
    def generate_seed(cls):
        for _ in range(50):
            P = random.choice([1, 2])
            K = random.randint(10, 60)
            ans_expr = cls.compute_exact_answer(K, P)
            final_ans = cls.get_abcd(ans_expr)
            if final_ans is not None and 0 < final_ans < 1000:
                return {'K': K, 'P': P, 'expected_t': final_ans}
        return {'K': 34, 'P': 1, 'expected_t': 259}

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            seed['target_x'] = random.randint(5, 50)
            seed['expected_t'] = float(seed['target_x'] % (4*seed['P'])) # Simplified for L1
            return seed
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Sawtooth Periodicity",
                "goal": "Understand the piecewise periodic function definition.",
                "details": "주어진 전개식 형태의 주기 함수 f(x)의 함숫값을 특정 지점에서 구하는 기초 상황을 설정하세요."
            }
        elif level == 2:
            return {
                "focus": "Functional Equation",
                "goal": "Solve f(x) = y for multiple solutions in an interval.",
                "details": "주기 함수와 특정 상수 값의 교점들의 합을 구하는 과정을 유도하세요."
            }
        return {
            "focus": "Geometric Intersection",
            "goal": "Find the sum of y-coordinates of intersections with a parabola.",
            "details": "톱니 함수 f(x)와 포물선 x = Ky^2의 모든 교점의 y좌표 합을 구하고 무리수 계수들의 합(a+b+c+d)을 구하는 AIME 스타일로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        return f"A periodic function $f(x)$ has period ${4*seed['P']}$ and is defined as $f(x)=x$ on $[-{seed['P']}, {seed['P']}]$ and $f(x)={2*seed['P']}-x$ on $[{seed['P']}, {3*seed['P']}]$. Find the sum of $y$-coordinates of all points of intersection of $y = f(x)$ and $x = {seed['K']}y^2$. Result in form (a+b*sqrt(c))/d."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Let $f(x) = x$ if $-{seed['P']} \\le x < {seed['P']}$, $f(x) = {2*seed['P']} - x$ if ${seed['P']} \\le x < {3*seed['P']}$, and $f(x+{4*seed['P']}) = f(x)$. Evaluate $f({seed['target_x']})$."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def generate_image(cls, seed, filepath):
        """
        Generates a visualization of the sawtooth function and the parabola.
        """
        K, P = seed['K'], seed['P']
        
        # Define the sawtooth function f(x)
        def f(x):
            period = 4 * P
            x_mod = (x + P) % period - P
            if x_mod < P: return x_mod
            return 2 * P - x_mod

        # Domain for x
        # Intersections occur for x = Ky^2. Min x = 0.
        # Max x is where y = 1 or something. Actually let's look at k range.
        # Let's plot from -2P to 20P to see the pattern
        x_vals = np.linspace(-P, 16 * P, 1000)
        y_f = [f(x) for x in x_vals]
        
        # Parabola: x = Ky^2 => y = sqrt(x/K)
        y_p = np.sqrt(x_vals[x_vals >= 0] / K)
        y_p_neg = -np.sqrt(x_vals[x_vals >= 0] / K)
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Plot sawtooth
        ax.plot(x_vals, y_f, color='#3b82f6', linewidth=2, label='$y=f(x)$', alpha=0.8)
        
        # Plot parabola parts
        ax.plot(x_vals[x_vals >= 0], y_p, color='#ef4444', linewidth=2, label='$x=Ky^2$', alpha=0.8)
        ax.plot(x_vals[x_vals >= 0], y_p_neg, color='#ef4444', linewidth=2, alpha=0.8)
        
        # Styling
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.set_ylim(-1.5 * P, 1.5 * P)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.set_title(f"AIME P11: Periodic Function & Parabola (K={K})", fontsize=10)

        plt.tight_layout()
        plt.savefig(filepath, dpi=150, transparent=True)
        plt.close(fig)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        if seed.get('drill_level', 3) == 3:
            if str(seed['K']) not in narrative: return False, "K missing"
        return True, "OK"
