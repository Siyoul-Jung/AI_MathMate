import json
import os
import sys
from kmath_engine.base import BaseTMaster

# amc_engine 경로 추가
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
amc_engine_path = os.path.join(current_dir, "amc_engine")
if amc_engine_path not in sys.path:
    sys.path.append(amc_engine_path)

from amc_engine.pipeline_manager import ProblemFactory

class AMCSolverMaster(BaseTMaster):
    """
    amc_engine의 Solver와 LLM 파이프라인을 직접 호출하여 문제를 생성하는 마스터
    """
    def __init__(self, spec_id="STD-AIME-2025-1", name="AIME 2025 I Two-Track"):
        super().__init__(spec_id, name)
        self.factory = ProblemFactory()

    def generate(self, difficulty="Normal", q_type="short_answer", **kwargs):
        """
        kwargs에서 year, exam, p_id, mode, level 등을 받아 생성 호출
        """
        year = kwargs.get('year', '2025')
        exam = kwargs.get('exam', 'AIME1')
        p_id = kwargs.get('p_id', 'P01')
        mode = kwargs.get('mode', 'MOCK')
        level = kwargs.get('level', 1)
        
        if mode == 'MOCK':
            level = None # MOCK 모드는 레벨이 없으므로 DB 조회 시 NULL로 처리

        # 1. 캐시 시도 (DB에서 랜덤하게 하나 가져오기)
        new_data = self.factory.get_random_variant(year, exam, p_id, mode, level)
        
        if not new_data:
            # 2. 캐시 없으면 실시간 생성
            new_data = self.factory.process_new_variant(year, exam, p_id, mode, level)
        
        if not new_data:
            return {"error": "Generation failed"}

        # BaseTMaster 규격에 맞게 변환
        pres = new_data.get('3_presentation', {})
        payload = new_data.get('4_solver_payload', {})
        sol = new_data.get('5_solution', {})
        
        # band 정보 가져오기 (get_supported_levels logic과 동일하게)
        # new_data에 이미 band가 명시되어 있을 수도 있고, 아니면 metadata에서 가져옴
        metadata = self.factory.get_problem_metadata(year, exam, p_id)
        band = new_data.get('band') or (metadata.get('difficulty_band') if metadata else "CHALLENGER")

        formatted_data = {
            "p_id": p_id,
            "band": band,
            "metadata": metadata,
            "question": pres.get('problem_statement', ''),
            "answer": str(payload.get('expected_t', '')),
            "explanation": sol.get('step_by_step', ''),
            "logic_steps": [], 
            "image": None 
        }
        
        # 이미지 필드 추출 (ProblemViewer에서 직접 사용할 수 있도록)
        if "![" in formatted_data['question']:
            import re
            match = re.search(r'!\[.*?\]\((.*?)\)', formatted_data['question'])
            if match:
                formatted_data['image'] = match.group(1)

        return self._format_response(formatted_data, q_type, difficulty)

    def get_supported_levels(self, p_id, year="2025", exam="AIME1"):
        return self.factory.get_supported_levels(year, exam, p_id)

