import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

# ==========================================
# [STD-11-08] 일차방정식의 활용 (T48 ~ T56)
# ==========================================

class T48_Master(BaseTMaster):
    """T48: 수에 관한 문제 (연속하는 수)"""
    def __init__(self):
        super().__init__("T48", "연속하는 수")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 연속하는 세 자연수의 합
        start = random.randint(5, 30)
        nums = [start, start + 1, start + 2]
        total = sum(nums)
        
        logic_steps = [
            {"step_id": 1, "description": "가운데 수를 x로 두고 연속하는 세 자연수를 표현합니다.", "target_expr": "x-1, x, x+1", "concept_id": "DEFINE_UNKNOWNS"},
            {"step_id": 2, "description": "세 수의 합이 주어졌으므로 방정식을 세웁니다.", "target_expr": f"(x-1) + x + (x+1) = {total}", "concept_id": "SETUP_EQUATION"},
            {"step_id": 3, "description": "방정식을 풀어 x를 구하고 가장 큰 수를 찾습니다.", "target_expr": "가장 큰 수 구하기", "concept_id": "SOLVE_AND_ANSWER"}
        ]

        data = {
            "question": f"연속하는 세 자연수의 합이 {total}일 때, 가장 큰 수는?",
            "answer": nums[2],
            "explanation": f"가운데 수를 x라 하면 (x-1) + x + (x+1) = {total} => 3x = {total} => x = {nums[1]}. 가장 큰 수는 {nums[2]}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(nums[2], 3, 5) + [nums[2]]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T49_Master(BaseTMaster):
    """T49: 나이에 관한 문제"""
    def __init__(self):
        super().__init__("T49", "나이 구하기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 아버지 나이 F, 아들 나이 S. x년 후에 아버지가 아들의 k배
        # F + x = k(S + x)
        k = random.randint(2, 3)
        x_ans = random.randint(5, 20)
        
        # 현재 나이 설정 (역산)
        # F - kS = x(k - 1)
        # 적절한 S 설정
        S = random.randint(10, 15)
        F = k * (S + x_ans) - x_ans
        
        logic_steps = [
            {"step_id": 1, "description": "x년 후의 아버지와 아들의 나이를 x를 사용하여 나타냅니다.", "target_expr": f"아버지: {F}+x, 아들: {S}+x", "concept_id": "EXPRESS_AGE"},
            {"step_id": 2, "description": "문제의 조건(k배)에 맞게 방정식을 세웁니다.", "target_expr": f"{F}+x = {k}({S}+x)", "concept_id": "SETUP_EQUATION"},
            {"step_id": 3, "description": "방정식을 풀어 x를 구합니다.", "target_expr": "x 구하기", "concept_id": "SOLVE_LINEAR_EQ"}
        ]

        data = {
            "question": f"현재 아버지의 나이는 {F}세, 아들의 나이는 {S}세이다. 아버지의 나이가 아들의 나이의 {k}배가 되는 것은 몇 년 후인가?",
            "answer": x_ans,
            "explanation": f"x년 후 아버지: {F}+x, 아들: {S}+x. \n{F}+x = {k}({S}+x) 방정식을 풀면 x = {x_ans}년 후입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(x_ans, 3, 5) + [x_ans]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T50_Master(BaseTMaster):
    """T50: 도형에 관한 문제 (둘레)"""
    def __init__(self):
        super().__init__("T50", "도형의 둘레/넓이")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 직사각형 둘레
        width = random.randint(5, 20)
        diff = random.randint(2, 8)
        length = width + diff
        perimeter = 2 * (width + length)
        
        logic_steps = [
            {"step_id": 1, "description": "세로의 길이를 x라 하고 가로의 길이를 x로 나타냅니다.", "target_expr": f"세로: x, 가로: x+{diff}", "concept_id": "DEFINE_UNKNOWNS"},
            {"step_id": 2, "description": "직사각형의 둘레 공식을 이용하여 방정식을 세웁니다.", "target_expr": f"2(x + x+{diff}) = {perimeter}", "concept_id": "SETUP_EQUATION"},
            {"step_id": 3, "description": "방정식을 풀어 세로의 길이를 구합니다.", "target_expr": "x 구하기", "concept_id": "SOLVE_LINEAR_EQ"}
        ]

        data = {
            "question": f"가로의 길이가 세로의 길이보다 {diff}cm 더 긴 직사각형이 있다. 이 직사각형의 둘레의 길이가 {perimeter}cm일 때, 세로의 길이는?",
            "answer": width,
            "explanation": f"세로를 x라 하면 가로는 x+{diff}. \n2(x + x+{diff}) = {perimeter} => 4x + {2*diff} = {perimeter} => 4x = {perimeter - 2*diff} => x = {width}cm",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(width, 3, 5) + [width]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T52_Master(BaseTMaster):
    """T52: 일의 양에 관한 문제"""
    def __init__(self):
        super().__init__("T52", "일의 양")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # A는 a일, B는 b일 걸림. 함께 하면 x일.
        # 1/a + 1/b = 1/x (x가 정수가 되도록 a, b 설정)
        # 예: A=10, B=15 -> 1/10 + 1/15 = 3/30 + 2/30 = 5/30 = 1/6 -> 6일
        pairs = [(10, 15, 6), (12, 24, 8), (20, 30, 12), (6, 12, 4)]
        a, b, ans = random.choice(pairs)
        
        logic_steps = [
            {"step_id": 1, "description": "전체 일의 양을 1로 두고, 형과 동생이 하루에 하는 일의 양을 구합니다.", "target_expr": f"형: 1/{a}, 동생: 1/{b}", "concept_id": "WORK_RATE"},
            {"step_id": 2, "description": "함께 일할 때 걸리는 날수를 x라 하고 방정식을 세웁니다.", "target_expr": f"(1/{a} + 1/{b})x = 1", "concept_id": "SETUP_EQUATION"},
            {"step_id": 3, "description": "방정식을 풀어 x를 구합니다.", "target_expr": "x 구하기", "concept_id": "SOLVE_LINEAR_EQ"}
        ]

        data = {
            "question": f"어떤 일을 혼자서 하면 형은 {a}일, 동생은 {b}일이 걸린다고 한다. 이 일을 형과 동생이 함께 한다면 며칠이 걸리는가?",
            "answer": ans,
            "explanation": f"전체 일의 양을 1이라 하면 형은 하루에 1/{a}, 동생은 1/{b}만큼 일합니다. \n함께 하면 하루에 1/{a} + 1/{b} = 1/{ans}만큼 하므로 {ans}일이 걸립니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 3) + [ans]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T53_Master(BaseTMaster):
    """T53: 거리, 속력, 시간에 관한 문제 (등산)"""
    def __init__(self):
        super().__init__("T53", "거속시 (등산/만남)")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        scenario = random.choice(["hiking", "meeting"])
        
        if scenario == "hiking":
            # 올라갈 때 v1, 내려올 때 v2, 총 시간 t
            # 거리 d = t * (v1 * v2) / (v1 + v2)
            pairs = [(2, 3, 5, 6), (3, 4, 7, 12), (2, 4, 3, 4), (3, 6, 3, 6), (4, 6, 5, 12)]
            v1, v2, t, d = random.choice(pairs)
            
            logic_steps = [
                {"step_id": 1, "description": "등산로의 거리를 x km라 둡니다.", "target_expr": "거리: x", "concept_id": "DEFINE_UNKNOWNS"},
                {"step_id": 2, "description": "시간 = 거리/속력 공식을 이용하여 총 시간에 대한 방정식을 세웁니다.", "target_expr": f"x/{v1} + x/{v2} = {t}", "concept_id": "SETUP_EQUATION"},
                {"step_id": 3, "description": "양변에 최소공배수를 곱하여 방정식을 풉니다.", "target_expr": "x 구하기", "concept_id": "SOLVE_LINEAR_EQ"}
            ]

            data = {
                "question": f"등산을 하는데 올라갈 때는 시속 {v1}km로 걷고, 내려올 때는 같은 길을 시속 {v2}km로 걸어서 총 {t}시간이 걸렸다. 등산로의 거리는 몇 km인가?",
                "answer": d,
                "explanation": f"거리를 x라 하면 시간 = 거리/속력 이므로 x/{v1} + x/{v2} = {t}. \n양변에 {MathUtils.get_lcm(v1, v2)}를 곱해 풀면 x = {d}km입니다.",
                "logic_steps": logic_steps
            }
        else: # meeting
            # 두 지점 사이 거리 D. A속력 v1, B속력 v2. 마주보고 출발.
            # t시간 후 만남. D = (v1 + v2) * t
            v1 = random.randint(3, 5) # 걷는 속력
            v2 = random.randint(3, 5)
            t = random.randint(1, 3)
            d = (v1 + v2) * t
            
            logic_steps = [
                {"step_id": 1, "description": "만날 때까지 걸린 시간을 x시간이라 둡니다.", "target_expr": "시간: x", "concept_id": "DEFINE_UNKNOWNS"},
                {"step_id": 2, "description": "두 사람이 이동한 거리의 합이 전체 거리와 같음을 이용하여 식을 세웁니다.", "target_expr": f"{v1}x + {v2}x = {d}", "concept_id": "SETUP_EQUATION"},
                {"step_id": 3, "description": "방정식을 풀어 x를 구합니다.", "target_expr": "x 구하기", "concept_id": "SOLVE_LINEAR_EQ"}
            ]

            data = {
                "question": f"두 지점 A, B 사이의 거리는 {d}km이다. A지점에서 철수가 시속 {v1}km로, B지점에서 영희가 시속 {v2}km로 동시에 마주 보고 출발하였다. 두 사람은 출발한 지 몇 시간 후에 만나는가?",
                "answer": t,
                "explanation": f"만날 때까지 걸린 시간을 x시간이라 하면, 두 사람이 이동한 거리의 합은 전체 거리와 같습니다.\n{v1}x + {v2}x = {d} \n{v1+v2}x = {d} \nx = {t}시간",
                "logic_steps": logic_steps
            }
            
        if q_type == "multi":
            ans = data["answer"]
            options = MathUtils.generate_distractors(ans, 3, 3) + [ans]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T54_Master(BaseTMaster):
    """T54: 농도에 관한 문제 (물 증발/첨가)"""
    def __init__(self):
        super().__init__("T54", "소금물 농도")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        scenario = random.choice(["evaporation", "dilution"])
        
        if scenario == "evaporation":
            # a% 소금물 Wg에서 물을 xg 증발시켜 b% 소금물 만듦
            cases = [
                (10, 200, 20, 100),
                (5, 400, 10, 200),
                (6, 300, 9, 100),
                (8, 500, 10, 100)
            ]
            a, W, b, ans = random.choice(cases)
            
            logic_steps = [
                {"step_id": 1, "description": "증발시킨 물의 양을 x g이라 둡니다.", "target_expr": "물: x", "concept_id": "DEFINE_UNKNOWNS"},
                {"step_id": 2, "description": "증발 전후 소금의 양은 변하지 않음을 이용하여 방정식을 세웁니다.", "target_expr": f"{a}/100 * {W} = {b}/100 * ({W}-x)", "concept_id": "SETUP_EQUATION"},
                {"step_id": 3, "description": "방정식을 풀어 x를 구합니다.", "target_expr": "x 구하기", "concept_id": "SOLVE_LINEAR_EQ"}
            ]

            data = {
                "question": f"{a}%의 소금물 {W}g이 있다. 여기서 물을 몇 g 증발시키면 {b}%의 소금물이 되는가?",
                "answer": ans,
                "explanation": f"증발시킨 물의 양을 x라 하면 소금의 양은 변하지 않으므로 \n{a}/100 × {W} = {b}/100 × ({W}-x). \n방정식을 풀면 x = {ans}g입니다.",
                "logic_steps": logic_steps
            }
        else: # dilution (adding water)
            # a% 소금물 Wg -> 물 xg 첨가 -> b%
            cases = [
                (20, 100, 10, 100),
                (15, 200, 10, 100),
                (10, 300, 6, 200),
                (12, 100, 4, 200)
            ]
            a, W, b, ans = random.choice(cases)
            
            logic_steps = [
                {"step_id": 1, "description": "더 넣은 물의 양을 x g이라 둡니다.", "target_expr": "물: x", "concept_id": "DEFINE_UNKNOWNS"},
                {"step_id": 2, "description": "물 첨가 전후 소금의 양은 변하지 않음을 이용하여 방정식을 세웁니다.", "target_expr": f"{a}/100 * {W} = {b}/100 * ({W}+x)", "concept_id": "SETUP_EQUATION"},
                {"step_id": 3, "description": "방정식을 풀어 x를 구합니다.", "target_expr": "x 구하기", "concept_id": "SOLVE_LINEAR_EQ"}
            ]

            data = {
                "question": f"{a}%의 소금물 {W}g이 있다. 여기에 물을 몇 g 더 넣으면 {b}%의 소금물이 되는가?",
                "answer": ans,
                "explanation": f"더 넣은 물의 양을 x라 하면 소금의 양은 변하지 않으므로 \n{a}/100 × {W} = {b}/100 × ({W}+x). \n방정식을 풀면 x = {ans}g입니다.",
                "logic_steps": logic_steps
            }
            
        if q_type == "multi":
            ans = data["answer"]
            options = MathUtils.generate_distractors(ans, 3, 50) + [ans]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T55_Master(BaseTMaster):
    """T55: 원가, 정가에 관한 문제"""
    def __init__(self):
        super().__init__("T55", "원가/정가/이익")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 원가 x, a% 이익 붙여 정가, b원 할인하여 팔았더니 c원 이익
        # (x * (1 + a/100)) - b - x = c
        # 예: 원가 1000, 30% 이익(1300), 100원 할인(1200) -> 이익 200
        cost = random.randint(10, 50) * 100 # 1000 ~ 5000
        profit_rate = random.choice([20, 30, 40, 50])
        discount = random.randint(1, 5) * 100 # 100 ~ 500
        
        price = cost * (1 + profit_rate/100)
        real_profit = price - discount - cost
        
        logic_steps = [
            {"step_id": 1, "description": "원가를 x원이라 두고, 정가와 판매가를 x로 나타냅니다.", "target_expr": f"정가: (1+{profit_rate}/100)x", "concept_id": "DEFINE_UNKNOWNS"},
            {"step_id": 2, "description": "판매가 - 원가 = 이익 임을 이용하여 방정식을 세웁니다.", "target_expr": f"(판매가) - x = {int(real_profit)}", "concept_id": "SETUP_EQUATION"},
            {"step_id": 3, "description": "방정식을 풀어 원가 x를 구합니다.", "target_expr": "x 구하기", "concept_id": "SOLVE_LINEAR_EQ"}
        ]

        data = {
            "question": f"어떤 물건의 원가에 {profit_rate}%의 이익을 붙여 정가를 정하고, 정가에서 {discount}원을 할인하여 팔았더니 {int(real_profit)}원의 이익이 생겼다. 이 물건의 원가는?",
            "answer": cost,
            "explanation": f"원가를 x라 하면 정가는 (1 + {profit_rate}/100)x. \n판매가 - 원가 = 이익 이므로 \n((1 + {profit_rate}/100)x - {discount}) - x = {int(real_profit)}. \n방정식을 풀면 x = {cost}원입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(cost, 3, 500) + [cost]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)
