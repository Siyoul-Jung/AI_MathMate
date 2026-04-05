"""CLI 진입점: python -m engine_v2.harness"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from engine_v2.harness.runner import PipelineHarness
from engine_v2.harness.reporter import print_summary, save_report, compare


def main():
    parser = argparse.ArgumentParser(description="AI_MathMate V2 Pipeline Test Harness")
    parser.add_argument("--n", type=int, default=10, help="Number of problems to generate")
    parser.add_argument("--daps", type=float, default=10.0, help="Target DAPS")
    parser.add_argument("--writer", type=str, default=None, help="Writer model override")
    parser.add_argument("--max-loop", type=int, default=3, help="Max BEq retry loops")
    parser.add_argument("--tag", type=str, default="", help="Run tag for identification")
    parser.add_argument("--compare", nargs=2, metavar=("TAG_A", "TAG_B"), help="Compare two runs")
    parser.add_argument("--no-narratives", action="store_true", help="Don't save narratives")

    args = parser.parse_args()

    if args.compare:
        compare(args.compare[0], args.compare[1])
    else:
        harness = PipelineHarness()
        report = harness.run_batch(
            n=args.n,
            target_daps=args.daps,
            writer_model=args.writer,
            max_loop=args.max_loop,
            save_narratives=not args.no_narratives,
            tag=args.tag,
        )
        print_summary(report)
        save_report(report, report.run_tag)


if __name__ == "__main__":
    main()
