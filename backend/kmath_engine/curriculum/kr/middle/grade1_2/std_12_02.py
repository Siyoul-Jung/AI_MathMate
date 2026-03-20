import random
from kmath_engine.base import BaseTMaster
from kmath_engine.geometry_utils import GeometryUtils

# ==========================================
# [STD-12-02] 위치 관계 (T76 ~ T82)
# ==========================================

class T76_Master(BaseTMaster):
    """T76: 점과 직선, 점과 평면의 위치 관계"""
    def __init__(self):
        super().__init__("T76", "점/직선/평면의 위치")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 문장 풀 확장
        statements = [
            {"text": "점 A가 직선 l 위에 있으면, 직선 l은 점 A를 지난다.", "is_correct": True, "expl": "점 A가 직선 위에 있다는 것은 직선이 점 A를 지난다는 것과 같습니다."},
            {"text": "점 A가 평면 P 위에 있으면, 평면 P는 점 A를 포함한다.", "is_correct": True, "expl": "점이 평면 위에 있다는 것은 평면이 점을 포함한다는 뜻입니다."},
            {"text": "직선 l이 점 A를 지나지 않으면, 점 A는 직선 l 위에 있다.", "is_correct": False, "expl": "지나지 않으면 위에 있지 않은 것입니다."},
            {"text": "평면 P가 점 A를 포함하지 않으면, 점 A는 평면 P 위에 있다.", "is_correct": False, "expl": "포함하지 않으면 위에 있지 않은 것입니다."},
            {"text": "교점은 선과 선 또는 선과 면이 만나서 생기는 점이다.", "is_correct": True, "expl": "교점의 정의입니다."},
            {"text": "교선은 면과 면이 만나서 생기는 선이다.", "is_correct": True, "expl": "교선의 정의입니다."}
        ]
        
        # 옳은 것 찾기 vs 옳지 않은 것 찾기
        target_type = random.choice([True, False])
        target_str = "옳은" if target_type else "옳지 않은"
        
        corrects = [s["text"] for s in statements if s["is_correct"] == target_type]
        wrongs = [s["text"] for s in statements if s["is_correct"] != target_type]
        
        answer = random.choice(corrects)
        options = random.sample(wrongs, min(3, len(wrongs))) + [answer]
        random.shuffle(options)
        
        data = {
            "question": f"다음 중 위치 관계에 대한 설명으로 {target_str} 것은?",
            "options": options,
            "answer": answer,
            "explanation": next(s["expl"] for s in statements if s["text"] == answer),
            "logic_steps": [
                {"step_id": 1, "description": "점, 직선, 평면의 위치 관계에 대한 정의를 떠올립니다.", "target_expr": "정의 확인", "concept_id": "POSITION_RELATION_DEF"},
                {"step_id": 2, "description": "각 보기가 정의에 부합하는지 판단합니다.", "target_expr": "참/거짓 판별", "concept_id": "LOGICAL_JUDGEMENT"}
            ]
        }
        
        if q_type == "short_answer":
            data = {
                "question": "점 A가 직선 l 위에 있을 때, 직선 l은 점 A를 무엇한다고 하는가?",
                "answer": "지난다",
                "explanation": "점 A가 직선 l 위에 있으면, 직선 l은 점 A를 지난다고 합니다.",
                "logic_steps": [
                    {"step_id": 1, "description": "점과 직선의 위치 관계 용어를 확인합니다.", "target_expr": "용어 확인", "concept_id": "GEOMETRIC_TERMS"},
                    {"step_id": 2, "description": "'위에 있다'와 같은 의미인 용어를 찾습니다.", "target_expr": "용어 매칭", "concept_id": "TERM_MATCHING"}
                ]
            }
            
        return self._format_response(data, q_type, difficulty)

class T77_Master(BaseTMaster):
    """T77: 평면에서 두 직선의 위치 관계"""
    def __init__(self):
        super().__init__("T77", "평면 위 두 직선")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 평면에서 두 직선의 위치 관계: 만난다(한 점), 평행하다(안 만난다), 일치한다
        # 꼬인 위치는 공간에서만 존재함
        
        data = {
            "question": "다음 중 한 평면 위에 있는 두 직선의 위치 관계가 될 수 없는 것은?",
            "options": [
                "한 점에서 만난다",
                "평행하다",
                "일치한다",
                "꼬인 위치에 있다"
            ],
            "answer": "꼬인 위치에 있다",
            "explanation": "꼬인 위치는 공간에서만 성립하는 위치 관계입니다. 평면에서는 만남, 평행, 일치 세 가지만 존재합니다.",
            "logic_steps": [
                {"step_id": 1, "description": "평면에서 두 직선의 위치 관계 3가지를 떠올립니다.", "target_expr": "평면 위치 관계", "concept_id": "PLANE_LINE_RELATION"},
                {"step_id": 2, "description": "공간에서만 존재하는 위치 관계를 보기에서 찾습니다.", "target_expr": "공간 위치 관계", "concept_id": "SPACE_ONLY_RELATION"}
            ]
        }
        
        if q_type == "multi":
            random.shuffle(data["options"])
            
        return self._format_response(data, q_type, difficulty)

