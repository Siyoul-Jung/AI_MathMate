import sqlite3
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# The database is located at backend/amc_engine/amc_factory.db
db_path = os.path.join(current_dir, '..', 'amc_engine', 'amc_factory.db')

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

r = conn.execute("SELECT engine_id, narrative FROM variants WHERE engine_id LIKE '%P01' LIMIT 1").fetchone()
if r:
    print(f"Engine: {r['engine_id']}")
    print("-" * 50)
    print(r['narrative'])
else:
    print("No data found for P01.")

conn.close()
