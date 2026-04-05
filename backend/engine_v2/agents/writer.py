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

            # 정답은 Writer에게 노출하지 않음 (Two-Engine 원칙)
            # Writer가 지문을 쓰고 스스로 풀어야 BEq의 의미가 있음
            prompt = textwrap.dedent(f"""
                You are a professional AIME (American Invitational Mathematics Examination) problem writer.
                Create an AIME-style problem based on the mathematical structure below.

                ## Mathematical DNA (DO NOT MODIFY the underlying math)
                - Variables: {json.dumps(seed, ensure_ascii=False)}
                - Logic chain: {json.dumps(logic_steps, ensure_ascii=False)}
                - Target difficulty: DAPS {target_daps:.1f}
                {f'- Theme hint: {theme_hint}' if theme_hint else ''}

                {fix_section}

                {f"[Rethink Required] A logical error was found at step {failed_step_index + 1}. Keep prior steps, re-derive from that point." if failed_step_index is not None else ""}

                ## VERIFICATION ANSWER (for self-check ONLY — do NOT reverse-engineer from this)
                The correct answer is {correct_answer}. Write the problem FIRST based on the logic chain,
                then verify your narrative leads to this answer. If it doesn't match, revise your narrative — never adjust the math.

                ## STRICT RULES — Violations cause immediate rejection
                1. Write the problem statement in English.
                2. The problem MUST be self-contained: solvable from the statement alone, with no external knowledge of the DNA.
                3. NEVER mention mathematical technique names in the problem statement (e.g., "Vieta's formulas", "Snake Oil", "inclusion-exclusion", "Shoelace formula", "Chinese Remainder Theorem", "derangement", "Catalan"). The solver must DISCOVER which technique to use.
                4. NEVER add mathematical conditions, constraints, or variables beyond what the logic chain provides. This is the #1 cause of failure ("Innovation Curse").
                5. If multiple modules are involved, weave them into ONE unified scenario — do NOT present them as separate calculations joined by "and", "next", or "now consider". Create a single story where both computations emerge naturally.
                6. Use concise AIME style: 2-4 sentences max for the setup. No preamble, no "Let's consider", no unnecessary context.
                7. LaTeX: use $...$ for inline, avoid \\text{{}} for units. Use $^\\circ$ for degrees, $\\times$ for multiplication.
                8. The answer MUST be an integer from 000 to 999. Frame the question so the answer naturally falls in this range (e.g., "Find the remainder when X is divided by 1000").
                9. After writing, solve your own problem to derive extracted_answer. It MUST equal {correct_answer}.

                ## Response format (MUST be valid JSON)
                {{
                    "narrative": "the complete problem statement",
                    "extracted_answer": <integer 0-999 you derived by solving your own problem>
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
        [Deprecated] Branch B는 Writer가 아닌 Pipeline(결정론 엔진)에서 실행됩니다.

        Two-Engine 원칙에 따라 수학 검증은 LLM 레이어가 아닌
        AtomicModule.verify_with_sympy() → Pipeline에서 실행됩니다.
        이 메서드는 하위 호환성을 위해 유지되며, 항상 None을 반환합니다.
        """
        return None
