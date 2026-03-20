import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils
from kmath_engine.geometry_utils import GeometryUtils

# ==========================================
# [STD-12-04] 다각형 (T87 ~ T91)
# ==========================================

class T87_Master(BaseTMaster):
    """T87: 다각형의 대각선 개수"""
    def __init__(self):
        super().__init__("T87", "다각형 대각선 개수")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": num_sides = random.randint(4, 6)
        elif difficulty == "Hard": num_sides = random.randint(10, 15)
        else: num_sides = random.randint(6, 10)
        
        num_diagonals = num_sides * (num_sides - 3) // 2
        
        logic_steps = [
            {"step_id": 1, "description": "다각형의 대각선 개수 구하는 공식 n(n-3)/2를 떠올립니다.", "target_expr": "공식 확인", "concept_id": "DIAGONAL_FORMULA"},
            {"step_id": 2, "description": "변의 개수 n을 공식에 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
        ]

        data = {
            "question": f"변의 개수가 {num_sides}개인 다각형의 대각선의 개수를 구하시오.",
            "answer": num_diagonals,
            "explanation": f"n각형의 대각선 개수는 n(n-3)/2 이므로, {num_sides}({num_sides}-3)/2 = {num_diagonals}개입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(num_diagonals, 3, 5) + [num_diagonals]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T88_Master(BaseTMaster):
    """T88: 삼각형의 내각과 외각의 성질"""
    def __init__(self):
        super().__init__("T88", "삼각형 내각/외각")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 두 내각의 합 = 다른 한 외각
        angle1 = random.randint(30, 70)
        angle2 = random.randint(30, 70)
        
        # 삼각형 성립 조건 고려 (180도 미만)
        while angle1 + angle2 >= 150: # 너무 큰 각 피하기
            angle1 = random.randint(30, 70)
            angle2 = random.randint(30, 70)
            
        exterior_angle = angle1 + angle2
        
        logic_steps = [
            {"step_id": 1, "description": "삼각형의 외각의 성질(한 외각은 이웃하지 않는 두 내각의 합과 같다)을 이용합니다.", "target_expr": "성질 적용", "concept_id": "EXTERIOR_ANGLE_PROPERTY"},
            {"step_id": 2, "description": "주어진 두 내각을 더하여 외각의 크기를 구합니다.", "target_expr": "덧셈 계산", "concept_id": "ADD_ANGLES"}
        ]

        data = {
            "question": f"삼각형의 두 내각의 크기가 각각 {angle1}°와 {angle2}°일 때, 나머지 한 외각의 크기를 구하시오.",
            "answer": exterior_angle,
            "explanation": f"삼각형의 한 외각의 크기는 그와 이웃하지 않는 두 내각의 크기의 합과 같으므로 {angle1}° + {angle2}° = {exterior_angle}°입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(exterior_angle, 3, 10) + [exterior_angle]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T89_Master(BaseTMaster):
    """T89: 다각형의 내각의 크기의 합"""
    def __init__(self):
        super().__init__("T89", "다각형 내각의 합")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": num_sides = random.randint(3, 5)
        elif difficulty == "Hard": num_sides = random.randint(10, 15)
        else: num_sides = random.randint(6, 9)
        
        sum_of_interior_angles = (num_sides - 2) * 180
        
        logic_steps = [
            {"step_id": 1, "description": "다각형의 내각의 합 구하는 공식 180(n-2)를 떠올립니다.", "target_expr": "공식 확인", "concept_id": "INTERIOR_ANGLE_SUM_FORMULA"},
            {"step_id": 2, "description": "변의 개수 n을 공식에 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
        ]

        data = {
            "question": f"변의 개수가 {num_sides}개인 다각형의 내각의 크기의 합을 구하시오.",
            "answer": sum_of_interior_angles,
            "explanation": f"n각형의 내각의 크기의 합은 (n-2) × 180° 이므로, ({num_sides}-2) × 180° = {sum_of_interior_angles}°입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(sum_of_interior_angles, 3, 50) + [sum_of_interior_angles]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T90_Master(BaseTMaster):
    """T90: 다각형의 외각의 크기의 합"""
    def __init__(self):
        super().__init__("T90", "다각형 외각의 합")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 다각형의 외각의 합은 항상 360도
        num_sides = random.randint(3, 10) # n값은 다양하게
        
        logic_steps = [
            {"step_id": 1, "description": "다각형의 외각의 합은 변의 개수와 관계없이 항상 일정함을 기억합니다.", "target_expr": "성질 확인", "concept_id": "EXTERIOR_ANGLE_SUM_PROPERTY"},
            {"step_id": 2, "description": "외각의 합인 360도를 답합니다.", "target_expr": "답 구하기", "concept_id": "CONSTANT_VALUE"}
        ]

        data = {
            "question": f"변의 개수가 {num_sides}개인 다각형의 외각의 크기의 합을 구하시오.",
            "answer": 360,
            "explanation": "모든 다각형의 외각의 크기의 합은 항상 360°입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = [360, 180, 540, 720]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T91_Master(BaseTMaster):
    """T91: 정다각형의 한 내각과 한 외각의 크기"""
    def __init__(self):
        super().__init__("T91", "정다각형 한 내각/외각")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy": num_sides = random.choice([3, 4, 5])
        elif difficulty == "Hard": num_sides = random.choice([9, 10, 12, 15])
        else: num_sides = random.choice([6, 7, 8])
        
        q_target = random.choice(["내각", "외각"])
        
        if q_target == "내각":
            ans = (num_sides - 2) * 180 // num_sides
            expl = f"정n각형의 한 내각의 크기는 (n-2) × 180° / n 이므로, ({num_sides}-2) × 180° / {num_sides} = {ans}°입니다."
            logic_steps = [
                {"step_id": 1, "description": "정다각형의 한 내각의 크기 구하는 공식을 떠올립니다.", "target_expr": "공식 확인", "concept_id": "ONE_INTERIOR_ANGLE_FORMULA"},
                {"step_id": 2, "description": "변의 개수 n을 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
            ]
        else:
            ans = 360 // num_sides
            expl = f"정n각형의 한 외각의 크기는 360° / n 이므로, 360° / {num_sides} = {ans}°입니다."
            logic_steps = [
                {"step_id": 1, "description": "정다각형의 한 외각의 크기 구하는 공식을 떠올립니다.", "target_expr": "공식 확인", "concept_id": "ONE_EXTERIOR_ANGLE_FORMULA"},
                {"step_id": 2, "description": "360도를 변의 개수 n으로 나눕니다.", "target_expr": "나눗셈 계산", "concept_id": "CALC_VALUE"}
            ]
            
        # SVG 이미지 생성 (정다각형)
        labels = [chr(65 + i) for i in range(num_sides)] # A, B, C...
        svg_image = GeometryUtils.create_regular_polygon_svg(num_sides, labels=labels)
            
        data = {
            "question": f"다음 정{num_sides}각형의 한 {q_target}의 크기를 구하시오.",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "image": svg_image
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 15) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
