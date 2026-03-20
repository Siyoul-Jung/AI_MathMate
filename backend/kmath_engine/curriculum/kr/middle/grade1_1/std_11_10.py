import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils
from kmath_engine.template import ProblemTemplate

# ==========================================
# [STD-11-10] 정비례와 반비례 (T63 ~ T70)
# ==========================================

class T63_Master(BaseTMaster):
    """T63: 정비례 관계의 이해와 식 세우기"""
    def __init__(self):
        super().__init__("T63", "정비례 식 세우기")

        # --- 유형 1: 기본 관계식 구하기 (교과서 예제 스타일) ---
        def gen_vars_type1():
            # 약분이 깔끔하게 되거나 정수가 나오는 숫자만 선택
            x = random.choice([2, 3, 4, 5, 10])
            a = random.choice([2, 3, 4, 5, -2, -3, -4, -5])
            y = a * x
            return {"x": x, "y": y, "a": a}

        self.template_type1 = ProblemTemplate(
            question_format="$y$가 $x$에 정비례하고, $x = {x}$일 때 $y = {y}$이다. $y$를 $x$에 대한 식으로 나타내시오.",
            variable_gen_func=gen_vars_type1,
            answer_calc_func=lambda v: f"y = {v['a']}x" if v['a'] != -1 and v['a'] != 1 else (f"y = -x" if v['a'] == -1 else "y = x"),
            explanation_format="정비례 관계식을 $y = ax$라 하면, $x={x}, y={y}$이므로 ${y} = a \\times {x}$ 입니다.\n따라서 $a = {a}$ 이므로 구하는 식은 $y = {a}x$ 입니다.",
            logic_step_gen_func=lambda v: [
                {"step_id": 1, "description": "정비례 관계식을 y = ax로 둡니다.", "target_expr": "y = ax", "concept_id": "DIRECT_PROP_FORM"},
                {"step_id": 2, "description": "주어진 x, y 값을 대입하여 a를 구합니다.", "target_expr": f"{v['y']} = a * {v['x']}", "concept_id": "FIND_CONSTANT"},
                {"step_id": 3, "description": "구한 a를 대입하여 식을 완성합니다.", "target_expr": f"y = {v['a']}x", "concept_id": "COMPLETE_EQUATION"}
            ]
        )

        # --- 유형 2: 함수값 구하기 (쎈 B단계 스타일) ---
        def gen_vars_type2():
            a = random.choice([2, 3, 4, 5, 6, -2, -3, -4])
            x1 = random.randint(2, 5)
            y1 = a * x1
            x2 = random.randint(6, 9) * random.choice([1, -1])
            return {"x1": x1, "y1": y1, "x2": x2, "a": a}

        self.template_type2 = ProblemTemplate(
            question_format="$y$가 $x$에 정비례하고, $x = {x1}$일 때 $y = {y1}$이다. $x = {x2}$일 때 $y$의 값은?",
            variable_gen_func=gen_vars_type2,
            answer_calc_func=lambda v: v['a'] * v['x2'],
            explanation_format="$y = ax$에 $x={x1}, y={y1}$을 대입하면 ${y1} = {x1}a$ 이므로 $a = {a}$ 입니다.\n따라서 관계식은 $y = {a}x$ 입니다.\n이 식에 $x = {x2}$를 대입하면 $y = {a} \\times ({x2}) = {answer}$ 입니다.",
            logic_step_gen_func=lambda v: [
                {"step_id": 1, "description": "정비례 관계식 y=ax에 첫 번째 조건을 대입하여 a를 구합니다.", "target_expr": f"a = {v['a']}", "concept_id": "FIND_CONSTANT"},
                {"step_id": 2, "description": "완성된 식에 두 번째 x값을 대입합니다.", "target_expr": f"y = {v['a']} * {v['x2']}", "concept_id": "CALC_VALUE"}
            ]
        )

        # --- 유형 3: 문장제 문제 (RPM 유형) ---
        def gen_vars_type3():
            items = [("휘발유", "L", "km"), ("철사", "m", "g"), ("물", "L", "분")]
            item, unit1, unit2 = random.choice(items)
            
            if item == "휘발유":
                per_unit = random.randint(8, 15) # 연비
                q_text = f"어떤 자동차는 {item} 1{unit1}로 {per_unit}{unit2}를 달릴 수 있다고 한다. 이 자동차가 {item} $x${unit1}로 달릴 수 있는 거리를 $y${unit2}라 할 때, $y$를 $x$에 대한 식으로 나타내시오."
            elif item == "철사":
                per_unit = random.randint(10, 30) # 무게
                q_text = f"굵기가 일정한 {item} 1{unit1}의 무게가 {per_unit}{unit2}이다. 이 {item} $x${unit1}의 무게를 $y${unit2}라 할 때, $y$를 $x$에 대한 식으로 나타내시오."
            else:
                per_unit = random.randint(2, 5) # 급수량
                q_text = f"매분 {per_unit}{unit1}씩 {item}을 넣는 물통이 있다. $x${unit2} 동안 넣은 {item}의 양을 $y${unit1}라 할 때, $y$를 $x$에 대한 식으로 나타내시오."
            
            return {"q_text": q_text, "a": per_unit}

        self.template_type3 = ProblemTemplate(
            question_format="{q_text}",
            variable_gen_func=gen_vars_type3,
            answer_calc_func=lambda v: f"y = {v['a']}x",
            explanation_format="1단위당 {a}씩 증가하므로 $x$단위일 때는 ${a}x$가 됩니다.\n따라서 $y = {a}x$ 입니다."
        )

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 난이도나 요청에 따라 템플릿 선택
        if difficulty == "Easy":
            selected_template = self.template_type1
        elif difficulty == "Hard":
            selected_template = self.template_type2
        else:
            selected_template = random.choice([self.template_type1, self.template_type2, self.template_type3])
        
        data = selected_template.generate(q_type)

        if q_type == "multi":
            ans = data["answer"]
            if "options" not in data:
                # 템플릿에 옵션 생성기가 없으면 기본 생성
                if isinstance(ans, str) and "=" in ans: # 식 형태
                    options = [ans, ans.replace("x", "/x"), ans.replace("=", "= -"), ans.replace("x", " + x")]
                else: # 숫자 형태
                    options = MathUtils.generate_distractors(ans, 3, 5) + [ans]
                random.shuffle(options)
                data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T64_Master(BaseTMaster):
    """T64: 정비례 관계의 그래프 성질"""
    def __init__(self):
        super().__init__("T64", "정비례 그래프 성질")

    def generate(self, difficulty="Normal", q_type="multi"):
        a = random.choice([-3, -2, 2, 3])
        
        if q_type == "short_answer":
            x_val = random.randint(1, 3)
            y_val = a * x_val
            logic_steps = [
                {"step_id": 1, "description": "주어진 점의 x좌표를 식에 대입합니다.", "target_expr": f"x = {x_val}", "concept_id": "SUBSTITUTION"},
                {"step_id": 2, "description": "y값을 계산하여 k를 구합니다.", "target_expr": "k 계산", "concept_id": "CALC_VALUE"}
            ]
            data = {
                "question": f"정비례 관계 y = {a}x 의 그래프가 점 ({x_val}, k)를 지날 때, k의 값은?",
                "answer": y_val,
                "explanation": f"x={x_val}을 대입하면 y = {a} * {x_val} = {y_val} 입니다.",
                "logic_steps": logic_steps
            }
            return self._format_response(data, q_type, difficulty)
        
        if a > 0:
            correct = "제1사분면과 제3사분면을 지난다."
            wrong = "제2사분면과 제4사분면을 지난다."
            trend = "x의 값이 증가하면 y의 값도 증가한다."
        else:
            correct = "제2사분면과 제4사분면을 지난다."
            wrong = "제1사분면과 제3사분면을 지난다."
            trend = "x의 값이 증가하면 y의 값은 감소한다."
            
        options = [
            "원점을 지나는 직선이다.",
            correct,
            trend,
            f"점 (1, {a})를 지난다.",
            wrong  # 정답 (옳지 않은 것 찾기 문제로 가정하거나, 옳은 것 찾기 등)
        ]
        
        # 문제를 '옳지 않은 것' 찾기로 설정
        logic_steps = [
            {"step_id": 1, "description": "비례상수 a의 부호를 확인합니다.", "target_expr": f"a = {a}", "concept_id": "CHECK_SIGN"},
            {"step_id": 2, "description": "a의 부호에 따른 그래프의 특징(지나는 사분면, 증감 상태)을 떠올립니다.", "target_expr": "성질 확인", "concept_id": "GRAPH_PROPERTIES"},
            {"step_id": 3, "description": "보기 중 성질과 다른 것을 찾습니다.", "target_expr": "오답 찾기", "concept_id": "IDENTIFY_ERROR"}
        ]
        data = {
            "question": f"정비례 관계 y = {a}x 의 그래프에 대한 설명으로 옳지 않은 것은?",
            "options": options,
            "answer": wrong,
            "explanation": f"a가 {'양수' if a > 0 else '음수'}이므로 그래프는 {correct.replace('을 지난다', '')}을 지납니다.",
            "logic_steps": logic_steps
        }
        return self._format_response(data, q_type, difficulty)

