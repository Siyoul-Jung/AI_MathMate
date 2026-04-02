"""
AI_MathMate V2 — 1. PDF 업로드 및 캐싱 스크립트
11MB짜리 거대한 AIME 1,000제 PDF 문서를 구글 클라우드에 업로드하고,
추출 스크립트들이 캐시된 파일을 즉시 사용할 수 있도록 URI를 저장합니다.
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# 최신 구글 공식 SDK (google-genai)
from google import genai

# 환경변수 및 경로 설정
BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "engine_v2" / "data"
PDF_PATH = DATA_DIR / "CompendiumAIME.pdf"
CACHE_PATH = DATA_DIR / "pdf_cache.json"

def main():
    if not PDF_PATH.exists():
        print(f"❌ 오류: PDF 파일을 찾을 수 없습니다! ({PDF_PATH})")
        return

    print("🚀 1단계: AIME 1,000제 PDF 업로드 시작 (11MB)")
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    print("  ⏳ 구글 서버로 전송 중...")
    # 파일 업로드
    uploaded_file = client.files.upload(
        file=str(PDF_PATH),
        config={"display_name": "AIME_Compendium_1983_2026"}
    )
    
    print(f"  ✅ 업로드 완료! (File ID: {uploaded_file.name})")
    
    # 문서가 처리될 때까지 대기 (11MB이므로 약 10~30초 소요)
    print("  ⏳ 서버 측 문서 처리 및 벡터화 대기 중...")
    while True:
        status_file = client.files.get(name=uploaded_file.name)
        state = status_file.state.name
        print(f"     상태: {state}")
        if state == "ACTIVE":
            break
        elif state == "FAILED":
            print("  ❌ 오류: 문서 처리에 실패했습니다.")
            return
        time.sleep(5)

    print("  ✨ 문서 처리 완료 (상태: ACTIVE)!")

    # 다음 스크립트(2_extract_chunks.py)에서 사용할 수 있도록 File 정보 캐싱
    cache_data = {
        "file_name": uploaded_file.name,
        "display_name": uploaded_file.display_name,
        "uri": uploaded_file.uri,
        "upload_time": time.time()
    }
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 완료! File 메타데이터가 임시 캐시 파일에 저장되었습니다: {CACHE_PATH}")
    print("👉 이제 'python 2_extract_chunks.py'를 실행할 준비가 되었습니다.")

if __name__ == "__main__":
    main()
