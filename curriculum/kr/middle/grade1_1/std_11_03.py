import random
from core.base import BaseTMaster
from core.math_utils import MathUtils

# ==========================================
# [STD-11-03] 정수와 유리수의 뜻과 대소 관계 (T16 ~ T20)
# ==========================================

class T16_Master(BaseTMaster):
    """T16: 정수와 유리수의 분류"""
    def __init__(self):
        super().__init__("T16", "정수와 유리수의 분류")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 다양한 수 생성
        integers = [random.randint(-10, 10) for _ in range(3)]
        fractions = [f"{random.choice([-1, 1]) * random.randint(1, 9)}/{random.randint(2, 9)}" for _ in range(3)]
        decimals = [f"{random.choice([-1, 1]) * random.randint(0, 5)}.{random.randint(1, 9)}" for _ in range(2)]
        
        all_nums = integers + fractions + decimals
        random.shuffle(all_nums)
        
        # 문제 유형: 정수가 아닌 유리수 찾기
        target_type = "정수가 아닌 유리수"
        
        # 정답 필터링 로직 (간단화: 분수/소수 형태면 정답으로 간주)
        answers = [n for n in all_nums if '/' in str(n) or '.' in str(n)]
        
        logic_steps = self.get_logic_steps("T16")

        data = {
            "question": f"다음 수 중에서 {target_type}를 모두 고르시오.\n{', '.join(map(str, all_nums))}",
            "answer": answers,
            "explanation": "양의 정수, 0, 음의 정수를 통틀어 정수라고 하며, 정수가 아닌 형태의 분수나 소수를 찾으면 됩니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            # 오답 생성: 정수만 포함, 일부 누락 등
            d1 = [n for n in all_nums if isinstance(n, int)]
            d2 = answers[:-1] if len(answers) > 1 else answers + [0]
            d3 = all_nums[:3]
            options = [answers, d1, d2, d3]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T17_Master(BaseTMaster):
    """T17: 수직선 위의 점 대응"""
    def __init__(self):
        super().__init__("T17", "수직선 위의 점")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": val = random.randint(1, 5)
        elif difficulty == "Hard": val = random.randint(10, 20)
        else: val = random.randint(5, 10)

        sign = random.choice([-1, 1])
        target = val * sign
        
        direction = "오른쪽" if sign > 0 else "왼쪽"
        
        data = {
            "question": f"수직선 위에서 원점을 기준으로 {direction}으로 {val}만큼 떨어진 점에 대응하는 수는?",
            "answer": target,
            "explanation": f"원점(0)에서 {direction}은 양수(+)와 음수(-) 방향을 의미하므로 {target}입니다."
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(target, 3, 5) + [target]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T18_Master(BaseTMaster):
    """T18: 절댓값의 정의와 성질"""
    def __init__(self):
        super().__init__("T18", "절댓값 구하기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": num = random.randint(-10, -1)
        elif difficulty == "Hard": num = random.randint(-100, -50)
        else: num = random.randint(-50, -10)
        
        logic_steps = self.get_logic_steps("T18")

        data = {
            "question": f"다음 수의 절댓값을 구하시오.\n{num}",
            "answer": abs(num),
            "explanation": f"절댓값은 수직선 위에서 원점으로부터의 거리이므로 부호를 뗀 {abs(num)}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(abs(num), 3, 10) + [abs(num)]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T19_Master(BaseTMaster):
    """T19: 유리수의 대소 관계 비교"""
    def __init__(self):
        super().__init__("T19", "유리수의 대소 비교")

    def generate(self, difficulty="Normal", q_type="single"):
        # 비교할 두 수 생성
        range_val = 10 if difficulty == "Easy" else (50 if difficulty == "Hard" else 20)
        
        a = random.randint(-range_val, range_val)
        b = random.randint(-range_val, range_val)
        while a == b:
            b = random.randint(-range_val, range_val)
            
        correct = ">" if a > b else "<"
        
        logic_steps = [
            {"step_id": 1, "description": "두 수를 수직선 위에 나타내었을 때의 위치를 비교합니다.", "target_expr": "수직선 위치 비교", "concept_id": "NUMBER_LINE_COMPARE"},
            {"step_id": 2, "description": "오른쪽에 있는 수가 더 크다는 성질을 이용합니다. (양수 > 0 > 음수)", "target_expr": "대소 관계 판단", "concept_id": "RATIONAL_COMPARE"}
        ]

        data = {
            "question": f"다음 두 수의 대소 관계로 옳은 것은?\n{a} □ {b}",
            "options": [">", "<", "=", "≥"],
            "answer": correct,
            "explanation": f"수직선 상에서 오른쪽에 있는 수가 더 큽니다. {max(a, b)}가 {min(a, b)}보다 큽니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "short_answer":
            data["question"] = f"두 수 {a}, {b} 중 더 큰 수를 구하시오."
            data["answer"] = max(a, b)
            data["options"] = []

        return self._format_response(data, q_type, difficulty)

class T20_Master(BaseTMaster):
    """T20: 부등호의 사용과 표현"""
    def __init__(self):
        super().__init__("T20", "부등호의 표현")

    def generate(self, difficulty="Normal", q_type="single"):
        if difficulty == "Easy": num = random.randint(-5, 5)
        elif difficulty == "Hard": num = random.randint(-50, 50)
        else: num = random.randint(-20, 20)
        
        # 케이스 정의
        cases = [
            {"text": f"x는 {num}보다 크다", "symbol": f"x > {num}"},
            {"text": f"x는 {num}보다 작다", "symbol": f"x < {num}"},
            {"text": f"x는 {num}보다 크거나 같다 (작지 않다)", "symbol": f"x ≥ {num}"},
            {"text": f"x는 {num}보다 작거나 같다 (크지 않다)", "symbol": f"x ≤ {num}"}
        ]
        
        target = random.choice(cases)
        options = [c["symbol"] for c in cases]
        random.shuffle(options)
        
        logic_steps = [
            {"step_id": 1, "description": "문장에 포함된 '크다', '작다', '같다' 등의 표현을 확인합니다.", "target_expr": "표현 분석", "concept_id": "INEQUALITY_TERMS"},
            {"step_id": 2, "description": "알맞은 부등호(>, <, ≥, ≤)를 선택하여 식을 완성합니다.", "target_expr": "부등호 선택", "concept_id": "INEQUALITY_SYMBOL"}
        ]

        data = {
            "question": f"다음 문장을 부등호를 사용하여 바르게 나타낸 것은?\n'{target['text']}'",
            "options": options,
            "answer": target['symbol'],
            "explanation": "크다는 >, 작다는 <, 크거나 같다는 ≥, 작거나 같다는 ≤를 사용합니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "short_answer":
            data["question"] = f"다음 문장을 부등호를 사용하여 나타내시오.\n'{target['text']}'"
            data["options"] = []
            
        return self._format_response(data, q_type, difficulty)