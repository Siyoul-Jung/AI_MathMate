import sqlite3
import os
import sys

# amc_engine 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from amc_engine.pipeline_manager import ProblemFactory

def refill_p06():
    factory = ProblemFactory()
    year, exam, p_id = "2025", "AIME1", "P06"
    
    conn = sqlite3.connect('amc_engine/amc_factory.db')
    cur = conn.cursor()
    
    print(f"--- Deleting existing P06 variants ---")
    cur.execute("DELETE FROM variants WHERE engine_id = ?", ("AIME1-2025-P06",))
    conn.commit()
    conn.close()
    
    print(f"--- Refilling P06 (MOCK mode, 10 variants) ---")
    for i in range(10):
        print(f"Generating Mock {i+1}/10...")
        factory.process_new_variant(year, exam, p_id, mode="MOCK")
    
    print(f"--- Refilling P06 (DRILL mode, 5 each) ---")
    for level in [1, 2, 3]:
        for i in range(5):
            print(f"Generating Drill LV{level} {i+1}/5...")
            factory.process_new_variant(year, exam, p_id, mode="DRILL", drill_level=level)

if __name__ == "__main__":
    refill_p06()
