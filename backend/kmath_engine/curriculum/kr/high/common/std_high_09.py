import random
import math
from kmath_engine.base import BaseTMaster
from kmath_engine.geometry_utils import GeometryUtils
from kmath_engine.math_utils import MathUtils

class High09_1_LineEq_Master(BaseTMaster):
    """
    고등 공통수학 - 직선의 방정식 (두 점을 지나는 직선)
    """
    def __init__(self):
        super().__init__("High09_1", "직선의 방정식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)
        x2 = random.randint(-5, 5)
        while x2 == x1: x2 = random.randint(-5, 5)
        y2 = random.randint(-5, 5)
        
        dy = y2 - y1
        dx = x2 - x1
        g = math.gcd(dy, dx)
        dy //= g
        dx //= g
        
        if dx < 0: dx, dy = -dx, -dy
            
        # dy*x - dx*y + (dx*y1 - dy*x1) = 0
        a, b, c = dy, -dx, dx*y1 - dy*x1
        
        if b == -1:
            ans_str = f"y = {a}x"
            if c > 0: ans_str += f" + {c}"
            elif c < 0: ans_str += f" - {abs(c)}"
        elif a == 0:
            ans_str = f"y = {-c//b}"
        else:
            if dx == 1:
                ans_str = f"y = {dy}x"
                intercept = y1 - dy*x1
                if intercept > 0: ans_str += f" + {intercept}"
                elif intercept < 0: ans_str += f" - {abs(intercept)}"
            else:
                ans_str = f"{dy}x - {dx}y + {c} = 0"
                if c == 0: ans_str = f"{dy}x - {dx}y = 0"
                
        svg = GeometryUtils.create_coordinate_plane_svg(
            points={'A': (x1, y1), 'B': (x2, y2)},
            lines=[((x1, y1), (x2, y2))]
        )
        
        logic_steps = self.get_logic_steps("High09_1", x1=x1, y1=y1, x2=x2, y2=y2)
        
        data = {
            "question": f"두 점 $A({x1}, {y1}), B({x2}, {y2})$ 를 지나는 직선의 방정식을 구하시오.",
            "answer": ans_str,
            "explanation": [
                f"기울기 $m = \\frac{{{y2}-({y1})}}{{{x2}-({x1})}}$",
                f"점 $({x1}, {y1})$을 지나므로 $y - ({y1}) = m(x - ({x1}))$",
                f"정리하면 ${ans_str}$"
            ],
            "logic_steps": logic_steps,
            "strategy": "두 점을 지나는 직선의 방정식은 먼저 기울기를 구한 후, 한 점을 대입하여 구합니다.",
            "image": svg
        }
        
        if q_type == "multi":
            options_set = {ans_str}
            while len(options_set) < 4:
                fake_a = a + random.randint(-1, 1)
                fake_c = c + random.randint(-2, 2)
                if b == -1:
                    fake_ans = f"y = {fake_a}x" + (f" + {fake_c}" if fake_c > 0 else f" - {abs(fake_c)}")
                else:
                    fake_ans = f"{fake_a}x - {dx}y + {fake_c} = 0"
                options_set.add(fake_ans)
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High09_2_PosRelation_Master(BaseTMaster):
    """
    고등 공통수학 - 직선의 방정식 (두 직선의 위치 관계)
    """
    def __init__(self):
        super().__init__("High09_2", "두 직선의 위치 관계")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        relation = random.choice(["parallel", "perpendicular"])
        a = random.randint(1, 3)
        b = random.choice([-1, 1, 2, -2])
        c = random.randint(-5, 5)
        
        l1_eq = f"{a}x" + (f" + {b}y" if b > 0 else f" - {abs(b)}y") + (f" + {c}" if c > 0 else f" - {abs(c)}") + " = 0"
        
        x1 = random.randint(-3, 3)
        y1 = random.randint(-3, 3)
        
        if relation == "parallel":
            # 평행: ax + by + k = 0
            const = -(a*x1 + b*y1)
            ans_eq = f"{a}x" + (f" + {b}y" if b > 0 else f" - {abs(b)}y") + (f" + {const}" if const > 0 else f" - {abs(const)}") + " = 0"
            q_text = f"직선 ${l1_eq}$ 에 평행하고 점 $({x1}, {y1})$을 지나는 직선의 방정식을 구하시오."
            strategy = "평행한 두 직선은 기울기가 같습니다."
            logic_steps = self.get_logic_steps("High09_2_parallel", a=a, b=b, x1=x1, y1=y1)
        else:
            # 수직: bx - ay + k = 0
            ap, bp = b, -a
            const = -(ap*x1 + bp*y1)
            ans_eq = f"{ap}x" + (f" + {bp}y" if bp > 0 else f" - {abs(bp)}y") + (f" + {const}" if const > 0 else f" - {abs(const)}") + " = 0"
            q_text = f"직선 ${l1_eq}$ 에 수직이고 점 $({x1}, {y1})$을 지나는 직선의 방정식을 구하시오."
            strategy = "수직인 두 직선의 기울기의 곱은 -1입니다."
            logic_steps = self.get_logic_steps("High09_2_perpendicular", a=a, b=b, x1=x1, y1=y1)

        data = {
            "question": q_text,
            "answer": ans_eq,
            "explanation": ["주어진 직선의 기울기 또는 계수비를 확인합니다.", f"따라서 ${ans_eq}$"],
            "logic_steps": logic_steps,
            "strategy": strategy
        }
        
        if q_type == "multi":
            options_set = {ans_eq}
            while len(options_set) < 4:
                fake_const = const + random.randint(-5, 5)
                if fake_const == const: fake_const += 1
                fake_eq = f"{a if relation=='parallel' else b}x + {b if relation=='parallel' else -a}y + {fake_const} = 0"
                options_set.add(fake_eq)
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High09_3_PointLineDist_Master(BaseTMaster):
    """
    고등 공통수학 - 직선의 방정식 (점과 직선 사이의 거리)
    """
    def __init__(self):
        super().__init__("High09_3", "점과 직선 사이의 거리")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        triples = [(3,4,5), (5,12,13), (6,8,10), (8,15,17)]
        a, b, hyp = random.choice(triples)
        if random.choice([True, False]): a, b = b, a
        if random.choice([True, False]): a = -a
        if random.choice([True, False]): b = -b
        
        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)
        
        k = random.randint(1, 3)
        val = a*x1 + b*y1
        target_val = k * hyp
        c = target_val - val
        
        line_eq = f"{a}x" + (f" + {b}y" if b > 0 else f" - {abs(b)}y") + (f" + {c}" if c > 0 else f" - {abs(c)}") + " = 0"
        
        logic_steps = self.get_logic_steps("High09_3", a=a, b=b, c=c, x1=x1, y1=y1)
        
        data = {
            "question": f"점 $({x1}, {y1})$과 직선 ${line_eq}$ 사이의 거리를 구하시오.",
            "answer": k,
            "explanation": [
                f"점과 직선 사이의 거리 공식: $d = \\frac{{|ax_1 + by_1 + c|}}{{\\sqrt{{a^2 + b^2}}}}$",
                f"$d = \\frac{{|{a}({x1}) + {b}({y1}) + {c}|}}{{\\sqrt{{{a}^2 + {b}^2}}}} = {k}$"
            ],
            "logic_steps": logic_steps,
            "strategy": "점과 직선 사이의 거리 공식을 사용합니다."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(k, 3, 2) + [k]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
