import random
from kmath_engine.base import BaseTMaster
from kmath_engine.geometry_utils import GeometryUtils

class High11_1_Translation_Master(BaseTMaster):
    """
    고등 공통수학 - 도형의 이동 (평행이동)
    """
    def __init__(self):
        super().__init__("High11_1", "평행이동")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        target_type = random.choice(["point", "circle"])
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        while a == 0 and b == 0: a = random.randint(-5, 5)
        
        move_desc = f"x축의 방향으로 {a}만큼, y축의 방향으로 {b}만큼"
        
        if target_type == "point":
            x = random.randint(-5, 5)
            y = random.randint(-5, 5)
            ans_x, ans_y = x + a, y + b
            ans = f"({ans_x}, {ans_y})"
            q_text = f"점 $({x}, {y})$를 {move_desc} 평행이동한 점의 좌표를 구하시오."
            logic_steps = self.get_logic_steps("High11_1_point", a=a, b=b)
            expl = [f"$({x} + ({a}), {y} + ({b})) = ({ans_x}, {ans_y})$"]
            img = GeometryUtils.create_coordinate_plane_svg(points={'P': (x, y), "P'": (ans_x, ans_y)}, lines=[((x, y), (ans_x, ans_y))])
        else:
            h = random.randint(-3, 3)
            k = random.randint(-3, 3)
            r = random.randint(1, 5)
            term_x = f"(x - {h})^2" if h > 0 else (f"(x + {abs(h)})^2" if h < 0 else "x^2")
            term_y = f"(y - {k})^2" if k > 0 else (f"(y + {abs(k)})^2" if k < 0 else "y^2")
            org_eq = f"{term_x} + {term_y} = {r**2}"
            
            new_h, new_k = h + a, k + b
            ans_term_x = f"(x - {new_h})^2" if new_h > 0 else (f"(x + {abs(new_h)})^2" if new_h < 0 else "x^2")
            ans_term_y = f"(y - {new_k})^2" if new_k > 0 else (f"(y + {abs(new_k)})^2" if new_k < 0 else "y^2")
            ans = f"{ans_term_x} + {ans_term_y} = {r**2}"
            
            q_text = f"원 ${org_eq}$ 를 {move_desc} 평행이동한 원의 방정식을 구하시오."
            logic_steps = self.get_logic_steps("High11_1_shape", a=a, b=b)
            expl = [f"중심 $({h}, {k})$ -> $({new_h}, {new_k})$", f"${ans}$"]
            img = GeometryUtils.create_coordinate_plane_svg(points={'C': (h, k), "C'": (new_h, new_k)}, lines=[((h, k), (new_h, new_k))])

        data = {
            "question": q_text,
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "strategy": "점의 평행이동은 좌표에 더하고, 도형의 평행이동은 x 대신 x-a, y 대신 y-b를 대입합니다.",
            "image": img
        }
        
        if q_type == "multi":
            options_set = {ans}
            while len(options_set) < 4:
                if target_type == "point":
                    options_set.add(f"({ans_x + random.randint(-2, 2)}, {ans_y + random.randint(-2, 2)})")
                else:
                    fh = new_h + random.randint(-2, 2)
                    fk = new_k + random.randint(-2, 2)
                    ft_x = f"(x - {fh})^2" if fh > 0 else (f"(x + {abs(fh)})^2" if fh < 0 else "x^2")
                    ft_y = f"(y - {fk})^2" if fk > 0 else (f"(y + {abs(fk)})^2" if fk < 0 else "y^2")
                    options_set.add(f"{ft_x} + {ft_y} = {r**2}")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High11_2_Symmetry_Master(BaseTMaster):
    """
    고등 공통수학 - 도형의 이동 (대칭이동)
    """
    def __init__(self):
        super().__init__("High11_2", "대칭이동")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x = random.randint(-5, 5)
        y = random.randint(-5, 5)
        while x == 0 or y == 0: x, y = random.randint(-5, 5), random.randint(-5, 5)
            
        sym_type = random.choice(["x_axis", "y_axis", "origin", "y_eq_x"])
        
        if sym_type == "x_axis":
            type_str = "x축"
            ans_x, ans_y = x, -y
            expl_rule = "y의 부호를 바꿉니다."
        elif sym_type == "y_axis":
            type_str = "y축"
            ans_x, ans_y = -x, y
            expl_rule = "x의 부호를 바꿉니다."
        elif sym_type == "origin":
            type_str = "원점"
            ans_x, ans_y = -x, -y
            expl_rule = "x, y의 부호를 모두 바꿉니다."
        else:
            type_str = "직선 $y=x$"
            ans_x, ans_y = y, x
            expl_rule = "x와 y를 서로 바꿉니다."
            
        ans = f"({ans_x}, {ans_y})"
        logic_steps = self.get_logic_steps("High11_2", type=type_str)
        
        lines = []
        if sym_type == "y_eq_x": lines.append(((-10, -10), (10, 10)))
        img = GeometryUtils.create_coordinate_plane_svg(points={'P': (x, y), "P'": (ans_x, ans_y)}, lines=lines)

        data = {
            "question": f"점 $({x}, {y})$를 {type_str}에 대하여 대칭이동한 점의 좌표를 구하시오.",
            "answer": ans,
            "explanation": [f"{type_str}에 대한 대칭이동은 {expl_rule}", f"따라서 $({ans_x}, {ans_y})$"],
            "logic_steps": logic_steps,
            "strategy": "대칭이동의 규칙을 기억합니다.",
            "image": img
        }
        
        if q_type == "multi":
            options_set = {ans}
            options_set.add(f"({x}, {-y})")
            options_set.add(f"({-x}, {y})")
            options_set.add(f"({-x}, {-y})")
            options_set.add(f"({y}, {x})")
            while len(options_set) < 4:
                 options_set.add(f"({x+random.randint(1,2)}, {y+random.randint(1,2)})")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
