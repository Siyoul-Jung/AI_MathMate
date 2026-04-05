"""
AI_MathMate V2 — 메인 파이프라인 매니저
Architect ➔ Module ➔ Writer ➔ Evaluator ➔ Judge 에 이르는 전체 MAS 루프를 관장합니다.
"""

from __future__ import annotations
import json
try:
    import psycopg2
except ImportError:
    psycopg2 = None  # PostgreSQL 미사용 시 graceful fallback
import time
from pathlib import Path

from engine_v2.config import PIPELINE, get_pg_dsn, USE_POSTGRES
from engine_v2.module_registry import ModuleRegistry
from engine_v2.agents.architect import ArchitectAgent
from engine_v2.agents.writer import WriterAgent
from engine_v2.agents.evaluator import EvaluatorAgent
from engine_v2.agents.judge import JudgeAgent
from engine_v2.agents.novelty_checker import NoveltyChecker


class EngineV2Pipeline:
    """V2 문항 생성 및 이중 검증 파이프라인 총괄"""

    def __init__(self):
        self.registry = ModuleRegistry.get_instance()
        self.dsn = get_pg_dsn()
        self.architect = ArchitectAgent(dsn=self.dsn)
        self.writer = WriterAgent()
        self.evaluator = EvaluatorAgent()
        self.judge = JudgeAgent()
        self.novelty_checker = NoveltyChecker()

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

        # ── 1. 설계 (Architect) ── 2-Track 조합 샘플링 ──────────
        from engine_v2.config import COMBINATION_SAMPLING
        from engine_v2.co_occurrence_matrix import CoOccurrenceMatrix

        combo_size = 3 if target_daps >= 13.0 else (2 if target_daps >= 10.0 else 1)
        exploitation_ratio = COMBINATION_SAMPLING.get("exploitation_ratio", 0.80)

        # Track A: 기출 기반 Jaccard 강화 composite_score 정렬
        candidates = self.registry.get_compatible_combinations(
            target_daps=target_daps, combination_size=combo_size, exam_type=exam_type
        )

        # Track B: 마르코프 Random Walk 탐색 (combo_size >= 2일 때만)
        if combo_size >= 2:
            import random as _rnd
            _matrix = CoOccurrenceMatrix()
            if not _matrix.load_from_db():
                _matrix.build_from_problem_map()
            track_b = _matrix.markov_sample(
                target_daps=target_daps,
                combo_size=combo_size,
                n_samples=max(3, int(len(candidates) * (1 - exploitation_ratio))),
            )
            # Track B 후보를 뒤에 추가 (Track A가 우선)
            for tb in track_b:
                if tb not in candidates:
                    candidates.append(tb)
            print(f"  📊 Track A: {len(candidates) - len(track_b)}개, Track B: {len(track_b)}개")

        # 만약 후보가 없으면 폴백
        if not candidates:
            all_mods = self.registry.list_modules()
            if all_mods:
                candidates = [[all_mods[0]]]
            else:
                return {"success": False, "error": "등록된 모듈이 없습니다."}

        # Bridge가 있는 조합을 우선 선별 → Top-K만 Architect에게 전달
        TOP_K = 20
        if combo_size >= 2:
            bridge_candidates = [
                c for c in candidates
                if any(
                    self.registry.get_bridge_connection(c[i], c[i+1])
                    or self.registry.get_bridge_connection(c[i+1], c[i])
                    for i in range(len(c) - 1)
                )
            ]
            if len(bridge_candidates) >= 5:
                print(f"  🔗 Bridge 후보 {len(bridge_candidates)}개 발견 → Bridge 우선 선택")
                candidates = bridge_candidates
        candidates = candidates[:TOP_K]

        # 모듈 메타데이터 준비 (Architect에 필요한 필드만 경량 전달)
        meta_dict = {}
        for combo in candidates:
            for mid in combo:
                if mid not in meta_dict:
                    mod = self.registry.get_module(mid)
                    if mod:
                        meta_dict[mid] = {
                            "name": mod.META.name,
                            "category": mod.META.category,
                            "tags": mod.META.tags,
                            "daps_contribution": mod.META.daps_contribution,
                            "logic_depth": mod.META.logic_depth,
                            "bridge_output_keys": mod.META.bridge_output_keys,
                            "bridge_input_accepts": mod.META.bridge_input_accepts,
                        }

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
        
        # ── 2. 수학적 인스턴스화 — Bridge Chain 우선, 폴백 시 additive ──────────
        seed = {}
        correct_answer = 0
        all_logic_steps = []
        daps_score = 0.0

        # 최적 실행 순서 탐색 (Bridge 연결 최대화)
        ordered_modules = self.registry.find_best_chain(selected_modules)

        # Bridge 체이닝 시도 (2모듈 이상, 인접 쌍에 bridge가 있을 때)
        bridge_used = False
        MAX_SEED_RETRIES = 3
        if len(ordered_modules) >= 2:
            for _seed_try in range(MAX_SEED_RETRIES + 1):
                chain_seeds: list[dict] = []
                chain_bridges: list[dict] = []
                chain_valid = True
                current_bridge: dict = {}
                seed = {}
                daps_score = 0.0
                bridge_used = False

                for i, mid in enumerate(ordered_modules):
                    module = self.registry.get_module(mid)
                    if i == 0:
                        m_seed = module.generate_seed(difficulty_hint=target_daps * 0.5)
                    else:
                        # 이전 모듈에서 bridge가 내려왔으면 활용
                        m_seed = module.generate_seed_with_bridge(
                            current_bridge, difficulty_hint=target_daps
                        )

                    chain_seeds.append(m_seed)
                    bridge_out = module.get_bridge_output(m_seed)
                    chain_bridges.append(bridge_out)
                    current_bridge = bridge_out  # 다음 모듈로 전달

                    # 마지막 모듈이면 execute()로 최종 정답 계산
                    if i == len(ordered_modules) - 1:
                        m_ans = module.execute(m_seed)
                        if isinstance(m_ans, dict):
                            m_ans = next(
                                (v for v in m_ans.values() if isinstance(v, (int, float))), 0
                            )
                        correct_answer = int(m_ans) % 1000

                    # 연결 체크: 이전 bridge → 현재 bridge_input_accepts 교집합
                    if i > 0:
                        prev_bridge = chain_bridges[i - 1]
                        shared_keys = set(prev_bridge.keys()) & set(module.META.bridge_input_accepts)
                        if shared_keys:
                            bridge_used = True

                    seed.update(m_seed)
                    daps_score += module.get_daps_contribution(m_seed)

                # Seed quality filter: reject trivial/invalid answers
                if correct_answer >= 1:
                    break
                if _seed_try < MAX_SEED_RETRIES:
                    print(f"  ⚠️  [Seed Quality] answer={correct_answer} (trivial/invalid), 재생성 시도 {_seed_try + 1}/{MAX_SEED_RETRIES}")
                else:
                    return {"success": False, "error": f"Seed quality: answer={correct_answer} after {MAX_SEED_RETRIES} retries"}

            # Logic Steps: 모듈 체인을 Bridge 설명과 함께 엮음
            for i, mid in enumerate(ordered_modules):
                module = self.registry.get_module(mid)
                all_logic_steps.extend(module.get_logic_steps(chain_seeds[i]))
                if i < len(ordered_modules) - 1:
                    next_mid = ordered_modules[i + 1]
                    bridge_keys = self.registry.get_bridge_connection(mid, next_mid)
                    if bridge_keys:
                        all_logic_steps.append(
                            f"[Bridge: {bridge_keys}] {mid}의 결과를 {next_mid}의 구조적 파라미터로 연결합니다."
                        )

            # ── Branch B: 터미널 모듈의 SymPy 독립 검증 ──────────────────────
            terminal_module = self.registry.get_module(ordered_modules[-1])
            terminal_seed = chain_seeds[-1]
            sympy_answer = terminal_module.verify_with_sympy(terminal_seed)

            if sympy_answer is not None:
                if sympy_answer != correct_answer:
                    print(f"  ❌ [Branch B] SymPy 검증 실패: Python={correct_answer}, SymPy={sympy_answer}")
                    print(f"     → 시드 폐기. 모듈 로직 버그 또는 부동소수점 오류 의심.")
                    return {"success": False, "error": f"[Branch B] SymPy 불일치: Python={correct_answer}, SymPy={sympy_answer}"}
                print(f"  ✅ [Branch B] SymPy 검증 통과: {sympy_answer}")
            else:
                print(f"  ⏭️  [Branch B] {terminal_module.META.module_id}: verify_with_sympy() 미구현 — 스킵")

            if bridge_used:
                print(f"  🔗 [Bridge Chain] {' → '.join(ordered_modules)}, 정답={correct_answer}, 합산DAPS={daps_score:.1f}")
            else:
                print(f"  ⚠️  [No Bridge] 모듈 조합에 수학적 연결 없음. Bridge 인터페이스 구현을 권장합니다.")
                print(f"  🧬 [수학적 DNA 생성] 모듈={ordered_modules}, 정답={correct_answer}, 합산DAPS={daps_score:.1f}")

        else:
            # 단일 모듈
            mid = ordered_modules[0]
            module = self.registry.get_module(mid)
            for _seed_try in range(MAX_SEED_RETRIES + 1):
                m_seed = module.generate_seed(difficulty_hint=target_daps)
                m_ans = module.execute(m_seed)
                if isinstance(m_ans, dict):
                    m_ans = next((v for v in m_ans.values() if isinstance(v, (int, float))), 0)
                correct_answer = int(m_ans) % 1000
                # Seed quality filter: reject trivial/invalid answers
                if correct_answer >= 1:
                    break
                if _seed_try < MAX_SEED_RETRIES:
                    print(f"  ⚠️  [Seed Quality] answer={correct_answer} (trivial/invalid), 재생성 시도 {_seed_try + 1}/{MAX_SEED_RETRIES}")
                else:
                    return {"success": False, "error": f"Seed quality: answer={correct_answer} after {MAX_SEED_RETRIES} retries"}
            seed.update(m_seed)
            all_logic_steps.extend(module.get_logic_steps(m_seed))
            daps_score += module.get_daps_contribution(m_seed)
            print(f"  🧬 [단일 모듈] {mid}, 정답={correct_answer}, DAPS={daps_score:.1f}")

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
                logic_steps=all_logic_steps,
                correct_answer=correct_answer,
                module_ids=selected_modules,
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
                # ── DAPS 사후 측정: Evaluator 풀이 데이터로 실제 난이도 역산 ──
                measured = self.judge.measure_daps(
                    evaluator_output=eval_res.output,
                    module_count=len(ordered_modules),
                    estimated_daps=daps_score,
                )
                measured_daps = measured["measured_daps"]
                deviation = measured["deviation"]
                band = measured["difficulty_band"]

                print(f"\n  ✅ [통과] BEq 검증 성공! (정답: {correct_answer})")
                print(f"  📊 [DAPS 사후 측정] 측정={measured_daps} (추정={daps_score:.1f}, 편차={deviation:+.1f})")
                print(f"     α={measured['alpha_computational']} β={measured['beta_logical_depth']} "
                      f"γ={measured['gamma_combination']} δ={measured['delta_heuristic']} → {band}")

                # ── Novelty Check: 기존 문제와의 중복 검사 ──────────────
                module_tags = {}
                for mid in ordered_modules:
                    mod = self.registry.get_module(mid)
                    if mod:
                        module_tags[mid] = getattr(mod.META, 'tags', [])

                novelty = self.novelty_checker.check(
                    narrative=narrative,
                    module_ids=ordered_modules,
                    module_tags=module_tags,
                )

                if not novelty["novel"]:
                    print(f"  ⚠️  [Novelty FAIL] {novelty['reason']}")
                    print(f"     가장 유사: variant #{novelty['most_similar_id']} "
                          f"(구조={novelty['structural_max_sim']:.3f}, 텍스트={novelty['textual_max_sim']:.3f})")
                    # 중복이면 저장하지 않고 재시도 — fix_history에 "다른 서술 방식" 요청
                    fix_history.append(
                        f"이전 문제(#{novelty['most_similar_id']})와 너무 유사합니다. "
                        f"완전히 다른 시나리오·서술 방식을 사용하세요."
                    )
                    continue
                else:
                    print(f"  🆕 [Novelty PASS] 참신한 문제 "
                          f"(구조={novelty['structural_max_sim']:.3f}, 텍스트={novelty['textual_max_sim']:.3f})")

                final_variant_id = self._save_final_variant(
                    blueprint_id=blueprint_id,
                    narrative=narrative,
                    seed=seed,
                    solution_steps=eval_res.output["steps"],
                    correct_answer=correct_answer,
                    daps_score=measured_daps,  # 사후 측정값을 저장
                    difficulty_band=difficulty_band,
                    exam_type=exam_type,
                    language=language
                )
                self._update_logs_variant_id(mas_logs, final_variant_id)
                self._update_blueprint_status(blueprint_id, "DONE")
                # 피드백 루프: PASS 이력 기록 → 시너지 계수 자동 진화
                self.registry.record_outcome(
                    module_ids=ordered_modules,
                    estimated_daps=daps_score,
                    measured_daps=measured_daps,
                    verdict="PASS",
                    attempt_count=attempt,
                )
                return {
                    "success": True,
                    "variant_id": final_variant_id,
                    "narrative": narrative,
                    "answer": correct_answer,
                    "daps_estimated": round(daps_score, 2),
                    "daps_measured": measured_daps,
                    "daps_detail": measured,
                    "novelty": novelty,
                    "logs_count": len(mas_logs),
                    # Harness 메트릭용 추가 필드
                    "selected_modules": ordered_modules,
                    "bridge_used": bridge_used,
                    "evaluator_confidence": eval_res.output.get("confidence", ""),
                    "evaluator_answer": eval_res.output.get("extracted_answer"),
                    "writer_attempts": writer_res.attempt_number,
                    "evaluator_attempts": eval_res.attempt_number,
                    "loop_iteration": attempt,
                }
            elif judge_res.output["verdict"] == "FIX_REQUIRED":
                fix_history.append(judge_res.fix_instruction)
                failed_step_index = judge_res.output.get("failed_step_index")
                # 피드백 루프: FIX_REQUIRED 이력 기록
                self.registry.record_outcome(
                    module_ids=ordered_modules,
                    estimated_daps=daps_score,
                    measured_daps=None,
                    verdict="FIX_REQUIRED",
                    fail_reason="WRITER_LOOP",
                    attempt_count=attempt,
                )
            else:  # FAIL
                print("  ❌ [실패] 수정 불가능한 치명적 수학 오류 발생")
                # 피드백 루프: FAIL 이력 기록 (감점 -30)
                self.registry.record_outcome(
                    module_ids=ordered_modules,
                    estimated_daps=daps_score,
                    measured_daps=None,
                    verdict="FAIL",
                    fail_reason="MATH_ERROR",
                    attempt_count=attempt,
                )
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
        if not USE_POSTGRES:
            # print(f"  [Skip] USE_POSTGRES=False, 로그 저장 생략")
            import random
            return random.randint(1000000, 9999999)
        
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
        if not USE_POSTGRES or not log_ids: return
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
        if not USE_POSTGRES: return
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
        if not USE_POSTGRES:
            # PostgreSQL 저장 스킵 (SQLite는 호출부인 pre_generate_v2 에서 수행됨)
            import random
            return random.randint(1000000, 9999999)

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
