import random
import math
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils
from kmath_engine.geometry_utils import GeometryUtils

# ==========================================
# [STD-12-07] 입체도형의 겉넓이와 부피 (T100 ~ T103)
# ==========================================

class T100_Master(BaseTMaster):
    """T100: 기둥의 겉넓이와 부피"""
    def __init__(self):
        super().__init__("T100", "기둥의 겉넓이/부피")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 원기둥 위주
        r = random.randint(3, 8)
        h = random.randint(5, 12)
        
        target = random.choice(["겉넓이", "부피"])
        
        svg = GeometryUtils.create_cylinder_svg(labels={'r': f"{r}cm", 'h': f"{h}cm"})
        
        if target == "겉넓이":
            # S = 2*pi*r^2 + 2*pi*r*h = 2*pi*r(r+h)
            val = 2 * r * (r + h)
            ans = f"{val}π"
            expl = f"밑넓이 = π×{r}² = {r*r}π, 옆넓이 = (2π×{r})×{h} = {2*r*h}π. \n겉넓이 = {r*r}π×2 + {2*r*h}π = {val}π cm²"
        else:
            # V = pi*r^2*h
            val = r * r * h
            ans = f"{val}π"
            expl = f"부피 = 밑넓이 × 높이 = (π×{r}²) × {h} = {val}π cm³"

        logic_steps = [
            {"step_id": 1, "description": f"원기둥의 {target} 구하는 공식을 떠올립니다.", "target_expr": "공식 확인", "concept_id": "CYLINDER_FORMULA"},
            {"step_id": 2, "description": "반지름과 높이를 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
        ]
            
        data = {
            "question": f"밑면의 반지름의 길이가 {r}cm이고 높이가 {h}cm인 원기둥의 {target}를 구하시오.",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "image": svg
        }
        
        if q_type == "multi":
            distractors = MathUtils.generate_distractors(val, 3, 20)
            options = [f"{d}π" for d in distractors] + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T101_Master(BaseTMaster):
    """T101: 뿔의 겉넓이와 부피"""
    def __init__(self):
        super().__init__("T101", "뿔의 겉넓이/부피")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 원뿔
        r = random.randint(3, 6)
        h = random.randint(4, 8) * 3 # 3의 배수로 설정하여 부피 계산 용이하게
        l = random.randint(h+1, h+5) # 모선 (실제 피타고라스 수 아닐 수 있음, 문제 단순화)
        
        # 부피 문제 위주 (높이 사용)
        target = "부피"
        
        svg = GeometryUtils.create_cone_svg(labels={'r': f"{r}cm", 'h': f"{h}cm"})
        
        # V = 1/3 * pi * r^2 * h
        val = (r * r * h) // 3
        ans = f"{val}π"
        expl = f"부피 = 1/3 × 밑넓이 × 높이 = 1/3 × (π×{r}²) × {h} = {val}π cm³"

        logic_steps = [
            {"step_id": 1, "description": "원뿔의 부피 구하는 공식을 떠올립니다.", "target_expr": "공식 확인", "concept_id": "CONE_VOLUME_FORMULA"},
            {"step_id": 2, "description": "반지름과 높이를 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
        ]
            
        data = {
            "question": f"밑면의 반지름의 길이가 {r}cm이고 높이가 {h}cm인 원뿔의 {target}를 구하시오.",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "image": svg
        }
        
        if q_type == "multi":
            distractors = MathUtils.generate_distractors(val, 3, 20)
            options = [f"{d}π" for d in distractors] + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T102_Master(BaseTMaster):
    """T102: 구의 겉넓이와 부피"""
    def __init__(self):
        super().__init__("T102", "구의 겉넓이/부피")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        r = random.randint(2, 9)
        if difficulty == "Easy": r = random.randint(2, 5)
        
        target = random.choice(["겉넓이", "부피"])
        
        # 부피의 경우 r이 3의 배수여야 정수로 떨어짐. 아니면 분수.
        # 여기서는 편의상 r을 3의 배수로 조정하거나 분수 표현
        if target == "부피" and r % 3 != 0:
            r = random.choice([3, 6, 9])
            
        svg = GeometryUtils.create_sphere_svg(radius=80, labels={'r': f"{r}cm"})
        
        if target == "겉넓이":
            # S = 4 * pi * r^2
            val = 4 * r * r
            ans = f"{val}π"
            expl = f"구의 겉넓이 = 4πr² = 4π×{r}² = {val}π cm²"
        else:
            # V = 4/3 * pi * r^3
            val = (4 * r * r * r) // 3
            ans = f"{val}π"
            expl = f"구의 부피 = 4/3πr³ = 4/3π×{r}³ = {val}π cm³"

        logic_steps = [
            {"step_id": 1, "description": f"구의 {target} 구하는 공식을 떠올립니다.", "target_expr": "공식 확인", "concept_id": "SPHERE_FORMULA"},
            {"step_id": 2, "description": "반지름을 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
        ]
            
        data = {
            "question": f"반지름의 길이가 {r}cm인 구의 {target}를 구하시오.",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "image": svg
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(val, 3, 20)
            options = [f"{o}π" for o in options] + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T103_Master(BaseTMaster):
    """T103: 복잡한 입체도형의 겉넓이와 부피"""
    def __init__(self):
        super().__init__("T103", "복잡한 도형")

    def _generate_hemisphere(self):
        r = random.choice([3, 6, 9, 12])
        target = random.choice(["겉넓이", "부피"])
        svg = GeometryUtils.create_hemisphere_svg(radius=80, labels={'r': f"{r}cm"})
        
        if target == "겉넓이":
            val = 3 * r * r
            expl = f"반구의 겉넓이 = (구의 겉넓이)÷2 + (밑면의 넓이) \n= (4π×{r}²)÷2 + π×{r}² = 2π×{r*r} + π×{r*r} = {val}π cm²"
        else:
            val = (2 * r * r * r) // 3
            expl = f"반구의 부피 = (구의 부피)÷2 = (4/3π×{r}³)÷2 = {val}π cm³"

        logic_steps = [
            {"step_id": 1, "description": f"반구의 {target}는 구의 {target}의 절반임을 이용합니다. (겉넓이는 밑면 추가)", "target_expr": "공식 변형", "concept_id": "HEMISPHERE_FORMULA"},
            {"step_id": 2, "description": "반지름을 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
        ]
            
        return {
            "question": f"반지름의 길이가 {r}cm인 반구의 {target}를 구하시오.",
            "answer": f"{val}π",
            "val": val, # 오답 생성을 위한 숫자 값
            "explanation": expl,
            "logic_steps": logic_steps,
            "image": svg
        }

    def _generate_hollow_cylinder(self):
        r_out = random.randint(4, 8)
        r_in = random.randint(1, r_out - 2)
        h = random.randint(5, 10)
        target = random.choice(["겉넓이", "부피"])
        
        svg = GeometryUtils.create_hollow_cylinder_svg(r_out=80, r_in=40, labels={'r_out': f"{r_out}cm", 'r_in': f"{r_in}cm", 'h': f"{h}cm"})
        
        if target == "겉넓이":
            base_area = (r_out**2 - r_in**2)
            side_out = 2 * r_out * h
            side_in = 2 * r_in * h
            val = 2 * base_area + side_out + side_in
            expl = f"밑넓이 = π({r_out}² - {r_in}²) = {base_area}π\n큰 옆넓이 = 2π×{r_out}×{h} = {side_out}π\n작은 옆넓이 = 2π×{r_in}×{h} = {side_in}π\n겉넓이 = {base_area}π×2 + {side_out}π + {side_in}π = {val}π cm²"
        else:
            val = (r_out**2 - r_in**2) * h
            expl = f"부피 = (큰 원기둥 부피) - (작은 원기둥 부피) \n= π×{r_out}²×{h} - π×{r_in}²×{h} = {r_out**2*h}π - {r_in**2*h}π = {val}π cm³"

        logic_steps = [
            {"step_id": 1, "description": "전체 도형에서 구멍 뚫린 부분을 뺀다고 생각하거나, 각 부분의 넓이/부피를 따로 구합니다.", "target_expr": "전략 수립", "concept_id": "COMPLEX_SHAPE_STRATEGY"},
            {"step_id": 2, "description": "공식에 반지름과 높이를 대입하여 계산합니다.", "target_expr": "대입 및 계산", "concept_id": "CALC_VALUE"}
        ]

        return {
            "question": f"밑면의 반지름의 길이가 {r_out}cm인 원기둥의 가운데에 반지름의 길이가 {r_in}cm인 원기둥 모양의 구멍이 뚫려 있다. 높이가 {h}cm일 때, 이 입체도형의 {target}를 구하시오.",
            "answer": f"{val}π",
            "val": val,
            "explanation": expl,
            "logic_steps": logic_steps,
            "image": svg
        }

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 시나리오별 생성기 매핑
        generators = [self._generate_hemisphere, self._generate_hollow_cylinder]
        handler = random.choice(generators)
        data = handler()
        
        if q_type == "multi":
            val = data['val']
            distractors = MathUtils.generate_distractors(val, 3, 20)
            options = [f"{d}π" for d in distractors] + [data['answer']]
            random.shuffle(options)
            data["options"] = options
            
        # 내부용 데이터 제거
        if 'val' in data: del data['val']
            
        return self._format_response(data, q_type, difficulty)
