import random
import math
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils
from kmath_engine.geometry_utils import GeometryUtils

# ==========================================
# [STD-12-05] 원과 부채꼴 (T92 ~ T95)
# ==========================================

class T92_Master(BaseTMaster):
    """T92: 원과 부채꼴의 용어"""
    def __init__(self):
        super().__init__("T92", "용어의 정의")

    def generate(self, difficulty="Normal", q_type="multi"):
        definitions = [
            {"term": "호", "desc": "원 위의 두 점을 양 끝으로 하는 원의 일부분"},
            {"term": "현", "desc": "원 위의 두 점을 이은 선분"},
            {"term": "부채꼴", "desc": "원 O에서 두 반지름과 호로 둘러싸인 도형"},
            {"term": "활꼴", "desc": "현과 호로 둘러싸인 도형"},
            {"term": "중심각", "desc": "부채꼴에서 두 반지름이 이루는 각"}
        ]
        
        target = random.choice(definitions)
        
        if q_type == "short_answer":
            data = {
                "question": f"다음 설명에 해당하는 용어를 쓰시오.\n'{target['desc']}'",
                "answer": target['term'],
                "explanation": f"{target['term']}의 정의입니다.",
                "logic_steps": [
                    {"step_id": 1, "description": "원과 관련된 용어들의 정의를 떠올립니다.", "target_expr": "용어 정의", "concept_id": "CIRCLE_TERMS"},
                    {"step_id": 2, "description": "설명에 해당하는 용어를 찾습니다.", "target_expr": "용어 매칭", "concept_id": "TERM_MATCHING"}
                ]
            }
        else:
            # 용어와 설명 연결 문제 (옳은 것/옳지 않은 것)
            is_correct = random.choice([True, False])
            
            if is_correct:
                q_text = "다음 중 용어의 뜻이 바르게 연결된 것은?"
                ans_item = f"{target['term']}: {target['desc']}"
                
                # 오답 생성 (용어와 설명을 섞음)
                wrong_opts = []
                others = [d for d in definitions if d != target]
                random.shuffle(others)
                for i in range(3):
                    wrong_opts.append(f"{others[i]['term']}: {others[(i+1)%len(others)]['desc']}")
                
                options = wrong_opts + [ans_item]
                random.shuffle(options)
                
                data = {
                    "question": q_text,
                    "options": options,
                    "answer": ans_item,
                    "explanation": f"{target['term']}은 {target['desc']}입니다.",
                    "logic_steps": [
                        {"step_id": 1, "description": "각 용어의 정의를 확인합니다.", "target_expr": "정의 확인", "concept_id": "CHECK_DEFINITIONS"},
                        {"step_id": 2, "description": "설명이 바르게 연결된 것을 찾습니다.", "target_expr": "정답 찾기", "concept_id": "IDENTIFY_CORRECT"}
                    ]
                }
            else:
                q_text = "다음 중 용어의 뜻이 옳지 않은 것은?"
                # 정답(틀린 설명) 생성
                other = random.choice([d for d in definitions if d != target])
                ans_item = f"{target['term']}: {other['desc']}"
                
                # 나머지 보기는 맞는 설명
                correct_opts = []
                others = [d for d in definitions if d != target]
                for d in random.sample(others, 3):
                    correct_opts.append(f"{d['term']}: {d['desc']}")
                
                options = correct_opts + [ans_item]
                random.shuffle(options)
                
                data = {
                    "question": q_text,
                    "options": options,
                    "answer": ans_item,
                    "explanation": f"{target['term']}은 {target['desc']}입니다.",
                    "logic_steps": [
                        {"step_id": 1, "description": "각 용어의 정의를 확인합니다.", "target_expr": "정의 확인", "concept_id": "CHECK_DEFINITIONS"},
                        {"step_id": 2, "description": "설명이 틀린 것을 찾습니다.", "target_expr": "오답 찾기", "concept_id": "IDENTIFY_INCORRECT"}
                    ]
                }

        return self._format_response(data, q_type, difficulty)

