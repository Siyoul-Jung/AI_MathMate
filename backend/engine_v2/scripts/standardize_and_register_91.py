import os
import sys
import importlib
import inspect
import io
import re
import sqlite3
from pathlib import Path

# backend 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# UTF-8 출력 강제
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from engine_v2.module_registry import ModuleRegistry
from engine_v2.modules.base_module import AtomicModule, ModuleMeta
from engine_v2.scripts.heritage91_inventory import ALL_HERITAGE_91

def standardize_and_register():
    registry = ModuleRegistry.get_instance()
    mod_root = os.path.join(os.path.dirname(__file__), "..", "modules")
    mod_root = os.path.abspath(mod_root)
    
    success_count = 0
    
    print("--- Heritage 91 Surgical Fix & Registration 시작 ---")

    for mid_target, rel_path in ALL_HERITAGE_91:
        full_path = os.path.join(mod_root, rel_path)
        if not os.path.exists(full_path):
            print(f"❌ 파일 없음: {rel_path}")
            continue

        # 1. 파일 내용 표준화 (Surgical Fix)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            # ModuleMeta 임포트 확인 및 추가
            if "ModuleMeta" not in content:
                content = content.replace("from backend.engine_v2.modules.base_module import AtomicModule", 
                                       "from engine_v2.modules.base_module import AtomicModule, ModuleMeta")
                content = content.replace("from engine_v2.modules.base_module import AtomicModule", 
                                       "from engine_v2.modules.base_module import AtomicModule, ModuleMeta")

            # 구형 super().__init__ 구조를 new self.META 구조로 변경 (정규표현식)
            # (매우 단순화된 패턴 매칭 - 실제로는 더 복잡할 수 있으나 91개에 대해 최적화)
            if "self.META =" not in content and "super().__init__" in content:
                # 대략적인 변환 로직 (module_id, domain 등을 추출하여 ModuleMeta로 재구성)
                # 여기서는 안전을 위해 파일 내용을 직접 덮어쓰기보다, 
                # 인벤토리의 정보를 바탕으로 META를 강제 주입하는 동적 등록 방식을 먼저 시도합니다.
                pass

            # 2. 동적 로딩 및 강제 등록
            # 파일 경로로부터 모듈명 생성
            module_name = rel_path.replace("/", ".").replace("\\", ".").replace(".py", "")
            full_module_path = f"engine_v2.modules.{module_name}"
            
            # 모듈 캐시 삭제 후 재로드
            if full_module_path in sys.modules:
                del sys.modules[full_module_path]
            
            module = importlib.import_module(full_module_path)
            
            # 클래스 찾기 및 META 주입
            found_class = False
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, AtomicModule) and obj is not AtomicModule:
                    instance = obj()
                    
                    # [V2 수술] META가 없거나 ID가 다르면 강제 보정
                    if not hasattr(instance, "META") or instance.META.module_id != mid_target:
                        # 한글 이름 유추 (파일명 기반 또는 기존 이름)
                        korean_name = mid_target.replace("_", " ").title() # 기본값
                        domain = "algebra" # 기본값
                        if "geometry" in rel_path or "geo" in mid_target: domain = "geometry"
                        if "number_theory" in rel_path or "nt_" in mid_target: domain = "number_theory"
                        if "combinatorics" in rel_path or "comb_" in mid_target: domain = "combinatorics"
                        if "meta" in rel_path: domain = "meta"

                        instance.META = ModuleMeta(
                            module_id=mid_target,
                            name=korean_name,
                            domain=domain,
                            logic_depth=3,
                            daps_contribution=3.0
                        )
                    
                    # 레지스트리 등록
                    registry.register(instance)
                    success_count += 1
                    found_class = True
                    print(f"✅ [{success_count}/91] 등록 완료: {mid_target}")
                    break
            
            if not found_class:
                print(f"⚠️ 클래스 미발견: {mid_target}")

        except Exception as e:
            print(f"❌ 처리 실패: {mid_target} | 사유: {e}")

    print(f"\n--- 최종 결과 ---")
    print(f"목표: 91 | 성공: {success_count}")
    
    # DB 최종 확인
    conn = sqlite3.connect(os.path.join(os.path.dirname(mod_root), "amc_factory_v2.db"))
    final_db_count = conn.execute("SELECT COUNT(*) FROM modules").fetchone()[0]
    print(f"DB 등록 수: {final_db_count}")
    conn.close()

if __name__ == "__main__":
    standardize_and_register()
