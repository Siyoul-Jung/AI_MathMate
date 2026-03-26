import sys
import os
import sqlite3
import time

# amc_engine 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.dirname(current_dir)
if backend_root not in sys.path:
    sys.path.append(backend_root)

from amc_engine.pipeline_manager import ProblemFactory

def equalize_variants():
    factory = ProblemFactory()
    # Normalize path for DB
    db_path = os.path.join(backend_root, 'amc_engine', 'amc_factory.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    year = "2025"
    exam = "AIME1"
    
    # Target Configuration
    TARGET_MOCK = 10
    TARGET_DRILL = 5 # per level
    DRILL_LEVELS = [1, 2, 3]
    
    problems = [f"P{i:02d}" for i in range(1, 16)]
    
    print(f"🚀 [Equalizer] Starting AIME1 2025 Population Equalization")
    print(f"Target: Mock={TARGET_MOCK}, Drill={TARGET_DRILL}x3")
    print("=" * 60)
    
    for p_id in problems:
        engine_id = f"AIME1-{year}-{p_id}" # Fixed engine_id pattern from pipeline_manager
        
        # 1. Check Mock
        cur.execute("SELECT COUNT(*) FROM variants WHERE engine_id = ? AND mode = 'MOCK'", (engine_id,))
        current_mock = cur.fetchone()[0]
        needed_mock = TARGET_MOCK - current_mock
        
        if needed_mock > 0:
            print(f"\n--- [{p_id}] MOCK: Current={current_mock}, Need={needed_mock} ---")
            for i in range(needed_mock):
                try:
                    if factory.process_new_variant(year, exam, p_id, mode="MOCK"):
                        print(f"  ✅ MOCK {i+1}/{needed_mock} generated.")
                        time.sleep(1.5)
                except Exception as e:
                    print(f"  ❌ MOCK Error: {e}")
        
        # 2. Check Drills
        for level in DRILL_LEVELS:
            cur.execute("SELECT COUNT(*) FROM variants WHERE engine_id = ? AND mode = 'DRILL' AND drill_level = ?", (engine_id, level))
            current_drill = cur.fetchone()[0]
            needed_drill = TARGET_DRILL - current_drill
            
            if needed_drill > 0:
                print(f"\n--- [{p_id}] DRILL L{level}: Current={current_drill}, Need={needed_drill} ---")
                for i in range(needed_drill):
                    try:
                        if factory.process_new_variant(year, exam, p_id, mode="DRILL", drill_level=level):
                            print(f"  ✅ DRILL L{level} {i+1}/{needed_drill} generated.")
                            time.sleep(1.5)
                    except Exception as e:
                        print(f"  ❌ DRILL Error: {e}")

    conn.close()
    print("\n🎉 [Equalizer] Population equalization complete!")

if __name__ == "__main__":
    equalize_variants()
