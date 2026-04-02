"""
AI_MathMate V2 — 파이프라인 단일 테스트
"""

import sys
from pathlib import Path

# backend/ 폴더를 파이썬 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine_v2.pipeline_v2 import EngineV2Pipeline
from engine_v2.modules.number_theory.nt_power_congruence import NTPowerCongruenceModule
import json

def run_test():
    print("🚀 V2 파이프라인(MAS) E2E 테스트 시작...")
    
    # 1. 파이프라인 초기화 및 모듈 등록
    pipeline = EngineV2Pipeline()
    module = NTPowerCongruenceModule()
    pipeline.registry.register(module)
    
    # 2. 문제 생성 실행 (target DAPS 12.0)
    print("\n--- 파이프라인 생성 실행 ---")
    result = pipeline.generate_problem(target_daps=12.0)
    
    # 3. 결과 출력
    print("\n\n" + "="*50)
    print(f"✅ 테스트 완료! 최종 결과:")
    print("="*50)
    
    if result["success"]:
        print(f"Variant ID : {result.get('variant_id')}")
        print(f"정답       : {result.get('answer')}")
        print(f"예상 DAPS  : {result.get('daps'):.1f}")
        print(f"로그 수    : {result.get('logs_count')}개")
        print("\n[ 최종 지문 (narrative) ]")
        print("-" * 40)
        print(result.get('narrative'))
        print("-" * 40)
    else:
        print(f"❌ 생성 실패: {result.get('error')}")

if __name__ == "__main__":
    run_test()
