import sys
import os
import re

# 1. 필수 라이브러리 체크
try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ 'python-dotenv' 라이브러리가 설치되지 않았습니다. 다음 명령어로 설치하세요:\n   pip install python-dotenv")
    sys.exit(1)

try:
    import openai
except ImportError:
    print("❌ 'openai' 라이브러리가 설치되지 않았습니다. 다음 명령어로 설치하세요:\n   pip install openai")
    sys.exit(1)

try:
    from pypdf import PdfReader
except ImportError:
    print("❌ 'pypdf' 라이브러리가 설치되지 않았습니다. 다음 명령어로 설치하세요:\n   pip install pypdf")
    sys.exit(1)

# 프로젝트 루트 경로 추가 (backend root)
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.dirname(current_dir)
if backend_root not in sys.path:
    sys.path.append(backend_root)

# .env 파일 로드 (backend 루트에 위치)
env_path = os.path.join(backend_root, ".env")
if os.path.exists(env_path):
    print(f"📄 .env 파일 로드 중: {env_path}")
    load_dotenv(env_path)
else:
    print(f"⚠️ .env 파일을 찾을 수 없습니다: {env_path}")

from kmath_engine.llm_service import LLMService

def extract_text_chunks(pdf_path, pages_per_chunk=3):
    """PDF 파일에서 텍스트를 청크 단위로 추출 (pypdf 라이브러리 필요)"""
    try:
        reader = PdfReader(pdf_path)
        chunks = []
        current_text = ""
        total_pages = len(reader.pages)
        print(f"📄 총 {total_pages} 페이지가 발견되었습니다.")

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                current_text += text + "\n"
            
            # 청크 크기 도달하거나 마지막 페이지면 저장
            if (i + 1) % pages_per_chunk == 0 or (i + 1) == total_pages:
                if current_text.strip():
                    chunks.append(current_text)
                current_text = ""
        return chunks
    except Exception as e:
        print(f"❌ PDF 읽기 오류: {e}")
        return []

def clean_code_block(code):
    """LLM 응답에서 마크다운 코드 블록 제거"""
    pattern = r"```python\s*(.*?)\s*```"
    match = re.search(pattern, code, re.DOTALL)
    if match:
        return match.group(1)
    # 코드 블록이 없는 경우, 혹시 모를 앞뒤 ``` 제거
    return code.replace("```python", "").replace("```", "").strip()

def main():
    if len(sys.argv) < 2:
        print("사용법: python tools/pdf_learner.py <pdf_file_path>")
        return

    # API 키 확인 및 대화형 설정
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OpenAI API 키가 설정되지 않았습니다.")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n⚠️  OpenAI API 키가 환경 변수에서 발견되지 않았습니다.")
        print("   이 도구를 사용하려면 OpenAI API 키가 필요합니다.")
        print("   (키 발급: https://platform.openai.com/api-keys)")
        
        try:
            key_input = input("\n👉 API 키를 입력하세요 (sk-...): ").strip()
        except KeyboardInterrupt:
            return
        
        if key_input and key_input.startswith("sk-"):
            with open(env_path, "a", encoding="utf-8") as f:
                f.write(f"\nOPENAI_API_KEY={key_input}\n")
            print(f"✅ API 키가 '{env_path}' 파일에 저장되었습니다.")
            os.environ["OPENAI_API_KEY"] = key_input
            openai.api_key = key_input
        else:
            print("❌ 유효한 API 키가 입력되지 않았습니다. 실행을 중단합니다.")
            return
    else:
        print(f"🔑 API 키 확인됨: {api_key[:8]}...")
        openai.api_key = api_key

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"❌ 파일을 찾을 수 없습니다: {pdf_path}")
        return

    print(f"📖 PDF 파일 로딩 중: {pdf_path}...")
    chunks = extract_text_chunks(pdf_path, pages_per_chunk=3)
    
    if not chunks:
        print("❌ PDF에서 텍스트를 추출할 수 없습니다.")
        return

    print(f"🔍 총 {len(chunks)}개의 파트로 나누어 분석을 시작합니다...")
    
    llm = LLMService()
    
    # LLMService 초기화 상태 확인
    if not llm.client:
        print("❌ LLMService 초기화 실패. API 키 설정이나 openai 라이브러리 설치를 확인해주세요.")
        return

    for i, text in enumerate(chunks):
        print(f"\n⏳ [Part {i+1}/{len(chunks)}] 문제 유형 분석 및 코드 생성 중...")
        code = llm.generate_template_code(text)
        
        if not code or "오류" in code or "API 키" in code:
            print(f"❌ [Part {i+1}] 코드 생성 실패:\n{code}")
            continue

        # 코드 정제
        clean_code = clean_code_block(code)

        # 결과를 파일로 저장
        output_file = f"{pdf_path}.part{i+1}.py"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(clean_code)
        
        print(f"✅ [Part {i+1}] 템플릿 코드가 저장되었습니다: {output_file}")

    print("\n🎉 모든 파트의 처리가 완료되었습니다. 생성된 파일들을 curriculum 폴더로 이동하여 사용하세요.")

if __name__ == "__main__":
    main()
