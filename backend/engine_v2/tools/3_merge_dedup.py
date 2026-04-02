"""
AI_MathMate V2 — 3. 병합 및 정규화 추출 (Reduce)
여러 청크 파일에 흩어져 있는 수백 개의 원시 원자 모듈들을 하나로 취합하고,
Gemini를 통해 중복 제거(Dedup) 및 70개 정예 모듈로 압축합니다.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "engine_v2" / "data"
CHUNKS_DIR = DATA_DIR / "chunks"

load_dotenv(BASE_DIR / ".env")

def merge_chunks() -> list:
    all_raw_modules = []
    if not CHUNKS_DIR.exists():
        print("❌ 오류: chunks 폴더가 없습니다. 2_extract_chunks.py를 먼저 실행하세요.")
        return []
        
    for chunk_file in CHUNKS_DIR.glob("chunk_*.json"):
        with open(chunk_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 연도 태그 추가 (병합 시 참고용)
            all_raw_modules.extend(data)
            
    print(f"📥 수집된 날것의 원자 모듈 총합: {len(all_raw_modules)}개")
    return all_raw_modules

def reduce_modules(client, raw_modules: list) -> dict:
    print("\n🚀 병합 및 중복제거(Reduce) 시작... (AI 연산 3~4분 소요 예상)")
    
    # 1. JSON 문자열로 변환 (너무 길면 분할해야 하지만 1M 토큰이면 충분히 전송 가능)
    raw_json_str = json.dumps(raw_modules, ensure_ascii=False)
    
    prompt = f"""
    당신은 AIME 수학 시스템의 수석 아키텍트입니다.
    다음은 제가 1983년부터 2026년까지 40년 치 기출를 전수조사하여 추출한 '모든 수학적 원시 모듈(Raw Modules)'들의 누적 리스트입니다. (총 {len(raw_modules)}개)

    [수행 과제]
    이 방대한 리스트에서 비슷한 수학적 개념이나 중복된 식(예: 3차 비에타, 비에타의 공식)들을 찾아 완벽하게 통・폐합하세요.
    최종적으로 대수(algebra), 기하(geometry), 정수론(number_theory), 조합론(combinatorics)의 4대 영역으로 나눈 후, 
    정확히 70개 전후의 '가장 순수하고 파편화된 핵심 수학 원자 모듈'로 압축해 주세요.
    다양한 연도에서 빈출된 개념일수록 높은 중요도(DAPS 기여도)를 가져야 합니다.

    [응답 규칙]
    - 오직 검증된 1개의 마스터 JSON 객체만 반환하세요.
    - JSON 구조는 다음과 같아야 합니다:
    {{
      "algebra": [
        {{
          "module_id": "algebra_vieta_cubic",
          "name": "3차 방정식 비에타 수식",
          "description": "다항식 계수를 이용한 근의 합, 곱 계산",
          "logic_depth": 3,
          "daps_contribution": 2.5,
          "tags": ["vieta", "polynomial", "cubic"]
        }}
      ],
      "geometry": [...],
      "number_theory": [...],
      "combinatorics": [...]
    }}
    
    [원시 데이터 List]
    {raw_json_str}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro", # 여기서는 논리적 병합을 위해 가장 똑똑한 Pro 모델 사용
            contents=prompt,
            config=GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            ),
        )
        
        raw_text = response.text
        if raw_text.startswith("```json"):
            raw_text = raw_text.split("```json")[-1].split("```")[0].strip()
            
        final_table = json.loads(raw_text)
        total_count = sum(len(lst) for lst in final_table.values())
        print(f"  ✅ 중복 제거 완료! 최종 도출된 모듈 수: {total_count}개")
        
        return final_table
        
    except Exception as e:
        print(f"  ❌ 병합 작업 실패: {e}")
        return {}

def main():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    # 1. 흩어진 수백 개 원자 수집
    raw_modules = merge_chunks()
    if not raw_modules:
        return
        
    # 2. AI Reduce 요청
    final_module_table = reduce_modules(client, raw_modules)
    if not final_module_table:
        return
        
    # 3. Master JSON 저장
    output_path = DATA_DIR / "modules_master.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_module_table, f, ensure_ascii=False, indent=2)
        
    print(f"\n🎉 최종 압축 완료! 마스터 모듈 테이블이 저장되었습니다: {output_path.name}")
    print("👉 이 JSON 파일을 검토한 후 이상이 없다면, V2 엔진의 파이썬 코드로 자동 생성(Generation) 할 수 있습니다.")

if __name__ == "__main__":
    main()
