import sqlite3
import os
import sys

# backend root 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.dirname(current_dir)
if backend_root not in sys.path:
    sys.path.append(backend_root)

from amc_engine.pipeline_manager import ProblemFactory

factory = ProblemFactory()

def repair_db():
    print("🚀 Starting Database LaTeX Repair v3...")
    db_path = factory.db_path
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Update variants table
        cursor.execute("SELECT id, narrative, solution_json FROM variants")
        rows = cursor.fetchall()
        print(f"Analyzing {len(rows)} variants...")
        
        for row_id, narrative, solution_json in rows:
            new_narrative = factory._normalize_latex(narrative)
            
            # Also normalize solution steps if they exist
            new_solution = solution_json
            if solution_json:
                try:
                    import json
                    sol_data = json.loads(solution_json)
                    if isinstance(sol_data, list):
                        sol_data = [factory._normalize_latex(s) for s in sol_data]
                    elif isinstance(sol_data, str):
                        sol_data = factory._normalize_latex(sol_data)
                    new_solution = json.dumps(sol_data)
                except Exception:
                    pass
            
            if new_narrative != narrative or new_solution != solution_json:
                cursor.execute(
                    "UPDATE variants SET narrative = ?, solution_json = ? WHERE id = ?",
                    (new_narrative, new_solution, row_id)
                )
        
        # 2. Update generated_problems table (legacy)
        cursor.execute("SELECT id, narrative, solution_steps FROM generated_problems")
        rows = cursor.fetchall()
        print(f"Analyzing {len(rows)} legacy problems...")
        
        for row_id, narrative, solution_steps in rows:
            new_narrative = factory._normalize_latex(narrative)
            new_solution = solution_steps
            if solution_steps:
                 try:
                    import json
                    sol_data = json.loads(solution_steps)
                    if isinstance(sol_data, list):
                        sol_data = [factory._normalize_latex(s) for s in sol_data]
                    new_solution = json.dumps(sol_data)
                 except Exception:
                    pass
            
            if new_narrative != narrative or new_solution != solution_steps:
                cursor.execute(
                    "UPDATE generated_problems SET narrative = ?, solution_steps = ? WHERE id = ?",
                    (new_narrative, new_solution, row_id)
                )

        conn.commit()
        print("✅ Database Repair Complete!")

if __name__ == "__main__":
    repair_db()
