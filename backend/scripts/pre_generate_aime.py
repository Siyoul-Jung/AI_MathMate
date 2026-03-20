# backend root 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.dirname(current_dir)
if backend_root not in sys.path:
    sys.path.append(backend_root)

from amc_engine.pipeline_manager import run_factory

# 설정
SOLVERS = ["P01", "P10", "P11", "P12", "P13", "P14", "P15"]
MODES = [
    ("MOCK", None),
    ("DRILL", 1),
    ("DRILL", 2),
    ("DRILL", 3)
]
TARGET_VARIANTS = 2 # 테스트를 위해 적게 설정 (실제로는 5~10 권장)

def main():
    print(f"🚀 AIME DB Pre-generation started. Target: {TARGET_VARIANTS} variants per type.")
    
    for p_id in SOLVERS:
        for mode, level in MODES:
            print(f"\n--- Generating {p_id} | Mode: {mode} | Level: {level} ---")
            try:
                # run_factory 는 내부적으로 process_new_variant 를 반복 호출하고 DB에 저장함
                run_factory(
                    year="2025",
                    exam="AIME1",
                    p_id=p_id,
                    target=TARGET_VARIANTS,
                    mode=mode,
                    level=level
                )
                print(f"✅ Finished {p_id} {mode} L{level}")
            except Exception as e:
                print(f"❌ Failed {p_id} {mode} L{level}: {e}")
            
            # OpenAI Rate Limit 방지 및 안정성
            time.sleep(1)

if __name__ == "__main__":
    main()
