import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils
from kmath_engine.geometry_utils import GeometryUtils

# ==========================================
# [STD-12-01] 기본 도형 (T71 ~ T75)
# ==========================================

class T71_Master(BaseTMaster):
    """T71: 점, 선, 면의 결정 조건"""
    def __init__(self):
        super().__init__("T71", "평면의 결정 조건")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 평면이 하나로 결정되는 조건
        correct_conditions = [
            "한 직선 위에 있지 않은 세 점",
            "한 직선과 그 직선 밖의 한 점",
            "한 점에서 만나는 두 직선",
            "평행한 두 직선"
        ]
        
        wrong_conditions = [
            "한 직선 위에 있는 세 점",
            "꼬인 위치에 있는 두 직선",
            "일치하는 두 직선",
            "임의의 세 점 (직선 위에 있을 수도 있음)"
        ]
        
        # 문제 유형 변주: 옳은 것 찾기 vs 옳지 않은 것 찾기
        q_variation = random.choice(["find_wrong", "find_correct"])
        
        if q_type == "multi":
            if q_variation == "find_wrong":
                answer = random.choice(wrong_conditions)
                options = random.sample(correct_conditions, 4) + [answer]
                random.shuffle(options)
                data = {
                    "question": "다음 중 평면이 하나로 결정되는 조건이 아닌 것은?",
                    "options": options,
                    "answer": answer,
                    "explanation": "한 직선 위에 있는 세 점이나 꼬인 위치에 있는 두 직선은 평면을 하나로 결정하지 못합니다.",
                    "logic_steps": [
                        {"step_id": 1, "description": "평면이 하나로 결정되는 4가지 조건을 떠올립니다.", "target_expr": "결정 조건 확인", "concept_id": "PLANE_DETERMINATION"},
                        {"step_id": 2, "description": "보기 중에서 조건에 해당하지 않는 것을 찾습니다.", "target_expr": "오답 찾기", "concept_id": "IDENTIFY_EXCEPTION"}
                    ]
                }
            else:
                answer = random.choice(correct_conditions)
                options = random.sample(wrong_conditions, 3) + [answer] + ["일치하는 두 직선"] # 오답 풀 채우기
                options = list(set(options))[:4] + [answer] # 중복 제거 및 개수 맞춤
                random.shuffle(options)
                data = {
                    "question": "다음 중 평면이 하나로 결정되는 조건인 것은?",
                    "options": options,
                    "answer": answer,
                    "explanation": "평면이 결정되려면 한 직선 위에 있지 않은 세 점, 한 직선과 그 밖의 점, 만나는 두 직선, 평행한 두 직선 중 하나여야 합니다.",
                    "logic_steps": [
                        {"step_id": 1, "description": "평면이 하나로 결정되는 4가지 조건을 떠올립니다.", "target_expr": "결정 조건 확인", "concept_id": "PLANE_DETERMINATION"},
                        {"step_id": 2, "description": "보기 중에서 조건에 해당하는 것을 찾습니다.", "target_expr": "정답 찾기", "concept_id": "IDENTIFY_CONDITION"}
                    ]
                }
        else:
            # 주관식: 조건 나열하기 (단순화)
            data = {
                "question": "공간에서 서로 다른 두 직선이 만나지도 않고 평행하지도 않을 때, 두 직선의 위치 관계를 무엇이라 하는가?",
                "answer": "꼬인 위치",
                "explanation": "공간에서 만나지도 않고 평행하지도 않은 두 직선은 '꼬인 위치'에 있다고 합니다.",
                "logic_steps": [
                    {"step_id": 1, "description": "공간에서 두 직선의 위치 관계 3가지를 떠올립니다.", "target_expr": "위치 관계 분류", "concept_id": "SPACE_LINE_RELATION"},
                    {"step_id": 2, "description": "만나지도 않고 평행하지도 않은 경우를 찾습니다.", "target_expr": "용어 확인", "concept_id": "SKEW_LINES"}
                ]
            }
            
        return self._format_response(data, q_type, difficulty)

class T72_Master(BaseTMaster):
    """T72: 직선, 반직선, 선분"""
    def __init__(self):
        super().__init__("T72", "직선/반직선/선분")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 직선 AB, 반직선 AB, 선분 AB의 기호와 의미
        # 반직선은 시작점과 방향이 중요함. AB != BA
        
        data = {
            "question": "다음 중 서로 같은 도형을 나타낸 것이 아닌 것은?",
            "options": [
                "직선 AB와 직선 BA",
                "선분 AB와 선분 BA",
                "반직선 AB와 반직선 BA",
                "두 점 A, B를 지나는 직선과 직선 AB"
            ],
            "answer": "반직선 AB와 반직선 BA",
            "explanation": "반직선은 시작점과 방향이 같아야 같은 도형입니다. 반직선 AB는 A에서 시작해 B로 가고, 반직선 BA는 B에서 시작해 A로 가므로 서로 다릅니다.",
            "logic_steps": [
                {"step_id": 1, "description": "직선, 반직선, 선분의 정의와 기호를 확인합니다.", "target_expr": "도형 정의", "concept_id": "GEOMETRIC_TERMS"},
                {"step_id": 2, "description": "반직선은 시작점과 방향이 모두 같아야 같은 도형임을 확인합니다.", "target_expr": "반직선 비교", "concept_id": "COMPARE_RAYS"}
            ]
        }
        
        if q_type == "short_answer":
            data = {
                "question": "서로 다른 두 점 A, B를 지나는 직선은 몇 개 그을 수 있는가?",
                "answer": 1,
                "explanation": "서로 다른 두 점을 지나는 직선은 오직 하나뿐입니다.",
                "logic_steps": [
                    {"step_id": 1, "description": "직선의 결정 조건을 떠올립니다.", "target_expr": "직선 결정", "concept_id": "LINE_DETERMINATION"},
                    {"step_id": 2, "description": "두 점을 지나는 직선의 개수를 답합니다.", "target_expr": "개수 확인", "concept_id": "COUNT_LINES"}
                ]
            }
            
        if q_type == "multi":
            random.shuffle(data["options"])
            
        return self._format_response(data, q_type, difficulty)