class T66_Master(BaseTMaster):
    """T66: 반비례 관계의 이해와 식 세우기"""
    def __init__(self):
        super().__init__("T66", "반비례 식 세우기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # y가 x에 반비례하고, x=a일 때 y=b이다.
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        k = a * b # 비례상수 a (y = a/x)
        
        logic_steps = [
            {"step_id": 1, "description": "반비례 관계식을 y = a/x로 둡니다.", "target_expr": "y = a/x", "concept_id": "INVERSE_PROP_FORM"},
            {"step_id": 2, "description": "주어진 x, y 값을 대입하여 a를 구합니다. (a = xy)", "target_expr": f"a = {a} * {b}", "concept_id": "FIND_CONSTANT"},
            {"step_id": 3, "description": "구한 a를 대입하여 식을 완성합니다.", "target_expr": "식 완성", "concept_id": "COMPLETE_EQUATION"}
        ]

        data = {
            "question": f"y가 x에 반비례하고, x = {a} 일 때 y = {b} 이다. y를 x에 대한 식으로 나타내시오.",
            "answer": f"y = {k}/x",
            "explanation": f"반비례 관계식은 y = a/x (또는 xy = a) 꼴입니다. {a} × {b} = a 이므로 a = {k}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = [f"y = {k}/x", f"y = {k}x", f"y = x/{k}", f"y = -{k}/x"]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T67_Master(BaseTMaster):
    """T67: 반비례 관계의 그래프 성질"""
    def __init__(self):
        super().__init__("T67", "반비례 그래프 성질")

    def generate(self, difficulty="Normal", q_type="ox"):
        a = random.choice([-5, -3, 3, 5])
        
        if a > 0:
            q_text = f"반비례 관계 y = {a}/x 의 그래프는 제1사분면과 제3사분면을 지난다."
            ans = "O"
            expl = "비례상수가 양수이므로 제1, 3사분면을 지나는 매끄러운 곡선입니다."
        else:
            q_text = f"반비례 관계 y = {a}/x 의 그래프는 x의 값이 증가하면 y의 값도 증가한다."
            ans = "O" # 음수일 때 x증가 -> y증가 (각 사분면 내에서)
            expl = "비례상수가 음수일 때, 각 사분면에서 x가 증가하면 y도 증가합니다."
            
        logic_steps = [
            {"step_id": 1, "description": "비례상수 a의 부호를 확인합니다.", "target_expr": f"a = {a}", "concept_id": "CHECK_SIGN"},
            {"step_id": 2, "description": "a의 부호에 따른 반비례 그래프의 특징을 확인합니다.", "target_expr": "성질 확인", "concept_id": "GRAPH_PROPERTIES"},
            {"step_id": 3, "description": "설명의 참/거짓을 판단합니다.", "target_expr": "판별", "concept_id": "LOGICAL_JUDGEMENT"}
        ]

        data = {
            "question": f"다음 설명의 참(O), 거짓(X)을 판별하시오.\n'{q_text}'",
            "options": ["O", "X"],
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps
        }
        
        if q_type == "short_answer":
            data["options"] = []
            
        return self._format_response(data, q_type, difficulty)

class T68_Master(BaseTMaster):
    """T68: 반비례 관계의 실생활 활용"""
    def __init__(self):
        super().__init__("T68", "반비례 활용")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        scenario = random.choice(["work", "rectangle"])
        
        if scenario == "work":
            # 전형적인 반비례: 곱이 일정한 경우
            # 어떤 일을 x명이 하면 y일 걸린다. (전체 일의 양 일정)
            total_work = random.choice([24, 30, 36, 40, 48, 60])
            x_val = random.choice([i for i in range(2, 10) if total_work % i == 0])
            
            logic_steps = [
                {"step_id": 1, "description": "사람 수와 날수의 곱이 일정함을 이용하여 전체 일의 양을 구합니다.", "target_expr": "xy = k", "concept_id": "INVERSE_RELATION"},
                {"step_id": 2, "description": "주어진 사람 수를 식에 대입하여 걸리는 날수를 구합니다.", "target_expr": "y 구하기", "concept_id": "SOLVE_FOR_UNKNOWN"}
            ]

            data = {
                "question": f"어떤 일을 {x_val}명이 함께 하면 완성하는 데 {total_work // x_val}일이 걸린다. 같은 일을 x명이 함께 할 때 걸리는 날수를 y일이라 하자. {total_work // 2}명이 함께 하면 며칠이 걸리는가?",
                "answer": 2,
                "explanation": f"사람 수(x)와 날수(y)의 곱은 전체 일의 양({total_work})으로 일정하므로 xy = {total_work} (반비례)입니다. \n{total_work // 2} × y = {total_work} 이므로 y = 2일입니다.",
                "logic_steps": logic_steps
            }
        else:
            # Rectangle area fixed
            area = random.choice([12, 18, 24, 30, 36])
            x_val = random.choice([i for i in range(2, area) if area % i == 0])
            y_val = area // x_val
            
            logic_steps = [
                {"step_id": 1, "description": "직사각형의 넓이 공식을 이용하여 x와 y의 관계식을 세웁니다.", "target_expr": "xy = 넓이", "concept_id": "INVERSE_RELATION"},
                {"step_id": 2, "description": "주어진 가로 길이를 대입하여 세로 길이를 구합니다.", "target_expr": "y 구하기", "concept_id": "SOLVE_FOR_UNKNOWN"}
            ]

            data = {
                "question": f"넓이가 {area}cm²인 직사각형의 가로의 길이를 x cm, 세로의 길이를 y cm라고 하자. 가로의 길이가 {x_val}cm일 때, 세로의 길이는?",
                "answer": y_val,
                "explanation": f"직사각형의 넓이는 가로 × 세로이므로 xy = {area} (반비례)입니다. \n{x_val} × y = {area} 이므로 y = {y_val}cm입니다.",
                "logic_steps": logic_steps
            }
            
        if q_type == "multi":
            ans = data["answer"]
            options = MathUtils.generate_distractors(ans, 3, 5) + [ans]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T69_Master(BaseTMaster):
    """T69: 정비례/반비례 관계의 혼합"""
    def __init__(self):
        super().__init__("T69", "정비례와 반비례 혼합")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 정비례 y=ax와 반비례 y=b/x가 점 P(p, q)에서 만난다.
        p = random.choice([-2, -1, 1, 2, 3])
        q = random.choice([-6, -4, -2, 2, 4, 6])
        
        # a = q/p, b = p*q
        # a를 구하라고 하거나 b를 구하라고 함
        
        logic_steps = [
            {"step_id": 1, "description": "교점은 두 그래프 모두 위에 있는 점임을 이해합니다.", "target_expr": "대입 가능", "concept_id": "INTERSECTION_POINT"},
            {"step_id": 2, "description": "점의 좌표를 반비례 관계식에 대입하여 상수를 구합니다.", "target_expr": "b 구하기", "concept_id": "SOLVE_FOR_CONSTANT"}
        ]

        data = {
            "question": f"정비례 관계 y = ax의 그래프와 반비례 관계 y = b/x의 그래프가 점 ({p}, {q})에서 만날 때, 상수 b의 값은?",
            "answer": p * q,
            "explanation": f"점 ({p}, {q})는 반비례 그래프 위의 점이므로 대입하면 {q} = b/{p} => b = {p} × {q} = {p*q}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(p * q, 3, 5) + [p * q]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T70_Master(BaseTMaster):
    """T70: 그래프와 도형의 넓이 응용"""
    def __init__(self):
        super().__init__("T70", "그래프와 도형")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 반비례 y = a/x 위의 점 P에서 x축, y축에 수선을 그어 만든 직사각형 넓이
        # 넓이 = |x| * |y| = |x * a/x| = |a|
        a = random.choice([i for i in range(-10, 11) if i != 0])
        
        logic_steps = [
            {"step_id": 1, "description": "직사각형의 가로와 세로 길이를 점 P의 좌표로 나타냅니다.", "target_expr": "가로:|x|, 세로:|y|", "concept_id": "RECTANGLE_DIMENSIONS"},
            {"step_id": 2, "description": "반비례 관계식 xy=a를 이용하여 넓이를 구합니다.", "target_expr": "넓이 = |a|", "concept_id": "AREA_CALCULATION"}
        ]

        data = {
            "question": f"반비례 관계 y = {a}/x 의 그래프 위의 한 점 P에서 x축, y축에 각각 수선을 그어 직사각형을 만들었다. 이 직사각형의 넓이는?",
            "answer": abs(a),
            "explanation": f"점 P의 좌표를 (x, y)라 하면 직사각형의 넓이는 |xy|입니다. \ny = {a}/x 에서 xy = {a}이므로 넓이는 |{a}| = {abs(a)}입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(abs(a), 3, 5) + [abs(a)]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)
