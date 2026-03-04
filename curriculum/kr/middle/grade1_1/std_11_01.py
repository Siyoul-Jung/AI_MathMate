import random
from core.math_utils import MathUtils
from core.base import BaseTMaster

# ==========================================
# [STD-11-01] 소인수분해의 이해 (T01 ~ T09)
# ==========================================

class T01_Master(BaseTMaster):
    """T01: 소수와 합성수의 구분"""
    def __init__(self):
        super().__init__("T01", "소수와 합성수의 구분")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 난이도별 범위 설정
        if difficulty == "Easy": num_range = (2, 20)
        elif difficulty == "Hard": num_range = (50, 150)
        else: num_range = (20, 50)

        target = 0
        while True:
            cand = random.randint(num_range[0], num_range[1])
            if MathUtils.is_prime(cand):
                target = cand
                break
        
        if q_type == "multi":
            distractors = []
            while len(distractors) < 4:
                cand = random.randint(num_range[0], num_range[1])
                if not MathUtils.is_prime(cand) and cand != 1 and cand not in distractors:
                    distractors.append(cand)
            
            options = [target] + distractors
            random.shuffle(options)
            
            data = {
                "question": f"다음 중 소수인 것을 고르시오.",
                "options": options,
                "answer": target,
                "explanation": f"정답은 {target}입니다. {target}은(는) 약수가 1과 자신뿐인 소수입니다."
            }
        else: # short_answer
            # 주관식 변형: ~보다 작은 소수의 개수 or ~보다 큰 가장 작은 소수
            start = random.randint(num_range[0], num_range[1] - 10)
            
            data = {
                "question": f"{start}보다 큰 자연수 중에서 가장 작은 소수를 구하시오.",
                "answer": target, # 위에서 구한 target이 아니라 start보다 큰 첫 소수로 재계산 필요하지만, 간단히 로직 변경
                "explanation": f"{start}보다 큰 수들을 차례로 확인하면 소수는 ..."
            }
            # 주관식 로직 보정
            curr = start + 1
            while not MathUtils.is_prime(curr): curr += 1
            data["answer"] = curr
            data["explanation"] = f"{start} 다음 수부터 확인해보면 {curr}이 약수가 1과 자기 자신뿐인 소수입니다."

        return self._format_response(data, q_type, difficulty)
    
class T02_Master(BaseTMaster):
    """T02: 소수의 성질 판단 (개념형)"""
    def __init__(self):
        super().__init__("T02", "소수의 성질 판단")
        self.facts = [
            {"q": "모든 소수는 홀수이다.", "a": "X", "e": "2는 짝수이면서 소수입니다."},
            {"q": "가장 작은 소수는 1이다.", "a": "X", "e": "1은 소수가 아닙니다. 가장 작은 소수는 2입니다."},
            {"q": "소수 중 짝수는 하나뿐이다.", "a": "O", "e": "2만이 유일한 짝수 소수입니다."},
            {"q": "자연수는 소수와 합성수로 이루어져 있다.", "a": "X", "e": "자연수는 1, 소수, 합성수로 이루어져 있습니다."}
        ]

    def generate(self, difficulty="Normal", q_type="ox"):
        fact = random.choice(self.facts)
        data = {
            "question": f"다음 문장의 참(O), 거짓(X)을 판별하세요.\n'{fact['q']}'",
            "options": ["O", "X"],
            "answer": fact['a'],
            "explanation": fact['e'],
            "logic_steps": [
                {"step_id": 1, "description": "소수의 정의와 성질(약수의 개수, 짝수 소수 등)을 떠올려봅니다.", "target_expr": "소수의 성질", "concept_id": "PRIME_PROPERTIES"},
                {"step_id": 2, "description": "주어진 문장이 소수의 성질과 일치하는지 판단합니다.", "target_expr": "참/거짓 판별", "concept_id": "LOGICAL_JUDGEMENT"}
            ]
        }
        return self._format_response(data, q_type, difficulty)

