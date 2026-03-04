import random
from sympy import symbols, Eq, solve, expand
from core.base import BaseTMaster
from core.math_utils import MathUtils

# ==========================================
# [STD-HIGH-03] 이차방정식과 이차함수
# ==========================================

class High03_QuadFunc_Eq_Master(BaseTMaster):
    """
    이차함수의 그래프와 x축의 위치 관계 (판별식 활용)
    """
    def __init__(self):
        super().__init__("High03_1", "이차함수와 x축의 위치 관계")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # y = x^2 + 2ax + b
        # x축과의 교점 개수 -> D = (2a)^2 - 4b의 부호
        
        a = random.randint(-5, 5)
        b = random.randint(-10, 10)
        
        # D/4 = a^2 - b
        discriminant_quarter = a**2 - b
        
        if discriminant_quarter > 0:
            ans = "서로 다른 두 점에서 만난다"
            count = 2
        elif discriminant_quarter == 0:
            ans = "한 점에서 만난다 (접한다)"
            count = 1
        else:
            ans = "만나지 않는다"
            count = 0
            
        func_str = f"$y = x^2 + {2*a}x + {b}$" if a != 0 else f"$y = x^2 + {b}$"
        if 2*a < 0: func_str = func_str.replace("+ -", "- ")
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "이차함수의 그래프와 x축의 교점의 개수는 이차방정식 $x^2 + 2ax + b = 0$의 실근의 개수와 같습니다.",
                "target_expr": f"$x^2 + {2*a}x + {b} = 0$",
                "concept_id": "QUAD_FUNC_EQ_RELATION"
            },
            {
                "step_id": 2,
                "description": "판별식 D/4를 계산하여 부호를 확인합니다.",
                "target_expr": f"$D/4 = ({a})^2 - ({b}) = {discriminant_quarter}$",
                "concept_id": "DISCRIMINANT_CHECK"
            },
            {
                "step_id": 3,
                "description": "판별식의 부호에 따라 위치 관계를 판단합니다. (D>0: 2개, D=0: 1개, D<0: 0개)",
                "target_expr": "",
                "concept_id": "DETERMINE_POSITION"
            }
        ]
        
        data = {
            "question": f"이차함수 {func_str} 의 그래프와 x축의 위치 관계를 말하시오.",
            "answer": ans,
            "explanation": [f"판별식 $D/4 = {discriminant_quarter}$", f"$D/4 {' > ' if discriminant_quarter > 0 else (' = ' if discriminant_quarter == 0 else ' < ')} 0$ 이므로 {ans}"],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = ["서로 다른 두 점에서 만난다", "한 점에서 만난다 (접한다)", "만나지 않는다", "알 수 없다"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High03_QuadFunc_MaxMin_Master(BaseTMaster):
    """
    이차함수의 최대/최소 (제한된 범위 포함)
    """
    def __init__(self):
        super().__init__("High03_2", "이차함수의 최대/최소")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # y = a(x-p)^2 + q
        a = random.choice([1, -1, 2, -2])
        p = random.randint(-3, 3)
        q = random.randint(-5, 5)
        
        # 전개형: y = ax^2 - 2apx + (ap^2 + q)
        b = -2 * a * p
        c = a * p**2 + q
        
        func_str = f"$y = {a}x^2 + {b}x + {c}$"
        func_str = func_str.replace("+ -", "- ").replace("1x", "x").replace("-1x", "-x")
        if b == 0: func_str = func_str.replace(" + 0x", "").replace(" - 0x", "")
        
        # 범위 설정 (p를 포함하거나 포함하지 않도록)
        range_type = random.choice(["include_p", "exclude_p"])
        if range_type == "include_p":
            start = p - random.randint(1, 3)
            end = p + random.randint(1, 3)
        else:
            if random.choice([True, False]): # p보다 오른쪽
                start = p + 1
                end = p + random.randint(2, 4)
            else: # p보다 왼쪽
                end = p - 1
                start = end - random.randint(1, 3)
                
        # 최대/최소 계산
        vals = [a*(x-p)**2 + q for x in [start, end, p] if start <= x <= end]
        max_val = max(vals)
        min_val = min(vals)
        
        target = "최댓값" if random.choice([True, False]) else "최솟값"
        ans = max_val if target == "최댓값" else min_val
        
        # 표준형 수식 포맷팅 (y = a(x-p)^2 + q)
        # a 처리
        if a == 1: a_str = ""
        elif a == -1: a_str = "-"
        else: a_str = str(a)
        
        # p 처리
        if p > 0: sq_term = f"(x - {p})^2"
        elif p < 0: sq_term = f"(x + {abs(p)})^2"
        else: sq_term = "x^2"
        
        # q 처리
        if q > 0: q_str = f"+ {q}"
        elif q < 0: q_str = f"- {abs(q)}"
        else: q_str = ""
        
        std_expr = f"y = {a_str}{sq_term} {q_str}".strip()
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "이차함수를 표준형 $y = a(x-p)^2 + q$ 꼴로 변형하여 꼭짓점을 찾습니다.",
                "target_expr": "",
                "concept_id": "STANDARD_FORM"
            },
            {
                "step_id": 2,
                "description": "주어진 범위의 양 끝값과 꼭짓점(범위 내에 있을 경우)에서의 함숫값을 계산합니다.",
                "target_expr": "",
                "concept_id": "EVALUATE_BOUNDARY"
            },
            {
                "step_id": 3,
                "description": "계산된 값 중 가장 큰 값(최댓값) 또는 가장 작은 값(최솟값)을 찾습니다.",
                "target_expr": "",
                "concept_id": "COMPARE_VALUES"
            }
        ]
        
        data = {
            "question": f"$x$의 범위가 ${start} \\le x \\le {end}$ 일 때, 이차함수 {func_str} 의 {target}을 구하시오.",
            "answer": f"${ans}$",
            "explanation": [f"표준형: $y = {a}(x - {p})^2 + {q}$", f"범위 내 함숫값 비교: ${vals}$", f"따라서 {target}은 ${ans}$"],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = [f"${d}$" for d in MathUtils.generate_distractors(ans, 3, 5)] + [f"${ans}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)