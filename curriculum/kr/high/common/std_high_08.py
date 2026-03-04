import random
import math
from core.base import BaseTMaster
from core.geometry_utils import GeometryUtils

class High08_1_Distance_Master(BaseTMaster):
    """
    고등 공통수학 - 평면좌표 (두 점 사이의 거리)
    """
    def __init__(self):
        super().__init__("High08_1", "두 점 사이의 거리")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # A(x1, y1), B(x2, y2)
        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)
        
        # 거리가 정수가 되도록 설정 (피타고라스 수 활용)
        triples = [(3,4,5), (5,12,13), (6,8,10), (8,15,17)]
        dx, dy, d = random.choice(triples)
        
        if random.choice([True, False]):
            dx, dy = dy, dx
            
        x2 = x1 + dx * random.choice([1, -1])
        y2 = y1 + dy * random.choice([1, -1])
        
        svg = GeometryUtils.create_coordinate_plane_svg(
            points={'A': (x1, y1), 'B': (x2, y2)},
            lines=[((x1, y1), (x2, y2))]
        )
        
        logic_steps = self.get_logic_steps("High08_1", x1=x1, y1=y1, x2=x2, y2=y2)
        
        data = {
            "question": f"두 점 $A({x1}, {y1}), B({x2}, {y2})$ 사이의 거리를 구하시오.",
            "answer": d,
            "explanation": [
                f"두 점 사이의 거리 공식: $\\sqrt{{(x_2-x_1)^2 + (y_2-y_1)^2}}$",
                f"$\\sqrt{{({x2}-({x1}))^2 + ({y2}-({y1}))^2}} = \\sqrt{{{dx**2} + {dy**2}}} = \\sqrt{{{d**2}}} = {d}$"
            ],
            "logic_steps": logic_steps,
            "strategy": "좌표평면 위의 두 점 사이의 거리는 피타고라스 정리를 이용한 공식을 사용하여 구합니다.",
            "image": svg
        }
        
        if q_type == "multi":
            options_set = {d}
            while len(options_set) < 4:
                options_set.add(d + random.randint(-2, 2))
                if 0 in options_set: options_set.remove(0)
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High08_2_DivisionPoint_Master(BaseTMaster):
    """
    고등 공통수학 - 평면좌표 (선분의 내분점과 외분점)
    """
    def __init__(self):
        super().__init__("High08_2", "내분점과 외분점")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # A(x1, y1), B(x2, y2)
        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)
        x2 = random.randint(-5, 5)
        y2 = random.randint(-5, 5)
        
        while (x1, y1) == (x2, y2):
            x2 = random.randint(-5, 5)
            y2 = random.randint(-5, 5)
            
        m = random.randint(1, 3)
        n = random.randint(1, 3)
        while m == n: n = random.randint(1, 3) # 외분점 분모 0 방지
        
        type_ = random.choice(["internal", "external"])
        
        if type_ == "internal":
            # 내분점 P
            px_num = m*x2 + n*x1
            py_num = m*y2 + n*y1
            denom = m + n
            q_text = f"두 점 $A({x1}, {y1}), B({x2}, {y2})$ 를 ${m}:{n}$ 으로 내분하는 점 $P$의 좌표를 구하시오."
            logic_key = "High08_2_internal"
            formula_sign = "+"
        else:
            # 외분점 Q
            px_num = m*x2 - n*x1
            py_num = m*y2 - n*y1
            denom = m - n
            q_text = f"두 점 $A({x1}, {y1}), B({x2}, {y2})$ 를 ${m}:{n}$ 으로 외분하는 점 $Q$의 좌표를 구하시오."
            logic_key = "High08_2_external"
            formula_sign = "-"
            
        ans_x = f"\\frac{{{px_num}}}{{{denom}}}" if px_num % denom != 0 else str(px_num // denom)
        ans_y = f"\\frac{{{py_num}}}{{{denom}}}" if py_num % denom != 0 else str(py_num // denom)
        ans = f"$({ans_x}, {ans_y})$"
        
        logic_steps = self.get_logic_steps(logic_key, m=m, n=n)

        data = {
            "question": q_text,
            "answer": ans,
            "explanation": f"공식에 대입하면 x좌표: $\\frac{{{m}({x2}) {formula_sign} {n}({x1})}}{{{m} {formula_sign} {n}}}$, y좌표: $\\frac{{{m}({y2}) {formula_sign} {n}({y1})}}{{{m} {formula_sign} {n}}}$",
            "logic_steps": logic_steps,
            "strategy": "내분점은 합(m+n), 외분점은 차(m-n)를 이용하며, 크로스로 곱하는 순서에 주의합니다."
        }
        
        if q_type == "multi":
            options = [ans, f"$({random.randint(-5,5)}, {random.randint(-5,5)})$", f"$({ans_y}, {ans_x})$", f"$({-int(px_num/denom) if px_num%denom==0 else 0}, {int(py_num/denom) if py_num%denom==0 else 0})$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)