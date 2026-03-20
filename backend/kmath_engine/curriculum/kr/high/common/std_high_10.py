import random
import math
from kmath_engine.base import BaseTMaster
from kmath_engine.geometry_utils import GeometryUtils

class High10_1_CircleEq_Master(BaseTMaster):
    """
    고등 공통수학 - 원의 방정식 (표준형, 일반형)
    """
    def __init__(self):
        super().__init__("High10_1", "원의 방정식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        r = random.randint(2, 6)
        
        A = -2 * a
        B = -2 * b
        C = a**2 + b**2 - r**2
        
        q_form = random.choice(["standard", "general"])
        
        if q_form == "standard":
            q_text = f"중심이 $({a}, {b})$이고 반지름의 길이가 ${r}$인 원의 방정식을 구하시오."
            term_x = f"(x - {a})^2" if a > 0 else (f"(x + {abs(a)})^2" if a < 0 else "x^2")
            term_y = f"(y - {b})^2" if b > 0 else (f"(y + {abs(b)})^2" if b < 0 else "y^2")
            ans_str = f"{term_x} + {term_y} = {r**2}"
            logic_steps = self.get_logic_steps("High10_1_standard", a=a, b=b, r=r)
            expl = [f"표준형: $(x-a)^2 + (y-b)^2 = r^2$", f"${ans_str}$"]
        else:
            eq_str = "x^2 + y^2" + (f" + {A}x" if A > 0 else f" - {abs(A)}x") + (f" + {B}y" if B > 0 else f" - {abs(B)}y") + (f" + {C}" if C > 0 else f" - {abs(C)}") + " = 0"
            q_text = f"원의 방정식 ${eq_str}$ 의 중심의 좌표와 반지름의 길이를 구하시오."
            ans_str = f"중심: $({a}, {b})$, 반지름: ${r}$"
            logic_steps = self.get_logic_steps("High10_1_general")
            expl = ["완전제곱식 꼴로 변형하여 표준형으로 만듭니다.", f"중심 $({a}, {b})$, 반지름 ${r}$"]

        svg = GeometryUtils.create_coordinate_plane_svg(points={'C': (a, b)})

        data = {
            "question": q_text,
            "answer": ans_str,
            "explanation": expl,
            "logic_steps": logic_steps,
            "strategy": "원의 방정식의 표준형 (x-a)² + (y-b)² = r² 을 이용합니다.",
            "image": svg
        }
        
        if q_type == "multi":
            options_set = {ans_str}
            while len(options_set) < 4:
                fa = a + random.randint(-2, 2)
                fb = b + random.randint(-2, 2)
                fr = r + random.randint(-1, 1)
                if fr <= 0: fr = 1
                if q_form == "standard":
                    ft_x = f"(x - {fa})^2" if fa > 0 else (f"(x + {abs(fa)})^2" if fa < 0 else "x^2")
                    ft_y = f"(y - {fb})^2" if fb > 0 else (f"(y + {abs(fb)})^2" if fb < 0 else "y^2")
                    options_set.add(f"{ft_x} + {ft_y} = {fr**2}")
                else:
                    options_set.add(f"중심: $({fa}, {fb})$, 반지름: ${fr}$")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High10_2_CircleLine_Master(BaseTMaster):
    """
    고등 공통수학 - 원과 직선의 위치 관계
    """
    def __init__(self):
        super().__init__("High10_2", "원과 직선의 위치 관계")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        r = random.randint(2, 5)
        m = random.choice([1, -1, 2, -2])
        relation = random.choice(["meet2", "meet1", "none"])
        denom = math.sqrt(m**2 + 1)
        
        if relation == "meet2":
            limit = int(r * denom)
            k = random.randint(-limit + 1, limit - 1)
            ans = "서로 다른 두 점에서 만난다"
            comp_str = "<"
        elif relation == "meet1":
            triples = [(3,4,5), (5,12,13), (8,15,17)]
            a, b, h = random.choice(triples)
            r = random.randint(2, 5)
            c = h * r * random.choice([1, -1])
            line_eq = f"{a}x + {b}y + {c} = 0"
            circle_eq = f"x^2 + y^2 = {r**2}"
            ans = "한 점에서 만난다 (접한다)"
            comp_str = "="
            d_val = r
        else:
            limit = int(r * denom)
            k = limit + random.randint(2, 5)
            k *= random.choice([1, -1])
            ans = "만나지 않는다"
            comp_str = ">"

        if relation != "meet1":
            line_eq = f"y = {m}x" + (f" + {k}" if k > 0 else f" - {abs(k)}")
            circle_eq = f"x^2 + y^2 = {r**2}"
            d_val = abs(k) / denom

        logic_steps = self.get_logic_steps("High10_2")
        
        data = {
            "question": f"원 ${circle_eq}$ 와 직선 ${line_eq}$ 의 위치 관계를 말하시오.",
            "answer": ans,
            "explanation": [
                f"원의 중심 $(0, 0)$과 직선 사이의 거리 $d$를 구합니다.",
                f"$d = {d_val:.2f}$...",
                f"반지름 $r = {r}$ 이므로 $d {comp_str} r$",
                f"따라서 {ans}"
            ],
            "logic_steps": logic_steps,
            "strategy": "원의 중심과 직선 사이의 거리(d)와 반지름(r)을 비교합니다."
        }
        
        if q_type == "multi":
            options = ["서로 다른 두 점에서 만난다", "한 점에서 만난다 (접한다)", "만나지 않는다", "알 수 없다"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
