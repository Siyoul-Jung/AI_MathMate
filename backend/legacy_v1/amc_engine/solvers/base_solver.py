import abc
import matplotlib
import os
from amc_engine.models.dna_model import DNAModel

class BaseAIMESolver(abc.ABC):
    """
    모든 AIME 수학 엔진이 상속받아야 하는 표준 인터페이스.
    DNAModel을 통해 데이터 규격(Golden Standard)을 강제합니다.
    """
    
    DNA = {
        "specific_tag": "UNKNOWN",
        "categories": ["Algebra"],
        "context_type": "abstract",
        "level": 1,
        "has_image": False,
        "is_mock_ready": True
    }
    
    SEED_CONSTRAINTS = {}
    
    DRILL_LEVELS = [1, 2, 3]

    def __init__(self, payload=None, config=None):
        self.payload = payload or {}
        self.config = config or {}
        
        # DNA 유효성 검사 (런타임)
        full_dna = {**self.DNA, "seed_constraints": self.SEED_CONSTRAINTS}
        self.validated_dna = DNAModel(**full_dna)
        
        if self.validated_dna.has_image:
            matplotlib.use('Agg')

    @classmethod
    def get_logic_steps(cls, seed):
        """[OVERRIDE RECOMMENDED] 문항 풀이의 핵심 논리적 단계를 반환합니다."""
        return []

    @abc.abstractmethod
    def execute(self) -> int:
        """
        payload(시드)를 바탕으로 최종 정답(0~999)을 계산하여 반환.
        주관식 정답의 정수 변환 로직은 여기서 처리됩니다.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def generate_seed(cls) -> dict:
        """
        문제 성립 조건을 만족하는 무작위 변수(Seed)들을 생성. 
        AIME의 난이도와 정답 범위(0~999)를 보장해야 함.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_narrative_instruction(cls, seed: dict) -> str:
        """
        LLM에게 전달할 코어 수학 지문 반환. 
        해당 시드의 수치가 들어갈 자리 {var}를 포함해야 함.
        """
        pass

    # --- 드릴(Drill) 생성 유틸리티 (필요시 오버라이딩) ---

    @classmethod
    def generate_drill_seed(cls, level: int) -> dict:
        """
        드릴 레벨별 시드 생성.
        기본적으로 메인 시드와 동일하거나 일부 변수를 고정하여 난이도를 낮춥니다.
        """
        seed = cls.generate_seed()
        seed['drill_level'] = level
        return seed

    @classmethod
    def get_drill_instruction(cls, seed: dict, level: int) -> str:
        """
        드릴 레벨별 지문 생성 가이드.
        기본적으로 원본 지침을 따르되, 레벨에 따른 특수 제약을 추가할 수 있습니다.
        """
        return cls.get_narrative_instruction(seed)

    @classmethod
    def get_drill_intent(cls, level: int) -> dict:
        """
        [NEW] LLM에게 전달할 '교육적 의도(Pedagogical Intent)'.
        하드코딩된 텍스트 대신, LLM이 동적으로 지문을 구성하도록 가이드를 제공합니다.
        """
        if level == 1:
            return {"focus": "Concept Isolation", "goal": "Isolate the most basic property."}
        elif level == 2:
            return {"focus": "Calculational Logic", "goal": "Focus on the intermediate algebraic step."}
        return {"focus": "Full Synthesis", "goal": "Solve the complete AIME-level problem structure."}

    # --- 검증 및 유틸리티 ---

    @classmethod
    def verify_narrative(cls, narrative: str, seed: dict) -> tuple:
        """
        생성된 지문에 필수 수치가 모두 포함되었는지 기본적인 정합성을 체크합니다.
        """
        for key, value in seed.items():
            if key in ['expected_t', 'drill_level']: continue
            if str(value) not in narrative:
                return False, f"필수 변수 '{key}'({value})가 지문에 누락됨"
        return True, "OK"

    @classmethod
    def generate_image(cls, seed: dict, img_path: str):
        """이미지 생성 로직 (has_image일 경우 반드시 오버라이딩 필요)"""
        if cls.DNA.get("has_image"):
            raise NotImplementedError("DNA['has_image']가 True이나 generate_image가 구현되지 않았습니다.")
        pass