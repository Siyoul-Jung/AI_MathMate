import random
from core.base import BaseTMaster
from core.math_utils import MathUtils
from core.geometry_utils import GeometryUtils

# ==========================================
# [STD-12-08] 자료의 정리와 해석 (T104 ~ T107)
# ==========================================

class T104_Master(BaseTMaster):
    """T104: 줄기와 잎 그림"""
    def __init__(self):
        super().__init__("T104", "줄기와 잎 그림")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 데이터 생성 (10~40대 숫자)
        data = []
        stems = [1, 2, 3, 4]
        for s in stems:
            count = random.randint(2, 5)
            for _ in range(count):
                data.append(s * 10 + random.randint(0, 9))
        data.sort()
        
        # 줄기와 잎 그림 텍스트 생성
        stem_leaf = {}
        for val in data:
            s, l = divmod(val, 10)
            if s not in stem_leaf: stem_leaf[s] = []
            stem_leaf[s].append(l)
            
        table_str = " [줄기] | [잎]\n"
        table_str += "----------------\n"
        for s in stems:
            leaves = " ".join(map(str, sorted(stem_leaf.get(s, []))))
            table_str += f"   {s}    | {leaves}\n"
            
        # 문제 유형: 전체 학생 수, 가장 많은 잎을 가진 줄기, 특정 값 찾기
        q_case = random.choice(["total", "max_stem", "range"])
        
        if q_case == "total":
            q_text = "위 줄기와 잎 그림에서 전체 학생 수는?"
            ans = len(data)
            expl = f"잎의 개수를 모두 세면 {len(data)}명입니다."
        elif q_case == "max_stem":
            q_text = "잎이 가장 많은 줄기는?"
            max_len = 0
            ans = 0
            for s, l_list in stem_leaf.items():
                if len(l_list) > max_len:
                    max_len = len(l_list)
                    ans = s
            expl = f"줄기 {ans}의 잎이 {max_len}개로 가장 많습니다."
        else:
            target = random.choice(data)
            q_text = f"자료의 값이 {target}인 학생은 몇 명인가?"
            ans = data.count(target)
            expl = f"줄기가 {target//10}이고 잎이 {target%10}인 값을 찾으면 {ans}명입니다."

        logic_steps = [
            {"step_id": 1, "description": "줄기와 잎 그림을 해석하는 방법을 떠올립니다.", "target_expr": "표 해석", "concept_id": "READ_STEM_LEAF"},
            {"step_id": 2, "description": "문제에서 요구하는 조건(전체 수, 특정 값 등)에 맞는 데이터를 찾습니다.", "target_expr": "데이터 찾기", "concept_id": "FIND_DATA"}
        ]

        data_obj = {
            "question": f"다음은 어느 반 학생들의 줄넘기 기록을 조사하여 나타낸 줄기와 잎 그림이다.\n{table_str}\n{q_text}",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 5) + [ans]
            random.shuffle(options)
            data_obj["options"] = options
            
        return self._format_response(data_obj, q_type, difficulty)

