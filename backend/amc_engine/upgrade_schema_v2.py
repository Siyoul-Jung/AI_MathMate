import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'amc_problems.db')

def upgrade_v2():
    print(f"Upgrading database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(problems)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'problem_mode' not in columns:
            print("Adding problem_mode...")
            cursor.execute("ALTER TABLE problems ADD COLUMN problem_mode TEXT DEFAULT 'MOCK'")
            
        if 'drill_level' not in columns:
            print("Adding drill_level...")
            cursor.execute("ALTER TABLE problems ADD COLUMN drill_level INTEGER")
            
        if 'scenario_tags' not in columns:
            print("Adding scenario_tags...")
            cursor.execute("ALTER TABLE problems ADD COLUMN scenario_tags TEXT")

        conn.commit()
        print("Schema upgrade to v2 complete!")
    except Exception as e:
        print(f"Error during upgrade: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    upgrade_v2()
