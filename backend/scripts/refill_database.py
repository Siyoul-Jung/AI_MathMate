import sys
import os
import sqlite3

# amc_engine 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from amc_engine.pipeline_manager import ProblemFactory

def refill_database():
    factory = ProblemFactory()
    db_path = 'amc_engine/amc_factory.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    year = "2025"
    exam = "AIME1"
    
    tasks = [
        # (p_id, mode, level, target_count)
        ("P02", "DRILL", 1, 5),
        ("P02", "DRILL", 2, 5),
        ("P03", "DRILL", 1, 5),
        ("P03", "DRILL", 2, 5),
        ("P10", "MOCK", None, 10),
        ("P14", "DRILL", 1, 5),
    ]
    
    for p_id, mode, level, target in tasks:
        engine_id = f"{exam}-{year}-{p_id}"
        # count current
        if mode == "MOCK":
            cur.execute("SELECT COUNT(*) FROM variants WHERE engine_id = ? AND mode = 'MOCK'", (engine_id,))
        else:
            cur.execute("SELECT COUNT(*) FROM variants WHERE engine_id = ? AND mode = 'DRILL' AND drill_level = ?", (engine_id, level))
        
        current_count = cur.fetchone()[0]
        needed = target - current_count
        
        if needed > 0:
            print(f"--- Refilling {p_id} ({mode} L{level if level else 'N/A'}) : Need {needed} ---")
            for i in range(needed):
                try:
                    res = factory.process_new_variant(year, exam, p_id, mode=mode, drill_level=level)
                    if res:
                        print(f"  [{p_id}] Variant {i+1}/{needed} generated.")
                    else:
                        print(f"  [{p_id}] Variant {i+1}/{needed} failed.")
                except Exception as e:
                    print(f"  [{p_id}] Variant {i+1}/{needed} error: {e}")
        else:
            print(f"--- {p_id} ({mode} L{level if level else 'N/A'}) already has {current_count} variants. ---")
            
    conn.close()

if __name__ == "__main__":
    refill_database()
