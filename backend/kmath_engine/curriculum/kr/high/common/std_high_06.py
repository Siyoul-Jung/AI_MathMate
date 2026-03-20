import random
from kmath_engine.base import BaseTMaster
from kmath_engine.registry import TemplateRegistry

class CasesSumProduct_Master(BaseTMaster):
    """
    [유형 1] 합의 법칙과 곱의 법칙 (Router)
    """
    def __init__(self):
        super().__init__("Cases_Basics", "합의 법칙과 곱의 법칙")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        templates = TemplateRegistry.get_by_category("Cases_Basics")
        if not templates:
            return {"error": "No templates found for 'Cases_Basics'. Please run 'fix_metadata.py' and restart server."}
        
        selected_template = random.choice(templates)
        try:
            return selected_template.generate(difficulty, q_type)
        except Exception as e:
            return {"error": f"Template Error ({selected_template.spec_id}): {str(e)}"}

class Permutations_Master(BaseTMaster):
    """
    [유형 2] 순열 (Router)
    """
    def __init__(self):
        super().__init__("Permutations", "순열")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        templates = TemplateRegistry.get_by_category("Permutations")
        if not templates:
            return {"error": "No templates found for 'Permutations'. Please run 'fix_metadata.py' and restart server."}
        
        selected_template = random.choice(templates)
        try:
            return selected_template.generate(difficulty, q_type)
        except Exception as e:
            return {"error": f"Template Error ({selected_template.spec_id}): {str(e)}"}

class Combinations_Master(BaseTMaster):
    """
    [유형 3] 조합 (Router)
    """
    def __init__(self):
        super().__init__("Combinations", "조합")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        templates = TemplateRegistry.get_by_category("Combinations")
        if not templates:
            return {"error": "No templates found for 'Combinations'. Please run 'fix_metadata.py' and restart server."}
        
        selected_template = random.choice(templates)
        try:
            return selected_template.generate(difficulty, q_type)
        except Exception as e:
            return {"error": f"Template Error ({selected_template.spec_id}): {str(e)}"}
