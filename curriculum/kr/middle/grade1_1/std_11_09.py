import random
from core.base import BaseTMaster
from core.math_utils import MathUtils
from core.geometry_utils import GeometryUtils

# ==========================================
# [STD-11-09] 좌표와 그래프 (T57 ~ T62)
# ==========================================

class T57_Master(BaseTMaster):
    """T57: 순서쌍과 좌표"""
    def __init__(self):
        super().__init__("T57", "순서쌍과 좌표")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        
        svg = GeometryUtils.create_coordinate_plane_svg(points={'P': (x, y)})
        
        logic_steps = [
            {"step_id": 1, "description": "x좌표와 y좌표를 확인합니다.", "target_expr": f"x={x}, y={y}", "concept_id": "IDENTIFY_COORDINATES"},
            {"step_id": 2, "description": "순서쌍 (x, y) 형태로 나타냅니다.", "target_expr": "순서쌍 작성", "concept_id": "ORDERED_PAIR"}
        ]

        data = {
            "question": f"x좌표가 {x}이고, y좌표가 {y}인 점 P의 좌표를 기호로 나타내시오.",
            "answer": f"({x}, {y})",
            "explanation": f"순서쌍은 (x좌표, y좌표) 순서로 나타내므로 ({x}, {y})입니다.",
            "logic_steps": logic_steps,
            "image": svg
        }

        if q_type == "multi":
            options_set = {f"({x}, {y})", f"({y}, {x})", f"({-x}, {y})", f"({x}, {-y})"}
            while len(options_set) < 4:
                options_set.add(f"({x + random.randint(1,3)}, {y})")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T58_Master(BaseTMaster):
    """T58: 사분면의 판별"""
    def __init__(self):
        super().__init__("T58", "사분면 판별")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x = random.choice([i for i in range(-10, 11) if i != 0])
        y = random.choice([i for i in range(-10, 11) if i != 0])
        
        svg = GeometryUtils.create_coordinate_plane_svg(points={'A': (x, y)})
        
        if x > 0 and y > 0: q = "제1사분면"
        elif x < 0 and y > 0: q = "제2사분면"
        elif x < 0 and y < 0: q = "제3사분면"
        else: q = "제4사분면"
        
        logic_steps = [
            {"step_id": 1, "description": "x좌표와 y좌표의 부호를 확인합니다.", "target_expr": "부호 확인", "concept_id": "CHECK_SIGNS"},
            {"step_id": 2, "description": "부호에 따른 사분면의 위치를 판단합니다. (+,+):1, (-,+):2, (-,-):3, (+,-):4", "target_expr": "사분면 결정", "concept_id": "DETERMINE_QUADRANT"}
        ]

        data = {
            "question": f"점 A({x}, {y})는 제몇 사분면 위의 점인가?",
            "answer": q,
            "explanation": f"x>0, y>0이면 제1사분면, x<0, y>0이면 제2사분면, x<0, y<0이면 제3사분면, x>0, y<0이면 제4사분면입니다.",
            "logic_steps": logic_steps,
            "image": svg
        }

        if q_type == "multi":
            options = ["제1사분면", "제2사분면", "제3사분면", "제4사분면"]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T59_Master(BaseTMaster):
    """T59: 대칭인 점의 좌표"""
    def __init__(self):
        super().__init__("T59", "대칭인 점")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        
        svg = GeometryUtils.create_coordinate_plane_svg(points={'P': (x, y)})
        
        type_ = random.choice(["x축", "y축", "원점"])
        
        if type_ == "x축":
            ans = f"({x}, {-y})"
            expl = "x축 대칭은 y좌표의 부호가 반대입니다."
        elif type_ == "y축":
            ans = f"({-x}, {y})"
            expl = "y축 대칭은 x좌표의 부호가 반대입니다."
        else:
            ans = f"({-x}, {-y})"
            expl = "원점 대칭은 x, y좌표의 부호가 모두 반대입니다."
            
        logic_steps = [
            {"step_id": 1, "description": f"{type_} 대칭의 성질을 떠올립니다.", "target_expr": "대칭 성질", "concept_id": "SYMMETRY_PROPERTY"},
            {"step_id": 2, "description": "성질에 맞게 좌표의 부호를 변경합니다.", "target_expr": "좌표 변환", "concept_id": "APPLY_SYMMETRY"}
        ]

        data = {
            "question": f"점 ({x}, {y})와 {type_}에 대하여 대칭인 점의 좌표를 구하시오.",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "image": svg
        }

        if q_type == "multi":
            options_set = {f"({x}, {y})", f"({-x}, {y})", f"({x}, {-y})", f"({-x}, {-y})"}
            while len(options_set) < 4:
                options_set.add(f"({x + random.randint(1,3)}, {y})")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T60_Master(BaseTMaster):
    """T60: 좌표평면 위 도형의 넓이"""
    def __init__(self):
        super().__init__("T60", "도형의 넓이")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 축에 평행한 변을 가진 직각삼각형 넓이
        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)
        
        width = random.randint(2, 8)
        height = random.randint(2, 8)
        
        p1 = (x1, y1)
        p2 = (x1 + width, y1)
        p3 = (x1, y1 + height)
        
        area = (width * height) / 2
        if area.is_integer():
            area = int(area)
            
        svg = GeometryUtils.create_coordinate_plane_svg(
            points={'A': p1, 'B': p2, 'C': p3},
            polygons=[[p1, p2, p3]]
        )
            
        logic_steps = [
            {"step_id": 1, "description": "좌표평면 위에 세 점을 찍고 삼각형을 그립니다.", "target_expr": "도형 그리기", "concept_id": "PLOT_POINTS"},
            {"step_id": 2, "description": "밑변과 높이의 길이를 구합니다.", "target_expr": f"밑변: {width}, 높이: {height}", "concept_id": "CALC_LENGTH"},
            {"step_id": 3, "description": "삼각형의 넓이 공식을 이용하여 계산합니다.", "target_expr": "넓이 계산", "concept_id": "TRIANGLE_AREA"}
        ]

        data = {
            "question": f"세 점 A({p1[0]}, {p1[1]}), B({p2[0]}, {p2[1]}), C({p3[0]}, {p3[1]})를 꼭짓점으로 하는 삼각형 ABC의 넓이를 구하시오.",
            "answer": area,
            "explanation": f"밑변 AB의 길이는 {width}, 높이 AC의 길이는 {height}이므로 넓이는 1/2 × {width} × {height} = {area}입니다.",
            "logic_steps": logic_steps,
            "image": svg
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(area, 3, 5) + [area]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T61_Master(BaseTMaster):
    """T61: 그래프의 해석"""
    def __init__(self):
        super().__init__("T61", "상황과 그래프")

    def generate(self, difficulty="Normal", q_type="multi"):
        scenarios = [
            {"text": "일정한 속력으로 달릴 때, 시간(x)에 따른 이동 거리(y)", "ans": "원점을 지나는 직선 (정비례)"},
            {"text": "멈춰 있다가 점점 속력을 높여 달릴 때, 시간(x)에 따른 속력(y)", "ans": "오른쪽 위로 올라가는 모양"},
            {"text": "집에서 출발하여 공원에 갔다가 잠시 쉬고 다시 돌아올 때, 시간(x)에 따른 집으로부터의 거리(y)", "ans": "올라갔다가 평평하다가 내려오는 모양"},
            {"text": "일정한 속도로 물을 채울 때, 시간(x)에 따른 물의 높이(y) (폭이 일정한 물통)", "ans": "원점을 지나는 직선"},
            {"text": "일정한 속도로 물을 채울 때, 시간(x)에 따른 물의 높이(y) (폭이 점점 넓어지는 물통)", "ans": "점점 완만하게 증가하는 곡선"}
        ]
        
        s = random.choice(scenarios)
        
        logic_steps = [
            {"step_id": 1, "description": "상황에서 변수 x와 y 사이의 관계(증가/감소, 일정 등)를 파악합니다.", "target_expr": "관계 분석", "concept_id": "ANALYZE_RELATIONSHIP"},
            {"step_id": 2, "description": "분석한 관계에 알맞은 그래프 모양을 찾습니다.", "target_expr": "그래프 매칭", "concept_id": "MATCH_GRAPH"}
        ]

        if q_type == "short_answer":
            data = {
                "question": f"다음 상황에 알맞은 그래프의 모양을 설명하시오.\n'{s['text']}'",
                "answer": s["ans"],
                "explanation": "상황에 따라 변수 x와 y의 관계를 생각해보면 알 수 있습니다.",
                "logic_steps": logic_steps
            }
            return self._format_response(data, q_type, difficulty)
            
        distractors = ["x축에 평행한 직선", "y축에 평행한 직선", "내려가는 모양", "오르락내리락하는 모양", "수직선"]
        options = [s["ans"]] + random.sample(distractors, 3)
        random.shuffle(options)
        
        data = {
            "question": f"다음 상황에 알맞은 그래프의 모양으로 가장 적절한 것은?\n'{s['text']}'",
            "options": options,
            "answer": s["ans"],
            "explanation": "상황에 따라 변수 x와 y의 관계를 생각해보면 알 수 있습니다.",
            "logic_steps": logic_steps
        }
        return self._format_response(data, q_type, difficulty)

class T62_Master(BaseTMaster):
    """T62: 그래프 읽기"""
    def __init__(self):
        super().__init__("T62", "그래프 읽기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        rate = random.randint(2, 5)
        t_target = random.randint(3, 8)
        
        max_val = max(t_target, rate*t_target) + 2
        svg = GeometryUtils.create_coordinate_plane_svg(
            points={'O': (0, 0), 'A': (1, rate)},
            lines=[((0, 0), (max_val, rate*max_val))],
            x_range=(-1, max_val), y_range=(-1, rate*max_val + 1)
        )
        
        logic_steps = [
            {"step_id": 1, "description": "그래프가 원점을 지나는 직선이므로 정비례 관계임을 파악합니다.", "target_expr": "y = ax", "concept_id": "IDENTIFY_PROPORTION"},
            {"step_id": 2, "description": "주어진 점 A의 좌표를 대입하여 관계식을 구합니다.", "target_expr": f"y = {rate}x", "concept_id": "FIND_RELATION_EQ"},
            {"step_id": 3, "description": "구한 식에 x좌표를 대입하여 y좌표를 구합니다.", "target_expr": "y값 계산", "concept_id": "CALC_VALUE"}
        ]

        data = {
            "question": f"원점 O(0,0)와 점 A(1, {rate})를 지나는 직선인 그래프가 있다. 이 그래프 위의 점 중에서 x좌표가 {t_target}인 점의 y좌표는?",
            "answer": rate * t_target,
            "explanation": f"x가 1 증가할 때 y가 {rate} 증가하는 정비례 관계입니다. x={t_target}일 때 y={rate}×{t_target}={rate * t_target}입니다.",
            "logic_steps": logic_steps,
            "image": svg
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(rate * t_target, 3, 5) + [rate * t_target]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)