class T03_Master(BaseTMaster):
    """T03: 거듭제곱의 표현"""
    def __init__(self):
        super().__init__("T03", "거듭제곱의 표현")

    def generate(self, difficulty="Normal", q_type="multi"):
        if difficulty == "Easy":
            base = random.randint(2, 5)
            exp = random.randint(2, 3)
        elif difficulty == "Hard":
            base = random.randint(11, 19)
            exp = random.randint(3, 5)
        else:
            base = random.randint(2, 9)
            exp = random.randint(2, 5)
        
        problem_str = " × ".join([str(base)] * exp)
        correct_answer = f"{base}^{exp}"
        
        data = {
            "question": f"다음 곱셈식을 거듭제곱으로 바르게 나타낸 것은?\n{problem_str}",
            "answer": correct_answer,
            "explanation": f"{base}를 {exp}번 곱했으므로 밑은 {base}, 지수는 {exp}입니다."
        }

        if q_type == "multi":
            # 오답 구성 (학생들이 자주 하는 실수)
            distract_1 = f"{base} × {exp}" # 밑 x 지수
            distract_2 = f"{exp}^{base}"   # 밑과 지수 반대로
            distract_3 = f"{base}^{exp+1}" # 개수 잘못 세기
            
            options_set = {correct_answer, distract_1, distract_2, distract_3}
            while len(options_set) < 4:
                options_set.add(f"{base}^{random.randint(2, 10)}")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
        else:
            data["question"] = f"다음 곱셈식을 거듭제곱으로 나타내시오.\n{problem_str}"

        return self._format_response(data, q_type, difficulty)

class T04_Master(BaseTMaster):
    """T04: 소인수분해 수행 (식 구성 능력을 측정)"""
    def __init__(self):
        super().__init__("T04", "소인수분해 수행")

    def generate(self, difficulty="Normal", q_type="multi"):
        if difficulty == "Easy": num = random.randint(10, 50)
        elif difficulty == "Hard": num = random.randint(150, 300)
        else: num = random.randint(50, 150)

        factors = MathUtils.get_prime_factors(num)
        # 결과 식 생성: 2^2 x 3 형태
        correct_answer = " x ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
        
        data = {
            "question": f"{num}을 소인수분해한 결과로 옳은 것은?",
            "answer": correct_answer,
            "explanation": f"{num}을 끝까지 나누면 {correct_answer}이 됩니다."
        }

        if q_type == "multi":
            # 오답: 지수를 틀리게 하거나 더하기로 표현한 함정
            distract_1 = " + ".join([f"{p}^{e}" for p, e in factors.items()])
            distract_2 = " x ".join([f"{p} x {e}" for p, e in factors.items()])
            # 임의의 오답 추가
            fake_num = num + random.randint(1, 10)
            fake_factors = MathUtils.get_prime_factors(fake_num)
            distract_3 = " x ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in fake_factors.items()])
            
            options_set = {correct_answer, distract_1, distract_2, distract_3}
            while len(options_set) < 4:
                options_set.add(f"{random.randint(2, 10)}^{random.randint(2, 5)}")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
        else:
            data["question"] = f"{num}을 소인수분해 하시오."

        return self._format_response(data, q_type, difficulty)

class T05_Master(BaseTMaster):
    """T05: 소인수 찾기 (밑만 추출하는 능력을 측정)"""
    def __init__(self):
        super().__init__("T05", "소인수 찾기")

    def generate(self, difficulty="Normal", q_type="multi"):
        if difficulty == "Easy": num = random.randint(20, 60)
        elif difficulty == "Hard": num = random.randint(150, 300)
        else: num = random.randint(60, 150)

        factors = MathUtils.get_prime_factors(num)
        correct_primes = sorted(list(factors.keys())) # 밑(base)들만 추출
        
        data = {
            "question": f"{num}의 소인수를 모두 고르시오.",
            "answer": correct_primes,
            "explanation": f"{num}을 소인수분해했을 때 밑에 해당하는 숫자가 소인수입니다."
        }

        if q_type == "multi":
            # 오답 생성: 소수가 아닌 약수 포함, 일부 소인수 누락 등
            d1 = correct_primes[:-1] if len(correct_primes) > 1 else [correct_primes[0] + 1]
            d2 = correct_primes + [random.choice([4, 6, 8, 9])]
            d3 = [p + 1 for p in correct_primes]
            options = [correct_primes, d1, d2, d3]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T06_Master(BaseTMaster):
    """T06: 약수 구하기 (나열 능력 측정)"""
    def __init__(self):
        super().__init__("T06", "약수 구하기")

    def generate(self, difficulty="Normal", q_type="multi"):
        if difficulty == "Easy": num = random.choice([6, 8, 10, 12, 15])
        elif difficulty == "Hard": num = random.choice([48, 50, 60, 72, 80])
        else: num = random.choice([18, 20, 24, 28, 30, 36, 40])

        # 실제 약수 리스트 생성 로직
        divisors = []
        for i in range(1, num + 1):
            if num % i == 0: divisors.append(i)
        
        data = {
            "question": f"{num}의 약수를 모두 나열한 것은?",
            "answer": divisors,
            "explanation": f"{num}을 나누어 떨어지게 하는 수는 {divisors}입니다."
        }
        
        if q_type == "multi":
            # 오답 생성: 약수가 아닌 수 포함 or 개수 부족
            d1 = divisors[:-1]
            d2 = divisors + [num+1]
            d3 = [d for d in divisors if d % 2 == 0]
            options = [divisors, d1, d2, d3]
            random.shuffle(options)
            data["options"] = options
        else:
            data["question"] = f"{num}의 약수를 모두 구하시오."

        return self._format_response(data, q_type, difficulty)

