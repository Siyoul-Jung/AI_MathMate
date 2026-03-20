import random
from kmath_engine.math_utils import MathUtils
from kmath_engine.base import BaseTMaster

# ==========================================
# [STD-11-02] 최대공약수와 최소공배수 (T10 ~ T15)
# ==========================================

class T10_Master(BaseTMaster):
    """T10: 최대공약수 구하기"""
    def __init__(self):
        super().__init__("T10", "최대공약수 구하기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy":
            common = random.randint(2, 5)
            a = common * random.randint(1, 5)
            b = common * random.randint(1, 5)
        elif difficulty == "Hard":
            common = random.randint(10, 20)
            a = common * random.randint(5, 15)
            b = common * random.randint(5, 15)
        else:
            common = random.randint(2, 12)
            a = common * random.randint(2, 10)
            b = common * random.randint(2, 10)
        
        answer = MathUtils.get_gcd(a, b)
        
        data = {
            "question": f"두 수 {a}와 {b}의 최대공약수를 구하시오.",
            "answer": answer,
            "explanation": f"{a}와 {b}를 소인수분해하거나 나눗셈을 이용하면 공통된 약수 중 가장 큰 수는 {answer}입니다."
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(answer, 3, 5) + [answer]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T11_Master(BaseTMaster):
    """T11: 최소공배수 구하기"""
    def __init__(self):
        super().__init__("T11", "최소공배수 구하기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy":
            a = random.randint(2, 10)
            b = random.randint(2, 10)
        elif difficulty == "Hard":
            a = random.randint(20, 50)
            b = random.randint(20, 50)
        else:
            a = random.randint(4, 20)
            b = random.randint(4, 20)
        
        answer = MathUtils.get_lcm(a, b)
        
        data = {
            "question": f"두 수 {a}와 {b}의 최소공배수를 구하시오.",
            "answer": answer,
            "explanation": f"{a}와 {b}의 공배수 중 가장 작은 수는 {answer}입니다."
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(answer, 3, 20) + [answer]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T12_Master(BaseTMaster):
    """T12: 세 수의 공약수와 공배수 관계"""
    def __init__(self):
        super().__init__("T12", "세 수의 최대공약수/최소공배수")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": base = random.randint(2, 4)
        elif difficulty == "Hard": base = random.randint(6, 12)
        else: base = random.randint(2, 6)

        # 세 수 생성 (난이도에 따라 배수 범위 조절)
        nums = [base * random.randint(1, 5 if difficulty != "Hard" else 8) for _ in range(3)]
        
        # 문제 유형 랜덤 (GCD or LCM)
        is_gcd = random.choice([True, False])
        
        if is_gcd:
            ans = nums[0]
            for n in nums[1:]:
                ans = MathUtils.get_gcd(ans, n)
            q_text = "최대공약수"
        else:
            ans = nums[0]
            for n in nums[1:]:
                ans = MathUtils.get_lcm(ans, n)
            q_text = "최소공배수"
            
        data = {
            "question": f"세 수 {nums[0]}, {nums[1]}, {nums[2]}의 {q_text}를 구하시오.",
            "answer": ans,
            "explanation": f"세 수의 {q_text}는 {ans}입니다."
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 10) + [ans]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T13_Master(BaseTMaster):
    """T13: 최대공약수의 활용 (나누어주기)"""
    def __init__(self):
        super().__init__("T13", "최대공약수 활용(분배)")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": gcd_val = random.randint(2, 6)
        elif difficulty == "Hard": gcd_val = random.randint(12, 24)
        else: gcd_val = random.randint(4, 12)

        item1_cnt = gcd_val * random.randint(2, 5 if difficulty != "Hard" else 8)
        item2_cnt = gcd_val * random.randint(2, 5 if difficulty != "Hard" else 8)
        
        scenario = random.choice(["stationery", "fruit"])
        
        if scenario == "stationery":
            q_text = f"연필 {item1_cnt}자루와 지우개 {item2_cnt}개를 가능한 많은 학생에게 남김없이 똑같이 나누어 주려고 한다. 몇 명의 학생에게 나누어 줄 수 있는가?"
        else:
            q_text = f"사과 {item1_cnt}개와 배 {item2_cnt}개를 가능한 많은 상자에 똑같이 나누어 담으려고 한다. 최대 몇 개의 상자가 필요한가?"
            
        data = {
            "question": q_text,
            "answer": gcd_val,
            "explanation": f"가능한 많은 대상에게 똑같이 나누어야 하므로 {item1_cnt}와 {item2_cnt}의 최대공약수를 구하면 {gcd_val}입니다."
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(gcd_val, 3, 5) + [gcd_val]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T14_Master(BaseTMaster):
    """T14: 최소공배수의 활용 (동시 출발)"""
    def __init__(self):
        super().__init__("T14", "최소공배수 활용(시간)")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy":
            term_a = random.choice([4, 6, 8]); term_b = random.choice([6, 8, 10])
        elif difficulty == "Hard":
            term_a = random.choice([12, 15, 18, 24]); term_b = random.choice([18, 24, 30, 36])
        else:
            term_a = random.choice([6, 8, 9, 10, 12]); term_b = random.choice([10, 12, 15, 18, 20])

        lcm_val = MathUtils.get_lcm(term_a, term_b)
        
        data = {
            "question": f"A 버스는 {term_a}분 간격, B 버스는 {term_b}분 간격으로 운행한다. 두 버스가 오전 9시에 동시에 출발했다면, 다음 번에 처음으로 다시 동시에 출발하는 시각은 몇 분 후인가?",
            "answer": lcm_val,
            "explanation": f"두 버스가 다시 동시에 출발하는 시간은 {term_a}와 {term_b}의 최소공배수인 {lcm_val}분 후입니다."
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(lcm_val, 3, 15) + [lcm_val]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T15_Master(BaseTMaster):
    """T15: 두 수의 곱과 GCD, LCM의 관계"""
    def __init__(self):
        super().__init__("T15", "두 수의 곱과 GCD, LCM")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": g = random.randint(2, 5)
        elif difficulty == "Hard": g = random.randint(10, 20)
        else: g = random.randint(2, 10)

        a_prime = random.randint(2, 5 if difficulty == "Easy" else 9)
        b_prime = random.randint(2, 5 if difficulty == "Easy" else 9)
        
        # 서로소가 되도록 조정 (간단히)
        while MathUtils.get_gcd(a_prime, b_prime) != 1:
            b_prime += 1
            
        A = g * a_prime
        B = g * b_prime
        L = g * a_prime * b_prime
        
        data = {
            "question": f"두 자연수의 곱이 {A*B}이고, 최대공약수가 {g}일 때, 이 두 수의 최소공배수를 구하시오.",
            "answer": L,
            "explanation": f"두 수의 곱 = 최대공약수 × 최소공배수입니다.\n{A*B} = {g} × (최소공배수) 이므로, 최소공배수는 {L}입니다."
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(L, 3, 20) + [L]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)
