import sqlite3
import re
import os

db_path = r'c:\AI_MathMate\backend\amc_engine\amc_factory.db'
if not os.path.exists(db_path):
    print(f"Error: {db_path} not found")
    exit(1)

def solve_hallucinations(text):
    if not text: return text
    
    # 0. Handle spaced versions (likely from user's copy-paste or renderer explanations)
    text = re.sub(r'e\s*x\s*t\s*c\s*i\s*r\s*c', 'extcirc', text)
    text = re.sub(r'r\s*i\s*a\s*n\s*g\s*l\s*e', 'riangle', text)
    text = re.sub(r'h\s*e\s*t\s*a', 'theta', text)
    text = re.sub(r'u\s*l\s*l\s*e\s*t', 'bullet', text)

    # 1. Literal replacements for common stripped degree patterns
    text = text.replace('ext{circ}', r'^\circ')
    text = text.replace('extcirc', r'^\circ')
    text = text.replace('text{circ}', r'^\circ')
    text = text.replace('textcirc', r'^\circ')
    text = text.replace(' imes', ' \\times ')
    text = text.replace('imes ', ' \\times ')

    # 2. Aggressive replacement for all degree hallucinations specifically for '60'
    text = re.sub(r'60\s*\^?(\^|\s|\\)*(\\text\{)?(circ|degree|bullet|theta|extcirc|ullet|heta)(\b|\})?\}?', r'60^\\circ', text)
    
    # 3. Aggressive 'times' replacement for specific patterns like '3 imes 3'
    text = re.sub(r'(\d)\s*im\s*e\s*s\s*(\d)', r'\1 \\times \2', text)
    
    # 4. Remove redundant \t artifacts
    text = text.replace('\\t ', ' ')
    text = re.sub(r'\\t\s*\\', r'\\', text)
    
    # 5. General cleanup for symbols missing 't' or 'b'
    text = text.replace('riangle', r'\triangle')
    text = text.replace('theta', r'\theta')
    text = text.replace('bullet', r'\bullet')
    
    return text

conn = sqlite3.connect(db_path)
c = conn.cursor()

# 1. Variants table
c.execute('SELECT id, narrative FROM variants')
rows = c.fetchall()
count = 0
for rid, narr in rows:
    new_narr = solve_hallucinations(narr)
    if new_narr != narr:
        c.execute('UPDATE variants SET narrative = ? WHERE id = ?', (new_narr, rid))
        count += 1

# 2. generated_problems table (legacy)
try:
    c.execute('SELECT id, narrative FROM generated_problems')
    rows = c.fetchall()
    for rid, narr in rows:
        new_narr = solve_hallucinations(narr)
        if new_narr != narr:
            c.execute('UPDATE generated_problems SET narrative = ? WHERE id = ?', (new_narr, rid))
            count += 1
except sqlite3.OperationalError:
    pass

conn.commit()
print(f'Updated {count} rows across all tables.')
conn.close()
