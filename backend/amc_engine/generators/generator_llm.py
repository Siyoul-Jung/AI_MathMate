from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# 프로젝트 루트의 .env 파일 자동 로드
load_dotenv()

def generate_variant_with_gemini(final_prompt):
    """
    파이프라인 매니저로부터 받은 프롬프트를 LLM에 전달하고
    순수한 JSON 결과물만 반환하는 범용 인터페이스입니다.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "❌ OPENAI_API_KEY가 설정되지 않았습니다.\n"
            "   .env.example을 복사하여 .env 파일을 만들고 API 키를 입력하세요:\n"
            "   cp .env.example .env"
        )
    
    # OpenAI 호환 API 클라이언트 초기화
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional AIME problem setter. You must output the result strictly in the requested JSON format."
                },
                {
                    "role": "user", 
                    "content": final_prompt
                }
            ],
            response_format={ "type": "json_object" }, # JSON 모드 활성화
            temperature=0.7 # 창의성과 일관성의 균형
        )
        
        # 응답 텍스트 추출 및 JSON 파싱
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print(f"⚠️ LLM 호출 중 오류 발생: {e}")
        return {}