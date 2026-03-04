import random
from core.base import BaseTMaster
from core.math_utils import MathUtils

# ==========================================
# [STD-11-05] 문자의 사용과 식의 값 (T29 ~ T31)
# ==========================================

class T29_Master(BaseTMaster):
    """T29: 문자를 사용한 식 세우기"""
    def __init__(self):
        super().__init__("T29", "문자를 사용한 식 세우기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 시나리오 데이터베이스 확장 (유형, 변수명, 값 생성기, 템플릿, 정답 생성기)
        scenarios = [
            # 1. 가격 (물건 구매 합계)
            {
                "vars": ["x", "y"],
                "vals": [random.randint(5, 15)*100, random.randint(2, 8)*100],
                "templates": [
                    "{v0}원짜리 공책 {x}권과 {v1}원짜리 연필 {y}자루의 가격의 합",
                    "한 개에 {v0}원인 빵 {x}개와 한 개에 {v1}원인 우유 {y}개를 샀을 때의 총 금액"
                ],
                "ans": lambda v, x, y: f"${v[0]}{x} + {v[1]}{y}$"
            },
            # 2. 거스름돈
            {
                "vars": ["a"],
                "vals": [random.randint(1, 5)*10000, random.randint(5, 15)*100],
                "templates": [
                    "{v0}원을 내고 한 개에 {v1}원인 아이스크림 {a}개를 샀을 때의 거스름돈",
                    "한 권에 {v1}원인 공책 {a}권을 사고 {v0}원을 냈을 때 거슬러 받는 돈"
                ],
                "ans": lambda v, a: f"${v[0]} - {v[1]}{a}$"
            },
            # 3. 거리 (속력 x 시간)
            {
                "vars": ["t"],
                "vals": [random.randint(3, 80)], # 시속
                "templates": [
                    "시속 {v0}km로 {t}시간 동안 이동한 거리(km)",
                    "매분 {v0}m의 속력으로 {t}분 동안 걸어간 거리(m)"
                ],
                "ans": lambda v, t: f"${v[0]}{t}$"
            },
            # 4. 시간 (거리 / 속력)
            {
                "vars": ["x"],
                "vals": [random.randint(5, 20)], # 거리
                "templates": [
                    "시속 {x}km로 {v0}km의 거리를 가는 데 걸리는 시간(시간)",
                    "{v0}km 떨어진 학교까지 시속 {x}km로 걸어갈 때 걸리는 시간"
                ],
                "ans": lambda v, x: f"$\\frac{{{v[0]}}}{{{x}}}$"
            },
            # 5. 도형 (삼각형 넓이)
            {
                "vars": ["a", "h"],
                "vals": [],
                "templates": [
                    "밑변의 길이가 {a}cm이고 높이가 {h}cm인 삼각형의 넓이(cm²)"
                ],
                "ans": lambda v, a, h: f"$\\frac{{1}}{{2}}{a}{h}$"
            },
            # 6. 수 (자릿수)
            {
                "vars": ["x", "y"],
                "vals": [],
                "templates": [
                    "십의 자리의 숫자가 {x}, 일의 자리의 숫자가 {y}인 두 자리의 자연수"
                ],
                "ans": lambda v, x, y: f"$10{x} + {y}$"
            }
        ]
        
        s = random.choice(scenarios)
        
        # 템플릿 포맷팅을 위한 딕셔너리 생성
        format_dict = {k: k for k in s["vars"]} # 변수명 매핑 (x='x')
        for i, val in enumerate(s["vals"]):
            format_dict[f"v{i}"] = val # 값 매핑 (v0=1000)
            
        # 랜덤 템플릿 선택 및 텍스트 생성
        template = random.choice(s["templates"])
        q_text = template.format(**format_dict)
        
        # 정답 생성
        ans = s["ans"](s["vals"], *s["vars"])

        logic_steps = self.get_logic_steps("T29")

        data = {
            "question": f"다음 문장을 문자를 사용한 식으로 나타내시오.\n'{q_text}'",
            "answer": ans,
            "explanation": "문제의 뜻에 맞게 수와 문자의 곱으로 표현합니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            # 객관식 오답 생성 (단순 변형)
            options = [ans, ans.replace("+", "-"), ans.replace("-", "+"), ans.replace("$", "") + " + 100$"]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T30_Master(BaseTMaster):
    """T30: 곱셈 및 나눗셈 기호의 생략"""
    def __init__(self):
        super().__init__("T30", "기호 생략하기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 케이스: 숫자*문자, 문자*문자, 나눗셈
        cases = [
            ("$x \\times 5$", "$5x$"),
            ("$a \\times (-1) \\times b$", "$-ab$"),
            ("$x \\div 3$", "$\\frac{x}{3}$"),
            ("$a \\times a \\times a$", "$a^3$"),
            ("$x \\times 0.1$", "$0.1x$")
        ]
        
        q, a = random.choice(cases)
        
        logic_steps = self.get_logic_steps("T30")

        data = {
            "question": f"다음 식을 곱셈, 나눗셈 기호를 생략하여 나타내시오.\n{q}",
            "answer": a,
            "explanation": "수는 문자 앞에 쓰고, 1은 생략하며, 나눗셈은 분수 꼴로 나타냅니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = [a, a.replace("x", "y"), a.replace("$", "") + "x$", "$1" + a.replace("$", "") + "$"]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T31_Master(BaseTMaster):
    """T31: 식의 값 대입"""
    def __init__(self):
        super().__init__("T31", "식의 값 구하기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": x_val = random.randint(1, 5)
        elif difficulty == "Hard": x_val = random.randint(-10, -5)
        else: x_val = random.randint(-5, 5)

        while x_val == 0: x_val = random.randint(-5, 5)
        
        # 식 유형: ax + b
        a = random.randint(2, 5)
        b = random.randint(-10, 10)
        
        expression = f"${a}x"
        if b >= 0: expression += f" + {b}"
        else: expression += f" - {abs(b)}"
        expression += "$"
        ans = a * x_val + b
        
        logic_steps = self.get_logic_steps("T31")

        data = {
            "question": f"$x = {x_val}$ 일 때, 식 {expression} 의 값을 구하시오.",
            "answer": ans,
            "explanation": f"$x$ 자리에 {x_val}을 대입하면: ${a} \\times ({x_val}) + ({b}) = {a*x_val} + {b} = {ans}$",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 5) + [ans]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)