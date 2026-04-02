"""
AI_MathMate V2 — Evaluator 에이전트 (BEq 역추론)
역할: 원본 DNA를 모른 상태에서 지문만 읽고 수식을 역추론합니다.

[핵심 원칙]
- "학생(Evaluator)이 지문만 읽어도 수학적으로 동일한 답에 도달해야 한다"
- DNA를 볼 수 없음 → 지문의 모호함/오류를 객관적으로 탐지
- GPT와 다른 회사 모델(Gemini)을 사용하여 편향(Bias) 완전 분리
"""

from __future__ import annotations
import json
import textwrap
from typing import Any

from engine_v2.agents.base_agent import BaseAgent, AgentResult
from engine_v2.config import MODELS


class EvaluatorAgent(BaseAgent):
    """
    BEq(양방향 등가성) 역추론 에이전트.
    Gemini 2.5 Flash를 사용하여 Writer와 독립적으로 지문을 분석합니다.
    """

    ROLE = "EVALUATOR"

    def __init__(self):
        super().__init__(model_name=MODELS["evaluator"], max_retries=2)

    def run(
        self,
        narrative: str,
        expected_answer: int,    # Judge가 비교에 사용 (Evaluator 자신은 모름)
    ) -> AgentResult:
        """
        :param narrative: Writer가 생성한 지문 (DNA 정보 없음)
        :param expected_answer: Judge 비교용 (이 에이전트는 사용하지 않음)
        :return: AgentResult (output = 역추론 결과 딕셔너리)
        """
        try:
            client = self._get_gemini_client()

            prompt = textwrap.dedent(f"""
                당신은 미국 수학 올림피아드(AIME) 수험생입니다.
                아래 문제를 풀어서 결과를 JSON으로 반환하세요.

                **중요**: 이 문제의 정답은 0 이상 999 이하의 정수입니다.

                ---
                {narrative}
                ---

                다음 단계로 분석하세요:
                1. 문제에서 주어진 수학적 조건들을 명확히 서술하세요.
                2. 풀이에 사용할 수학적 전략을 설명하세요.
                3. 단계별로 계산을 수행하세요.
                4. 최종 정수 정답을 도출하세요.

                ## 응답 형식 (반드시 JSON)
                {{
                    "conditions_extracted": ["조건1", "조건2", ...],
                    "mathematical_strategy": "풀이 전략 설명",
                    "step_by_step": ["단계1", "단계2", ...],
                    "final_answer": 정수_정답,
                    "confidence": "HIGH" | "MEDIUM" | "LOW",
                    "ambiguity_detected": "지문 모호성이 발견된 경우 설명, 없으면 빈 문자열"
                }}
            """).strip()

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )

            result = json.loads(response.text)
            extracted_answer = int(result.get("final_answer", -1))
            ambiguity = result.get("ambiguity_detected", "")
            confidence = result.get("confidence", "LOW")

            return AgentResult(
                success=True,
                agent_role=self.ROLE,
                agent_model=self.model_name,
                input_summary=f"narrative[:200]={narrative[:200]}",
                output={
                    "extracted_answer": extracted_answer,
                    "conditions": result.get("conditions_extracted", []),
                    "strategy": result.get("mathematical_strategy", ""),
                    "steps": result.get("step_by_step", []),
                    "confidence": confidence,
                    "ambiguity": ambiguity,
                    "raw_result": result,
                },
                verdict="PENDING",  # Judge가 최종 판정
            )

        except json.JSONDecodeError as e:
            return AgentResult(
                success=False, agent_role=self.ROLE, agent_model=self.model_name,
                input_summary=narrative[:200],
                output=None, error=f"JSON 파싱 실패: {e}"
            )
        except Exception as e:
            return AgentResult(
                success=False, agent_role=self.ROLE, agent_model=self.model_name,
                input_summary=narrative[:200],
                output=None, error=str(e)
            )
