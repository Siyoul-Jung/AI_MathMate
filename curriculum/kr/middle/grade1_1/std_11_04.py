import random
from fractions import Fraction
from core.math_utils import MathUtils
from core.base import BaseTMaster

# ==========================================
# [STD-11-04] 유리수의 사칙계산 (T21 ~ T28)
# ==========================================

class T21_Master(BaseTMaster):
    """T21: 유리수의 덧셈과 뺄셈"""
    def __init__(self):
        super().__init__("T21", "유리수의 덧셈/뺄셈")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        limit = 5 if difficulty == "Easy" else (20 if difficulty == "Hard" else 10)
        
        a = MathUtils.get_random_fraction(den_limit=limit)
        b = MathUtils.get_random_fraction(den_limit=limit)
        op = random.choice(['+', '-'])
        
        if op == '+':
            ans = a + b
        else:
            ans = a - b
            
        logic_steps = [
            {"step_id": 1, "description": "분모가 다르면 통분합니다.", "target_expr": "통분", "concept_id": "FRACTION_COMMON_DENOMINATOR"},
            {"step_id": 2, "description": "부호가 같으면 더하고, 다르면 뺀 후 절댓값이 큰 쪽의 부호를 붙입니다.", "target_expr": "덧셈/뺄셈 계산", "concept_id": "RATIONAL_ADD_SUB"}
        ]

        data = {
            "question": f"다음 식을 계산하시오.\n{a} {op} ({b})",
            "answer": str(ans),
            "explanation": f"통분하여 계산하면 {ans}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            # 오답 생성 (부호 실수 등)
            options_set = {str(ans), str(-ans), str(ans + 1), str(ans - 1)}
            while len(options_set) < 4:
                options_set.add(str(ans + random.randint(2, 5)))
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T23_Master(BaseTMaster):
    """T23: 유리수의 곱셈과 나눗셈"""
    def __init__(self):
        super().__init__("T23", "유리수의 곱셈/나눗셈")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        limit = 5 if difficulty == "Easy" else (20 if difficulty == "Hard" else 10)

        a = MathUtils.get_random_fraction(den_limit=limit)
        b = MathUtils.get_random_fraction(den_limit=limit)
        op = random.choice(['×', '÷'])
        
        if op == '×':
            ans = a * b
            expr = f"{a} × ({b})"
        else:
            while b == 0: b = MathUtils.get_random_fraction()
            ans = a / b
            expr = f"{a} ÷ ({b})"
            
        logic_steps = [
            {"step_id": 1, "description": "나눗셈은 역수의 곱셈으로 바꿉니다.", "target_expr": "역수 변환", "concept_id": "DIVISION_TO_MULTIPLICATION"},
            {"step_id": 2, "description": "부호를 결정하고(같은 부호 +, 다른 부호 -), 약분하여 계산합니다.", "target_expr": "곱셈 계산", "concept_id": "RATIONAL_MUL_DIV"}
        ]

        data = {
            "question": f"다음 식을 계산하시오.\n{expr}",
            "answer": str(ans),
            "explanation": f"부호를 결정하고 역수를 이용하여 계산하면 {ans}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options_set = {str(ans), str(-ans), str(1/ans) if ans != 0 else "0", str(-(1/ans)) if ans != 0 else "1"}
            while len(options_set) < 4:
                options_set.add(str(ans + random.randint(1, 5)))
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T25_Master(BaseTMaster):
    """T25: 거듭제곱을 포함한 식의 계산"""
    def __init__(self):
        super().__init__("T25", "거듭제곱 계산")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": base = random.randint(-3, -1); exp = 2
        elif difficulty == "Hard": base = random.randint(-5, -2); exp = random.randint(4, 5)
        else: base = random.randint(-5, -2); exp = random.randint(2, 4)

        ans = base ** exp
        
        logic_steps = [
            {"step_id": 1, "description": "밑의 부호와 지수의 홀짝 여부를 확인하여 결과의 부호를 정합니다.", "target_expr": "부호 결정", "concept_id": "POWER_SIGN"},
            {"step_id": 2, "description": "절댓값을 지수만큼 거듭제곱하여 계산합니다.", "target_expr": "거듭제곱 계산", "concept_id": "POWER_CALCULATION"}
        ]

        data = {
            "question": f"다음 식을 계산하시오.\n({base})^{exp}",
            "answer": ans,
            "explanation": f"({base})를 {exp}번 곱하면 {ans}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            # 오답: 부호 실수, 곱셈 실수
            options_set = {ans, -ans, base * exp, -(base * exp)}
            while len(options_set) < 4: 
                options_set.add(ans + random.randint(1, 10))
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T26_Master(BaseTMaster):
    """T26: 사칙연산 혼합 계산"""
    def __init__(self):
        super().__init__("T26", "혼합 계산")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy":
            a = random.randint(1, 5); b = random.randint(1, 5); c = random.randint(1, 5)
        elif difficulty == "Hard":
            a = random.randint(-15, 15); b = random.randint(-10, 10); c = random.randint(-10, 10)
        else:
            a = random.randint(-10, 10); b = random.randint(-5, 5); c = random.randint(-5, 5)
        
        # 0 제외 및 보정
        if b == 0: b = 2
        if c == 0: c = 3
        
        # 연산자 및 구조 랜덤 선택
        ops = ['+', '-', '×'] # 나눗셈은 분수 처리가 복잡해질 수 있어 일단 제외하거나 간단한 경우만
        op1 = random.choice(ops)
        op2 = random.choice(ops)
        
        # 구조 패턴: 1=(A op B) op C, 2=A op (B op C), 3=A op B op C (괄호 없음)
        pattern = random.choice([1, 2, 3])
        
        # 파이썬 eval 계산을 위해 연산자 변환
        py_op1 = '*' if op1 == '×' else op1
        py_op2 = '*' if op2 == '×' else op2
        
        if pattern == 1:
            expr_str = f"({a} {op1} {b}) {op2} {c}"
            ans = eval(f"({a} {py_op1} {b}) {py_op2} {c}")
        elif pattern == 2:
            expr_str = f"{a} {op1} ({b} {op2} {c})"
            ans = eval(f"{a} {py_op1} ({b} {py_op2} {c})")
        else:
            expr_str = f"{a} {op1} {b} {op2} {c}"
            ans = eval(f"{a} {py_op1} {b} {py_op2} {c}")
        
        logic_steps = [
            {"step_id": 1, "description": "거듭제곱이 있으면 먼저 계산합니다.", "target_expr": "거듭제곱 처리", "concept_id": "ORDER_POWER"},
            {"step_id": 2, "description": "괄호 안을 먼저 계산합니다.", "target_expr": "괄호 처리", "concept_id": "ORDER_PARENTHESIS"},
            {"step_id": 3, "description": "곱셈과 나눗셈을 먼저 계산하고, 덧셈과 뺄셈을 나중에 계산합니다.", "target_expr": "사칙연산 순서", "concept_id": "ORDER_OPERATIONS"}
        ]

        data = {
            "question": f"다음 식을 계산하시오.\n{expr_str}",
            "answer": ans,
            "explanation": "괄호가 있으면 괄호 안을 먼저, 곱셈/나눗셈을 덧셈/뺄셈보다 먼저 계산합니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 10) + [ans]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)