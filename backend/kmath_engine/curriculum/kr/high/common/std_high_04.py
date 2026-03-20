import random
from sympy import symbols, expand
from kmath_engine.base import BaseTMaster

class High04_HighOrderEq_Master(BaseTMaster):
    """
    고등 공통수학 - 여러 가지 방정식 (삼차방정식)
    """
    def __init__(self):
        super().__init__("High04_1", "삼차/사차방정식의 풀이")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x = symbols('x')
        
        # 삼차방정식: (x-a)(x-b)(x-c) = 0
        # 간단하게 정수 근 3개
        roots = [random.randint(-5, 5) for _ in range(3)]
        
        # 식 전개
        expr = expand((x - roots[0]) * (x - roots[1]) * (x - roots[2]))
        
        eq_str = str(expr).replace("**", "^").replace("*", "") + " = 0"
        
        # 정답 문자열
        sorted_roots = sorted(roots)
        ans_str = f"x = {sorted_roots[0]}, x = {sorted_roots[1]}, x = {sorted_roots[2]}"
        # 중근 처리
        if len(set(roots)) < 3:
            unique_roots = sorted(list(set(roots)))
            ans_parts = []
            for r in unique_roots:
                count = roots.count(r)
                if count == 1: ans_parts.append(f"x = {r}")
                elif count == 2: ans_parts.append(f"x = {r} (중근)")
                else: ans_parts.append(f"x = {r} (삼중근)")
            ans_str = ", ".join(ans_parts)

        logic_steps = self.get_logic_steps("High04_1")
        
        data = {
            "question": f"다음 삼차방정식을 푸시오.\n${eq_str}$",
            "answer": ans_str,
            "explanation": [
                f"f(x) = ${str(expr).replace('**', '^').replace('*', '')}$ 라 하면",
                f"f({roots[0]}) = 0 이므로 조립제법을 이용하면",
                f"$(x - {roots[0]})(x - {roots[1]})(x - {roots[2]}) = 0$",
                f"따라서 {ans_str}"
            ],
            "logic_steps": logic_steps,
            "strategy": "상수항의 약수 중 대입하여 0이 되는 값을 찾아 조립제법을 사용합니다."
        }
        
        if q_type == "multi":
            # 오답 생성
            options_set = {ans_str}
            while len(options_set) < 4:
                fake_roots = [r + random.randint(-2, 2) for r in roots]
                fake_roots.sort()
                fake_ans = f"x = {fake_roots[0]}, x = {fake_roots[1]}, x = {fake_roots[2]}"
                options_set.add(fake_ans)
            
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High04_SystemEq_Master(BaseTMaster):
    """
    고등 공통수학 - 연립이차방정식
    """
    def __init__(self):
        super().__init__("High04_2", "연립이차방정식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 미지수가 2개인 연립이차방정식
        # Case 1: 일차식 + 이차식
        x_val = random.randint(-5, 5)
        y_val = random.randint(-5, 5)
        
        # x + y = a
        a = x_val + y_val
        eq1 = f"x + y = {a}"
        
        # x^2 + y^2 = b
        b = x_val**2 + y_val**2
        eq2 = f"x^2 + y^2 = {b}"
        
        ans_str = f"x={x_val}, y={y_val}"
        if x_val != y_val:
            ans_str += f" 또는 x={y_val}, y={x_val}"
            
        logic_steps = self.get_logic_steps("High04_2", a=a)
        
        data = {
            "question": f"다음 연립방정식을 푸시오.\n$\\begin{{cases}} {eq1} \\\\ {eq2} \\end{{cases}}$",
            "answer": ans_str,
            "explanation": [
                f"1번 식에서 y = {a} - x 로 놓고 2번 식에 대입하면",
                f"$x^2 + ({a} - x)^2 = {b}$",
                f"정리하여 풀면 x는 {x_val} 또는 {y_val}",
                f"따라서 {ans_str}"
            ],
            "logic_steps": logic_steps,
            "strategy": "일차식이 있으면 한 문자에 대해 정리하여 이차식에 대입하는 대입법을 사용합니다."
        }
        
        if q_type == "multi":
            options_set = {ans_str}
            while len(options_set) < 4:
                fx = x_val + random.randint(-2, 2)
                fy = y_val + random.randint(-2, 2)
                fake = f"x={fx}, y={fy}"
                if fx != fy: fake += f" 또는 x={fy}, y={fx}"
                options_set.add(fake)
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
