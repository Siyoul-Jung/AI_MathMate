import random
from kmath_engine.base import BaseTMaster
from kmath_engine.geometry_utils import GeometryUtils

# ==========================================
# [STD-12-03] 작도와 합동 (T83 ~ T86)
# ==========================================

class T83_Master(BaseTMaster):
    """T83: 간단한 도형의 작도"""
    def __init__(self):
        super().__init__("T83", "작도 순서")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 크기가 같은 각의 작도 순서 문제
        # 1. 점 O를 중심으로 원을 그려 OA, OB 교점 C, D
        # 2. 점 P를 중심으로 같은 반지름 원 그려 PX 교점 E
        # 3. 점 E를 중심으로 CD 길이만큼 원 그려 교점 F
        # 4. 반직선 PF 그리기
        
        steps = [
            "점 O를 중심으로 하는 원을 그려 두 반직선과의 교점을 각각 C, D라 한다.",
            "점 P를 중심으로 하고 반지름의 길이가 OC인 원을 그려 반직선 PQ와의 교점을 E라 한다.",
            "컴퍼스로 선분 CD의 길이를 잰다.",
            "점 E를 중심으로 하고 반지름의 길이가 CD인 원을 그려 앞의 원과의 교점을 F라 한다.",
            "반직선 PF를 긋는다."
        ]
        
        # 순서 섞기 (정답은 고정)
        correct_order = "㉠-㉡-㉢-㉣-㉤" # 가상의 기호 매핑 필요하지만 단순화
        
        data = {
            "question": "다음은 ∠XOY와 크기가 같은 각을 반직선 PQ 위에 작도하는 과정이다. 작도 순서로 옳은 것은?\n" + 
                        "㉠ " + steps[0] + "\n" +
                        "㉡ " + steps[1] + "\n" +
                        "㉢ " + steps[2] + "\n" +
                        "㉣ " + steps[3] + "\n" +
                        "㉤ " + steps[4],
            "answer": "㉠ → ㉡ → ㉢ → ㉣ → ㉤",
            "explanation": "기준 각에서 원을 그리고(㉠), 옮길 위치에 같은 원을 그리고(㉡), 폭을 재서(㉢), 옮길 위치에 표시하고(㉣), 잇는다(㉤).",
            "logic_steps": [
                {"step_id": 1, "description": "크기가 같은 각을 작도하는 순서를 떠올립니다.", "target_expr": "작도 순서", "concept_id": "CONSTRUCTION_STEPS"},
                {"step_id": 2, "description": "기준 각에서의 작업과 옮길 위치에서의 작업을 번갈아 수행함을 확인합니다.", "target_expr": "순서 배열", "concept_id": "ORDER_LOGIC"}
            ]
        }
        
        if q_type == "multi":
            options = [
                "㉠ → ㉡ → ㉢ → ㉣ → ㉤",
                "㉠ → ㉢ → ㉡ → ㉣ → ㉤",
                "㉡ → ㉠ → ㉢ → ㉣ → ㉤",
                "㉢ → ㉠ → ㉡ → ㉣ → ㉤"
            ]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T84_Master(BaseTMaster):
    """T84: 삼각형의 결정 조건"""
    def __init__(self):
        super().__init__("T84", "삼각형 결정 조건")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 삼각형이 하나로 정해지는 조건
        # 1. 세 변 (가장 긴 변 < 나머지 합)
        # 2. 두 변과 끼인각
        # 3. 한 변과 양 끝각
        
        data = {
            "question": "다음 중 삼각형 ABC가 하나로 정해지지 않는 경우는?",
            "options": [
                "AB=5cm, BC=6cm, CA=7cm",
                "AB=5cm, BC=6cm, ∠B=50°",
                "BC=6cm, ∠B=50°, ∠C=60°",
                "AB=5cm, BC=6cm, ∠A=50°" # 정답 (끼인각 아님)
            ],
            "answer": "AB=5cm, BC=6cm, ∠A=50°",
            "explanation": "두 변이 주어질 때는 반드시 그 '끼인각'인 ∠B가 주어져야 하나로 결정됩니다. ∠A가 주어지면 삼각형이 2개 그려지거나 안 그려질 수 있습니다.",
            "logic_steps": [
                {"step_id": 1, "description": "삼각형이 하나로 정해지는 3가지 조건을 확인합니다.", "target_expr": "결정 조건", "concept_id": "TRIANGLE_DETERMINATION"},
                {"step_id": 2, "description": "두 변이 주어졌을 때 끼인각이 아닌 다른 각이 주어진 경우를 찾습니다.", "target_expr": "조건 위배 찾기", "concept_id": "IDENTIFY_EXCEPTION"}
            ]
        }
        
        if q_type == "short_answer":
            data = {
                "question": "삼각형의 세 변의 길이가 3cm, 5cm, x cm일 때, x의 값이 될 수 있는 자연수의 개수는?",
                "answer": 5,
                "explanation": "가장 긴 변 < 나머지 두 변의 합. \n1) x가 가장 길 때: x < 3+5=8 \n2) 5가 가장 길 때: 5 < 3+x => x > 2 \n따라서 2 < x < 8 이므로 3,4,5,6,7 (5개)",
                "logic_steps": [
                    {"step_id": 1, "description": "삼각형의 성립 조건(가장 긴 변 < 나머지 두 변의 합)을 이용합니다.", "target_expr": "부등식 세우기", "concept_id": "TRIANGLE_INEQUALITY"},
                    {"step_id": 2, "description": "x의 범위를 구하고 자연수의 개수를 셉니다.", "target_expr": "개수 세기", "concept_id": "COUNT_INTEGERS"}
                ]
            }
            
        return self._format_response(data, q_type, difficulty)

