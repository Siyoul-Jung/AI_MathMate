import sqlite3
import json

db_path = r'c:\AI_MathMate\amc_engine\amc_factory.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, exam_year, exam_type, problem_num, problem_mode, drill_level, theme FROM generated_problems WHERE problem_num = 'P01' AND problem_mode = 'DRILL'")
rows = cursor.fetchall()

print(f"Found {len(rows)} P01 DRILL problems:")
for row in rows:
    print(row)

conn.close()
