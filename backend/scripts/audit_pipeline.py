import sqlite3
import json
import os
import sys
import re

# amc_engine 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from amc_engine.pipeline_manager import ProblemFactory

def audit_database(auto_repair=False):
    factory = ProblemFactory()
    db_path = factory.db_path
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT id, engine_id, mode, narrative, variables_json, solution_json FROM variants")
    rows = cur.fetchall()

    print(f"--- 🛡️  AI MathMate Database Audit Start ({len(rows)} variants) ---")
    
    infected_ids = []
    
    for r_id, e_id, mode, narrative, v_json, s_json in rows:
        if r_id == 99: # Debug for P09
            print(f"--- FULL DEBUG ID 99 START ---")
            print(narrative)
            print(f"--- FULL DEBUG ID 99 END ---")
        issues = []
        full_text = f"{narrative} {s_json}"
        
        # 1. Check for 'reqs' or '{reqs}'
        if 'reqs' in full_text.lower() or 'req ' in full_text.lower():
            issues.append("Artifact 'reqs' found")
            
        # 2. Check for duplicated math/text pairs
        # - Duplicated numbers like "4 4"
        if re.search(r'\b(\d+)\b[\s\$]+\1\b', full_text):
            issues.append("Numerical duplication detected")
        # - Duplicated degree symbols like "120^\circ 120^\circ" or "120^\text{\circ} 120^\text{\circ}"
        if re.search(r'(\d+)\^?(?:\\text)?\{\\?circ\}[\s\$]*\1', full_text, re.IGNORECASE):
            issues.append("Degree symbol duplication detected")
        if re.search(r'circ[\s\$]*circ', full_text.lower()):
            issues.append("Mangled degree duplication detected")
            
        # - Duplicated math blocks like "$r$ $r$" or "$x^2-4$ $x^2-4$"
        if re.search(r'\$([^\$]+)\$[\s]*\$\1\$', full_text):
            issues.append("Math block duplication detected")
            
        # 3. Check for broken LaTeX (unbalanced $)
        if narrative.count('$') % 2 != 0:
            issues.append("Unbalanced LaTeX $ delimiters")
            
        # 4. Check for 'NaN' or '[object]'
        if 'nan' in narrative.lower() or '[object' in narrative.lower():
            issues.append("Uninitialized JS artifacts (NaN/Object) found")

        if issues:
            print(f"❌ [ID {r_id}] {e_id} ({mode}): {', '.join(issues)}")
            infected_ids.append((r_id, e_id, mode))

    print(f"\n--- Audit Summary: {len(infected_ids)} infected variants found ---")
    
    if auto_repair and infected_ids:
        print(f"\n⚙️  Starting Auto-Repair (Refilling infected problems)...")
        # To be safe, we categorize by engine_id and refill them
        to_refill = {}
        for r_id, e_id, mode in infected_ids:
            if e_id not in to_refill:
                to_refill[e_id] = {'MOCK': 0, 'DRILL': {1:0, 2:0, 3:0}}
            
            # Note: We don't know the exact level here easily from the query, 
            # but we can just refill the whole problem if it's infected.
            pass
        
        # Better: Just delete infected individual rows and call process_new_variant
        for r_id, e_id, mode in infected_ids:
            cur.execute("DELETE FROM variants WHERE id = ?", (r_id,))
            print(f"  🗑️  Deleted ID {r_id}")
        conn.commit()
        
        print("\n✨ Deleted bad data. You should now run the refill script for these IDs.")

    conn.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repair", action="store_true", help="Delete infected rows")
    args = parser.parse_args()
    
    # Run audit and potentially repair
    audit_database(auto_repair=args.repair)
