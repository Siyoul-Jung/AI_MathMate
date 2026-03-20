import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils
from kmath_engine.geometry_utils import GeometryUtils

# ==========================================
# [STD-12-06] 다면체와 회전체 (T96 ~ T99)
# ==========================================

class T96_Master(BaseTMaster):
    """T96: 다면체의 성질 (오일러 공식)"""
    def __init__(self):
        super().__init__("T96", "다면체의 성질")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 오일러 공식: v - e + f = 2
        # 각기둥, 각뿔, 각뿔대 중 하나 선택
        shape_type = random.choice(["prism", "pyramid", "frustum"])
        n = random.randint(3, 8) # 밑면의 변의 수
        
        if shape_type == "prism":
            name = f"{n}각기둥"
            v, e, f = 2*n, 3*n, n+2
        elif shape_type == "pyramid":
            name = f"{n}각뿔"
            v, e, f = n+1, 2*n, n+1
        else:
            name = f"{n}각뿔대"
            v, e, f = 2*n, 3*n, n+2
            
        target = random.choice(["꼭짓점", "모서리", "면"])
        
        if target == "꼭짓점": ans = v
        elif target == "모서리": ans = e
        else: ans = f
        
        logic_steps = [
            {"step_id": 1, "description": f"{name}의 밑면의 모양과 옆면의 개수를 파악합니다.", "target_expr": "도형 파악", "concept_id": "POLYHEDRON_PROPERTIES"},
            {"step_id": 2, "description": f"{target}의 개수를 구하는 규칙을 적용합니다.", "target_expr": "개수 계산", "concept_id": "COUNT_ELEMENTS"}
        ]

        data = {
            "question": f"{name}의 {target}의 개수를 구하시오.",
            "answer": ans,
            "explanation": f"{name}의 꼭짓점은 {v}개, 모서리는 {e}개, 면은 {f}개입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 5) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T97_Master(BaseTMaster):
    """T97: 정다면체의 종류와 성질"""
    def __init__(self):
        super().__init__("T97", "정다면체")

    def generate(self, difficulty="Normal", q_type="multi"):
        polyhedrons = [
            {"name": "정사면체", "face": "정삼각형", "vertex_faces": 3},
            {"name": "정육면체", "face": "정사각형", "vertex_faces": 3},
            {"name": "정팔면체", "face": "정삼각형", "vertex_faces": 4},
            {"name": "정십이면체", "face": "정오각형", "vertex_faces": 3},
            {"name": "정이십면체", "face": "정삼각형", "vertex_faces": 5}
        ]
        
        target = random.choice(polyhedrons)
        
        q_case = random.choice(["face_shape", "vertex_gather"])
        
        if q_case == "face_shape":
            q_text = f"{target['name']}의 면의 모양은?"
            ans = target['face']
            options = ["정삼각형", "정사각형", "정오각형", "정육각형"]
        else:
            q_text = f"{target['name']}의 한 꼭짓점에 모이는 면의 개수는?"
            ans = target['vertex_faces']
            options = [3, 4, 5, 6]
            
        logic_steps = [
            {"step_id": 1, "description": f"{target['name']}의 정의와 성질을 떠올립니다.", "target_expr": "성질 확인", "concept_id": "REGULAR_POLYHEDRON_PROPERTIES"},
            {"step_id": 2, "description": "질문에 맞는 값을 찾습니다.", "target_expr": "값 찾기", "concept_id": "RECALL_FACT"}
        ]

        data = {
            "question": q_text,
            "options": options,
            "answer": ans,
            "explanation": f"{target['name']}은 {target['face']}로 이루어져 있으며, 한 꼭짓점에 {target['vertex_faces']}개의 면이 모입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "short_answer":
            data["options"] = []
            
        return self._format_response(data, q_type, difficulty)

class T98_Master(BaseTMaster):
    """T98: 회전체의 성질"""
    def __init__(self):
        super().__init__("T98", "회전체")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 원기둥, 원뿔, 구
        shape = random.choice(["cylinder", "cone"])
        
        if shape == "cylinder":
            r = random.randint(3, 8)
            h = random.randint(5, 12)
            svg = GeometryUtils.create_cylinder_svg(labels={'r': str(r), 'h': str(h)})
            name = "원기둥"
            q_text = f"밑면의 반지름의 길이가 {r}cm이고 높이가 {h}cm인 {name}이 있다."
        else:
            r = random.randint(3, 8)
            h = random.randint(5, 12)
            svg = GeometryUtils.create_cone_svg(labels={'r': str(r), 'h': str(h)})
            name = "원뿔"
            q_text = f"밑면의 반지름의 길이가 {r}cm이고 높이가 {h}cm인 {name}이 있다."
            
        # 회전축을 포함하는 평면으로 자른 단면의 넓이
        # 원기둥: 직사각형 (2r * h), 원뿔: 이등변삼각형 (1/2 * 2r * h = rh)
        if shape == "cylinder":
            ans = 2 * r * h
            expl = f"회전축을 포함하는 평면으로 자른 단면은 가로 {2*r}, 세로 {h}인 직사각형이므로 넓이는 {ans}입니다."
        else:
            ans = r * h
            expl = f"회전축을 포함하는 평면으로 자른 단면은 밑변 {2*r}, 높이 {h}인 이등변삼각형이므로 넓이는 {ans}입니다."
            
        logic_steps = [
            {"step_id": 1, "description": "회전축을 포함하는 평면으로 자른 단면의 모양을 파악합니다.", "target_expr": "단면 모양", "concept_id": "CROSS_SECTION_SHAPE"},
            {"step_id": 2, "description": "단면의 가로(또는 밑변)와 세로(또는 높이) 길이를 구합니다.", "target_expr": "길이 확인", "concept_id": "DIMENSIONS"},
            {"step_id": 3, "description": "도형의 넓이를 계산합니다.", "target_expr": "넓이 계산", "concept_id": "AREA_CALCULATION"}
        ]

        data = {
            "question": f"{q_text} 이 입체도형을 회전축을 포함하는 평면으로 자를 때 생기는 단면의 넓이를 구하시오.",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "image": svg
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 10) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T99_Master(BaseTMaster):
    """T99: 회전체의 단면과 전개도"""
    def __init__(self):
        super().__init__("T99", "단면과 전개도")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 전개도 모양 묻기
        logic_steps = [
            {"step_id": 1, "description": "원뿔을 펼쳤을 때의 모양을 상상합니다.", "target_expr": "전개도 상상", "concept_id": "NET_OF_CONE"},
            {"step_id": 2, "description": "옆면과 밑면의 모양을 확인합니다.", "target_expr": "모양 확인", "concept_id": "IDENTIFY_SHAPES"}
        ]

        data = {
            "question": "다음 중 원뿔의 전개도에 대한 설명으로 옳은 것은?",
            "options": ["옆면은 부채꼴이다.", "옆면은 직사각형이다.", "밑면은 두 개다.", "옆면은 삼각형이다."],
            "answer": "옆면은 부채꼴이다.",
            "explanation": "원뿔을 펼치면 밑면은 원, 옆면은 부채꼴 모양이 됩니다.",
            "logic_steps": logic_steps
        }
        
        return self._format_response(data, q_type, difficulty)
