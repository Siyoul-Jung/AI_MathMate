"""
AI_MathMate V2 — 공통 에이전트 베이스 클래스
모든 에이전트(Writer, Evaluator, Judge, Architect)가 상속받는 기반입니다.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import time
import os
from dotenv import load_dotenv

# .env 로드 (backend/.env)
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")


@dataclass
class AgentResult:
    """에이전트 실행 결과의 표준 포맷."""
    success: bool
    agent_role: str
    agent_model: str
    input_summary: str    # 입력 내용 요약 (로깅용)
    output: Any           # 실제 출력 (역할별로 다름)
    verdict: str = ""     # "PASS" | "FAIL" | "FIX_REQUIRED" | "PENDING"
    fix_instruction: str = ""  # Judge가 발행하는 수정 지시
    duration_ms: int = 0
    attempt_number: int = 1
    error: str = ""

    def to_log_dict(self) -> dict:
        """mas_logs 테이블에 저장할 딕셔너리로 변환합니다."""
        return {
            "agent_role": self.agent_role,
            "agent_model": self.agent_model,
            "input_sent": self.input_summary[:2000],  # DB 저장 한도
            "output_received": str(self.output)[:4000],
            "verdict": self.verdict,
            "fix_instruction": self.fix_instruction,
            "attempt_number": self.attempt_number,
            "duration_ms": self.duration_ms,
        }


class BaseAgent(ABC):
    """
    모든 V2 에이전트의 기반 클래스.

    [에이전트 역할 정의]
    - WRITER    : 시나리오 작성 (GPT-4o-mini)
    - EVALUATOR : 역추론 검증 (Gemini 2.5 Flash)
    - JUDGE     : BEq 판별 (Python - LLM 없음)
    - ARCHITECT : 모듈 조합 설계 (Gemini 2.5 Flash)
    """

    ROLE: str = "BASE"    # 하위 클래스에서 반드시 정의

    def __init__(self, model_name: str = "", max_retries: int = 3):
        self.model_name = model_name
        self.max_retries = max_retries

    @abstractmethod
    def run(self, **kwargs) -> AgentResult:
        """에이전트의 핵심 작업을 실행합니다."""
        ...

    def run_with_retry(self, **kwargs) -> AgentResult:
        """
        실패 시 max_retries만큼 재시도합니다.
        각 시도의 결과는 attempt_number에 기록됩니다.
        """
        last_result = None
        for attempt in range(1, self.max_retries + 1):
            start = time.time()
            try:
                result = self.run(**kwargs)
                result.attempt_number = attempt
                result.duration_ms = int((time.time() - start) * 1000)
                if result.success:
                    return result
                last_result = result
                print(f"  ⚠️  [{self.ROLE}] 시도 {attempt}/{self.max_retries} 실패: {result.error}")
            except Exception as e:
                last_result = AgentResult(
                    success=False,
                    agent_role=self.ROLE,
                    agent_model=self.model_name,
                    input_summary="",
                    output=None,
                    error=str(e),
                    attempt_number=attempt,
                    duration_ms=int((time.time() - start) * 1000),
                )
                print(f"  ❌ [{self.ROLE}] 시도 {attempt}/{self.max_retries} 예외: {e}")

        print(f"  ❌ [{self.ROLE}] {self.max_retries}회 모두 실패")
        return last_result

    def _get_openai_client(self):
        """OpenAI 클라이언트를 반환합니다."""
        from openai import OpenAI
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def _get_gemini_client(self):
        """Gemini 클라이언트를 반환합니다."""
        from google import genai
        return genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: role={self.ROLE}, model={self.model_name}>"
