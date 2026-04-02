import sys
import os
import sqlite3
import json

# Add backend to path
sys.path.append(os.path.abspath('backend'))

from amc_engine.pipeline_manager import ProblemFactory

def test_save_to_db_v4():
    factory = ProblemFactory()
    
    # Mock data for a REJECTED variant
    p_id = "P99"
    year = 2025
    exam = "AIME1"
    seed_key = "test_key_rejected"
    perfect_seed = {"radius": 10, "expected_t": 314}
    
    print("Testing _save_to_db with REJECTED status...")
    factory._save_to_db(
        data=None, # Sparse data
        year=year,
        exam=exam,
        p_id=p_id,
        theme_name="DEBUG",
        seed_key=seed_key,
        attempt_count=1,
        mode="MOCK",
        drill_level=None,
        status='REJECTED',
        failed_stage=2,
        reason="Numerical mismatch for radius"
    )
    
    # Check DB
    conn = sqlite3.connect(factory.db_path)
    cur = conn.cursor()
    
    # Check engines
    cur.execute("SELECT dna_path FROM engines WHERE engine_id LIKE '%P99%'")
    engine = cur.fetchone()
    print(f"Engine auto-registered: {engine[0] if engine else 'NO'}")
    
    # Check variants
    cur.execute("SELECT id, status, raw_variables FROM variants WHERE seed_key=?", (seed_key,))
    variant = cur.fetchone()
    if variant:
        v_id, status, raw_vars = variant
        print(f"Variant saved: ID={v_id}, Status={status}")
        print(f"Raw variables count: {len(json.loads(raw_vars)) if raw_vars else '0'}")
        
        # Check logs
        cur.execute("SELECT error_type, details FROM verification_logs WHERE variant_id=?", (v_id,))
        log = cur.fetchone()
        if log:
            print(f"Log found: Type={log[0]}, Details={log[1]}")
        else:
            print("Error: No log found for REJECTED variant")
    else:
        print("Error: Variant not found")
        
    conn.close()

if __name__ == "__main__":
    test_save_to_db_v4()