class T93_Master(BaseTMaster):
    """T93: 부채꼴의 성질 (정비례)"""
    def __init__(self):
        super().__init__("T93", "중심각과 호/넓이")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 중심각 A : 중심각 B = 호 A : 호 B
        angle_a = random.randint(20, 60)
        ratio = random.randint(2, 4)
        angle_b = angle_a * ratio
        
        arc_a = random.randint(3, 8)
        arc_b = arc_a * ratio
        
        logic_steps = [
            {"step_id": 1, "description": "중심각의 크기와 호의 길이는 정비례함을 이용합니다.", "target_expr": "정비례 관계", "concept_id": "PROPORTIONALITY"},
            {"step_id": 2, "description": "비례식을 세워 호의 길이를 구합니다.", "target_expr": "비례식 풀기", "concept_id": "SOLVE_PROPORTION"}
        ]

        # 문제: 각도 A, 호 A, 각도 B 주어지고 호 B 구하기
        data = {
            "question": f"한 원에서 중심각의 크기가 {angle_a}°인 부채꼴의 호의 길이가 {arc_a}cm이다. 중심각의 크기가 {angle_b}°인 부채꼴의 호의 길이는?",
            "answer": arc_b,
            "explanation": f"호의 길이는 중심각의 크기에 정비례합니다. {angle_a}:{angle_b} = 1:{ratio} 이므로 호의 길이도 {arc_a}의 {ratio}배인 {arc_b}cm입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(arc_b, 3, 5) + [arc_b]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T94_Master(BaseTMaster):
    """T94: 부채꼴의 호의 길이와 넓이"""
    def __init__(self):
        super().__init__("T94", "호의 길이와 넓이")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        r = random.randint(3, 9)
        angle = random.choice([30, 45, 60, 90, 120, 135, 180, 270])
        
        target = random.choice(["length", "area"])
        
        svg = GeometryUtils.create_sector_svg(radius=100, angle=angle, labels={'r': str(r), 'x': f"{angle}°"})
        
        if target == "length":
            # l = 2 * pi * r * (x/360)
            # 계산 편의를 위해 파이 포함 문자열로 정답 처리
            num = 2 * r * angle
            den = 360
            g = math.gcd(num, den)
            ans_str = f"{num//g}/{den//g}π" if den//g != 1 else f"{num//g}π"
            
            logic_steps = [
                {"step_id": 1, "description": "부채꼴의 호의 길이 공식을 떠올립니다.", "target_expr": "공식 확인", "concept_id": "ARC_LENGTH_FORMULA"},
                {"step_id": 2, "description": "반지름과 중심각을 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
            ]

            data = {
                "question": f"반지름의 길이가 {r}cm이고 중심각의 크기가 {angle}°인 부채꼴의 호의 길이를 구하시오.",
                "answer": ans_str,
                "explanation": f"호의 길이 l = 2πr × (x/360) = 2π×{r} × ({angle}/360) = {ans_str} cm",
                "logic_steps": logic_steps,
                "image": svg
            }
        else:
            # S = pi * r^2 * (x/360)
            num = r * r * angle
            den = 360
            g = math.gcd(num, den)
            ans_str = f"{num//g}/{den//g}π" if den//g != 1 else f"{num//g}π"
            
            logic_steps = [
                {"step_id": 1, "description": "부채꼴의 넓이 공식을 떠올립니다.", "target_expr": "공식 확인", "concept_id": "SECTOR_AREA_FORMULA"},
                {"step_id": 2, "description": "반지름과 중심각을 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
            ]

            data = {
                "question": f"반지름의 길이가 {r}cm이고 중심각의 크기가 {angle}°인 부채꼴의 넓이를 구하시오.",
                "answer": ans_str,
                "explanation": f"넓이 S = πr² × (x/360) = π×{r}² × ({angle}/360) = {ans_str} cm²",
                "logic_steps": logic_steps,
                "image": svg
            }
            
        if q_type == "multi":
            # 오답 생성 (단순화: 숫자만 다르게)
            options_set = {ans_str, f"{r}π", f"{angle}π", f"{r+angle}π"}
            while len(options_set) < 4:
                options_set.add(f"{random.randint(1, 20)}π")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)
