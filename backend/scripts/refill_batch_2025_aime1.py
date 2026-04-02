import os
import sys
import sqlite3
import time

# Add backend to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from amc_engine.pipeline_manager import ProblemFactory

def refill_aime1_2025():
    factory = ProblemFactory()
    db_path = factory.db_path
    
    print("\n" + "="*50)
    print("💎 [AIME1 2025 SYSTEMIC REFILL] Logic-Driven Protocol")
    print("="*50)
    
    print("\n--- 🗑️  Clearing Database Variants ---")
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM variants")
        conn.commit()
    print("✨ Database cleared.")

    # P01 to P15
    engines = [f"P{i:02d}" for i in range(1, 16)]
    year, exam = "2025", "AIME1"

    total_success = 0
    start_time = time.time()

    for p_id in engines:
        print(f"\n🚀 [Refilling {p_id}] Stage: Anchor & Analyze")
        
        # 1. First Mock + Analysis (The "Anchor" for pedagogy)
        anchor_variant = factory.process_new_variant(year, exam, p_id, mode="MOCK")
        if not anchor_variant:
            print(f"  ❌ Failed to generate anchor Mock for {p_id}. Skipping engine.")
            continue
        
        total_success += 1
        explanation = anchor_variant.get('5_solution', {}).get('step_by_step', '')
        steps = factory.analyze_logic_steps(explanation)
        
        print(f"  ↳ Found {len(steps)} logical bridges.")
        
        # 2. Generate Dynamic Drills based on isolated logic steps (Analysis-First)
        num_drills = len(steps)
        print(f"  ↳ Synthesis: Generating {num_drills} Isolated Drills (Dynamic)...")
        for i, step in enumerate(steps):
            if i >= 5: break # Safety cap to prevent logic-bloat
            if factory.process_new_variant(year, exam, p_id, mode="DRILL", drill_level=(i+1), drill_intent=step):
                total_success += 1
            time.sleep(1)

        # 3. Generate remaining 9 Mocks
        print(f"  ↳ Volume: Generating 9 more Mock variants...")
        for j in range(2, 11): # We already did 1st
            if factory.process_new_variant(year, exam, p_id, mode="MOCK"):
                total_success += 1
            time.sleep(1)

    elapsed = time.time() - start_time
    print("\n" + "="*50)
    print(f"✅ REFILL COMPLETE!")
    print(f"📊 Total Variants Ingested: {total_success}")
    print(f"⏱️  Time Elapsed: {elapsed/60:.1f} minutes")
    print("="*50)

if __name__ == "__main__":
    refill_aime1_2025()
