import sqlite3
import os
import re
import shutil

DB_PATH = r'c:\AI_MathMate\amc_engine\amc_factory.db'
IMAGES_DIR = r'c:\AI_MathMate\amc_engine\images'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all generated problems
cursor.execute('SELECT id, narrative, exam_year, exam_type FROM generated_problems')
rows = cursor.fetchall()

modified_count = 0
for row_id, narrative, year, exam in rows:
    if not narrative: continue
    # Target images/P11_xxxxx.png or similar
    new_data = re.sub(r'images/(P\d+_[a-f0-9a-zA-Z]+)\.png', f'images/{year}/{exam}/\\1.png', narrative)
    if new_data != narrative:
        cursor.execute('UPDATE generated_problems SET narrative = ? WHERE id = ?', (new_data, row_id))
        modified_count += 1

conn.commit()
conn.close()

# Now move the actual files
files_moved = 0
if os.path.exists(IMAGES_DIR):
    for filename in os.listdir(IMAGES_DIR):
        if filename.endswith('.png'):
            target_dir = os.path.join(IMAGES_DIR, '2025', 'AIME1') # Currently all images are 2025 AIME1
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(os.path.join(IMAGES_DIR, filename), os.path.join(target_dir, filename))
            files_moved += 1
        
print(f'Migration complete! DB rows updated: {modified_count}, Files moved: {files_moved}')
