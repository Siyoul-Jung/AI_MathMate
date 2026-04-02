import os
import sys
import importlib
import inspect
import sqlite3
import io
from pathlib import Path

# backend 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# UTF-8 출력 강제 (Windows 대응)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from engine_v2.module_registry import ModuleRegistry
from engine_v2.modules.base_module import AtomicModule

def final_folder_register():
    registry = ModuleRegistry.get_instance()
    mod_root = os.path.join(os.path.dirname(__file__), "..", "modules")
    mod_root = os.path.abspath(mod_root)
    
    count = 0
    print("--- Heritage 91 폴더 기반 전수 등록 시작 ---")

    for root, dirs, files in os.walk(mod_root):
        if "legacy_backup" in root or "__pycache__" in root: continue
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                rel = os.path.relpath(os.path.join(root, f), mod_root)
                module_name = f"engine_v2.modules.{rel.replace(os.sep, '.').replace('.py', '')}"
                
                try:
                    if module_name in sys.modules: del sys.modules[module_name]
                    m = importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(m):
                        if inspect.isclass(obj) and issubclass(obj, AtomicModule) and obj is not AtomicModule:
                            registry.register(obj())
                            count += 1
                            print(f"✅ [{count}] 등록 성공: {module_name}")
                            break # 파일당 하나
                except Exception as e:
                    print(f"❌ [{f}] 등록 실패 | 사유: {e}")

    print(f"\n[최종 결과] 폴더 내 등록 총계: {count}")
    
    # DB 카운트 확인
    db_path = os.path.join(mod_root, "..", "amc_factory_v2.db")
    conn = sqlite3.connect(db_path)
    db_count = conn.execute("SELECT COUNT(*) FROM modules").fetchone()[0]
    print(f"DB 저장 총계: {db_count}")
    conn.close()

if __name__ == "__main__":
    final_folder_register()
