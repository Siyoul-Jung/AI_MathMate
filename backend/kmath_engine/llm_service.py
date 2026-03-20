import os
import json
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
    print("[LLMService] ⚠️ 'openai' library not found. Install it via 'pip install openai'.")

# 성취기준 ID -> 이름 매핑
STANDARD_NAMES = {
    "STD-11-01": "소인수분해의 이해",
    "STD-11-02": "최대공약수와 최소공배수",
    "STD-11-03": "정수와 유리수의 뜻과 대소 관계",
    "STD-11-04": "유리수의 사칙계산",
    "STD-11-05": "문자의 사용과 식의 값",
    "STD-11-06": "일차식의 계산",
    "STD-11-07": "일차방정식의 풀이",
    "STD-11-08": "일차방정식의 활용",
    "STD-11-09": "좌표와 그래프",
    "STD-11-10": "정비례와 반비례",
    "STD-12-01": "점, 선, 면, 각",
    "STD-12-02": "위치 관계",
    "STD-12-03": "작도와 합동",
    "STD-12-04": "다각형",
    "STD-12-05": "원과 부채꼴",
    "STD-12-06": "다면체와 회전체",
    "STD-12-07": "입체도형의 겉넓이와 부피",
    "STD-12-08": "자료의 정리와 해석",
    "STD-21-01": "유리수와 순환소수",
    "STD-21-02": "단항식의 계산",
    "STD-21-03": "다항식의 계산",
    "STD-21-04": "일차부등식",
    "STD-21-05": "일차부등식의 활용",
    "STD-21-06": "연립일차방정식",
    "STD-21-07": "연립일차방정식의 풀이",
    "STD-21-08": "연립일차방정식의 활용",
    "STD-HIGH-01": "다항식",
    "STD-HIGH-02": "복소수와 이차방정식",
    "STD-HIGH-03": "이차방정식과 이차함수",
    "STD-HIGH-04": "여러 가지 방정식",
    "STD-HIGH-05": "여러 가지 부등식",
    "STD-HIGH-06": "경우의 수",
    "STD-HIGH-07": "행렬",
    "STD-HIGH-08": "평면좌표",
    "STD-HIGH-09": "직선의 방정식",
    "STD-HIGH-10": "원의 방정식",
    "STD-HIGH-11": "도형의 이동",
    "STD-HIGH-12": "집합",
    "STD-HIGH-13": "명제",
    "STD-HIGH-14": "함수",
    "STD-HIGH-15": "유리함수와 무리함수"
}

class LLMService:
    """
    LLM(GPT-4o 등)을 활용하여 수학 문제 풀이 과정을 진단하는 서비스
    """
    def __init__(self):
        # 환경 변수에서 API 키 로드 (실제 운영 시 설정 필요)
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = None
        
        print(f"[LLMService] Status Check -> OpenAI Lib: {'✅ Installed' if OpenAI else '❌ Missing'}, API Key: {'✅ Found' if self.api_key else '❌ Missing'}")

        # 디버깅용 로그
        if not self.api_key:
            print("[LLMService] ⚠️ Warning: OPENAI_API_KEY not found in environment variables.")
            
        if OpenAI and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            print(f"[LLMService] ✅ Initialized with API Key: {self.api_key[:10]}...")

    def diagnose_student_answer(self, question, logic_steps, student_input, correct_answer):
        """
        학생의 답안을 logic_steps(Golden Path)와 비교하여 오답 원인을 진단
        """
        if not self.client:
            return {
                "status": "error",
                "message": "API 키 오류: .env 파일을 확인하거나 서버를 재시작해주세요.",
                "mock_hint": "API 키를 설정하면 AI 튜터의 실시간 진단을 받을 수 있습니다."
            }

        # 명세서 M2에 정의된 시스템 프롬프트
        system_prompt = """
Role: You are an elite math tutor for high-achieving students (preparing for CSAT/AMC).
Input: Logic_Steps (Golden Path), Student_Input.

Your Goal: Foster deep mathematical understanding and problem-solving intuition.

Task:
1. Compare Student_Input against Logic_Steps sequentially.
2. Identify the FIRST point of failure (Break-point).
3. Categorize error: CONCEPT (Wrong logic/misunderstanding), CALC (Calculation error), or STRATEGY (Wrong approach).

Guidelines for High-Level Tutoring:
- **Socratic Method**: Do not just give the formula. Ask guiding questions (e.g., "What theorem relates the coefficients to the roots?").
- **Strategic Insight**: If the student is stuck, highlight the problem-solving strategy or key concept involved.
- **Precision**: Distinguish between a simple slip and a fundamental gap in understanding.
- **Tone**: Professional, insightful, and encouraging. Respond in Korean.

Output JSON Format:
{
    "is_correct": boolean,
    "failed_step_id": int | null,
    "error_type": "CONCEPT" | "CALC" | "STRATEGY" | null,
    "feedback": "string (Encouraging feedback)",
    "hint": "string (Deep, insight-provoking hint)"
}
"""

        user_prompt = f"""
[Problem]
{question}

[Correct Answer]
{correct_answer}

[Logic Steps]
{json.dumps(logic_steps, ensure_ascii=False, indent=2)}

[Student Input]
{student_input}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def generate_learning_advice(self, proficiency, weak_points):
        """
        학생의 성취도 데이터를 바탕으로 맞춤형 학습 조언 생성
        """
        if not self.client:
            if not self.api_key:
                return "⚠️ API 키가 설정되지 않았습니다. .env 파일을 확인해주세요."
            if not OpenAI:
                return "⚠️ openai 라이브러리가 설치되지 않았습니다."
            return "⚠️ AI 서비스 초기화에 실패했습니다."

        # ID를 이름으로 변환
        prof_with_names = {STANDARD_NAMES.get(k, k): v for k, v in proficiency.items()}
        weak_with_names = [STANDARD_NAMES.get(k, k) for k in weak_points]

        system_prompt = """
