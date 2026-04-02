import os
import re
from engine_v2.scripts.heritage91_inventory import ALL_HERITAGE_91

def audit():
    mod_root = r"C:\AI_MathMate\backend\engine_v2\modules"
    fs_mods = {}
    for root, dirs, files in os.walk(mod_root):
        if "__pycache__" in dirs: dirs.remove("__pycache__")
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, "r", encoding="utf-8") as f_in:
                        content = f_in.read()
                        match = re.search(r'module_id=["\'](.*?)["\']', content)
                        if match:
                            mid = match.group(1)
                            fs_mods[mid] = full_path
                except: pass

    with open("C:/AI_MathMate/backend/engine_v2/scripts/audit_result.txt", "w", encoding="utf-8") as f_out:
        f_out.write(f"FileSystem Scan: Found {len(fs_mods)} modules with IDs.\n")
        
        target_ids = {m[0] for m in ALL_HERITAGE_91}
        found_91 = [mid for mid in target_ids if mid in fs_mods]
        missing_91 = [mid for mid in target_ids if mid not in fs_mods]

        f_out.write(f"\n--- Heritage 91 Audit --- \n")
        f_out.write(f"Matched 91 Inventory: {len(found_91)} / 91\n")
        if missing_91:
            f_out.write(f"Missing IDs: {missing_91}\n")
        
        extra_ids = [mid for mid in fs_mods if mid not in target_ids]
        f_out.write(f"\nFound {len(extra_ids)} extra modules not in 91 List:\n")
        for eid in extra_ids:
            f_out.write(f" - {eid} ({os.path.relpath(fs_mods[eid], mod_root)})\n")

if __name__ == "__main__":
    audit()
