import sqlite3
import os

# Root of the project
BASE_DIR = r"c:\AI_MathMate"
db_path = os.path.join(BASE_DIR, "backend", "engine_v2", "amc_factory_v2.db")

print(f"Checking DB: {db_path}")

if not os.path.exists(db_path):
    print("DB NOT FOUND.")
    exit(1)

try:
    # Use URI format for Read-Only mode to avoid locks
    # On Windows, need to be careful with paths in URIs
    db_uri = f"file:{db_path.replace('\\', '/')}?mode=ro"
    conn = sqlite3.connect(db_uri, uri=True)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Schema Check
    cursor.execute("PRAGMA table_info(variants)")
    cols = [row['name'] for row in cursor.fetchall()]
    print(f"Columns: {cols}")

    # 2. MASTER Statistics
    cursor.execute("SELECT COUNT(*) as total FROM variants WHERE difficulty_band = 'MASTER'")
    total = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as empty FROM variants WHERE difficulty_band = 'MASTER' AND (problem_text IS NULL OR problem_text = '')")
    empty = cursor.fetchone()['empty']
    
    print(f"MASTER Total: {total}")
    print(f"MASTER Empty: {empty}")

    # 3. Sample Row
    cursor.execute("SELECT * FROM variants WHERE difficulty_band = 'MASTER' AND problem_text IS NOT NULL AND problem_text != '' LIMIT 1")
    row = cursor.fetchone()
    if row:
        print("\n--- SAMPLE MASTER ROW ---")
        for key in row.keys():
            val = row[key]
            # Avoid printing huge text
            if isinstance(val, str) and len(val) > 100:
                val = val[:100] + "..."
            print(f"  {key}: {val}")
    else:
        print("\nNo valid MASTER rows found with content.")

    conn.close()
except Exception as e:
    print(f"DB Error: {e}")