Role: You are a supportive and analytical math learning coach.
Task: Analyze the student's proficiency data and provide personalized learning advice.
Input:
- Proficiency: {Standard_ID: Score (0-100)}
- Weak Points: List of Standard_IDs with low scores.

Guidelines:
1. Start with encouragement based on their strengths (high scores).
2. Gently point out areas for improvement (weak points).
3. Suggest specific study strategies for the weak areas.
4. Keep the tone motivating and constructive.
5. Respond in Korean.
6. Keep it concise (within 3-4 sentences).
7. Use the Standard Names provided in the input, do NOT use internal codes like STD-xx-xx.
"""

        user_prompt = f"""
[Proficiency Data]
{json.dumps(prof_with_names, indent=2, ensure_ascii=False)}

[Weak Points]
{json.dumps(weak_with_names, indent=2, ensure_ascii=False)}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"조언 생성 중 오류가 발생했습니다: {str(e)}"

    def generate_template_code(self, problem_text: str) -> str:
        """
        주어진 문제 텍스트(교과서/PDF 추출)를 분석하여 ProblemTemplate 정의 코드를 생성합니다.
        """
        if not self.client:
            return "API 키가 설정되지 않아 코드를 생성할 수 없습니다."

        system_prompt = """
Role: Python Code Generator for Math Problem Templates.
Task: Analyze the given math problem text (which may have OCR errors) and generate a Python code snippet using the `ProblemTemplate` class.

Context:
- The input text comes from a PDF and may contain broken math symbols (e.g., "x 2" instead of "x^2", "3/4" instead of fraction).
- You must infer the correct mathematical context and fix these errors in the generated code.
- **Use `sympy` library** for mathematical operations (expansion, factorization, solving equations) to ensure accuracy.
- Return the answer in LaTeX format using `sympy.latex()` where appropriate.

One-Shot Example (Strictly follow this structure):
```python
import random
from sympy import symbols, expand, latex

def variable_gen_func():
    # Generate random integers
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    x = symbols('x')
    return {"a": a, "b": b, "x": x}

def answer_calc_func(variables):
    a = variables["a"]
    b = variables["b"]
    x = variables["x"]
    # Example: Calculate area expression (a*x) * (b*x)
    expr = (a * x) * (b * x)
    return latex(expand(expr))

question_format = "Calculate the area of a rectangle with width ${a}x$ and height ${b}x$."
explanation_format = "The area is width * height = {a} * {b} = {answer}."

problem_template = ProblemTemplate(
    question_format=question_format,
    variable_gen_func=variable_gen_func,
    answer_calc_func=answer_calc_func,
    explanation_format=explanation_format
)
```

Requirements:
1. **variable_gen_func**: Must return a dictionary of variables.
2. **answer_calc_func**: Must accept the dictionary and return the answer.
3. **question_format**: Use `{variable_name}` for placeholders.
4. **Output**: ONLY the Python code snippet. No markdown formatting.
"""

        user_prompt = f"Analyze this problem and generate Python code:\n'{problem_text}'"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"코드 생성 중 오류가 발생했습니다: {str(e)}"