import os
import sqlite3
import re

def find_missing():
    mod_root = r"C:\AI_MathMate\backend\engine_v2\modules"
    db = r"C:\AI_MathMate\backend\engine_v2\amc_factory_v2.db"
    
    conn = sqlite3.connect(db)
    registered = {row[0] for row in conn.execute("SELECT module_id FROM modules")}
    conn.close()
    
    missing = []
    for root, dirs, files in os.walk(mod_root):
        if "legacy_backup" in root or "__pycache__" in root: continue
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                p = os.path.join(root, f)
                try:
                    with open(p, "r", encoding="utf-8") as fin:
                        content = fin.read()
                        # Match both single and double quotes
                        m = re.search(r'module_id=["\'](.*?)["\']', content)
                        if m:
                            mid = m.group(1)
                            if mid not in registered:
                                missing.append((mid, p))
                        else:
                            missing.append(("NO_ID_FOUND", p))
                except:
                    pass
    
    print(f"Total files in modules/: {len(missing) + len(registered)}")
    print(f"Registered: {len(registered)}")
    print(f"Missing: {len(missing)}")
    for mid, path in missing:
        print(f"MISSING|{mid}|{path}")

if __name__ == "__main__":
    find_missing()
