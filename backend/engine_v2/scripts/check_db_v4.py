import sqlite3
import os

db_path = "C:/AI_MathMate/backend/engine_v2/amc_factory_v2.db"
print(f"Checking DB: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Get ALL columns
    cursor.execute("PRAGMA table_info(variants)")
    rows = cursor.fetchall()
    cols = [row['name'] for row in rows]
    print(f"ACTUAL COLUMNS in 'variants' table: {cols}")

    # 2. Check for common alternatives to 'problem_text'
    # we'll look for any column containing 'text', 'content', 'problem', 'question', 'narrative'
    suspects = [c for c in cols if any(x in c.lower() for x in ['text', 'content', 'problem', 'question', 'narrative'])]
    print(f"Potential content columns: {suspects}")

    # 3. MASTER Mode Status
    cursor.execute("SELECT COUNT(*) as total FROM variants WHERE difficulty_band = 'MASTER'")
    total = cursor.fetchone()['total']
    print(f"MASTER Total rows: {total}")

    # 4. Sample a row to see the data
    if total > 0:
        cursor.execute("SELECT * FROM variants WHERE difficulty_band = 'MASTER' LIMIT 1")
        row = cursor.fetchone()
        print("\n--- MASTER ROW DATA (ALL FIELDS) ---")
        for k in row.keys():
            v = row[k]
            if isinstance(v, str) and len(v) > 100:
                v = v[:100] + "..."
            print(f"  {k}: {v}")
    
    conn.close()
except Exception as e:
    print(f"Script Error: {e}")
