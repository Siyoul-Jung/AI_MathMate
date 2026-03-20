import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

# ==========================================
# [STD-21-08] 연립일차방정식의 활용 (T137 ~ T141)
# ==========================================

class T137_Master(BaseTMaster):
    """T137: 수와 자릿수에 관한 문제"""
    def __init__(self):
        super().__init__("T137", "자릿수 문제")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 두 자리 자연수. 각 자리 숫자의 합은 S. 십의 자리와 일의 자리를 바꾼 수는 처음 수보다 D만큼 크다/작다.
        # 10x + y (처음), 10y + x (바꾼)
        # (10y + x) - (10x + y) = 9(y - x) = D
        
        diff = random.choice([1, 2, 3, 4]) # y - x
        D = 9 * diff
        
        # x + y = S
        # y - x = diff
        # 2y = S + diff => S + diff는 짝수여야 함
        
        x = random.randint(1, 8 - diff)
        y = x + diff
        S = x + y
        
        original_num = 10 * x + y
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "처음 수의 십의 자리 숫자를 $x$, 일의 자리 숫자를 $y$라 하고 미지수를 정합니다.",
                "target_expr": "처음 수: $10x + y$, 바꾼 수: $10y + x$",
                "concept_id": "DEFINE_UNKNOWNS"
            },
            {
                "step_id": 2,
                "description": "문제의 뜻에 맞게 연립방정식을 세웁니다. (각 자리 숫자의 합, 바꾼 수와 처음 수의 차)",
                "target_expr": f"$x + y = {S}$, $(10y + x) - (10x + y) = {D}$",
                "concept_id": "SETUP_EQUATIONS"
            },
            {
                "step_id": 3,
                "description": "연립방정식을 풀어 $x$와 $y$를 구하고 처음 수를 찾습니다.",
                "target_expr": "",
                "concept_id": "SOLVE_AND_ANSWER"
            }
        ]

        data = {
            "question": f"두 자리의 자연수가 있다. 각 자리의 숫자의 합은 ${S}$이고, 십의 자리의 숫자와 일의 자리의 숫자를 바꾼 수는 처음 수보다 ${D}$만큼 크다고 한다. 처음 수는?",
            "answer": original_num,
            "explanation": [
                "처음 수의 십의 자리 숫자를 $x$, 일의 자리 숫자를 $y$라 하면",
                f"각 자리 숫자의 합: $x + y = {S}$",
                f"바꾼 수 - 처음 수: $(10y + x) - (10x + y) = {D} \\Rightarrow 9y - 9x = {D} \\Rightarrow y - x = {diff}$",
                f"연립방정식을 풀면 $x={x}, y={y}$ 이므로 처음 수는 ${original_num}$입니다."
            ],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(original_num, 3, 10) + [original_num]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T138_Master(BaseTMaster):
    """T138: 나이와 개수에 관한 문제"""
    def __init__(self):
        super().__init__("T138", "개수/나이 문제")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 합해서 N개, 다리 수(또는 가격) 합계 M
        # 닭(2)과 토끼(4)
        heads = random.randint(10, 30)
        rabbits = random.randint(1, heads - 1)
        chickens = heads - rabbits
        
        legs = 2 * chickens + 4 * rabbits
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "닭의 수를 $x$, 토끼의 수를 $y$라 하고 미지수를 정합니다.",
                "target_expr": "닭: $x$마리, 토끼: $y$마리",
                "concept_id": "DEFINE_UNKNOWNS"
            },
            {
                "step_id": 2,
                "description": "전체 마리 수와 전체 다리 수에 대한 연립방정식을 세웁니다.",
                "target_expr": f"$x + y = {heads}$, $2x + 4y = {legs}$",
                "concept_id": "SETUP_EQUATIONS"
            },
            {
                "step_id": 3,
                "description": "연립방정식을 풀어 토끼의 수($y$)를 구합니다.",
                "target_expr": "",
                "concept_id": "SOLVE_AND_ANSWER"
            }
        ]

        data = {
            "question": f"닭과 토끼가 합하여 ${heads}$마리가 있다. 다리의 수의 합이 ${legs}$개일 때, 토끼는 몇 마리인가?",
            "answer": rabbits,
            "explanation": [
                "닭을 $x$마리, 토끼를 $y$마리라 하면",
                f"$x + y = {heads}$",
                f"$2x + 4y = {legs}$",
                f"연립방정식을 풀면 $x={chickens}, y={rabbits}$ 입니다."
            ],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(rabbits, 3, 5) + [rabbits]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T139_Master(BaseTMaster):
    """T139: 거리, 속력, 시간에 관한 문제 (강물)"""
    def __init__(self):
        super().__init__("T139", "강물 속력 문제")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 배 속력 v, 강물 속력 w
        # 올라갈 때: v - w, 내려올 때: v + w
        # 거리 d
        
        w = random.randint(2, 5)
        v = random.randint(w + 5, 20)
        
        # 시간 = 거리 / 속력
        # 시간이 정수가 되도록 거리 설정 (v-w, v+w의 공배수)
        speed_up = v - w
        speed_down = v + w
        lcm = MathUtils.get_lcm(speed_up, speed_down)
        d = lcm * random.randint(1, 3)
        
        t_up = d // speed_up
        t_down = d // speed_down
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "배의 속력을 $x$, 강물의 속력을 $y$라 합니다.",
                "target_expr": "올라갈 때 속력: $x-y$, 내려올 때 속력: $x+y$",
                "concept_id": "DEFINE_SPEEDS"
            },
            {
                "step_id": 2,
                "description": "속력 = 거리 / 시간 공식을 이용하여 연립방정식을 세웁니다.",
                "target_expr": f"$x - y = {d}/{t_up}$, $x + y = {d}/{t_down}$",
                "concept_id": "SETUP_EQUATIONS"
            },
            {
                "step_id": 3,
                "description": "두 식을 연립하여 배의 속력($x$)을 구합니다.",
                "target_expr": "",
                "concept_id": "SOLVE_AND_ANSWER"
            }
        ]

        data = {
            "question": f"배를 타고 길이가 ${d}$km인 강을 거슬러 올라가는 데 ${t_up}$시간, 내려오는 데 ${t_down}$시간이 걸렸다. 정지한 물에서의 배의 속력은 시속 몇 km인가?",
            "answer": v,
            "explanation": [
                "배의 속력을 $x$, 강물의 속력을 $y$라 하면",
                f"올라갈 때: $x - y = {d} \\div {t_up} = {speed_up}$",
                f"내려올 때: $x + y = {d} \\div {t_down} = {speed_down}$",
                f"두 식을 더하면 $2x = {speed_up + speed_down} \\Rightarrow x = {v}$ km/h"
            ],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(v, 3, 5) + [v]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T140_Master(BaseTMaster):
    """T140: 농도에 관한 문제 (두 소금물 섞기)"""
    def __init__(self):
        super().__init__("T140", "소금물 섞기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # a% 소금물 x g + b% 소금물 y g = c% 소금물 (x+y) g
        a = random.choice([3, 4, 5, 6])
        b = random.choice([8, 9, 10, 12])
        
        # x, y를 간단한 비율로 설정 (1:1, 1:2, 2:1 등)
        ratio_x = random.randint(1, 3)
        ratio_y = random.randint(1, 3)
        unit = 100
        x = ratio_x * unit
        y = ratio_y * unit
        total_weight = x + y
        
        # 혼합 농도 c 계산
        salt_x = x * a / 100
        salt_y = y * b / 100
        total_salt = salt_x + salt_y
        c = int(total_salt / total_weight * 100) # 정수로 떨어지게 조정 필요하지만 일단 진행
        
        # 정수가 안 나오면 다시 생성 (간단한 해결책)
        while (x * a + y * b) % total_weight != 0:
             x = random.randint(1, 5) * 100
             y = random.randint(1, 5) * 100
             total_weight = x + y
        
        c = (x * a + y * b) // total_weight
        
        logic_steps = [
            {
                "step_id": 1,
                "description": f"${a}\\%$ 소금물의 양을 $x$g, ${b}\\%$ 소금물의 양을 $y$g이라 합니다.",
                "target_expr": "$x, y$ 설정",
                "concept_id": "DEFINE_UNKNOWNS"
            },
            {
                "step_id": 2,
                "description": "전체 소금물의 양과 소금의 양에 대한 연립방정식을 세웁니다.",
                "target_expr": f"$x + y = {total_weight}$, $\\frac{{{a}}}{{100}}x + \\frac{{{b}}}{{100}}y = \\frac{{{c}}}{{100}} \\times {total_weight}$",
                "concept_id": "SETUP_EQUATIONS"
            },
            {
                "step_id": 3,
                "description": "연립방정식을 풀어 $x$의 값을 구합니다.",
                "target_expr": "",
                "concept_id": "SOLVE_AND_ANSWER"
            }
        ]

        data = {
            "question": f"${a}\\%$의 소금물과 ${b}\\%$의 소금물을 섞어서 ${c}\\%$의 소금물 ${total_weight}$g을 만들었다. ${a}\\%$의 소금물은 몇 g 섞었는가?",
            "answer": x,
            "explanation": [
                f"{a}% 소금물을 $x$g, {b}% 소금물을 $y$g이라 하면",
                f"1) $x + y = {total_weight}$",
                f"2) 소금의 양: $\\frac{{{a}}}{{100}}x + \\frac{{{b}}}{{100}}y = \\frac{{{c}}}{{100}} \\times {total_weight}$",
                f"연립방정식을 풀면 $x = {x}$g 입니다."
            ],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(x, 3, 50) + [x]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T141_Master(BaseTMaster):
    """T141: 일의 양과 증가/감소"""
    def __init__(self):
        super().__init__("T141", "증가/감소 문제")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 작년 남학생 x, 여학생 y. 올해 남 +a%, 여 -b%. 전체 변화 +c명.
        # x + y = Total_last
        # a/100 x - b/100 y = change
        
        x = random.randint(2, 6) * 100 # 200 ~ 600
        y = random.randint(2, 6) * 100
        total_last = x + y
        
        inc_rate = random.choice([5, 10, 15, 20])
        dec_rate = random.choice([5, 10, 15, 20])
        
        change = (x * inc_rate // 100) - (y * dec_rate // 100)
        change_str = f"{abs(change)}명 {'증가' if change >= 0 else '감소'}"
        if change == 0: change_str = "변화가 없었다"
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "작년 남학생 수를 $x$, 여학생 수를 $y$라 합니다.",
                "target_expr": "$x, y$ 설정",
                "concept_id": "DEFINE_UNKNOWNS"
            },
            {
                "step_id": 2,
                "description": "작년 전체 학생 수와 올해 변화한 학생 수에 대한 식을 세웁니다.",
                "target_expr": f"$x + y = {total_last}$, $\\frac{{{inc_rate}}}{{100}}x - \\frac{{{dec_rate}}}{{100}}y = {change}$",
                "concept_id": "SETUP_EQUATIONS"
            },
            {
                "step_id": 3,
                "description": "연립방정식을 풀어 작년 남학생 수($x$)를 구합니다.",
                "target_expr": "",
                "concept_id": "SOLVE_AND_ANSWER"
            }
        ]

        data = {
            "question": f"작년 전체 학생 수는 ${total_last}$명이었다. 올해는 작년에 비해 남학생은 ${inc_rate}\\%$ 증가하고, 여학생은 ${dec_rate}\\%$ 감소하여 전체적으로 {change_str}하였다. 작년 남학생 수는?",
            "answer": x,
            "explanation": [
                "작년 남학생 수를 $x$, 여학생 수를 $y$라 하면",
                f"1) $x + y = {total_last}$",
                f"2) $\\frac{{{inc_rate}}}{{100}}x - \\frac{{{dec_rate}}}{{100}}y = {change}$",
                f"연립방정식을 풀면 $x = {x}$명입니다."
            ],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(x, 3, 50) + [x]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
