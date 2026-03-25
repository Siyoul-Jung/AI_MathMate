import sqlite3
import os
import sys
import time

# amc_engine 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from amc_engine.pipeline_manager import ProblemFactory

LOCK_FILE = os.path.join(current_dir, ".refill.lock")

def prioritize_refill():
    # Force clear old lock to start fresh for user
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

    try:
        factory = ProblemFactory()
        year, exam = "2025", "AIME1"
        db_path = factory.db_path
        
        # Expert/Master targets
        p_ids = [f"P{i:02d}" for i in range(15, 5, -1)] # P15 down to P06
        
        print(f"--- 🚀 PRIORITY REFILL: {year} {exam} (EXPERT & MASTER) ---")
        
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS refill_status (engine_id TEXT PRIMARY KEY, status TEXT)")
        conn.commit()

        for p_id in p_ids:
            engine_id = f"{exam}-{year}-{p_id}"
            
            # Skip if already populated (unless forced, but here we want speed)
            cur.execute("SELECT count(*) FROM variants WHERE engine_id = ?", (engine_id,))
            if cur.fetchone()[0] >= 10:
                print(f"[{p_id}] Already populated. Skipping...")
                continue
                
            print(f"[{p_id}] Starting Priority Refill...")
            cur.execute("INSERT OR REPLACE INTO refill_status (engine_id, status) VALUES (?, ?)", (engine_id, "PROCESSING"))
            cur.execute("DELETE FROM variants WHERE engine_id = ?", (engine_id,))
            conn.commit()
            
            # Atomic Generation
            for i in range(10): # Mock
                try:
                    factory.process_new_variant(year, exam, p_id, mode="MOCK")
                    print(f"  ✅ MOCK {i+1}/10", end='\r')
                except: pass
            
            for level in [1, 2, 3]: # Drill
                for i in range(5):
                    try:
                        factory.process_new_variant(year, exam, p_id, mode="DRILL", drill_level=level)
                        print(f"  ✅ LVL{level} {i+1}/5", end='\r')
                    except: pass
            
            cur.execute("DELETE FROM refill_status WHERE engine_id = ?", (engine_id,))
            conn.commit()
            print(f"\n  ✨ {p_id} Restoration Complete.")

        conn.close()
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

if __name__ == "__main__":
    prioritize_refill()
