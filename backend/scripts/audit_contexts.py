import os
import re

base_path = 'amc_engine/exams/2025/AIME1'
bands = ['CHALLENGER', 'EXPERT', 'MASTER']

print("| Problem | Context |")
print("|---|---|")

for b in bands:
    bp = os.path.join(base_path, b)
    if not os.path.exists(bp): continue
    for p in sorted(os.listdir(bp)):
        sp = os.path.join(bp, p, 'solver.py')
        if os.path.exists(sp):
            with open(sp, 'r', encoding='utf-8') as f:
                c = f.read()
                m = re.search(r'"context_type":\s*"(\w+)"', c)
                ctype = m.group(1) if m else "N/A"
                print(f"| {p} | {ctype} |")
