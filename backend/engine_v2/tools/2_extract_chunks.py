"""
AI_MathMate V2 — 2. 연대별 분할 추출 (Map)
업로드된 PDF를 사용하여 100문항 단위(연대별)로 원자 모듈을 전수 추출합니다.
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "engine_v2" / "data"
CACHE_PATH = DATA_DIR / "pdf_cache.json"

load_dotenv(BASE_DIR / ".env")

# 약 100문항 단위로 끊은 연대 블록 (AIME I, II 가 생기면서 이후 연도는 기간이 짧음)
YEAR_CHUNKS = [
    (1983, 1989), # 7년 * 15 = 105
    (1990, 1996), # 7년 * 15 = 105
    (1997, 2001), # 약 100문제
    (2002, 2006), # 매년 2회 = 150문제
    (2007, 2011), # 150문제
    (2012, 2016), # 150문제
    (2017, 2021), # 150문제
    (2022, 2026), # 150문제
]

def load_cached_file(client):
    if not CACHE_PATH.exists():
        raise FileNotFoundError("pdf_cache.json 이 없습니다. 1_upload_pdf.py를 먼저 실행하세요.")
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"📄 캐시 파일 로드 완료: {data['file_name']}")
    return client.files.get(name=data["file_name"])

def extract_chunk(client, pdf_file, start_year, end_year, chunk_index) -> list:
    print(f"\n🚀 [Chunk {chunk_index}] {start_year}~{end_year}년 추출 시작...")
    
    prompt = f"""
    당신은 AIME 수학 올림피아드 분석 전문가이자 데이터 엔지니어입니다.
    첨부된 파일은 1983년부터 2026년까지의 모든 AIME (I, II) 기출문제 모음집인 'CompendiumAIME.pdf'입니다.
    
    [작업 목표]
    오직 **{start_year}년부터 {end_year}년까지 출제된 문제와 해설들만 엄밀하게 분석**하여, 
    해당 기간 내의 100여 개 문항을 풀기 위해 사용된 **가장 핵심적이고 순수한 수학적 원자 모듈(Atomic Modules)을 모두 추출**하세요.

    [원자 모듈 추출 규칙]
    1. 표면적 스토리텔링은 완전히 무시하고, "문제 해결의 뼈대가 된 수학적 정리 및 테크닉"만 뽑아냅니다.
    2. 중복되는 개념은 하나의 모듈로 합치세요. (예: 1983년과 1985년에 둘 다 다항식의 근과 계수의 관계가 쓰였다면 하나로 통일)
    3. 분류 도메인: 'algebra', 'geometry', 'number_theory', 'combinatorics' 중 하나.
    
    반드시 아래 JSON 형태의 List 배열로만 응답하세요. 다른 설명은 일절 추가하지 마세요. (마크다운 백틱은 허용)

    [응답 예시]
    [
      {{
        "module_id": "algebra_vieta_cubic",
        "domain": "algebra",
        "name": "3차 방정식 비에타 수식",
        "description": "3차 방정식에서 세 근의 곱과 합을 이용하여 다항식 계수를 구함",
        "logic_depth": 3,
        "source_years": [{start_year}]
      }},
      {{
        "module_id": "nt_power_congruence",
        "domain": "number_theory",
        "name": "거듭제곱 합동식",
        "description": "다항식 거듭제곱 형태에서 특정 수의 배수 여부를 합동식으로 판별 및 LTE 보조정리 활용",
        "logic_depth": 5,
        "source_years": [{start_year}, {end_year}]
      }}
    ]
    """

    try:
        t0 = time.time()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[pdf_file, prompt],
            config=GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2 # 환각 최소화
            ),
        )
        duration = time.time() - t0
        
        # JSON 파싱 시도
        raw_text = response.text
        # 가끔 ```json ``` 마크다운이 붙을 수 있음
        if raw_text.startswith("```json"):
            raw_text = raw_text.split("```json")[-1].split("```")[0].strip()
        
        extracted_modules = json.loads(raw_text)
        print(f"  ✅ 추출 완료! ({len(extracted_modules)}개 모듈 발견) - 소요 시간: {duration:.1f}초")
        return extracted_modules
        
    except Exception as e:
        print(f"  ❌ 오류 발생: {e}")
        return []

def main():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    pdf_file = load_cached_file(client)
    
    all_chunks_dir = DATA_DIR / "chunks"
    all_chunks_dir.mkdir(exist_ok=True)
    
    print(f"👉 총 {len(YEAR_CHUNKS)}개 청크로 분할하여 전수조사를 시작합니다.")
    
    for i, (sy, ey) in enumerate(YEAR_CHUNKS, 1):
        chunk_file = all_chunks_dir / f"chunk_{i}_{sy}_{ey}.json"
        
        # 이미 추출된 청크면 건너뜀 (안전 장치)
        if chunk_file.exists():
            print(f"\n⏭️ [Chunk {i}] {sy}~{ey}년은 이미 추출되었습니다. 건너뜁니다.")
            continue
            
        modules = extract_chunk(client, pdf_file, sy, ey, i)
        if modules:
            with open(chunk_file, "w", encoding="utf-8") as f:
                json.dump(modules, f, ensure_ascii=False, indent=2)
            print(f"  💾 저장 완료: {chunk_file.name}")
            
        # API Rate Limit 보호를 위해 대기
        time.sleep(3)
        
    print("\n🎉 모든 분할 추출(Map) 단계가 완료되었습니다!")
    print("👉 이제 'python 3_merge_dedup.py'를 실행하여 모듈을 통합하세요.")

if __name__ == "__main__":
    main()
