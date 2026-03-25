import os
import sys
import time

# backend root 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.dirname(current_dir)
if backend_root not in sys.path:
    sys.path.append(backend_root)

from amc_engine.pipeline_manager import run_factory

# MASTER Phase 전용 생성 리스트
SOLVERS = ["P11", "P12", "P13", "P14", "P15"]
MODES = [
    ("MOCK", None),
    ("DRILL", 3) # 레벨 3 하나만 생성해둠 (속도 우선)
]
TARGET_VARIANTS = 2

def main():
    print(f"🚀 Master Phase Generation started. Target: {TARGET_VARIANTS} variants.")
    
    for p_id in SOLVERS:
        for mode, level in MODES:
            print(f"\n--- Generating {p_id} | Mode: {mode} | Level: {level} ---")
            try:
                run_factory(
                    year="2025",
                    exam="AIME1",
                    p_id=p_id,
                    target=TARGET_VARIANTS,
                    mode=mode,
                    level=level
                )
                print(f"✅ Success: {p_id} {mode}")
            except Exception as e:
                print(f"❌ Failed: {p_id} {mode}: {e}")
            
            time.sleep(1)

if __name__ == "__main__":
    main()
