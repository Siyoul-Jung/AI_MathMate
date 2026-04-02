import sqlite3
import os

db_path = 'backend/amc_engine/amc_factory.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("--- [MIGRATION V4 START] ---")

    # 1. Update engines table
    print("Updating 'engines' table...")
    new_engine_cols = [
        ("dna_path", "TEXT"),
        ("required_vars", "TEXT"),
        ("min_inventory", "INTEGER DEFAULT 50")
    ]
    for col_name, col_type in new_engine_cols:
        try:
            cur.execute(f"ALTER TABLE engines ADD COLUMN {col_name} {col_type}")
            print(f"  + Added column {col_name} to engines")
        except sqlite3.OperationalError:
            print(f"  . Column {col_name} already exists in engines")

    # 2. Update variants table
    print("Updating 'variants' table...")
    new_variant_cols = [
        ("status", "TEXT DEFAULT 'VERIFIED'"),
        ("raw_variables", "TEXT") # For storing the full seed JSON
    ]
    for col_name, col_type in new_variant_cols:
        try:
            cur.execute(f"ALTER TABLE variants ADD COLUMN {col_name} {col_type}")
            print(f"  + Added column {col_name} to variants")
        except sqlite3.OperationalError:
            print(f"  . Column {col_name} already exists in variants")

    # 3. Create verification_logs table
    print("Creating 'verification_logs' table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS verification_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            variant_id INTEGER,
            error_type TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (variant_id) REFERENCES variants(id)
        )
    """)
    print("  + Table verification_logs ready")

    conn.commit()
    conn.close()
    print("--- [MIGRATION V4 COMPLETE] ---")

if __name__ == "__main__":
    migrate()
