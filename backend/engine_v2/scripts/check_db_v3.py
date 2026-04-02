import sqlite3
import os

# Dead simple absolute path with forward slashes
db_path = "C:/AI_MathMate/backend/engine_v2/amc_factory_v2.db"
print(f"Checking DB: {db_path}")

if not os.path.exists(db_path):
    print("DB NOT FOUND at the expected absolute path.")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Schema
    cursor.execute("PRAGMA table_info(variants)")
    rows = cursor.fetchall()
    cols = [row['name'] for row in rows]
    print(f"Columns in 'variants' table: {cols}")

    # 2. MASTER Mode Counts
    cursor.execute("SELECT COUNT(*) as total FROM variants WHERE difficulty_band = 'MASTER'")
    total = cursor.fetchone()['total']
    
    # Check for empty problem_text
    cursor.execute("SELECT COUNT(*) as empty FROM variants WHERE difficulty_band = 'MASTER' AND (problem_text IS NULL OR problem_text = '')")
    empty = cursor.fetchone()['empty']
    
    print(f"MASTER - Total rows: {total}")
    print(f"MASTER - Empty problem_text rows: {empty}")

    # 3. Sample a valid MASTER row
    cursor.execute("SELECT * FROM variants WHERE difficulty_band = 'MASTER' AND problem_text IS NOT NULL AND problem_text != '' LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        print("\n--- SAMPLE MASTER ROW (NON-EMPTY) ---")
        for key in row.keys():
            val = row[key]
            # Truncate long text
            if isinstance(val, str) and len(val) > 80:
                val = val[:80] + "..."
            print(f"  {key}: {val}")
    else:
        print("\n[CRITICAL] No MASTER rows with non-empty problem_text found!")

    conn.close()
except Exception as e:
    print(f"DB Access Error: {e}")