class T78_Master(BaseTMaster):
    """T78: 공간에서 두 직선의 위치 관계 (꼬인 위치)"""
    def __init__(self):
        super().__init__("T78", "꼬인 위치")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 정육면체 그림 활용
        svg = GeometryUtils.create_cube_svg()
        
        # 다양한 기준 모서리에 대한 시나리오 정의
        # Front: ABCD, Back: EFGH, Top: ABFE, Bot: DCGH
        scenarios = [
            {"target": "AB", "skew": ["CG", "DH", "EH", "FG"]}, # Top-Front
            {"target": "BC", "skew": ["AE", "DH", "EF", "HG"]}, # Top-Right
            {"target": "CG", "skew": ["AB", "AD", "EF", "EH"]}, # Right-Back Vertical
            {"target": "EF", "skew": ["AD", "BC", "CG", "DH"]}, # Top-Back
        ]
        s = random.choice(scenarios)
        target_edge = s["target"]
        skew_edges = s["skew"]
        
        if difficulty == "Easy":
            ans = random.choice(skew_edges)
            q_text = f"다음 정육면체에서 모서리 {target_edge}와 꼬인 위치에 있는 모서리를 하나만 쓰시오."
        else:
            ans = len(skew_edges)
            q_text = f"다음 정육면체에서 모서리 {target_edge}와 꼬인 위치에 있는 모서리의 개수를 구하시오."

        logic_steps = [
            {"step_id": 1, "description": "꼬인 위치의 정의(만나지도 않고 평행하지도 않음)를 확인합니다.", "target_expr": "정의 확인", "concept_id": "SKEW_LINES_DEF"},
            {"step_id": 2, "description": "주어진 모서리와 만나는 모서리와 평행한 모서리를 제외합니다.", "target_expr": "제외하기", "concept_id": "ELIMINATE_EDGES"},
            {"step_id": 3, "description": "남은 모서리들을 찾습니다.", "target_expr": "꼬인 위치 찾기", "concept_id": "FIND_SKEW_LINES"}
        ]

        data = {
            "question": q_text,
            "answer": ans,
            "explanation": f"모서리 {target_edge}와 만나지도 않고 평행하지도 않은 모서리를 찾으면 {', '.join(skew_edges)} 입니다.",
            "logic_steps": logic_steps,
            "image": svg
        }
        
        if q_type == "multi":
            if difficulty == "Easy":
                options = ["BC", "DC", "AE", ans] # 만나는거, 평행한거, 만나는거, 정답
                random.shuffle(options)
                data["options"] = options
            else:
                options = [2, 3, 4, 5]
                random.shuffle(options)
                data["options"] = options
                
        return self._format_response(data, q_type, difficulty)

class T79_Master(BaseTMaster):
    """T79: 공간에서 직선과 평면의 위치 관계"""
    def __init__(self):
        super().__init__("T79", "공간 직선/평면")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 포함된다, 한 점에서 만난다, 평행하다
        
        data = {
            "question": "공간에서 직선 l과 평면 P가 만나지 않을 때, 두 도형의 위치 관계는?",
            "options": [
                "평행하다",
                "수직이다",
                "포함된다",
                "꼬인 위치에 있다"
            ],
            "answer": "평행하다",
            "explanation": "직선과 평면이 만나지 않으면 서로 평행하다고 합니다.",
            "logic_steps": [
                {"step_id": 1, "description": "직선과 평면의 위치 관계 3가지를 떠올립니다.", "target_expr": "위치 관계 확인", "concept_id": "LINE_PLANE_RELATION"},
                {"step_id": 2, "description": "만나지 않는 경우를 무엇이라 하는지 확인합니다.", "target_expr": "용어 확인", "concept_id": "PARALLEL_DEF"}
            ]
        }
        
        if q_type == "multi":
            random.shuffle(data["options"])
            
        return self._format_response(data, q_type, difficulty)

