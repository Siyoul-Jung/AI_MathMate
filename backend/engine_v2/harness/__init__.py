"""
AI_MathMate V2 -- Pipeline Test Harness

N문제 배치 실행 -> 자동 통계 수집 -> A/B 비교 체계.

Usage:
    python -m engine_v2.harness --n 10 --daps 10.0 --tag "baseline"
    python -m engine_v2.harness --compare tag_a tag_b
"""
from engine_v2.harness.models import HarnessResult, HarnessReport
from engine_v2.harness.runner import PipelineHarness

__all__ = ["HarnessResult", "HarnessReport", "PipelineHarness"]
