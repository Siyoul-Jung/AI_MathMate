"""
AI_MathMate V2 — 4. Python 원자 모듈 자동 생성기
`modules_master.json` 파일을 읽어들여 V2 엔진 규격(AtomicModule)에 맞는
47개의 파이썬 클래스 파일(Boilerplate)을 자동으로 생성합니다.
"""

import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
ENGINE_DIR = BASE_DIR / "engine_v2"
DATA_DIR = ENGINE_DIR / "data"
MASTER_JSON = DATA_DIR / "modules_master.json"
MODULES_DIR = ENGINE_DIR / "modules"

# 파이썬 템플릿
TEMPLATE = """\"\"\"
{name} ({module_id})
Domain: {domain}
Description: {description}
\"\"\"
from backend.engine_v2.modules.base_module import AtomicModule

class {class_name}(AtomicModule):
    def __init__(self):
        super().__init__(
            module_id="{module_id}",
            domain="{domain}",
            logic_depth={logic_depth},
            daps_contribution={daps_contribution}
        )
        # TODO: 해당 모듈의 구체적인 수학적 DNA 스키마 정의
        self.schema = {{
            "constants": [],
            "variables": []
        }}
        
    def generate_seed(self) -> dict:
        \"\"\"
        수학적으로 무결한 무작위 변수와 정답(Ground Truth)을 생성합니다.
        \"\"\"
        # TODO: SymPy 등을 이용해 정교한 시드 생성 및 파이썬 기반 정답 연산 로직 구현
        seed_data = {{
            # "k": 3,
            # "answer": 15
        }}
        return seed_data
"""

def to_pascal_case(snake_str):
    components = snake_str.split('_')
    return "".join(x.title() for x in components)

def generate_modules():
    if not MASTER_JSON.exists():
        print(f"❌ 오류: {MASTER_JSON.name} 파일이 없습니다. 3_merge_dedup.py를 먼저 실행하세요.")
        return

    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    count = 0
    for domain, modules in master_data.items():
        # 도메인별 폴더 생성 (예: modules/algebra)
        domain_dir = MODULES_DIR / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        # __init__.py 생성 (패키지화)
        (domain_dir / "__init__.py").touch(exist_ok=True)

        for mod in modules:
            module_id = mod["module_id"]
            class_name = to_pascal_case(module_id) + "Module"
            file_name = f"{module_id}.py"
            file_path = domain_dir / file_name
            
            # 파이썬 코드 문자열 포매팅
            py_code = TEMPLATE.format(
                module_id=module_id,
                domain=domain,
                name=mod.get("name", ""),
                description=mod.get("description", ""),
                logic_depth=mod.get("logic_depth", 3),
                daps_contribution=mod.get("daps_contribution", 3.0),
                class_name=class_name
            )
            
            # 파일 쓰기 (기존 파일이 있으면 덮어쓰지 않음 - 안전 장치)
            if not file_path.exists():
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(py_code)
                print(f"✅ 생성됨: {domain}/{file_name}")
                count += 1
            else:
                print(f"⏭️ 유지됨(이미존재): {domain}/{file_name}")

    print(f"\n🎉 템플릿 생성 완료! 총 {count}개의 파이썬 모듈 파일이 만들어졌습니다.")
    print("👉 `backend/engine_v2/modules/` 하위 폴더들을 확인해 보세요.")

if __name__ == "__main__":
    generate_modules()
