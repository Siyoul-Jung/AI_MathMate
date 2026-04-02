"""
AI_MathMate V2 — 메인 파이프라인 매니저
Architect ➔ Module ➔ Writer ➔ Evaluator ➔ Judge 에 이르는 전체 MAS 루프를 관장합니다.
"""

from __future__ import annotations
import json
import psycopg2
import time
from pathlib import Path

from engine_v2.config import PIPELINE, get_pg_dsn
from engine_v2.module_registry import ModuleRegistry
from engine_v2.agents.architect import ArchitectAgent
from engine_v2.agents.writer import WriterAgent
from engine_v2.agents.evaluator import EvaluatorAgent
from engine_v2.agents.judge import JudgeAgent


class EngineV2Pipeline:
    """V2 문항 생성 및 이중 검증 파이프라인 총괄"""

    def __init__(self):
        self.registry = ModuleRegistry.get_instance()
        self.dsn = get_pg_dsn()
        self.architect = ArchitectAgent(dsn=self.dsn)
        self.writer = WriterAgent()
        self.evaluator = EvaluatorAgent()
        self.judge = JudgeAgent()

    def generate_problem(
        self,
        target_daps: float = 13.5,
        difficulty_band: str = "MASTER",
        exam_type: str = "AIME",
        language: str = "en",
        theme_hint: str = "",
        max_loop: int = 3
    ) -> dict:
        """
        단일 문제 생성의 전체 라이프사이클을 실행합니다.
        """
        print(f"\n🚀 [Pipeline 시작] 목표 DAPS: {target_daps} ({exam_type})")

        # ── 1. 설계 (Architect) ──────────
        candidates = self.registry.get_compatible_combinations(
            target_daps=target_daps, combination_size=1, exam_type=exam_type
        ) # 우선 1개짜리 모듈로만 테스트
        
        # 만약 후보가 없으면 임시로 등록된 모든 모듈 중 첫 번째 사용 (테스트용)
        if not candidates:
            all_mods = self.registry.list_modules()
            if all_mods:
                candidates = [[all_mods[0]]]
            else:
                return {"success": False, "error": "등록된 모듈이 없습니다."}

        # 모듈 메타데이터 준비
        meta_dict = {mid: self.registry.get_module(mid).META.__dict__ 
                     for combo in candidates for mid in combo}
        
        arch_res = self.architect.run(
            candidate_combinations=candidates,
            module_metadata=meta_dict,
            target_daps=target_daps,
            difficulty_band=difficulty_band,
            exam_type=exam_type,
            language=language
        )
        
        if not arch_res.success:
            return {"success": False, "error": f"Architect 실패: {arch_res.error}"}

        blueprint_id = arch_res.output["blueprint_id"]
        selected_modules = arch_res.output["selected_modules"]
        
        # 현재는 단일 모듈에 대한 처리만 구현 (향후 조합 로직으로 확장)
        primary_module_id = selected_modules[0]
        module = self.registry.get_module(primary_module_id)
        
        # ── 2. 초기 수학적 인스턴스화 (Seed) ──────────
        seed = module.generate_seed(difficulty_hint=target_daps)
        correct_answer = module.execute(seed)
        logic_steps = module.get_logic_steps(seed)
        daps_score = module.get_daps_contribution(seed)
        
        print(f"  🧬 [수학적 DNA 생성] 모듈={primary_module_id}, 정답={correct_answer}, 예상DAPS={daps_score:.1f}")

        # ── 3. 생성-검증 루프 (Writer ↔ Evaluator ↔ Judge) ──────────
        fix_history = []
        final_variant_id = None
        mas_logs = []
        failed_step_index = None # AR-Sampling용 변수
        
        for attempt in range(1, max_loop + 1):
            print(f"\n  🔄 [Loop {attempt}/{max_loop}] 시작")
            
            # Writer 실행
            writer_res = self.writer.run_with_retry(
                seed=seed,
                logic_steps=logic_steps,
                correct_answer=correct_answer,
                module_ids=[primary_module_id],
                target_daps=target_daps,
                theme_hint=theme_hint,
                fix_history=fix_history,
                failed_step_index=failed_step_index
            )
            mas_logs.append(self._log_agent(blueprint_id, None, writer_res))
            
            if not writer_res.success:
                print(f"  ❌ Writer 생성 실패: {writer_res.error}")
                break
                
            narrative = writer_res.output["narrative"]
            
            # Evaluator 실행
            eval_res = self.evaluator.run_with_retry(
                narrative=narrative,
                expected_answer=correct_answer
            )
            mas_logs.append(self._log_agent(blueprint_id, None, eval_res))
            
            if not eval_res.success:
                print(f"  ❌ Evaluator 역추론 실패: {eval_res.error}")
                # AI 오류이므로 다시 작성 지시
                fix_history.append("검증자가 지문을 파싱하지 못했습니다. 형식을 단순화하세요.")
                continue
                
            # Judge 실행
            judge_res = self.judge.run(
                original_answer=correct_answer,
                evaluator_output=eval_res.output,
                narrative=narrative
            )
            mas_logs.append(self._log_agent(blueprint_id, None, judge_res))
            
            # 판정 결과 처리
            if judge_res.output["verdict"] == "PASS":
                print(f"\n  ✅ [통과] BEq 검증 성공! (정답: {correct_answer})")
                final_variant_id = self._save_final_variant(
                    blueprint_id=blueprint_id,
                    narrative=narrative,
                    seed=seed,
                    solution_steps=eval_res.output["steps"], # Evaluator가 푼 과정을 솔루션으로 등록
                    correct_answer=correct_answer,
                    daps_score=daps_score,
                    difficulty_band=difficulty_band,
                    exam_type=exam_type,
                    language=language
                )
                self._update_logs_variant_id(mas_logs, final_variant_id)
                self._update_blueprint_status(blueprint_id, "DONE")
                return {
                    "success": True,
                    "variant_id": final_variant_id,
                    "narrative": narrative,
                    "answer": correct_answer,
                    "daps": daps_score,
                    "logs_count": len(mas_logs)
                }
            elif judge_res.output["verdict"] == "FIX_REQUIRED":
                fix_history.append(judge_res.fix_instruction)
                # AR-Sampling: 판정 보고서에서 오류 단계 추출 (있는 경우)
                failed_step_index = judge_res.output.get("failed_step_index")
            else: # FAIL
                print("  ❌ [실패] 수정 불가능한 치명적 수학 오류 발생")
                break
                
        # ── 4. Fallback: 최대 루프 초과 시 난이도 하향 ──────────
        if attempt >= max_loop and target_daps >= 8.0:
            print(f"  ⚠️ [Circuit Breaker] 최대 루프 초과 (DAPS {target_daps:.1f}). 난이도를 낮춰 재시도합니다.")
            self._update_logs_variant_id(mas_logs, None)
            
            # DAPS를 1.5 낮추고 다시 파이프라인 호출
            new_target_daps = max(6.0, target_daps - 1.5)
            return self.generate_problem(
                target_daps=new_target_daps,
                difficulty_band=difficulty_band,
                exam_type=exam_type,
                language=language
            )

        self._update_logs_variant_id(mas_logs, None)
        self._update_blueprint_status(blueprint_id, "FAILED")
        return {"success": False, "error": "최대 재시도(Loop) 초과 또는 치명적 오류"}

    # ── DB 저장 연산 ───────────────────────────────────────────────────

    def _log_agent(self, blueprint_id: str, variant_id: int | None, res) -> int:
        """대화 로그 임시 저장 및 ID 반환 (Postgres 연결 실패 시 콘솔 출력 및 가상 ID 반환)"""
        log_data = res.to_log_dict()
        try:
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO mas_logs
                        (blueprint_id, variant_id, agent_role, agent_model, input_sent, 
                         output_received, verdict, fix_instruction, attempt_number, duration_ms)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        blueprint_id, variant_id, res.agent_role, res.agent_model,
                        log_data["input_sent"], log_data["output_received"], log_data["verdict"],
                        log_data["fix_instruction"], log_data["attempt_number"], log_data["duration_ms"]
                    ))
                    conn.commit()
                    return cursor.fetchone()[0]
        except Exception as e:
            print(f"  [DB_FALLBACK] MAS 로그 저장 실패 (PostgreSQL 미가동?): {e}")
            import random
            return random.randint(1000000, 9999999) # Return a mock ID to prevent crash

    def _update_logs_variant_id(self, log_ids: list[int], variant_id: int | None):
        """생성 완료 후 로그에 variant_id 연결 (Postgres 연결 실패 시 경고만 출력)"""
        if not log_ids: return
        try:
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE mas_logs SET variant_id = %s WHERE id = ANY(%s)
                    """, (variant_id, log_ids))
                    conn.commit()
        except Exception as e:
            print(f"  [DB_FALLBACK] 로그 variant_id 업데이트 실패: {e}")

    def _update_blueprint_status(self, blueprint_id: str, status: str):
        """블루프린트 상태 업데이트 (Postgres 연결 실패 시 경고만 출력)"""
        try:
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE blueprints SET status = %s WHERE blueprint_id = %s", (status, blueprint_id))
                    conn.commit()
        except Exception as e:
            print(f"  [DB_FALLBACK] 블루프린트 상태 업데이트 실패: {e}")

    def _save_final_variant(self, blueprint_id, narrative, seed, solution_steps, 
                            correct_answer, daps_score, difficulty_band, exam_type, language) -> int:
        """최종 결과물 저장 (Postgres 연결 실패 시 가상 ID 반환)"""
        try:
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO variants
                        (blueprint_id, mode, difficulty_band, narrative, variables_json, 
                         solution_json, correct_answer, status, exam_type, language)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        blueprint_id, "MOCK", difficulty_band, narrative,
                        json.dumps(seed, ensure_ascii=False),
                        json.dumps(solution_steps, ensure_ascii=False),
                        correct_answer, "VERIFIED", exam_type, language
                    ))
                    variant_id = cursor.fetchone()[0]
                    # daps_scores 업데이트
                    cursor.execute("""
                        INSERT INTO daps_scores (variant_id, final_daps) VALUES (%s, %s)
                    """, (variant_id, daps_score))
                    
                    conn.commit()
                    return variant_id
        except Exception as e:
            print(f"  [DB_FALLBACK] 최종 변체 저장 실패 (PostgreSQL 미가동?): {e}")
            import random
            return random.randint(1000000, 9999999) # Return a mock ID to prevent crash


if __name__ == "__main__":
    # 간단한 테스트 스크립트 실행
    from engine_v2.modules.algebra.algebra_polynomials_vieta import AlgebraPolynomialsVietaModule
    from engine_v2.modules.geometry.geometry_circles_tangency import GeometryCirclesTangencyModule
    from engine_v2.modules.number_theory.nt_power_congruence import NTPowerCongruenceModule
    from engine_v2.modules.combinatorics.comb_path_counting import CombPathCountingModule
    from engine_v2.modules.algebra.algebra_sequences_series_recurrence import AlgebraSequencesSeriesRecurrenceModule
    
    pipeline = EngineV2Pipeline()
    # 수동 모듈 등록
    pipeline.registry.register(AlgebraPolynomialsVietaModule())
    pipeline.registry.register(GeometryCirclesTangencyModule())
    pipeline.registry.register(NTPowerCongruenceModule())
    pipeline.registry.register(CombPathCountingModule())
    pipeline.registry.register(AlgebraSequencesSeriesRecurrenceModule())
    
    print("\n--- 파이프라인 단독 실행 테스트 ---")
    result = pipeline.generate_problem(target_daps=13.0)
    
    print("\n[최종 결과]")
    print(json.dumps(result, indent=2, ensure_ascii=False))
