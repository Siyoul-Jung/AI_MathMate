"""Harness 리포트 — 콘솔 출력, JSON 저장, A/B 비교."""
from __future__ import annotations
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from engine_v2.harness.config import RESULTS_DIR
from engine_v2.harness.models import HarnessReport


def print_summary(r: HarnessReport) -> None:
    """리포트를 콘솔에 출력합니다."""
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  HARNESS REPORT: {r.run_tag}")
    print(sep)
    print(f"  Runs: {r.total_runs}")
    print(f"  Writer: {r.config.get('writer_model', '?')}")
    print(f"  Target DAPS: {r.config.get('target_daps', '?')}")
    print(f"\n  --- Pass Rates ---")
    print(f"  BEq Pass:              {r.beq_pass_rate:.1%}")
    print(f"  Novelty Pass:          {r.novelty_pass_rate:.1%}")
    print(f"  Overall Success:       {r.overall_success_rate:.1%}")
    print(f"\n  --- DAPS ---")
    print(f"  Measured Mean:         {r.daps_measured_mean} +/- {r.daps_measured_std}")
    print(f"  Deviation Mean:        {r.daps_deviation_mean}")
    print(f"  delta Distribution:    {r.delta_distribution}")
    print(f"  Confidence:            {r.confidence_distribution}")
    print(f"\n  --- Quality ---")
    print(f"  Technique Concealment: {r.technique_concealment_rate:.1%}")
    print(f"  Bridge Usage:          {r.bridge_usage_rate:.1%}")
    print(f"\n  --- Performance ---")
    print(f"  Avg Duration:          {r.avg_duration_ms/1000:.1f}s")
    print(f"  Avg Writer Attempts:   {r.avg_writer_attempts}")
    print(f"  Avg LLM Calls:         {r.avg_llm_calls}")
    print(f"\n  --- Top Modules ---")
    for m, c in list(r.module_frequency.items())[:5]:
        print(f"    {m}: {c}x")
    print(sep)


def save_report(report: HarnessReport, tag: str) -> Path:
    """리포트를 JSON 파일로 저장합니다."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = RESULTS_DIR / f"{tag}_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, ensure_ascii=False, indent=2, default=str)
    print(f"  Saved: {path}")
    return path


def compare(tag_a: str, tag_b: str) -> None:
    """두 태그의 가장 최근 결과를 비교합니다."""
    def _load_latest(tag: str) -> dict | None:
        files = sorted(RESULTS_DIR.glob(f"{tag}_*.json"), reverse=True)
        if not files:
            print(f"  No results found for tag: {tag}")
            return None
        with open(files[0], encoding="utf-8") as f:
            return json.load(f)

    a = _load_latest(tag_a)
    b = _load_latest(tag_b)
    if not a or not b:
        return

    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  A/B COMPARISON")
    print(sep)
    print(f"  {'Metric':<30} {'[A] ' + tag_a:<20} {'[B] ' + tag_b:<20} {'Delta'}")
    print(f"  {'─'*80}")

    def _row(label: str, key: str, fmt: str = ".1%", higher_better: bool = True):
        va = a.get(key, 0)
        vb = b.get(key, 0)
        delta = vb - va
        arrow = ""
        if delta > 0:
            arrow = " ^" if higher_better else " v"
        elif delta < 0:
            arrow = " v" if higher_better else " ^"
        print(f"  {label:<30} {va:{fmt}:<20} {vb:{fmt}:<20} {delta:+{fmt}}{arrow}")

    _row("BEq Pass Rate", "beq_pass_rate")
    _row("Overall Success", "overall_success_rate")
    _row("Technique Concealment", "technique_concealment_rate")
    _row("Bridge Usage", "bridge_usage_rate")
    _row("DAPS Mean", "daps_measured_mean", ".1f")
    _row("DAPS Std", "daps_measured_std", ".1f", False)
    _row("Avg Duration (ms)", "avg_duration_ms", ".0f", False)
    _row("Avg Writer Attempts", "avg_writer_attempts", ".1f", False)
    _row("Avg LLM Calls", "avg_llm_calls", ".1f", False)

    print(f"\n  delta Distribution:")
    print(f"    [A]: {a.get('delta_distribution', {})}")
    print(f"    [B]: {b.get('delta_distribution', {})}")
    print(f"\n  Confidence Distribution:")
    print(f"    [A]: {a.get('confidence_distribution', {})}")
    print(f"    [B]: {b.get('confidence_distribution', {})}")
    print(sep)
