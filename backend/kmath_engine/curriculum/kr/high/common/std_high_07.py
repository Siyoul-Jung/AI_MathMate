import random
from kmath_engine.base import BaseTMaster
from kmath_engine.registry import TemplateRegistry

class MatrixMeaning_Master(BaseTMaster):
    """
    [유형 1] 행렬의 뜻 (Router)
    - 행렬의 정의, 성분, 상등(Equality) 등과 관련된 템플릿을 연결
    """
    def __init__(self):
        super().__init__("Matrix_Meaning", "행렬의 뜻")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 해당 카테고리에 등록된 템플릿 중 하나를 랜덤 선택하여 실행
        templates = TemplateRegistry.get_by_category("Matrix_Meaning")
        
        # [DEBUG] 로드된 템플릿 개수 확인
        print(f"[DEBUG] Matrix_Meaning: Found {len(templates)} templates")
        
        if not templates:
            return {"error": "No templates found for 'Matrix_Meaning'. Please run 'fix_metadata.py' and restart server."}
        
        selected_template = random.choice(templates)
        try:
            return selected_template.generate(difficulty, q_type)
        except Exception as e:
            return {"error": f"Template Error ({selected_template.spec_id}): {str(e)}"}

class MatrixOperation_Master(BaseTMaster):
    """
    [유형 2] 행렬의 연산 (Router)
    - 덧셈, 뺄셈, 실수배, 곱셈, 거듭제곱 등 연산 관련 템플릿을 연결
    """
    def __init__(self):
        super().__init__("Matrix_Operation", "행렬의 연산")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 해당 카테고리에 등록된 템플릿 중 하나를 랜덤 선택하여 실행
        templates = TemplateRegistry.get_by_category("Matrix_Operation")
        
        # [DEBUG] 로드된 템플릿 개수 확인
        print(f"[DEBUG] Matrix_Operation: Found {len(templates)} templates")
        
        if not templates:
            return {"error": "No templates found for 'Matrix_Operation'. Please run 'fix_metadata.py' and restart server."}
        
        selected_template = random.choice(templates)
        try:
            return selected_template.generate(difficulty, q_type)
        except Exception as e:
            return {"error": f"Template Error ({selected_template.spec_id}): {str(e)}"}
