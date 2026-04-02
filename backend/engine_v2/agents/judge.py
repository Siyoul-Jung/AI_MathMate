"""
AI_MathMate V2 — Judge 에이전트 (BEq 최종 판별)
역할: Evaluator의 역추론 결과를 원본 정답과 비교하고, 구체적인 수정 보고서를 발행합니다.

[LLM 없음 - 순수 Python]
Judge는 외부 API를 호출하지 않습니다.
파이썬 로직으로 수학적 정확성을 판별하여 비용 절감과 속도를 동시에 달성합니다.
"""

from __future__ import annotations
from typing import Any

from engine_v2.agents.base_agent import BaseAgent, AgentResult
from engine_v2.config import PIPELINE


class JudgeAgent(BaseAgent):
    """
    BEq(양방향 등가성) 최종 판별 에이전트.

    판별 기준:
    1. Evaluator의 추출 답 == 원본 정답?     → 수학 검증
    2. Evaluator의 신뢰도가 HIGH인가?        → 지문 명확성 검증
    3. 지문 모호성이 감지되었는가?           → 중의성 검증
    """

    ROLE = "JUDGE"

    def __init__(self):
        super().__init__(model_name="python-logic", max_retries=1)

    def run(
        self,
        original_answer: int,
        evaluator_output: dict[str, Any],
        narrative: str = "",
    ) -> AgentResult:
        """
        :param original_answer: 파이썬 Solver의 정답 (Ground Truth)
        :param evaluator_output: EvaluatorAgent.run()의 output 딕셔너리
        :param narrative: 원본 지문 (수정 지시 생성 시 참조)
        :return: AgentResult (verdict = "PASS" | "FAIL" | "FIX_REQUIRED")
        """

        extracted = evaluator_output.get("extracted_answer", -1)
        confidence = evaluator_output.get("confidence", "LOW")
        ambiguity = evaluator_output.get("ambiguity", "")
        conditions = evaluator_output.get("conditions", [])
        steps = evaluator_output.get("steps", [])

        issues = []
        fix_parts = []

        # ── 판별 1: 수학적 정확성 (가장 중요) ──────────────────────────────
        if extracted != original_answer:
            issues.append(
                f"[수학 오류] Evaluator 추출 답={extracted}, 원본={original_answer}"
            )
            fix_parts.append(
                f"지문을 읽은 학생이 {extracted}라는 답을 구했습니다. "
                f"정답은 {original_answer}이어야 합니다. "
                f"지문의 수학적 조건을 재검토하여 {original_answer}로 유도되도록 수정하세요."
            )

        # ── 판별 2: Evaluator 신뢰도 ──────────────────────────────────────
        if confidence == "LOW":
            issues.append("[낮은 신뢰도] Evaluator가 지문을 이해하기 어렵다고 판단")
            fix_parts.append(
                "Evaluator가 지문을 이해하기 어렵다고 판단했습니다. "
                "수학적 조건을 더 명확하게 기술하고, 불필요한 수식 생략을 없애세요."
            )

        # ── 판별 3: 지문 모호성 ───────────────────────────────────────────
        if ambiguity:
            issues.append(f"[모호성 감지] {ambiguity[:100]}")
            fix_parts.append(
                f"다음 모호성을 해결하세요: {ambiguity}"
            )

        # ── 판별 4: 조건 추출 최소 기준 ───────────────────────────────────
        if len(conditions) < 2:
            issues.append("[조건 부족] Evaluator가 추출한 조건이 2개 미만")
            fix_parts.append(
                "지문에서 수학적 조건이 명확히 드러나지 않습니다. "
                "핵심 제약 조건(예: 범위, 관계식)을 지문에 더 명시적으로 포함하세요."
            )

        # ── 최종 판정 ─────────────────────────────────────────────────────
        if not issues:
            verdict = "PASS"
            fix_instruction = ""
            print(f"  ✅ [JUDGE] PASS — 원본={original_answer}, Evaluator={extracted}, 신뢰도={confidence}")
        elif extracted != original_answer:
            verdict = "FAIL"          # 수학 오류는 즉시 실패
            fix_instruction = "\n".join(fix_parts)
            print(f"  ❌ [JUDGE] FAIL — 수학 오류: 원본={original_answer}, Evaluator={extracted}")
        else:
            verdict = "FIX_REQUIRED"  # 모호성/신뢰도 문제는 수정 요청
            fix_instruction = "\n".join(fix_parts)
            print(f"  ⚠️  [JUDGE] FIX_REQUIRED — {len(issues)}개 이슈: {issues}")

        return AgentResult(
            success=(verdict == "PASS"),
            agent_role=self.ROLE,
            agent_model=self.model_name,
            input_summary=f"original={original_answer}, extracted={extracted}",
            output={
                "verdict": verdict,
                "original_answer": original_answer,
                "evaluator_answer": extracted,
                "issues": issues,
                "logic_steps_count": len(steps),
            },
            verdict=verdict,
            fix_instruction=fix_instruction,
        )

    def generate_collision_report(
        self,
        original_answer: int,
        evaluator_answer: int,
        narrative: str,
        evaluator_steps: list[str],
    ) -> str:
        """
        수학 오류 발생 시 Writer에게 전달할 상세 충돌 보고서를 생성합니다.
        Writer가 어느 부분을 고쳐야 하는지 구체적으로 안내합니다.
        """
        return (
            f"[충돌 보고서]\n"
            f"원본 정답: {original_answer}\n"
            f"Evaluator 추출 답: {evaluator_answer}\n"
            f"Evaluator 풀이 단계:\n"
            + "\n".join(f"  {i+1}. {s}" for i, s in enumerate(evaluator_steps))
            + f"\n\n수정 지시: 지문을 읽은 학생이 {evaluator_answer}에 도달했습니다. "
            f"정답 {original_answer}으로 유도되도록 지문의 수학적 조건을 재검토하세요."
        )
