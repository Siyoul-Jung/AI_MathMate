import random
import math
from core.base import BaseTMaster
from itertools import combinations

class High06_1_Counting_Master(BaseTMaster):
    """
    고등 공통수학 - 경우의 수 (합의 법칙, 곱의 법칙)
    확장: 방정식의 해, 정수 만들기, 주사위, 길찾기 등 다양한 유형 포함
    """
    def __init__(self):
        super().__init__("High06_1", "합의 법칙과 곱의 법칙")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 시나리오 확장: 주사위, 길찾기, 방정식, 정수 만들기
        scenario = random.choice(["dice", "path", "equation", "integer"])
        
        if scenario == "dice":
            # 서로 다른 두 개의 주사위를 동시에 던질 때, 나오는 눈의 수의 합이 k의 배수가 되는 경우의 수
            k = random.choice([3, 4, 5])
            
            # 가능한 합: 2 ~ 12
            # k의 배수: k, 2k, 3k...
            targets = [i for i in range(k, 13, k)]
            
            cases = []
            for t in targets:
                # 합이 t가 되는 경우 (a, b)
                start = max(1, t - 6)
                end = min(6, t - 1)
                count = max(0, end - start + 1)
                cases.append(count)
                
            ans = sum(cases)
            
            logic_steps = self.get_logic_steps("High06_1_dice", k=k)
            
            explanation = [
                f"두 주사위의 눈의 합이 {k}의 배수가 되는 경우는 합이 {', '.join(map(str, targets))}인 경우입니다.",
            ]
            for t, c in zip(targets, cases):
                explanation.append(f"합이 {t}인 경우: {c}가지")
            explanation.append(f"따라서 구하는 경우의 수는 {' + '.join(map(str, cases))} = {ans}가지입니다.")
            
            question = f"서로 다른 두 개의 주사위를 동시에 던질 때, 나오는 눈의 수의 합이 {k}의 배수가 되는 경우의 수를 구하시오."

        elif scenario == "path":
            # A -> B (m가지), B -> C (n가지). A -> C로 가는 경우의 수
            m = random.randint(2, 5)
            n = random.randint(2, 5)
            ans = m * n
            
            logic_steps = self.get_logic_steps("High06_1_path", m=m, n=n)
            
            question = f"A지점에서 B지점으로 가는 길이 {m}가지, B지점에서 C지점으로 가는 길이 {n}가지 있을 때, A지점에서 B지점을 거쳐 C지점으로 가는 방법의 수를 구하시오."
            explanation = [
                "A지점에서 B지점으로 가는 각 경우에 대하여 B지점에서 C지점으로 가는 경우가 각각 존재하므로 곱의 법칙을 이용합니다.",
                f"{m} × {n} = {ans}가지"
            ]

        elif scenario == "equation":
            # 방정식 ax + by + cz = k 의 자연수 해의 개수 (교과서 단골 문제)
            coeffs = random.sample([1, 2, 3], 3)
            a, b, c = coeffs
            # 해가 적당히 나오도록 k 설정 (대략 10~15 범위)
            k = random.randint(10, 15)
            
            count = 0
            solutions = []
            # Brute force for small range (자연수 해 x,y,z >= 1)
            for x in range(1, k):
                for y in range(1, k):
                    current_val = a*x + b*y
                    rem = k - current_val
                    if rem > 0 and rem % c == 0:
                        z = rem // c
                        count += 1
                        if count <= 2: # 해설용 예시
                            solutions.append(f"({x}, {y}, {z})")

            # 만약 해가 없으면(0개) 다시 생성 (재귀 호출 대신 간단히 기본값 처리)
            if count == 0:
                return self.generate(difficulty, q_type)

            question = f"방정식 ${a}x + {b}y + {c}z = {k}$를 만족시키는 자연수 $x, y, z$의 순서쌍 $(x, y, z)$의 개수를 구하시오."
            explanation = [
                f"계수가 가장 큰 문자를 기준으로 경우를 나누어 셉니다.",
                f"가능한 순서쌍은 {', '.join(solutions)} ... 등입니다.",
                f"직접 대입하여 구하면 총 {count}개입니다."
            ]
            ans = count
            logic_steps = [] # TODO: Add specific logic steps for equation

        elif scenario == "integer":
            # 0~4 또는 1~5 카드로 n자리 정수 만들기 (짝수/홀수 조건)
            cards = [1, 2, 3, 4, 5]
            cond_type = random.choice(["짝수", "홀수"])
            target_digits = [c for c in cards if (c % 2 == 0 if cond_type == "짝수" else c % 2 != 0)]
            
            # 십의 자리(5개 중 1개) x 일의 자리(조건 만족하는 것) - 중복 허용 가정 시 5 * len
            # 서로 다른 2장을 뽑는 경우:
            # 일의 자리 결정(len) -> 십의 자리(나머지 4개)
            ans = len(target_digits) * 4
            question = f"1, 2, 3, 4, 5의 숫자가 각각 적힌 5장의 카드 중에서 서로 다른 2장을 뽑아 두 자리 자연수를 만들 때, {cond_type}의 개수를 구하시오."
            explanation = [
                f"{cond_type}가 되려면 일의 자리 숫자가 {cond_type}이어야 합니다.",
                f"일의 자리에 올 수 있는 수: {len(target_digits)}가지 ({', '.join(map(str, target_digits))})",
                f"십의 자리에 올 수 있는 수: 일의 자리 숫자를 제외한 4가지",
                f"따라서 구하는 개수는 {len(target_digits)} × 4 = {ans}개"
            ]
            logic_steps = []

        data = {
            "question": question,
            "answer": ans,
            "explanation": explanation,
            "logic_steps": logic_steps,
            "strategy": "사건이 동시에 일어나지 않으면 합의 법칙, 잇달아 일어나면 곱의 법칙을 사용합니다."
        }
        
        if q_type == "multi":
            options_set = {ans}
            while len(options_set) < 4:
                options_set.add(ans + random.randint(-5, 5))
                if 0 in options_set: options_set.remove(0)
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High06_2_Permutation_Master(BaseTMaster):
    """
    고등 공통수학 - 순열 (nPr)
    """
    def __init__(self):
        super().__init__("High06_2", "순열")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 시나리오: 단순 순열, 이웃하는 순열, 특정 위치 고정
        scenario = random.choice(["basic", "neighbor", "fixed"])
        
        if scenario == "basic":
            n = random.randint(4, 7)
            r = random.randint(2, n)
            ans = math.perm(n, r)
            logic_steps = self.get_logic_steps("High06_2", n=n, r=r)
            question = f"{n}명의 학생 중에서 {r}명을 뽑아 일렬로 세우는 경우의 수를 구하시오."
            calc_str = " × ".join([str(n-i) for i in range(r)])
            explanation = [
                f"{n}명 중에서 {r}명을 택하여 일렬로 세우는 순열의 수는 $_ {n}P_{r}$ 입니다.",
                f"$_ {n}P_{r} = {calc_str} = {ans}$"
            ]

        elif scenario == "neighbor":
            # n명 중 A, B가 이웃하게 서는 경우
            n = random.randint(4, 6)
            # (n-1)! * 2!
            ans = math.factorial(n - 1) * 2
            logic_steps = []
            question = f"{n}명의 학생이 일렬로 설 때, 특정한 2명이 서로 이웃하게 서는 경우의 수를 구하시오."
            explanation = [
                "이웃하는 2명을 한 묶음으로 생각하여 $(n-1)$명을 나열하는 경우의 수: $( {n} - 1 )! = {math.factorial(n-1)}$",
                "묶음 안에서 2명이 자리를 바꾸는 경우의 수: $2! = 2$",
                f"따라서 구하는 경우의 수는 ${math.factorial(n-1)} \\times 2 = {ans}$"
            ]

        elif scenario == "fixed":
            # n명 중 반장 1명, 부반장 1명을 뽑는데 A가 반장이 되는 경우
            n = random.randint(5, 8)
            # A는 반장 고정, 나머지 n-1명 중 부반장 1명 뽑기
            ans = n - 1
            logic_steps = []
            question = f"{n}명의 학생 중에서 반장 1명, 부반장 1명을 뽑을 때, 특정 학생 A가 반장으로 뽑히는 경우의 수를 구하시오."
            explanation = [
                "반장은 A로 이미 정해져 있습니다.",
                f"나머지 {n-1}명의 학생 중에서 부반장 1명을 뽑으면 되므로 경우의 수는 {n-1}가지입니다."
            ]

        data = {
            "question": question,
            "answer": ans,
            "explanation": explanation,
            "logic_steps": logic_steps,
            "strategy": "순서가 중요하면 순열(P)을 사용합니다."
        }
        
        if q_type == "multi":
            options_set = {ans}
            options_set.add(math.comb(n, r))
            options_set.add(math.factorial(n))
            while len(options_set) < 4:
                options_set.add(ans + random.randint(-10, 10) * 10)
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High06_3_Combination_Master(BaseTMaster):
    """
    고등 공통수학 - 조합 (nCr)
    """
    def __init__(self):
        super().__init__("High06_3", "조합")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 시나리오: 단순 조합, 그룹별 추출(남자/여자), 악수/경기
        scenario = random.choice(["basic", "group", "handshake"])
        
        if scenario == "basic":
            n = random.randint(5, 9)
            r = random.randint(2, 4)
            ans = math.comb(n, r)
            logic_steps = self.get_logic_steps("High06_3", n=n, r=r)
            question = f"{n}명의 학생 중에서 대표 {r}명을 뽑는 경우의 수를 구하시오."
            num_str = " × ".join([str(n-i) for i in range(r)])
            den_str = " × ".join([str(r-i) for i in range(r)])
            explanation = [
                f"{n}명 중에서 자격이 같은 {r}명을 뽑는 조합의 수는 $_ {n}C_{r}$ 입니다.",
                f"$_ {n}C_{r} = \\frac{{_ {n}P_{r}}}{{{r}!}} = \\frac{{{num_str}}}{{{den_str}}} = {ans}$"
            ]

        elif scenario == "group":
            # 남자 n1명, 여자 n2명 중 남자 r1, 여자 r2 뽑기
            n1 = random.randint(3, 5)
            n2 = random.randint(3, 5)
            r1 = random.randint(1, 2)
            r2 = random.randint(1, 2)
            
            ans = math.comb(n1, r1) * math.comb(n2, r2)
            logic_steps = []
            question = f"남학생 {n1}명, 여학생 {n2}명이 있다. 이 중에서 남학생 {r1}명, 여학생 {r2}명을 뽑는 경우의 수를 구하시오."
            explanation = [
                f"남학생 {n1}명 중 {r1}명을 뽑는 경우의 수: $_{{{n1}}}C_{{{r1}}} = {math.comb(n1, r1)}$",
                f"여학생 {n2}명 중 {r2}명을 뽑는 경우의 수: $_{{{n2}}}C_{{{r2}}} = {math.comb(n2, r2)}$",
                f"두 사건이 동시에 일어나므로 곱의 법칙을 적용합니다: {math.comb(n1, r1)} × {math.comb(n2, r2)} = {ans}"
            ]

        elif scenario == "handshake":
            # n명이 서로 한 번씩 악수하는 횟수 (nC2)
            n = random.randint(5, 10)
            ans = math.comb(n, 2)
            logic_steps = []
            question = f"{n}명의 사람이 모임에 참석하여 서로 빠짐없이 한 번씩 악수를 나누었다. 악수를 나눈 총 횟수를 구하시오."
            explanation = [
                f"{n}명 중에서 순서에 상관없이 2명을 뽑는 경우의 수와 같습니다.",
                f"$_{{{n}}}C_2 = \\frac{{{n} \\times {n-1}}}{{2}} = {ans}$"
            ]
        
        data = {
            "question": question,
            "answer": ans,
            "explanation": explanation,
            "logic_steps": logic_steps,
            "strategy": "순서가 중요하지 않으면 조합(C)을 사용합니다."
        }
        
        if q_type == "multi":
            options_set = {ans}
            options_set.add(math.perm(n, r))
            while len(options_set) < 4:
                options_set.add(ans + random.randint(-5, 5))
                if 0 in options_set: options_set.remove(0)
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)