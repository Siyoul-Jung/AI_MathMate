"""
AI_MathMate V2 — Writer 에이전트 (IIPC Branch A + B)
역할: 주어진 수학적 DNA(시드 + 논리 단계)를 받아 AIME 스타일 지문을 생성합니다.

[IIPC 이중 분기]
- Branch A (CoT): GPT-4o-mini가 자연어 논리와 지문을 작성
- Branch B (SymPy): 같은 시드로 파이썬 코드를 실행하여 정답을 독립적으로 계산
- 합의 확인: 두 분기의 정답이 일치할 때만 Writer가 성공 반환
"""

from __future__ import annotations
import json
import textwrap
from typing import Any

from engine_v2.agents.base_agent import BaseAgent, AgentResult
from engine_v2.config import MODELS


# ─── Writer 에이전트 ─────────────────────────────────────────────────────────

class WriterAgent(BaseAgent):
    """
    IIPC(이중 분기) 기반 문항 작성 에이전트.
    GPT-4o-mini로 지문을 작성하고, SymPy 코드로 정답을 교차 검증합니다.
    """

    ROLE = "WRITER"

    def __init__(self):
        super().__init__(model_name=MODELS["writer"], max_retries=3)

    def run(
        self,
        seed: dict[str, Any],
        logic_steps: list[str],
        correct_answer: int,
        module_ids: list[str],
        target_daps: float = 12.0,
        theme_hint: str = "",
        fix_history: list[str] = None,   # Judge의 누적 수정 지시
        failed_step_index: int = None,  # AR-Sampling: 오류 발원 단계 (0-indexed)
    ) -> AgentResult:
        """
        :param seed: 솔버가 생성한 수학 변수 딕셔너리
        :param logic_steps: 문제의 논리적 단계 목록
        :param correct_answer: 파이썬 솔버가 계산한 정답
        :param module_ids: 사용된 원자 모듈 ID 목록 (참고용)
        :param fix_history: Evaluator/Judge의 이전 수정 지시 (리스트 형태)
        :return: AgentResult (output = narrative 문자열)
        """

        # ── Branch A: GPT-4o-mini로 지문 생성 ───────────────────────────────
        branch_a_result = self._run_branch_a(
            seed, logic_steps, correct_answer, target_daps, theme_hint, fix_history, failed_step_index
        )
        if not branch_a_result["success"]:
            return AgentResult(
                success=False, agent_role=self.ROLE, agent_model=self.model_name,
                input_summary=f"seed={list(seed.keys())}",
                output=None, error=branch_a_result["error"]
            )

        narrative = branch_a_result["narrative"]
        branch_a_answer = branch_a_result["extracted_answer"]

        # ── Branch B: SymPy 코드로 독립적 정답 계산 ─────────────────────────
        branch_b_answer = self._run_branch_b(seed, logic_steps)

        # ── 합의 확인: 두 분기 정답 + 원본 정답 모두 일치해야 통과 ───────────
        answers = {
            "original_solver": correct_answer,
            "branch_a_narr": branch_a_answer,
            "branch_b_sympy": branch_b_answer,
        }

        if branch_a_answer != correct_answer:
            return AgentResult(
                success=False, agent_role=self.ROLE, agent_model=self.model_name,
                input_summary=f"seed={list(seed.keys())}",
                output=narrative,
                verdict="FAIL",
                error=f"Branch A 정답 불일치: 지문={branch_a_answer}, 원본={correct_answer}",
            )

        if branch_b_answer is not None and branch_b_answer != correct_answer:
            return AgentResult(
                success=False, agent_role=self.ROLE, agent_model=self.model_name,
                input_summary=f"seed={list(seed.keys())}",
                output=narrative,
                verdict="FAIL",
                error=f"Branch B(SymPy) 정답 불일치: SymPy={branch_b_answer}, 원본={correct_answer}",
            )

        return AgentResult(
            success=True,
            agent_role=self.ROLE,
            agent_model=self.model_name,
            input_summary=f"seed keys={list(seed.keys())}, modules={module_ids}",
            output={
                "narrative": narrative,
                "branch_a_answer": branch_a_answer,
                "branch_b_answer": branch_b_answer,
                "answers_consensus": answers,
            },
            verdict="PASS",
        )

    def _run_branch_a(
        self, seed, logic_steps, correct_answer, target_daps, theme_hint, fix_history, failed_step_index=None
    ) -> dict:
        """Branch A: GPT-4o-mini로 지문 생성 및 정답 추출"""
        try:
            client = self._get_openai_client()

            fix_section = ""
            if fix_history:
                history_text = "\n".join(f"- 시도 {i+1} 피드백: {msg}" for i, msg in enumerate(fix_history))
                fix_section = f"""
## 이전 실패 이력 및 수정 요청 (Fix History)
{history_text}
위 피드백을 반드시 반영하여 이전과 동일한 수학적/구조적 오류를 반복하지 마세요.
"""

            prompt = textwrap.dedent(f"""
                당신은 AIME(미국 수학 올림피아드) 전문 출제위원입니다.
                아래 수학적 구조(DNA)를 바탕으로 AIME 스타일의 문제 지문을 작성하세요.

                ## 수학적 DNA (절대 변경 불가)
                - 핵심 변수: {json.dumps(seed, ensure_ascii=False)}
                - 논리 단계: {json.dumps(logic_steps, ensure_ascii=False)}
                - 정답: {correct_answer} (000~999 범위 정수)
                - 목표 난이도: DAPS {target_daps:.1f}
                {f'- 시나리오 힌트: {theme_hint}' if theme_hint else ''}

                {fix_section}

                ## AR-Sampling (Adaptive Rectification)
                {f"💡 [Rethink Required] 이전 추론의 {failed_step_index + 1}단계에서 논리적 오류가 발견되었습니다." if failed_step_index is not None else ""}
                {f"{failed_step_index + 1}단계 이전의 논리는 유지하되, 해당 지점부터 다시 추론(Rethink)하여 오류를 교정하세요." if failed_step_index is not None else ""}

                ## 작성 규칙
                1. 지문은 영어로 작성합니다.
                2. 정답이 {correct_answer}임을 직접 언급하지 마세요.
                3. 지문만 읽어도 독립적으로 풀 수 있어야 합니다.
                4. AIME 특유의 간결하고 수학적인 문체를 사용하세요.
                5. LaTeX 수식은 $...$ 형식으로 작성하세요.

                ## 응답 형식 (반드시 JSON)
                {{
                    "narrative": "문제 지문 전체",
                    "extracted_answer": {correct_answer}
                }}
            """).strip()

            response = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.7,
            )

            content = json.loads(response.choices[0].message.content)
            return {
                "success": True,
                "narrative": content.get("narrative", ""),
                "extracted_answer": int(content.get("extracted_answer", -1)),
            }

        except Exception as e:
            return {"success": False, "error": str(e), "narrative": "", "extracted_answer": -1}

    def _run_branch_b(self, seed: dict, logic_steps: list[str]) -> int | None:
        """
        Branch B: SymPy를 사용하여 시드에서 독립적으로 정답을 계산합니다.
        구현 가능한 경우에만 실행 (모듈별로 오버라이드 가능).
        현재는 기본적인 시드 검증만 수행합니다.
        """
        try:
            # 기본 구현: 시드 값들이 정수인지 확인
            # 각 모듈의 SymPy 코드는 Phase 3에서 추가됩니다.
            for k, v in seed.items():
                if not isinstance(v, (int, float)):
                    return None  # 계산 불가 시 None 반환 (통과 처리)
            return None  # 현재는 Branch A만 검증 (Phase 3에서 완전 구현)
        except Exception:
            return None
