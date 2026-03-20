import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

# ==========================================
# [STD-21-05] 일차부등식의 활용 (T126 ~ T129)
# ==========================================

class T126_Master(BaseTMaster):
    """T126: 수에 관한 문제 (평균, 연속하는 수)"""
    def __init__(self):
        super().__init__("T126", "수에 관한 문제")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 평균 문제: 3번 시험 점수 a, b, c. 4번째 x점. 평균 >= target
        # (a+b+c+x)/4 >= target => x >= 4*target - (a+b+c)
        
        scores = [random.randint(70, 95) for _ in range(3)]
        target_avg = random.choice([80, 85, 90])
        
        # x가 100을 넘지 않도록 조정
        while (4 * target_avg - sum(scores)) > 100:
            scores = [random.randint(80, 98) for _ in range(3)]
            
        min_score = 4 * target_avg - sum(scores)
        if min_score < 0: min_score = 0
        
        data = {
            "question": f"철수의 3회까지의 수학 시험 점수는 각각 {scores[0]}점, {scores[1]}점, {scores[2]}점이다. 4회까지의 평균 점수가 {target_avg}점 이상이 되려면 4회 시험에서 최소 몇 점을 받아야 하는가?",
            "answer": min_score,
            "explanation": f"4회 점수를 $x$라 하면 $\\frac{{ {scores[0]} + {scores[1]} + {scores[2]} + x }}{{4}} \\ge {target_avg}$ \n${sum(scores)} + x \\ge {4*target_avg}$ \n$x \\ge {min_score}$ \n따라서 최소 {min_score}점을 받아야 합니다."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(min_score, 3, 5) + [min_score]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T127_Master(BaseTMaster):
    """T127: 비용과 요금에 관한 문제 (유리한 방법)"""
    def __init__(self):
        super().__init__("T127", "유리한 방법 선택")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 동네 가게: 개당 p1원
        # 도매 시장: 개당 p2원 (p2 < p1), 왕복 교통비 c원
        # 몇 개 이상 사야 도매 시장이 유리한가?
        # p1*x > p2*x + c  => (p1-p2)x > c => x > c/(p1-p2)
        
        p1 = random.randint(10, 20) * 100 # 1000 ~ 2000
        diff = random.randint(2, 5) * 100 # 200 ~ 500
        p2 = p1 - diff
        
        min_count = random.randint(5, 20)
        c = diff * min_count + random.randint(1, diff - 1) # c / diff = min_count.xxx
        
        # x > c / diff
        ans = int(c / diff) + 1
        
        data = {
            "question": f"집 앞 가게에서는 사과 한 개에 {p1}원이고, 도매 시장에서는 {p2}원이다. 도매 시장에 다녀오는 데 왕복 교통비가 {c}원 든다고 할 때, 사과를 몇 개 이상 살 경우 도매 시장에서 사는 것이 유리한가?",
            "answer": ans,
            "explanation": f"사과를 $x$개 산다고 하면 ${p1}x > {p2}x + {c}$ \n${p1-p2}x > {c}$ \n$x > {c/(p1-p2):.1f}...$ \n따라서 {ans}개 이상 사야 유리합니다."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 3) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T128_Master(BaseTMaster):
    """T128: 거리, 속력, 시간에 관한 문제"""
    def __init__(self):
        super().__init__("T128", "거속시 부등식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 역에서 기차 출발까지 t분 여유. 시속 v km로 상점 다녀옴. 물건 사는데 s분. 최대 거리?
        # (x/v) + (x/v) + (s/60) <= t/60
        # 2x/v <= (t-s)/60
        # x <= (t-s)/60 * v / 2
        
        v = random.choice([3, 4, 5]) # 시속
        t_total = random.choice([40, 50, 60, 70, 80, 90]) # 분
        s_shop = random.choice([10, 15, 20]) # 분
        
        time_walk_min = t_total - s_shop
        
        # 답이 깔끔하게 나오도록 조정
        while (time_walk_min * v) % 12 != 0: # 120으로 나누어 떨어지거나 .5 등으로 끝나게 (120 = 12 * 10)
             t_total = random.choice([40, 50, 60, 70, 80, 90])
             s_shop = random.choice([10, 15, 20])
             time_walk_min = t_total - s_shop
             if time_walk_min <= 0: continue
        
        ans = (time_walk_min * v) / 120
        if ans.is_integer(): ans = int(ans)
        
        data = {
            "question": f"기차 출발 시각까지 {t_total}분의 여유가 있어 역전 상점에서 물건을 사 오려고 한다. 물건을 사는 데 {s_shop}분이 걸리고 시속 {v}km로 걷는다면, 역에서 최대 몇 km 이내에 있는 상점을 이용할 수 있는가?",
            "answer": ans,
            "explanation": f"거리를 $x$ km라 하면 (왕복 시간) + (물건 사는 시간) $\\le \\frac{{{t_total}}}{{60}}$ (시간)\n$\\frac{{2x}}{{{v}}} + \\frac{{{s_shop}}}{{60}} \\le \\frac{{{t_total}}}{{60}}$ \n$\\frac{{2x}}{{{v}}} \\le \\frac{{{time_walk_min}}}{{60}}$ \n$x \\le {ans}$ \n따라서 최대 {ans}km 이내입니다."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 2) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T129_Master(BaseTMaster):
    """T129: 농도에 관한 문제"""
    def __init__(self):
        super().__init__("T129", "농도 부등식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # a% 소금물 Ag에 물(0%)을 넣어 b% 이하가 되게 하려면 물을 최소 몇 g?
        # 소금 양: A * a/100
        # 전체 양: A + x
        # 농도: (A*a/100) / (A+x) * 100 <= b
        # A*a <= b(A+x)
        # x >= A*a/b - A = A(a/b - 1)
        
        a = random.choice([10, 12, 15, 20])
        A = random.choice([100, 200, 300, 400])
        b = random.choice([i for i in range(2, a) if a % i == 0]) # a의 약수여야 계산 깔끔
        
        min_water = int(A * (a/b - 1))
        
        data = {
            "question": f"{a}%의 소금물 {A}g이 있다. 여기에 물을 더 넣어 농도가 {b}% 이하가 되게 하려고 한다. 물을 최소 몇 g 더 넣어야 하는가?",
            "answer": min_water,
            "explanation": f"더 넣을 물의 양을 $x$ g이라 하면 \n$\\frac{{{a}}}{{100}} \\times {A} \\div ({A} + x) \\times 100 \\le {b}$ \n${a*A} \\le {b}({A} + x)$ \n${a*A} \\le {b*A} + {b}x$ \n${b}x \\ge {a*A - b*A}$ \n$x \\ge {min_water}$"
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(min_water, 3, 50) + [min_water]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
