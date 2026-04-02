import os
import sys
import importlib
import inspect
import io
from pathlib import Path

# backend 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# UTF-8 출력 강제 (Windows 대응)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from engine_v2.module_registry import ModuleRegistry
from engine_v2.modules.base_module import AtomicModule
from engine_v2.scripts.heritage91_inventory import ALL_HERITAGE_91

def register_91():
    registry = ModuleRegistry.get_instance()
    mod_root = os.path.join(os.path.dirname(__file__), "..", "modules")
    mod_root = os.path.abspath(mod_root)
    
    registered_count = 0
    errors = []

    print("--- Heritage 91 전수 등록 시작 (정예 리스트 기반) ---")

    for mid_target, rel_path in ALL_HERITAGE_91:
        # algebra/algebra_absolute_value.py -> algebra.algebra_absolute_value
        module_name = rel_path.replace("/", ".").replace("\\", ".").replace(".py", "")
        full_module_path = f"engine_v2.modules.{module_name}"
        
        try:
            module = importlib.import_module(full_module_path)
            # 클래스 찾기
            found_class = False
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, AtomicModule) and obj is not AtomicModule:
                    instance = obj()
                    # ID 검증 (인벤토리 ID와 파일 내 ID가 일치해야 함)
                    if instance.META.module_id == mid_target:
                        registry.register(instance)
                        registered_count += 1
                        found_class = True
                        print(f"✅ [{registered_count}/91] 등록 완료: {mid_target}")
                        break
            
            if not found_class:
                print(f"⚠️ 클래스 또는 ID 미발견: {mid_target} ({full_module_path})")
                errors.append(mid_target)
        except Exception as e:
            print(f"❌ 등록 실패: {mid_target} | 사유: {e}")
            errors.append(mid_target)

    print(f"\n[최종 결과] 등록 완료: {registered_count} / 91")
    if errors:
        print(f"⚠️ 누락된 모듈 {len(errors)}건: {errors}")
            
    registry.print_summary()

if __name__ == "__main__":
    register_91()
