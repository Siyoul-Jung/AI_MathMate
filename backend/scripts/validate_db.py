import sqlite3
import re
import os
import json

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'amc_engine', 'amc_factory.db')

def validate_latex(text):
    """Checks for balanced braces and structural LaTeX integrity."""
    errors = []
    if not text: return errors
    
    # 1. Brace check
    if text.count('{') != text.count('}'):
        errors.append(f"Unbalanced braces {{}}: {text.count('{')} vs {text.count('}')}")
    
    # 2. Math delimiter check
    if text.count('$') % 2 != 0:
        errors.append("Unbalanced math delimiters $")
    
    # 3. Environment check
    env_starts = re.findall(r'\\begin\{(.*?)\}', text)
    env_ends = re.findall(r'\\end\{(.*?)\}', text)
    if len(env_starts) != len(env_ends):
        errors.append(f"Unbalanced environments: begin={len(env_starts)}, end={len(env_ends)}")
    
    return errors

def audit_db():
    print(f"🔍 Starting Database Audit: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("❌ Database not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, engine_id, mode, drill_level, narrative, image_url FROM variants")
    rows = cursor.fetchall()

    print(f"📊 Total Variants to Scan: {len(rows)}")
    print("-" * 60)

    issue_count = 0
    figure_keywords = ['figure', 'graph', 'diagram', 'triangle', 'circle', 'parabola', 'coordinate plane', 'plot']

    for row in rows:
        vid = row['id']
        p_id = row['engine_id']
        narrative = row['narrative']
        img_url = row['image_url']
        
        errors = validate_latex(narrative)
        
        # Check for missing images
        mentions_figure = any(kw in narrative.lower() for kw in figure_keywords)
        if mentions_figure and not img_url:
            errors.append("MISSING FIGURE: Text mentions figure but image_url is empty")
        
        if errors:
            issue_count += 1
            mode_str = f"({row['mode']} L{row['drill_level']})" if row['mode'] == 'DRILL' else f"({row['mode']})"
            print(f"❌ Valid ID {vid} | {p_id} {mode_str}:")
            for err in errors:
                print(f"   - {err}")
            print("-" * 40)

    conn.close()
    
    print("\n" + "=" * 60)
    print(f"✅ Audit Complete.")
    print(f"   - Total Scanned: {len(rows)}")
    print(f"   - Issues Found: {issue_count}")
    if issue_count == 0:
        print("   - Result: CLEAN ✨")
    else:
        print(f"   - Result: NEEDS ATTENTION ({issue_count} issues)")
    print("=" * 60)

if __name__ == "__main__":
    audit_db()
