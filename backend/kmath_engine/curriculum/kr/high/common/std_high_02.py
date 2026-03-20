import random
from sympy import symbols, Eq, solve, expand, I
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

# ==========================================
# [STD-HIGH-02] 복소수와 이차방정식
# ==========================================

class High02_Quadratic_Master(BaseTMaster):
    """
    고등 수학(상) - 이차방정식의 풀이 (복소수 범위 포함)
    """
    def __init__(self):
        super().__init__("High02", "이차방정식의 풀이")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x = symbols('x')
        root_type = random.choice(['real', 'complex'])
        
        if root_type == 'real':
            alpha = random.randint(-9, 9)
            beta = random.randint(-9, 9)
            while alpha == beta: beta = random.randint(-9, 9)
            
            a = random.choice([1, 2, -1])
            equation_expr = expand(a * (x - alpha) * (x - beta))
            
            ans_str = f"$x = {alpha}$ 또는 $x = {beta}$"
            if alpha > beta: ans_str = f"$x = {beta}$ 또는 $x = {alpha}$"
            
            logic_steps = [
                {
                    "step_id": 1,
                    "description": "인수분해를 시도합니다.",
                    "target_expr": f"${a}(x - {alpha})(x - {beta}) = 0$",
                    "concept_id": "FACTORIZATION"
                },
                {
                    "step_id": 2,
                    "description": "각 인수가 0이 되는 x값을 찾습니다.",
                    "target_expr": f"$x = {alpha}, x = {beta}$",
                    "concept_id": "ZERO_PRODUCT_PROPERTY"
                }
            ]
            
            explanation_list = [
                f"좌변을 인수분해하면 ${a}(x - {alpha})(x - {beta}) = 0$ 입니다.",
                f"따라서 $x - {alpha} = 0$ 또는 $x - {beta} = 0$ 이므로",
                f"정답은 {ans_str} 입니다."
            ]
            strategy = "이차방정식의 해를 구할 때, 먼저 인수분해가 가능한지 확인하는 것이 효율적입니다."
            
        else:
            p = random.randint(-5, 5)
            q = random.randint(1, 5)
            
            equation_expr = expand((x - (p + q*I)) * (x - (p - q*I)))
            
            ans_str = f"$x = {p} \\pm {q}i$"
            if p == 0: ans_str = f"$x = \\pm {q}i$"
            
            b_coeff = -2 * p
            c_coeff = p**2 + q**2
            discriminant = b_coeff**2 - 4 * 1 * c_coeff
            
            logic_steps = [
                {
                    "step_id": 1,
                    "description": "판별식을 확인합니다.",
                    "target_expr": f"$D = ({b_coeff})^2 - 4(1)({c_coeff}) = {discriminant}$",
                    "concept_id": "DISCRIMINANT"
                },
                {
                    "step_id": 2,
                    "description": "근의 공식을 적용합니다.",
                    "target_expr": f"$x = \\frac{{-({b_coeff}) \\pm \\sqrt{{{discriminant}}}}}{{2}}$",
                    "concept_id": "QUADRATIC_FORMULA"
                },
                {
                    "step_id": 3,
                    "description": "근호 안의 음수를 허수단위 i로 표현하여 정리합니다.",
                    "target_expr": ans_str,
                    "concept_id": "COMPLEX_NUMBER_SIMPLIFICATION"
                }
            ]
            
            explanation_list = [
                f"판별식 $D = {b_coeff}^2 - 4(1)({c_coeff}) = {discriminant}$",
                f"근의 공식에 대입하면 $x = \\frac{{-({b_coeff}) \\pm \\sqrt{{{discriminant}}}}}{{2}}$",
                f"$\\sqrt{{{discriminant}}} = \\sqrt{{{abs(discriminant)}}}i = {q*2}i$ 이므로",
                f"정답은 {ans_str} 입니다."
            ]
            strategy = "계수가 실수인 이차방정식에서 판별식 D < 0 이면 서로 다른 두 허근을 갖습니다."

        eq_str = str(equation_expr).replace("**", "^").replace("*", "") + " = 0"
        
        data = {
            "question": f"다음 이차방정식의 해를 구하시오.\n${eq_str}$",
            "answer": ans_str,
            "explanation": explanation_list,
            "logic_steps": logic_steps,
            "strategy": strategy
        }
        
        if q_type == "multi":
            options_set = {ans_str}
            if root_type == 'real':
                def make_opt(r1, r2):
                    if r1 > r2: r1, r2 = r2, r1
                    return f"x = {r1} 또는 x = {r2}"
                candidates = [(-alpha, -beta), (alpha, -beta), (-alpha, beta), (alpha + 1, beta + 1)]
                for r1, r2 in candidates:
                    options_set.add(make_opt(r1, r2))
                while len(options_set) < 4:
                    options_set.add(make_opt(random.randint(-9, 9), random.randint(-9, 9)))
            else:
                def make_complex_opt(rp, rq):
                    return f"x = {rp} ± {rq}i" if rp != 0 else f"x = ± {rq}i"
                candidates = [(-p, q), (p, q + 1), (p, q - 1 if q > 1 else q + 2)]
                for rp, rq in candidates:
                    options_set.add(make_complex_opt(rp, rq))
                while len(options_set) < 4:
                    options_set.add(make_complex_opt(random.randint(-5, 5), random.randint(1, 5)))
            
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)