class T07_Master(BaseTMaster):
    """T07: 약수의 개수 구하기 (공식 활용 능력 측정)"""
    def __init__(self):
        super().__init__("T07", "약수의 개수 구하기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": num = random.randint(12, 50)
        elif difficulty == "Hard": num = random.randint(200, 500)
        else: num = random.randint(50, 200)

        factors = MathUtils.get_prime_factors(num)
        
        count = 1
        formula = []
        for p, e in factors.items():
            count *= (e + 1)
            formula.append(f"({e}+1)")
            
        data = {
            "question": f"{num}의 약수의 개수를 구하시오.",
            "answer": count,
            "explanation": f"지수에 1을 더해 곱하면 {' x '.join(formula)} = {count}개입니다."
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(count, 3, 5) + [count]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T08_Master(BaseTMaster):
    """T08: 약수의 개수를 이용한 미지수 구하기 (역추론 능력)"""
    def __init__(self):
        super().__init__("T08", "미지수 추론")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy":
            a = 2; x_answer = 1
        elif difficulty == "Hard":
            a = random.randint(4, 6); x_answer = random.randint(3, 5)
        else:
            a = random.randint(2, 4); x_answer = random.randint(1, 3)

        total_count = (a + 1) * (x_answer + 1)
        
        data = {
            "question": f"2^{a} × 3^x 의 약수의 개수가 {total_count}개일 때, 자연수 x의 값은?",
            "answer": x_answer,
            "explanation": f"약수의 개수는 (지수+1)의 곱이므로, ({a}+1) × (x+1) = {total_count}입니다. \n{a+1} × (x+1) = {total_count}에서 x+1 = {x_answer+1}이 되어야 하므로 x = {x_answer}입니다."
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(x_answer, 3, 3) + [x_answer]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)
            
class T09_Master(BaseTMaster):
    """T09: 제곱수 만들기"""
    def __init__(self):
        super().__init__("T09", "제곱수 만들기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": base_num = random.choice([8, 12, 18, 20])
        elif difficulty == "Hard": base_num = random.choice([72, 98, 108, 120, 150])
        else: base_num = random.choice([24, 28, 45, 50, 60])

        factors = MathUtils.get_prime_factors(base_num)
        
        to_multiply = 1
        formula_parts = []
        for p, e in factors.items():
            formula_parts.append(f"{p}^{e}")
            if e % 2 != 0:
                to_multiply *= p
        
        type_ = random.choice(["multiply", "divide"])
        
        if type_ == "multiply":
            q_text = f"{base_num}에 자연수 n을 곱하여 어떤 자연수의 제곱이 되게 할 때, n의 최솟값은?"
            expl = f"{base_num} = {' x '.join(formula_parts)}이므로 지수가 홀수인 인수를 곱해줘야 합니다."
        else:
            q_text = f"{base_num}을 자연수 n으로 나누어 어떤 자연수의 제곱이 되게 할 때, n의 최솟값은?"
            expl = f"{base_num} = {' x '.join(formula_parts)}이므로 지수가 홀수인 인수를 나누어 없애야 합니다."

        data = {
            "question": q_text,
            "answer": to_multiply,
            "explanation": expl
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(to_multiply, 3, 5) + [to_multiply]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)