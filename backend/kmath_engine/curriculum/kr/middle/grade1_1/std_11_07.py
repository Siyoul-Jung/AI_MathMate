import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

# ==========================================
# [STD-11-07] 일차방정식의 풀이 (T39 ~ T47)
# ==========================================

class T39_Master(BaseTMaster):
    """T39: 등식의 종류 (방정식과 항등식)"""
    def __init__(self):
        super().__init__("T39", "방정식과 항등식")

    def generate(self, difficulty="Normal", q_type="multi"):
        if q_type == "short_answer":
            a = random.randint(2, 9)
            data = {
                "question": f"등식 {a}(x + 1) = ax + b 가 x에 대한 항등식이 되도록 하는 상수 b의 값은?",
                "answer": a,
                "explanation": f"좌변을 전개하면 {a}x + {a} 이므로, 우변 {a}x + b 와 같으려면 b = {a} 이어야 합니다.",
                "logic_steps": self.get_logic_steps("T39_short", a=a)
            }
            return self._format_response(data, q_type, difficulty)

        # 항등식 찾기
        a = random.randint(2, 5)
        
        # 항등식 예시
        identity = f"{a}(x + 1) = {a}x + {a}"
        
        # 방정식 예시
        eq1 = f"x + 3 = 5"
        eq2 = f"2x = 4"
        eq3 = f"3x - 1 = x + 5"
        
        options = [identity, eq1, eq2, eq3]
        random.shuffle(options)
        
        logic_steps = self.get_logic_steps("T39_multi")

        data = {
            "question": "다음 중 x의 값에 관계없이 항상 참인 등식(항등식)은?",
            "options": options,
            "answer": identity,
            "explanation": "좌변과 우변을 정리했을 때 모양이 같으면 항등식입니다.",
            "logic_steps": logic_steps
        }
        return self._format_response(data, q_type, difficulty)

class T43_Master(BaseTMaster):
    """T43: 일차방정식의 기본 풀이"""
    def __init__(self):
        super().__init__("T43", "일차방정식 풀기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # Type 1: ax + b = c
        # Type 2: ax + b = cx + d
        type_ = random.choice([1, 2])
        
        if difficulty == "Easy": x = random.randint(1, 5)
        elif difficulty == "Hard": x = random.randint(-10, 10)
        else: x = random.randint(-5, 5)
        
        if type_ == 1:
            a = random.choice([i for i in range(-5, 6) if i != 0])
            b = random.randint(-10, 10)
            c = a * x + b
            eq = f"{a}x"
            if b >= 0: eq += f" + {b}"
            else: eq += f" - {abs(b)}"
            eq += f" = {c}"
            expl = f"이항하여 정리하면 {a}x = {c - b}, 따라서 x = {x}입니다."
        else:
            a = random.randint(2, 6)
            c = random.randint(-3, 1) # a != c
            while a == c: c = random.randint(-3, 1)
            b = random.randint(-10, 10)
            
            # ax + b = cx + d  => (a-c)x = d - b => d = (a-c)x + b
            d = (a - c) * x + b
            
            eq = f"{a}x"
            if b >= 0: eq += f" + {b}"
            else: eq += f" - {abs(b)}"
            rhs = f"{c}x"
            if d >= 0: rhs += f" + {d}"
            else: rhs += f" - {abs(d)}"
            eq += f" = {rhs}"
            expl = f"x항은 좌변으로, 상수항은 우변으로 이항하여 정리하면 {a-c}x = {d-b}, 따라서 x = {x}입니다."
        
        logic_steps = self.get_logic_steps("T43")

        data = {
            "question": f"다음 일차방정식을 푸시오.\n{eq}",
            "answer": f"x = {x}",
            "explanation": expl,
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = [f"x = {d}" for d in MathUtils.generate_distractors(x, 3, 5)] + [f"x = {x}"]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T44_Master(BaseTMaster):
    """T44: 복잡한 일차방정식 (괄호)"""
    def __init__(self):
        super().__init__("T44", "복잡한 일차방정식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # a(x + b) = c
        x = random.randint(-5, 5)
        a = random.randint(2, 5)
        b = random.randint(1, 5)
        
        rhs = a * (x + b)
        
        eq = f"{a}(x + {b}) = {rhs}"
        
        logic_steps = self.get_logic_steps("T44", a=a, ab=a*b, rhs=rhs, rhs_minus_ab=rhs-a*b)

        data = {
            "question": f"다음 일차방정식을 푸시오.\n{eq}",
            "answer": f"x = {x}",
            "explanation": f"분배법칙으로 괄호를 풀면 {a}x + {a*b} = {rhs}, 이항하면 {a}x = {rhs - a*b}, 따라서 x = {x}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = [f"x = {d}" for d in MathUtils.generate_distractors(x, 3, 5)] + [f"x = {x}"]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T46_Master(BaseTMaster):
    """T46: 두 방정식의 해가 같을 조건"""
    def __init__(self):
        super().__init__("T46", "해가 같은 방정식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 1. 쉬운 방정식: x + a = b -> 해 x1
        x_val = random.randint(2, 5)
        a = random.randint(1, 5)
        b = x_val + a
        eq1 = f"x + {a} = {b}"
        
        # 2. 미지수 k가 있는 방정식: 2x + k = c
        # 2*x_val + k = c
        k_val = random.randint(1, 5)
        c = 2 * x_val + k_val
        eq2 = f"2x + k = {c}"
        
        logic_steps = self.get_logic_steps("T46", x_val=x_val, c=c)

        data = {
            "question": f"두 일차방정식 {eq1} 과 {eq2} 의 해가 같을 때, 상수 k의 값은?",
            "answer": k_val,
            "explanation": f"첫 번째 방정식의 해는 x = {x_val}입니다. 이를 두 번째 식에 대입하면 2({x_val}) + k = {c} 이므로 k = {k_val}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(k_val, 3, 5) + [k_val]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)
