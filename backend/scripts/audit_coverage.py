import sqlite3
import os

db_path = os.path.join('amc_engine', 'amc_factory.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

print("| Engine | Verified | Rejected | Total | Success Rate |")
print("|---|---|---|---|---|")

engines = [f"P{i:02d}" for i in range(1, 16)]
for p_id in engines:
    engine_id_pattern = f"%{p_id}"
    
    verified = conn.execute("SELECT COUNT(*) FROM variants WHERE engine_id LIKE ? AND status IN ('VERIFIED', 'NONE') AND narrative IS NOT NULL", (engine_id_pattern,)).fetchone()[0]
    rejected = conn.execute("SELECT COUNT(*) FROM variants WHERE engine_id LIKE ? AND status='REJECTED'", (engine_id_pattern,)).fetchone()[0]
    
    total = verified + rejected
    if total > 0:
        rate = (verified / total) * 100
        print(f"| {p_id} | {verified} | {rejected} | {total} | {rate:.1f}% |")

conn.close()
