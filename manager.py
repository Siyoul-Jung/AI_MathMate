import json
import importlib
import os
import traceback

# ==========================================
# 통합 문제 관리자 (Central Content Manager)
# ==========================================

class ProblemManager:
    """
    전체 교육과정의 문제 생성기를 계층적으로 관리하는 클래스
    구조: Curriculum -> Grade -> Standard -> Type -> Master
    설정: manifest.json 파일을 읽어 동적으로 모듈을 로드함
    """
    def __init__(self):
        # 계층적 레지스트리 초기화
        self.registry = {}
        self._load_manifest()
        
    def _load_manifest(self):
        """manifest.json을 읽어 정의된 모든 모듈을 로드"""
        manifest_path = os.path.join(os.path.dirname(__file__), 'manifest.json')
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            for curriculum, grades in config.items():
                for grade, standards in grades.items():
                    for standard, module_path in standards.items():
                        self._import_and_register(curriculum, grade, standard, module_path)
        except FileNotFoundError:
            print("Error: manifest.json 파일을 찾을 수 없습니다.")

    def _import_and_register(self, curriculum, grade, standard, module_path):
        """문자열 경로로 모듈을 import하고 등록"""
        try:
            module = importlib.import_module(module_path)
            self._register_module(curriculum, grade, standard, module)
        except ModuleNotFoundError as e:
            print(f"Warning: 모듈을 찾을 수 없습니다 - {module_path}")
            print(f"  원인: {e}")
        except Exception as e:
            print(f"Error loading module {module_path}: {e}")

    def _register_module(self, curriculum, grade, standard, module):
        """모듈 내의 모든 T-Master 클래스를 자동으로 찾아 등록"""
        if curriculum not in self.registry: self.registry[curriculum] = {}
        if grade not in self.registry[curriculum]: self.registry[curriculum][grade] = {}
        if standard not in self.registry[curriculum][grade]: self.registry[curriculum][grade][standard] = {}

        # 모듈 내부의 속성 중 '_Master'로 끝나는 클래스 인스턴스화 및 등록
        for attr_name in dir(module):
            if attr_name.endswith("_Master") and attr_name != "BaseTMaster":
                master_class = getattr(module, attr_name)
                try:
                    # 클래스 인스턴스 생성
                    instance = master_class()
                    # T코드 추출: 클래스 이름 파싱 대신 인스턴스의 spec_id 사용 (중복/오류 방지)
                    t_code = instance.spec_id
                    
                    self.registry[curriculum][grade][standard][t_code] = instance
                except Exception as e:
                    print(f"Error registering class {attr_name}: {e}")

    def get_problem(self, curriculum, grade, standard, t_code, difficulty="Normal", q_type="short_answer"):
        """계층적 키를 사용하여 문제 생성"""
        # 1. Registry Lookup
        try:
            master = self.registry[curriculum][grade][standard][t_code]
        except KeyError:
            return {
                "error": "Problem Type Not Found",
                "path": f"{curriculum} > {grade} > {standard} > {t_code}"
            }
        
        # 2. Problem Generation
        try:
            return master.generate(difficulty, q_type)
        except Exception as e:
            # 상세 에러 로깅
            print(f"[Error] Generation failed for {t_code}: {str(e)}")
            traceback.print_exc()
            return {
                "error": f"Generation Error: {str(e)}",
                "path": f"{curriculum} > {grade} > {standard} > {t_code}"
            }

    def list_supported_types(self, curriculum, grade, standard):
        """특정 성취기준에 등록된 모든 유형 리스트 반환"""
        try:
            types_list = []
            for t_id, master in self.registry[curriculum][grade][standard].items():
                types_list.append({"id": t_id, "name": master.name})
            return types_list
        except KeyError:
            return []

    def get_all_standards(self):
        """등록된 모든 성취기준 ID 목록을 반환 (테스트 및 디버깅용)"""
        standards = []
        for curriculum, grades in self.registry.items():
            for grade, stds in grades.items():
                for std_id in stds.keys():
                    standards.append(std_id)
        # 정렬하여 반환
        return sorted(standards)

    def get_standards_by_category(self, category):
        """프론트엔드 카테고리(KR_Middle, KR_High 등)에 해당하는 성취기준 ID 목록 반환"""
        standards = []
        
        target_curr = "KR"
        target_grade_prefix = ""
        
        if category == "KR_Middle":
            target_curr = "KR"
            target_grade_prefix = "Middle"
        elif category == "KR_High":
            target_curr = "KR"
            target_grade_prefix = "High"
        elif category == "AMC":
            target_curr = "US"
            target_grade_prefix = "AMC"
        else:
            return self.get_all_standards()

        if target_curr in self.registry:
            for grade, stds in self.registry[target_curr].items():
                if grade.startswith(target_grade_prefix):
                    standards.extend(stds.keys())
                    
        return standards