import os
import re

def deep_audit():
    mod_root = r"C:\AI_MathMate\backend\engine_v2\modules"
    all_metadata = []
    
    for root, dirs, files in os.walk(mod_root):
        if "__pycache__" in dirs: dirs.remove("__pycache__")
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, mod_root)
                try:
                    with open(full_path, "r", encoding="utf-8") as f_in:
                        content = f_in.read()
                        mid = re.search(r'module_id=["\'](.*?)["\']', content)
                        name = re.search(r'name=["\'](.*?)["\']', content)
                        domain = re.search(r'domain=["\'](.*?)["\']', content)
                        
                        all_metadata.append({
                            "mid": mid.group(1) if mid else "N/A",
                            "name": name.group(1) if name else "N/A",
                            "domain": domain.group(1) if domain else "N/A",
                            "path": rel_path
                        })
                except: pass

    # 결과를 파일로 저장
    with open("C:/AI_MathMate/backend/engine_v2/scripts/deep_audit_result.txt", "w", encoding="utf-8") as f_out:
        for m in sorted(all_metadata, key=lambda x: (x['domain'], x['mid'])):
            f_out.write(f"[{m['domain']}] ID: {m['mid']} | Name: {m['name']} | Path: {m['path']}\n")

if __name__ == "__main__":
    deep_audit()
