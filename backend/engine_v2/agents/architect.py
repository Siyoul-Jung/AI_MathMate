"""
AI_MathMate V2 — Architect 에이전트 (모듈 조합 설계자)
역할: DAPS 필터가 추려낸 후보 조합 중 가장 창의적이고 참신한 조합을 선택합니다.

[2단계 설계 프로세스]
  Step 1 (자동/수학): ModuleRegistry.get_compatible_combinations() → 후보 필터링
  Step 2 (창의/LLM): Architect가 후보 중 최종 1개를 창의적으로 선택 + 설계 의도 기록
"""

from __future__ import annotations
import json
import textwrap
import uuid
from typing import Any

from engine_v2.agents.base_agent import BaseAgent, AgentResult
from engine_v2.config import MODELS, get_pg_dsn
try:
    import psycopg2
except ImportError:
    psycopg2 = None


class ArchitectAgent(BaseAgent):
    """
    모듈 조합 설계 에이전트.
    config.py의 MODELS["architect"] 설정에 따라 OpenAI(gpt-*) 또는 Gemini 모델을 사용하여
    최적의 하이브리드 모듈 조합을 선택합니다. (3-Company Separation 지원)
    """

    ROLE = "ARCHITECT"

    def __init__(self, dsn: str = None):
        super().__init__(model_name=MODELS["architect"], max_retries=2)
        self.dsn = dsn or get_pg_dsn()

    def run(
        self,
        candidate_combinations: list[list[str]],
        module_metadata: dict[str, dict],   # module_id → META 딕셔너리
        target_daps: float = 13.5,
        difficulty_band: str = "MASTER",
        exam_type: str = "AIME",
        language: str = "en",
        previously_used: list[str] = None,  # 최근 사용된 조합 (중복 방지)
    ) -> AgentResult:
        """
        :param candidate_combinations: DAPS 필터 통과한 가능 조합 목록
        :param module_metadata: 각 모듈의 META 정보 (이름, 카테고리, 태그 등)
        :param target_daps: 목표 DAPS 점수
        :param previously_used: 직전 N개 조합 (참신성 강제)
        :return: AgentResult (output = 선택된 blueprint 정보)
        """

        if not candidate_combinations:
            return AgentResult(
                success=False, agent_role=self.ROLE, agent_model=self.model_name,
                input_summary=f"candidates=0, target_daps={target_daps}",
                output=None, error="후보 조합이 없습니다. 모듈을 더 등록하거나 DAPS 허용 범위를 넓히세요."
            )

        previously_used = previously_used or []

        try:
            # 후보 조합 설명 텍스트 생성
            combo_descriptions = []
            for i, combo in enumerate(candidate_combinations):
                modules_info = []
                for mid in combo:
                    meta = module_metadata.get(mid, {})
                    modules_info.append(
                        f"{meta.get('name', mid)} (depth={meta.get('logic_depth', '?')}, "
                        f"DAPS기여={meta.get('daps_contribution', '?')})"
                    )
                estimated_daps = sum(
                    module_metadata.get(mid, {}).get("daps_contribution", 0) for mid in combo
                )
                combo_descriptions.append(
                    f"조합 {i+1}: [{', '.join(combo)}]\n"
                    f"  구성: {' + '.join(modules_info)}\n"
                    f"  예상 DAPS: {estimated_daps:.1f}"
                )

            recently_used_str = (
                f"\n최근 사용된 조합 (가능하면 피하세요): {previously_used}"
                if previously_used else ""
            )

            prompt = textwrap.dedent(f"""
                당신은 AIME 문제 설계 전문가(Architect)입니다.
                아래 후보 모듈 조합들 중 하나를 선택하고, 선택 이유를 설명하세요.

                ## 설계 목표
                - 목표 난이도: DAPS {target_daps:.1f} ({difficulty_band}급)
                - 시험 유형: {exam_type}
                - 참신성: 기존 기출에서 보기 어려운 독창적인 조합 우선
                - 수학적 깊이: 논리 단계가 깊을수록 좋음
                {recently_used_str}

                ## 후보 조합
                {chr(10).join(combo_descriptions)}

                ## 선택 기준 (중요도 순)
                1. 두 개념이 융합될 때 예상치 못한 방식으로 연결되는가?
                2. 한 가지 공식을 아는 것만으로는 바로 풀 수 없는가?
                3. 최근에 사용한 조합과 다른가?

                ## 응답 형식 (반드시 JSON)
                {{
                    "selected_combination_index": 1부터_시작하는_번호,
                    "selected_module_ids": ["module_id_1", "module_id_2"],
                    "reasoning": "선택 이유 (2~4문장)",
                    "expected_problem_structure": "예상되는 문제 구조 설명",
                    "presentation_style": "storytelling" | "pure_formal",
                    "requires_image": true | false,
                    "anti_formulaic_risk": "LOW" | "MEDIUM" | "HIGH"
                }}
            """).strip()

            # 3-Company Separation: 모델에 따라 OpenAI 또는 Gemini 클라이언트 사용
            if self.model_name.startswith("gpt"):
                result = self._call_openai(prompt)
            else:
                result = self._call_gemini(prompt)
            selected_idx = result.get("selected_combination_index", 1) - 1
            selected_idx = max(0, min(selected_idx, len(candidate_combinations) - 1))
            selected_combo = result.get(
                "selected_module_ids",
                candidate_combinations[selected_idx]
            )
            reasoning = result.get("reasoning", "")
            risk = result.get("anti_formulaic_risk", "MEDIUM")
            style = result.get("presentation_style", "pure_formal")
            req_img = result.get("requires_image", False)

            # Blueprint 생성 및 DB 저장
            blueprint_id = self._save_blueprint(
                selected_combo, target_daps, difficulty_band,
                exam_type, language, reasoning
            )

            print(f"  🏗️  [ARCHITECT] Blueprint 생성: {blueprint_id}")
            print(f"     선택 조합: {selected_combo}")
            print(f"     스타일 정립: {style} (이미지 필요: {req_img})")

            return AgentResult(
                success=True,
                agent_role=self.ROLE,
                agent_model=self.model_name,
                input_summary=f"candidates={len(candidate_combinations)}, target_daps={target_daps}",
                output={
                    "blueprint_id": blueprint_id,
                    "selected_modules": selected_combo,
                    "reasoning": reasoning,
                    "expected_structure": result.get("expected_problem_structure", ""),
                    "presentation_style": style,
                    "requires_image": req_img,
                    "anti_formulaic_risk": risk,
                },
                verdict="PASS",
            )

        except Exception as e:
            return AgentResult(
                success=False, agent_role=self.ROLE, agent_model=self.model_name,
                input_summary=f"candidates={len(candidate_combinations)}",
                output=None, error=str(e)
            )

    def _call_openai(self, prompt: str) -> dict:
        """OpenAI 모델로 JSON 응답을 생성합니다."""
        client = self._get_openai_client()
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are an AIME problem design expert. Always respond in valid JSON."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

    def _call_gemini(self, prompt: str) -> dict:
        """Gemini 모델로 JSON 응답을 생성합니다."""
        client = self._get_gemini_client()
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        return json.loads(response.text)

    def _save_blueprint(
        self,
        module_ids: list[str],
        target_daps: float,
        difficulty_band: str,
        exam_type: str,
        language: str,
        reasoning: str,
    ) -> str:
        """Blueprint를 DB에 저장하고 blueprint_id를 반환합니다. (Postgres 연결 실패 시 가상 ID 반환)"""
        blueprint_id = f"bp_{uuid.uuid4().hex[:12]}"

        try:
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO blueprints
                        (blueprint_id, target_daps, difficulty_band, exam_type, language,
                         architect_model, architect_reasoning, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 'PENDING')
                    """, (blueprint_id, target_daps, difficulty_band, exam_type, language,
                          self.model_name, reasoning))

                    for order, mid in enumerate(module_ids):
                        cur.execute("""
                            INSERT INTO blueprint_modules (blueprint_id, module_id, combination_order)
                            VALUES (%s, %s, %s)
                        """, (blueprint_id, mid, order))

                conn.commit()
        except Exception as e:
            print(f"  [DB_FALLBACK] Blueprint 저장 실패 (PostgreSQL 미가동?): {e}")
            # 이미 생성된 가상 blueprint_id를 그대로 사용하여 진행을 허용합니다.

        return blueprint_id