class T80_Master(BaseTMaster):
    """T80: 공간에서 두 평면의 위치 관계"""
    def __init__(self):
        super().__init__("T80", "면과 면의 위치 관계")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        svg = GeometryUtils.create_cube_svg()
        
        # 다양한 기준 면에 대한 시나리오
        # Faces: ABCD(Front), EFGH(Back), ABFE(Top), DCGH(Bot), ADHE(Left), BCGF(Right)
        scenarios = [
            {"target": "ABCD", "perp": ["ABFE", "BCGF", "CDHG", "DAEH"]}, # Front
            {"target": "ABFE", "perp": ["ABCD", "EFGH", "ADHE", "BCGF"]}, # Top
            {"target": "BCGF", "perp": ["ABCD", "EFGH", "ABFE", "DCGH"]}, # Right
        ]
        s = random.choice(scenarios)
        target_face = s["target"]
        perp_faces = s["perp"]
        
        if difficulty == "Easy":
            ans = random.choice(perp_faces)
            q_text = f"다음 정육면체에서 면 {target_face}와 수직인 면을 하나만 쓰시오."
        else:
            ans = len(perp_faces)
            q_text = f"다음 정육면체에서 면 {target_face}와 수직인 면의 개수를 구하시오."
            
        logic_steps = [
            {"step_id": 1, "description": "면과 면이 수직인 경우를 확인합니다.", "target_expr": "수직 조건", "concept_id": "PERPENDICULAR_PLANES"},
            {"step_id": 2, "description": "주어진 면과 90도로 만나는 면들을 찾습니다.", "target_expr": "면 찾기", "concept_id": "FIND_FACES"}
        ]

        data = {
            "question": q_text,
            "answer": ans,
            "explanation": f"면 {target_face}와 만나는 4개의 옆면 {', '.join(perp_faces)}이 모두 수직입니다.",
            "logic_steps": logic_steps,
            "image": svg
        }
        
        if q_type == "multi":
             if difficulty == "Easy":
                options = ["EFGH", ans, "없다", "모든 면"] # 평행, 정답, 오답
                random.shuffle(options)
                data["options"] = options
             else:
                data["options"] = [2, 3, 4, 5]
                
        return self._format_response(data, q_type, difficulty)

class T81_Master(BaseTMaster):
    """T81: 동위각과 엇각"""
    def __init__(self):
        super().__init__("T81", "동위각/엇각")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 평행한 두 직선에서 동위각과 엇각의 크기는 같다.
        angle = random.randint(40, 140)
        
        data = {
            "question": f"평행한 두 직선 l, m이 다른 한 직선 n과 만날 때 생기는 동위각 중 하나의 크기가 {angle}°이다. 이때 엇각의 크기를 구하시오.",
            "answer": angle,
            "explanation": "두 직선이 평행하면 동위각의 크기와 엇각의 크기는 서로 같습니다. 따라서 엇각도 {angle}°입니다.",
            "logic_steps": [
                {"step_id": 1, "description": "평행선에서 동위각과 엇각의 성질을 떠올립니다.", "target_expr": "성질 확인", "concept_id": "PARALLEL_ANGLES"},
                {"step_id": 2, "description": "동위각과 엇각의 크기가 같음을 이용하여 답을 구합니다.", "target_expr": "크기 결정", "concept_id": "EQUAL_ANGLES"}
            ]
        }
        
        if q_type == "multi":
            supple = 180 - angle
            options = [angle, supple, 90, 180]
            options = list(set(options))
            while len(options) < 4: options.append(random.randint(1, 179))
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T82_Master(BaseTMaster):
    """T82: 평행선과 꺾인 선"""
    def __init__(self):
        super().__init__("T82", "평행선 활용")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 꺾인 선 문제 (보조선 긋기)
        # l // m 사이에 꺾인 점 P가 있음.
        # 위쪽 각 a, 아래쪽 각 b -> 꺾인 각 x = a + b
        
        a = random.randint(20, 60)
        b = random.randint(20, 60)
        x = a + b
        
        svg = GeometryUtils.create_parallel_bent_line_svg(a, b)
        
        logic_steps = [
            {"step_id": 1, "description": "꺾인 점 P를 지나고 두 직선에 평행한 보조선을 긋습니다.", "target_expr": "보조선 긋기", "concept_id": "AUXILIARY_LINE"},
            {"step_id": 2, "description": "엇각의 성질을 이용하여 꺾인 각을 두 부분으로 나눕니다.", "target_expr": "각 나누기", "concept_id": "ALTERNATE_ANGLES"},
            {"step_id": 3, "description": "나누어진 두 각의 합을 구합니다.", "target_expr": "합 구하기", "concept_id": "ADD_ANGLES"}
        ]

        data = {
            "question": f"평행한 두 직선 l, m 사이에 꺾인 점 P가 있다. 직선 l과 점 P를 잇는 선분이 l과 이루는 예각이 {a}°이고, 직선 m과 점 P를 잇는 선분이 m과 이루는 예각이 {b}°일 때, 꺾인 부분의 각 x의 크기를 구하시오. (단, 꺾인 방향은 안쪽으로 같음)",
            "answer": x,
            "explanation": f"꺾인 점 P를 지나고 두 직선에 평행한 보조선을 그으면, 엇각의 성질에 의해 x = {a}° + {b}° = {x}°가 됩니다.",
            "logic_steps": logic_steps,
            "image": svg
        }
        
        if q_type == "multi":
            options = [x, abs(a-b), 180-x, 360-x]
            # 중복 및 음수 처리
            options = [o for o in options if o > 0]
            while len(options) < 4: options.append(random.randint(10, 170))
            options = list(set(options))[:4]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
