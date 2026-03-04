from abc import ABC, abstractmethod
import json
import os
import glob

# ==========================================
# 2. 표준 인터페이스 (Base Class)
# ==========================================
class BaseTMaster(ABC):
    """모든 T-Master가 상속받아야 할 표준 규격"""
    _logic_steps_data = None

    def __init__(self, spec_id, name):
        self.spec_id = spec_id
        self.name = name
        self._load_logic_steps_data()

    @classmethod
    def _load_logic_steps_data(cls):
        if cls._logic_steps_data is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")
            cls._logic_steps_data = {}
            
            # 1. 단일 파일 로드 (하위 호환성)
            single_file = os.path.join(data_dir, "logic_steps.json")
            if os.path.exists(single_file):
                with open(single_file, "r", encoding="utf-8") as f:
                    cls._logic_steps_data.update(json.load(f))
            
            # 2. 분리된 파일들 로드 (data/logic_steps/*.json)
            split_dir = os.path.join(data_dir, "logic_steps")
            if os.path.exists(split_dir):
                # 하위 디렉토리까지 재귀적으로 검색
                for json_file in glob.glob(os.path.join(split_dir, "**", "*.json"), recursive=True):
                    with open(json_file, "r", encoding="utf-8") as f:
                        try:
                            cls._logic_steps_data.update(json.load(f))
                        except json.JSONDecodeError:
                            print(f"[BaseTMaster] Warning: Failed to decode JSON from {json_file}")

            # 3. core 디렉토리 파일 로드 (Fallback)
            core_dir = os.path.dirname(os.path.abspath(__file__))
            core_file = os.path.join(core_dir, "logic_steps.json")
            if os.path.exists(core_file):
                with open(core_file, "r", encoding="utf-8") as f:
                        cls._logic_steps_data.update(json.load(f))

    def get_logic_steps(self, key, **kwargs):
        if not self._logic_steps_data or key not in self._logic_steps_data:
            return []
        
        steps_template = self._logic_steps_data[key]
        # JSON 데이터를 깊은 복사하지 않고 사용하면 템플릿이 오염될 수 있으므로 매번 새로 생성
        # 간단한 구조이므로 리스트 컴프리헨션으로 처리
        steps = []
        for step in steps_template:
            new_step = step.copy()
            if "description" in new_step:
                new_step["description"] = new_step["description"].format(**kwargs)
            if "target_expr" in new_step:
                new_step["target_expr"] = new_step["target_expr"].format(**kwargs)
            steps.append(new_step)
        return steps

    @abstractmethod
    def generate(self, difficulty="Normal", q_type="single"):
        pass

    def _generate_hints_from_explanation(self, explanation, answer_val):
        logic_steps = []
        steps_source = []
        if isinstance(explanation, list):
            steps_source = explanation[:] # 복사
        else:
            steps_source = str(explanation).split('\n')
        
        # 빈 줄 제거
        steps_source = [s.strip() for s in steps_source if s.strip()]
        
        # 1. 여러 줄인 경우, 마지막 줄(보통 정답 결론)은 힌트에서 제외
        if len(steps_source) > 1:
            steps_source.pop()
        
        for i, step_text in enumerate(steps_source):
            # 2. 힌트 내용 중에 정답이 직접 포함되어 있으면 [?]로 가림 (복구)
            # 정확한 매칭
            if answer_val in step_text:
                step_text = step_text.replace(answer_val, "[?]")
            
            # LaTeX 기호($)를 제거한 값으로도 매칭 시도 (예: 정답 '$3$' -> 텍스트 '3' 도 가림)
            raw_val = answer_val.replace("$", "").strip()
            if raw_val and raw_val in step_text:
                    step_text = step_text.replace(raw_val, "[?]")

            if step_text:
                logic_steps.append({
                    "step_id": i + 1,
                    "description": step_text,
                    "target_expr": "", # 자동 생성된 힌트에는 수식 타겟 없음
                    "concept_id": "AUTO_GENERATED"
                })
        return logic_steps

    def _format_response(self, data, q_type, difficulty):
        explanation = data['explanation']
        logic_steps = data.get('logic_steps', [])
        answer_val = str(data['answer'])

        # logic_steps가 명시적으로 제공되지 않은 경우, explanation을 기반으로 자동 생성
        if not logic_steps and explanation:
            logic_steps = self._generate_hints_from_explanation(explanation, answer_val)
        
        # 리스트인 경우 줄바꿈으로 연결
        if isinstance(explanation, list):
            explanation = "\n".join(explanation)
            
        return {
            "id": self.spec_id,
            "name": self.name,
            "type": q_type,
            "difficulty": difficulty,
            "question": data['question'],
            "options": data.get('options', []),
            "answer": data['answer'],
            "explanation": explanation,
            "image": data.get('image', None),
            "logic_steps": logic_steps,
            "strategy": data.get('strategy', None)  # 핵심 전략/개념 필드 추가
        }
