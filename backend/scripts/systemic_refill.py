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

def systemic_refill_2025_aime1():
    # 1. Singleton Guard
    has_lock = False
    if os.path.exists(LOCK_FILE):
        try:
            pid_old = int(open(LOCK_FILE, 'r').read().strip())
            # Check if process is still alive (psutil would be better, but this is basic)
            import psutil
            if psutil.pid_exists(pid_old):
                print(f"⚠️ 이미 다른 리필 프로세스(PID {pid_old})가 실행 중입니다.")
                return
        except:
            pass

    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))
    has_lock = True

    try:
        factory = ProblemFactory()
        year, exam = "2025", "AIME1"
        db_path = factory.db_path
        
        # 2. Status Table Setup
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS refill_status (engine_id TEXT PRIMARY KEY, status TEXT)")
        cur.execute("DELETE FROM refill_status") # Clear old status
        conn.commit()
        
        # We target P01 to P15
        p_ids = [f"P{i:02d}" for i in range(1, 16)]
        
        print(f"--- 🚀 SYSTEMIC SMART REFILL: {year} {exam} ---")
        
        for p_id in p_ids:
            engine_id = f"{exam}-{year}-{p_id}"
            print(f"[{p_id}] Starting Atomic Refill...")
            
            # Status: PROCESSING
            cur.execute("INSERT OR REPLACE INTO refill_status (engine_id, status) VALUES (?, ?)", (engine_id, "PROCESSING"))
            conn.commit()
            
            # 3. Atomic Delete
            cur.execute("DELETE FROM variants WHERE engine_id = ?", (engine_id,))
            conn.commit()
            
            # 4. Generation Loop
            success_mock = 0
            for i in range(10):
                try:
                    if factory.process_new_variant(year, exam, p_id, mode="MOCK"):
                        success_mock += 1
                        print(f"  ✅ MOCK {success_mock}/10 saved.", end='\r')
                    time.sleep(0.5)
                except Exception as e:
                    print(f"\n  ⚠️ MOCK Exception: {e}")
            
            for level in [1, 2, 3]:
                success_drill = 0
                for i in range(5):
                    try:
                        if factory.process_new_variant(year, exam, p_id, mode="DRILL", drill_level=level):
                            success_drill += 1
                            print(f"  ✅ LVL{level} {success_drill}/5 saved.", end='\r')
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"\n  ⚠️ DRILL LV{level} Exception: {e}")
            
            # Status: COMPLETE
            cur.execute("DELETE FROM refill_status WHERE engine_id = ?", (engine_id,))
            conn.commit()
            print(f"\n  ✨ {p_id} Refill Complete.")

        print(f"\n--- 🎉 ALL MISSIONS REFILLED ---")
    
    finally:
        if has_lock and os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

if __name__ == "__main__":
    systemic_refill_2025_aime1()
