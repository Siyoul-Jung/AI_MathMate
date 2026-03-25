import os
import sys
import time

# backend root 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.dirname(current_dir)
if backend_root not in sys.path:
    sys.path.append(backend_root)

from amc_engine.pipeline_manager import run_factory

# MASTER Phase 부족한 부분 채우기
SOLVERS = ["P12", "P13", "P14", "P15"]
MODES = [
    ("MOCK", None),
    ("DRILL", 3)
]
TARGET_VARIANTS = 3

def main():
    print(f"🚀 FINAL Master Phase Restoration started.")
    
    for p_id in SOLVERS:
        for mode, level in MODES:
            print(f"\n--- [Restoring] {p_id} {mode} L{level} ---")
            try:
                run_factory(
                    year="2025",
                    exam="AIME1",
                    p_id=p_id,
                    target=TARGET_VARIANTS,
                    mode=mode,
                    level=level
                )
            except Exception as e:
                print(f"❌ Error in {p_id}: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
