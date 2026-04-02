import os
import sys

# Add backend root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.dirname(current_dir)
if backend_root not in sys.path:
    sys.path.append(backend_root)

from amc_engine.pipeline_manager import run_factory

def main():
    # Problems for 'New System' Testing (Narrative/Generalized)
    targets = [
        {"year": "2025", "exam": "AIME1", "pid": "P03", "count": 10},
        {"year": "2025", "exam": "AIME1", "pid": "P07", "count": 10},
        {"year": "2025", "exam": "AIME1", "pid": "P13", "count": 10},
        {"year": "2025", "exam": "AIME1", "pid": "P14", "count": 10},
    ]
    
    print("🚀 Starting Focused Narrative Generation Test (P03 & P14)")
    print("=" * 60)
    
    for target in targets:
        pid = target["pid"]
        year = target["year"]
        exam = target["exam"]
        count = target["count"]
        mode = "MOCK"
        
        print(f"\n📦 Testing {year} {exam} {pid} | Variants: {count}")
        try:
            run_factory(
                year=year,
                exam=exam,
                p_id=pid,
                target=count,
                mode=mode
            )
            print(f"✅ Batch completed for {pid}")
        except Exception as e:
            print(f"❌ Error during generation for {pid}: {e}")

if __name__ == "__main__":
    main()
