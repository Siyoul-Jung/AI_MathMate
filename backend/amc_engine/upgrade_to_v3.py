import sqlite3
import os
import sys
import json
import importlib.util

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "amc_factory.db")
exams_dir = os.path.join(current_dir, "exams")

def get_engine_id(year, exam, p_id):
    return f"{exam}-{year}-{p_id}"

def load_solver_class(solver_path):
    spec = importlib.util.spec_from_file_location("solver_module", solver_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, 'Solver')

def upgrade():
    print(f"🚀 Starting migration to V3 schema on {db_path}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Create new tables
    print("Creating new tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS engines (
            engine_id TEXT PRIMARY KEY,
            dna_tag TEXT,
            category TEXT,
            difficulty_band TEXT,
            has_image_support BOOLEAN,
            reference_note TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            engine_id TEXT,
            mode TEXT,
            drill_level INTEGER,
            drill_focus TEXT,
            narrative TEXT,
            variables_json TEXT,
            solution_json TEXT,
            correct_answer TEXT,
            theme_name TEXT,
            image_url TEXT,
            seed_key TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (engine_id) REFERENCES engines(engine_id)
        )
    """)
    
    # 2. Populate 'engines' table by scanning filesystem
    print("Registering engines from solvers...")
    # Walk through exams/2025/AIME1/
    aime_2025_dir = os.path.join(exams_dir, "2025", "AIME1")
    if os.path.exists(aime_2025_dir):
        for band in os.listdir(aime_2025_dir):
            band_path = os.path.join(aime_2025_dir, band)
            if not os.path.isdir(band_path): continue
            
            for p_id in os.listdir(band_path):
                p_path = os.path.join(band_path, p_id)
                solver_file = os.path.join(p_path, "solver.py")
                if os.path.exists(solver_file):
                    try:
                        Solver = load_solver_class(solver_file)
                        dna = getattr(Solver, 'DNA', {})
                        engine_id = get_engine_id("2025", "AIME1", p_id)
                        
                        cursor.execute("""
                            INSERT OR REPLACE INTO engines 
                            (engine_id, dna_tag, category, difficulty_band, has_image_support, reference_note)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            engine_id,
                            dna.get('specific_tag', dna.get('core_concept', 'UNKNOWN')),
                            dna.get('category', 'Math'),
                            getattr(Solver, 'DIFFICULTY_BAND', 'MASTER'),
                            dna.get('has_image', False),
                            f"Inspired by AIME 2025 I {p_id}"
                        ))
                        print(f"  - Registered engine: {engine_id}")
                    except Exception as e:
                        print(f"  - Error loading solver {p_id}: {e}")

    # 3. Migrate existing data from generated_problems to variants
    print("Migrating records from 'generated_problems' to 'variants'...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='generated_problems'")
    if cursor.fetchone():
        cursor.execute("""
            SELECT exam_year, exam_type, problem_num, narrative, variables, 
                   solution_steps, correct_answer, theme, seed_key, problem_mode, drill_level 
            FROM generated_problems
        """)
        old_records = cursor.fetchall()
        
        migrated_count = 0
        for rec in old_records:
            year, exam, p_id, narrative, var_json, sol_json, ans, theme, seed, mode, drill_lvl = rec
            engine_id = get_engine_id(year, exam, p_id)
            
            # Check if engine exists (some old records might point to engines we haven't scanned yet)
            cursor.execute("SELECT 1 FROM engines WHERE engine_id = ?", (engine_id,))
            if not cursor.fetchone():
                # Create a placeholder engine if not found
                cursor.execute("INSERT OR IGNORE INTO engines (engine_id, category) VALUES (?, ?)", (engine_id, 'Generic'))
            
            cursor.execute("""
                INSERT INTO variants 
                (engine_id, mode, drill_level, narrative, variables_json, solution_json, correct_answer, theme_name, seed_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                engine_id, mode, drill_lvl, narrative, var_json, sol_json, str(ans), theme, seed
            ))
            migrated_count += 1
        
        print(f"  - Migrated {migrated_count} records.")
    else:
        print("  - 'generated_problems' table not found. Skipping data migration.")

    conn.commit()
    conn.close()
    print("✅ V3 Migration Complete!")

if __name__ == "__main__":
    upgrade()