class T105_Master(BaseTMaster):
    """T105: 도수분포표"""
    def __init__(self):
        super().__init__("T105", "도수분포표")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 도수 생성
        freqs = [random.randint(2, 8) for _ in range(4)]
        total = sum(freqs)
        
        # 빈칸 뚫기 (A)
        missing_idx = random.randint(0, 3)
        missing_val = freqs[missing_idx]
        
        table_str = " [계급(점)] | [도수(명)]\n"
        table_str += "----------------------\n"
        for i in range(4):
            start = 60 + i*10
            end = start + 10
            val_str = "A" if i == missing_idx else str(freqs[i])
            table_str += f" {start} ~ {end} |   {val_str}\n"
        table_str += "----------------------\n"
        table_str += f"   합계    |   {total}\n"
        
        logic_steps = [
            {"step_id": 1, "description": "도수의 총합과 나머지 계급의 도수를 확인합니다.", "target_expr": "도수 확인", "concept_id": "CHECK_FREQUENCY"},
            {"step_id": 2, "description": "총합에서 나머지 도수들의 합을 빼서 빈칸의 값을 구합니다.", "target_expr": "뺄셈 계산", "concept_id": "CALC_MISSING_VALUE"}
        ]

        data = {
            "question": f"다음 도수분포표에서 A에 알맞은 수는?\n{table_str}",
            "answer": missing_val,
            "explanation": f"전체 도수의 합은 {total}이므로, A = {total} - ({sum(freqs) - missing_val}) = {missing_val}입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(missing_val, 3, 5) + [missing_val]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T106_Master(BaseTMaster):
    """T106: 히스토그램과 도수분포다각형"""
    def __init__(self):
        super().__init__("T106", "히스토그램")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 데이터 생성
        freqs = [random.randint(2, 10) for _ in range(5)]
        labels = [f"{i*10}~{(i+1)*10}" for i in range(5)] # 0~10, 10~20 ...
        
        # 랜덤하게 도수분포다각형(꺾은선) 표시
        show_poly = random.choice([True, False])
        svg = GeometryUtils.create_histogram_svg(freqs, labels, x_label="점수", y_label="학생 수", show_polygon=show_poly)
        
        q_case = random.choice(["total", "class_width", "max_class"])
        
        if q_case == "total":
            q_text = "전체 학생 수는 몇 명인가?"
            ans = sum(freqs)
            expl = f"각 계급의 도수를 모두 더하면 {' + '.join(map(str, freqs))} = {ans}명입니다."
        elif q_case == "class_width":
            q_text = "계급의 크기는 얼마인가?"
            ans = 10
            expl = "직사각형의 가로 폭인 10입니다."
        else:
            max_val = max(freqs)
            idx = freqs.index(max_val)
            q_text = "도수가 가장 큰 계급의 도수는?"
            ans = max_val
            expl = f"가장 높은 막대의 도수는 {max_val}명입니다."
            
        logic_steps = [
            {"step_id": 1, "description": "히스토그램의 가로축(계급)과 세로축(도수)을 확인합니다.", "target_expr": "축 확인", "concept_id": "READ_HISTOGRAM"},
            {"step_id": 2, "description": "문제에서 요구하는 정보(전체 수, 계급 크기 등)를 그래프에서 읽어냅니다.", "target_expr": "정보 추출", "concept_id": "EXTRACT_INFO"}
        ]

        data = {
            "question": f"다음 히스토그램을 보고 물음에 답하시오.\n{q_text}",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "image": svg
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 5) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T107_Master(BaseTMaster):
    """T107: 상대도수의 분포와 활용"""
    def __init__(self):
        super().__init__("T107", "상대도수")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        total = random.choice([20, 25, 40, 50]) # 계산하기 좋은 수
        freq = random.randint(2, 10)
        
        # 상대도수 = 도수 / 전체
        rel_freq = freq / total
        
        logic_steps = [
            {"step_id": 1, "description": "상대도수 구하는 공식(도수 / 전체 도수)을 떠올립니다.", "target_expr": "공식 확인", "concept_id": "RELATIVE_FREQ_FORMULA"},
            {"step_id": 2, "description": "주어진 도수와 전체 도수를 대입하여 계산합니다.", "target_expr": "나눗셈 계산", "concept_id": "CALC_VALUE"}
        ]

        data = {
            "question": f"전체 도수가 {total}명인 도수분포표에서 어떤 계급의 도수가 {freq}명일 때, 이 계급의 상대도수는?",
            "answer": rel_freq,
            "explanation": f"상대도수 = (그 계급의 도수) / (도수의 총합) = {freq} / {total} = {rel_freq}입니다.",
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            # 오답: 분모/분자 반대, 계산 실수 등
            options = [rel_freq, round(rel_freq + 0.05, 2), round(rel_freq - 0.05, 2), round(1 - rel_freq, 2)]
            # 음수 제거 및 범위 체크
            options = [o for o in options if 0 < o < 1]
            while len(options) < 4:
                options.append(round(random.random(), 2))
            options = list(set(options))[:4]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)