class T85_Master(BaseTMaster):
    """T85: 삼각형의 합동 조건"""
    def __init__(self):
        super().__init__("T85", "삼각형의 합동")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 합동 조건: SSS, SAS, ASA
        # 시각적 문제 생성
        a, b, c = 6, 8, 10 # 3:4:5 비율
        svg = GeometryUtils.create_congruent_triangles_svg(a, b, c, {'A':'A', 'B':'B', 'C':'C'}, {'D':'D', 'E':'E', 'F':'F'})
        
        cond = random.choice(["SSS", "SAS", "ASA"])
        
        if cond == "SSS":
            q_text = "세 변의 길이가 각각 같을 때"
        elif cond == "SAS":
            q_text = "두 변의 길이가 같고 그 끼인각의 크기가 같을 때"
        else:
            q_text = "한 변의 길이가 같고 그 양 끝각의 크기가 같을 때"
            
        logic_steps = [
            {"step_id": 1, "description": "주어진 조건(변의 길이, 각의 크기)을 확인합니다.", "target_expr": "조건 분석", "concept_id": "ANALYZE_CONDITION"},
            {"step_id": 2, "description": "SSS, SAS, ASA 합동 조건 중 해당하는 것을 찾습니다.", "target_expr": "합동 조건 매칭", "concept_id": "MATCH_CONGRUENCE"}
        ]

        data = {
            "question": f"다음 두 삼각형이 합동이라고 할 때, 사용된 합동 조건은 무엇인가?\n({q_text})",
            "answer": f"{cond} 합동",
            "explanation": f"{cond} 합동 조건에 해당합니다.",
            "logic_steps": logic_steps,
            "image": svg
        }
        
        if q_type == "multi":
            options = ["SSS 합동", "SAS 합동", "ASA 합동", "RHS 합동"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T86_Master(BaseTMaster):
    """T86: 삼각형의 합동의 활용"""
    def __init__(self):
        super().__init__("T86", "합동의 활용")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 정삼각형/정사각형 내의 합동 찾기 등 복잡한 문제
        # 텍스트로 단순화
        logic_steps = [
            {"step_id": 1, "description": "주어진 도형의 성질(정삼각형 등)을 이용하여 길이가 같은 변과 크기가 같은 각을 찾습니다.", "target_expr": "성질 이용", "concept_id": "GEOMETRIC_PROPERTIES"},
            {"step_id": 2, "description": "합동 조건(SAS 등)을 만족하는 두 삼각형을 찾습니다.", "target_expr": "합동 찾기", "concept_id": "FIND_CONGRUENT_TRIANGLES"}
        ]

        data = {
            "question": "정삼각형 ABC의 변 BC 위의 점 D에 대하여, 정삼각형 ADE를 만들었다. 이때 △ABD와 합동인 삼각형은?",
            "answer": "△ACE",
            "explanation": "AB=AC, AD=AE이고 ∠BAD = 60°-∠DAC = ∠CAE 이므로 SAS 합동입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = ["△ACE", "△ADC", "△ABE", "△CDE"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