class T73_Master(BaseTMaster):
    """T73: 두 점 사이의 거리"""
    def __init__(self):
        super().__init__("T73", "두 점 사이의 거리")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 수직선 상의 거리 (기하 기초)
        if difficulty == "Easy":
            a = random.randint(-5, 0); b = random.randint(1, 5)
        elif difficulty == "Hard":
            a = random.randint(-20, -10); b = random.randint(10, 20)
        else:
            a = random.randint(-10, 0); b = random.randint(1, 10)
            
        dist = b - a
        
        # SVG 이미지 생성
        svg_image = GeometryUtils.create_number_line_svg(a, b, {a: 'A', b: 'B'})
        
        logic_steps = [
            {"step_id": 1, "description": "수직선 위의 두 점의 좌표를 확인합니다.", "target_expr": f"A({a}), B({b})", "concept_id": "IDENTIFY_COORDINATES"},
            {"step_id": 2, "description": "큰 좌표에서 작은 좌표를 빼서 거리를 구합니다.", "target_expr": "거리 계산", "concept_id": "CALC_DISTANCE"}
        ]

        data = {
            "question": f"다음 수직선 위의 두 점 A({a}), B({b}) 사이의 거리를 구하시오.",
            "answer": dist,
            "explanation": f"두 점 사이의 거리는 큰 수에서 작은 수를 빼면 됩니다. {b} - ({a}) = {dist}",
            "logic_steps": logic_steps,
            "image": svg_image
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(dist, 3, 5, min_val=0) + [dist]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T74_Master(BaseTMaster):
    """T74: 각의 크기와 분류"""
    def __init__(self):
        super().__init__("T74", "각의 분류")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 예각, 직각, 둔각, 평각
        angle_types = {
            "예각": (1, 89),
            "직각": (90, 90),
            "둔각": (91, 179),
            "평각": (180, 180)
        }
        
        target_type = random.choice(list(angle_types.keys()))
        min_val, max_val = angle_types[target_type]
        angle = random.randint(min_val, max_val)
        
        data = {
            "question": f"크기가 {angle}°인 각은 어떤 각인가?",
            "answer": target_type,
            "explanation": f"0° < {angle}° < 90° 이면 예각, 90°이면 직각, 90° < {angle}° < 180° 이면 둔각, 180°이면 평각입니다.",
            "logic_steps": [
                {"step_id": 1, "description": "각의 크기에 따른 분류 기준(예각, 직각, 둔각, 평각)을 떠올립니다.", "target_expr": "각의 분류", "concept_id": "ANGLE_CLASSIFICATION"},
                {"step_id": 2, "description": "주어진 각도가 어느 범위에 속하는지 확인합니다.", "target_expr": "범위 확인", "concept_id": "CHECK_RANGE"}
            ]
        }
        
        if q_type == "multi":
            options = ["예각", "직각", "둔각", "평각"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T75_Master(BaseTMaster):
    """T75: 맞꼭지각과 수직"""
    def __init__(self):
        super().__init__("T75", "맞꼭지각/수직")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 맞꼭지각의 크기는 같다.
        # 두 직선이 교차할 때 생기는 각 a, b, c, d
        # a와 c가 맞꼭지각 -> a = c
        
        angle = random.randint(30, 150)
        
        # 문제: 그림 대신 텍스트로 설명 (추후 그림 추가 가능)
        # 두 직선이 한 점에서 만날 때 생기는 네 각 중 한 각의 크기가 x도일 때, 그 맞꼭지각의 크기는?
        
        data = {
            "question": f"두 직선이 한 점에서 만날 때 생기는 네 각 중 한 각의 크기가 {angle}°이다. 이 각의 맞꼭지각의 크기를 구하시오.",
            "answer": angle,
            "explanation": "맞꼭지각의 크기는 서로 같습니다.",
            "logic_steps": [
                {"step_id": 1, "description": "맞꼭지각의 성질을 떠올립니다.", "target_expr": "성질 확인", "concept_id": "VERTICAL_ANGLES_PROPERTY"},
                {"step_id": 2, "description": "맞꼭지각의 크기는 서로 같음을 이용하여 답을 구합니다.", "target_expr": "크기 결정", "concept_id": "DETERMINE_ANGLE"}
            ]
        }
        
        if q_type == "multi":
            # 오답: 보각(180-angle), 90도, 180도 등
            supple = 180 - angle
            options = [angle, supple, 90, 180]
            # 중복 제거 및 부족분 채우기
            options = list(set(options))
            while len(options) < 4: options.append(random.randint(1, 179))
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
