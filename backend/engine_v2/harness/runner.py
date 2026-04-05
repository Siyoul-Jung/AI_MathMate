"""Harness 실행 엔진 — 배치 문제 생성 + 메트릭 수집."""
from __future__ import annotations
import importlib
import time
import uuid
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from engine_v2.harness.config import TECHNIQUE_WORDS
from engine_v2.harness.models import HarnessResult, HarnessReport


class PipelineHarness:
    """파이프라인 배치 실행 + 통계 수집 + A/B 비교."""

    def __init__(self):
        self.pipeline = None

    def _ensure_pipeline(self) -> None:
        """파이프라인 + 85개 모듈 메모리 로드 (1회)."""
        if self.pipeline is not None:
            return
        from engine_v2.pipeline_v2 import EngineV2Pipeline
        from engine_v2.modules.base_module import AtomicModule

        self.pipeline = EngineV2Pipeline()
        for d in ["algebra", "geometry", "number_theory", "combinatorics", "meta"]:
            modules_dir = Path(__file__).parent.parent / "modules" / d
            for py in modules_dir.glob("*.py"):
                if py.name.startswith("__"):
                    continue
                try:
                    mod = importlib.import_module(f"engine_v2.modules.{d}.{py.stem}")
                    for attr in dir(mod):
                        obj = getattr(mod, attr)
                        if (isinstance(obj, type)
                                and issubclass(obj, AtomicModule)
                                and obj is not AtomicModule
                                and hasattr(obj, "META")):
                            inst = obj()
                            self.pipeline.registry._modules[inst.META.module_id] = inst
                except Exception:
                    pass
        print(f"Harness: {len(self.pipeline.registry._modules)} modules loaded")

    @staticmethod
    def check_technique_concealment(narrative: str) -> tuple[bool, list[str]]:
        """기법 이름이 지문에 노출되었는지 검사."""
        if not narrative:
            return True, []
        lower = narrative.lower()
        exposed = [t for t in TECHNIQUE_WORDS if t in lower]
        return len(exposed) == 0, exposed

    def _extract_result(
        self, raw: dict, target_daps: float, writer_model: str, duration_ms: int
    ) -> HarnessResult:
        """pipeline.generate_problem() 반환값에서 HarnessResult 추출."""
        r = HarnessResult(
            run_id=str(uuid.uuid4())[:8],
            timestamp=datetime.now().isoformat(),
            target_daps=target_daps,
            writer_model=writer_model,
            success=raw.get("success", False),
            error=raw.get("error", ""),
            selected_modules=raw.get("selected_modules", []),
            bridge_used=raw.get("bridge_used", False),
            correct_answer=raw.get("answer"),
            evaluator_answer=raw.get("evaluator_answer"),
            daps_estimated=raw.get("daps_estimated"),
            daps_measured=raw.get("daps_measured"),
            writer_attempts=raw.get("writer_attempts", 0),
            evaluator_attempts=raw.get("evaluator_attempts", 0),
            loop_count=raw.get("loop_iteration", 0),
            total_duration_ms=duration_ms,
            narrative=raw.get("narrative"),
            evaluator_confidence=raw.get("evaluator_confidence", ""),
        )

        # DAPS 상세
        detail = raw.get("daps_detail", {})
        if detail:
            r.daps_alpha = detail.get("alpha_computational")
            r.daps_beta = detail.get("beta_logical_depth")
            r.daps_gamma = detail.get("gamma_combination")
            r.daps_delta = detail.get("delta_heuristic")
            r.difficulty_band = detail.get("difficulty_band")

        # Novelty
        novelty = raw.get("novelty", {})
        if novelty:
            r.novelty_pass = novelty.get("novel")
            r.novelty_structural_sim = novelty.get("structural_max_sim")
            r.novelty_textual_sim = novelty.get("textual_max_sim")

        # BEq verdict
        r.beq_verdict = "PASS" if raw.get("success") else "FAIL"

        # 기법 은폐
        concealed, exposed = self.check_technique_concealment(raw.get("narrative", ""))
        r.technique_concealment = concealed
        r.exposed_techniques = exposed

        # combo_size
        r.combo_size = len(r.selected_modules) if r.selected_modules else 0

        return r

    # ── 메인 실행 ───────────────────────────────────────────────

    def run_batch(
        self,
        n: int = 10,
        target_daps: float = 10.0,
        writer_model: str | None = None,
        max_loop: int = 3,
        save_narratives: bool = True,
        tag: str = "",
    ) -> HarnessReport:
        """N문제를 배치 실행하고 통계를 수집합니다."""
        from engine_v2 import config

        self._ensure_pipeline()

        # Writer 모델 임시 교체
        original_model = config.MODELS["writer"]
        if writer_model:
            config.MODELS["writer"] = writer_model
            self.pipeline.writer.model_name = writer_model
        effective_model = config.MODELS["writer"]

        if not tag:
            tag = f"{effective_model.replace('-', '')}_{target_daps:.0f}"

        conf = {
            "writer_model": effective_model,
            "target_daps": target_daps,
            "max_loop": max_loop,
            "n": n,
        }

        sep = "=" * 60
        print(f"\n{sep}")
        print(f"  HARNESS: {n} problems | DAPS={target_daps} | Writer={effective_model}")
        print(f"  Tag: {tag}")
        print(sep)

        results: list[HarnessResult] = []

        for i in range(n):
            print(f"\n{'─'*50}")
            print(f"  [{i+1}/{n}] Generating...")
            print(f"{'─'*50}")

            t0 = time.time()
            try:
                raw = self.pipeline.generate_problem(
                    target_daps=target_daps,
                    difficulty_band="EXPERT" if target_daps < 13 else "MASTER",
                    exam_type="AIME",
                    language="en",
                    max_loop=max_loop,
                )
            except Exception as e:
                raw = {"success": False, "error": str(e)}
            duration = int((time.time() - t0) * 1000)

            hr = self._extract_result(raw, target_daps, effective_model, duration)
            if not save_narratives:
                hr.narrative = None
            results.append(hr)

            status = "PASS" if hr.success else "FAIL"
            print(f"  -> [{status}] ans={hr.correct_answer} dur={duration/1000:.1f}s bridge={hr.bridge_used}")

        # 모델 복원
        config.MODELS["writer"] = original_model

        # 집계
        report = self._aggregate(results, tag, conf)
        return report

    @staticmethod
    def _aggregate(results: list[HarnessResult], tag: str, config: dict) -> HarnessReport:
        """개별 결과를 집계."""
        n = len(results)
        if n == 0:
            return HarnessReport(run_tag=tag, config=config)

        passes = [r for r in results if r.success]
        n_pass = len(passes)

        # DAPS 통계
        daps_vals = [r.daps_measured for r in passes if r.daps_measured is not None]
        daps_mean = sum(daps_vals) / len(daps_vals) if daps_vals else 0.0
        daps_std = (sum((v - daps_mean) ** 2 for v in daps_vals) / len(daps_vals)) ** 0.5 if len(daps_vals) > 1 else 0.0
        dev_vals = [
            (r.daps_measured - r.daps_estimated)
            for r in passes
            if r.daps_measured is not None and r.daps_estimated is not None
        ]
        dev_mean = sum(dev_vals) / len(dev_vals) if dev_vals else 0.0

        # delta 분포
        delta_dist: dict[str, int] = {}
        for r in passes:
            if r.daps_delta is not None:
                k = str(r.daps_delta)
                delta_dist[k] = delta_dist.get(k, 0) + 1

        # confidence 분포
        conf_dist: dict[str, int] = {}
        for r in results:
            if r.evaluator_confidence:
                conf_dist[r.evaluator_confidence] = conf_dist.get(r.evaluator_confidence, 0) + 1

        # 모듈 빈도
        mod_freq: dict[str, int] = {}
        for r in results:
            for m in r.selected_modules:
                mod_freq[m] = mod_freq.get(m, 0) + 1

        # Bridge, 기법 은폐, Novelty
        bridge_count = sum(1 for r in results if r.bridge_used)
        conceal_count = sum(1 for r in passes if r.technique_concealment)
        novelty_passes = [r for r in passes if r.novelty_pass is True]

        # 성능
        durations = [r.total_duration_ms for r in results]
        w_attempts = [r.writer_attempts for r in results if r.writer_attempts > 0]
        llm_calls = [r.writer_attempts + r.evaluator_attempts for r in results]

        return HarnessReport(
            run_tag=tag,
            total_runs=n,
            config=config,
            beq_pass_rate=n_pass / n if n else 0,
            novelty_pass_rate=len(novelty_passes) / n_pass if n_pass else 0,
            overall_success_rate=n_pass / n if n else 0,
            daps_measured_mean=round(daps_mean, 2),
            daps_measured_std=round(daps_std, 2),
            daps_deviation_mean=round(dev_mean, 2),
            delta_distribution=delta_dist,
            confidence_distribution=conf_dist,
            bridge_usage_rate=bridge_count / n if n else 0,
            module_frequency=dict(sorted(mod_freq.items(), key=lambda x: -x[1])[:15]),
            technique_concealment_rate=conceal_count / n_pass if n_pass else 0,
            avg_duration_ms=round(sum(durations) / n) if n else 0,
            avg_writer_attempts=round(sum(w_attempts) / len(w_attempts), 1) if w_attempts else 0,
            avg_llm_calls=round(sum(llm_calls) / n, 1) if n else 0,
            results=[asdict(r) for r in results],
        )
