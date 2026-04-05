"""
AI_MathMate V2 — 85개 모듈 일괄 등록 스크립트
파일시스템 디스커버리 → domain 검증 → DB 초기화 → 순차 등록 (호환성 + Bridge 자동 탐지)

Usage:
    cd c:/AI_MathMate/backend
    python -m engine_v2.scripts.register_all_85
"""
from __future__ import annotations
import sys
import importlib
import inspect
import time
from pathlib import Path

# backend 디렉토리를 sys.path에 추가
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from engine_v2.modules.base_module import AtomicModule
from engine_v2.module_registry import ModuleRegistry

VALID_DOMAINS = {"integer", "real", "complex"}
MODULE_DIRS = ["algebra", "geometry", "number_theory", "combinatorics", "meta"]


def discover_modules() -> list[tuple[str, AtomicModule]]:
    """modules/ 하위 디렉토리에서 AtomicModule 서브클래스를 자동 탐지."""
    modules_base = BACKEND_DIR / "engine_v2" / "modules"
    discovered: list[tuple[str, AtomicModule]] = []

    for category in MODULE_DIRS:
        cat_dir = modules_base / category
        if not cat_dir.is_dir():
            print(f"  [SKIP] 디렉토리 없음: {cat_dir}")
            continue

        for py_file in sorted(cat_dir.glob("*.py")):
            if py_file.name.startswith("__"):
                continue

            module_path = f"engine_v2.modules.{category}.{py_file.stem}"
            try:
                mod = importlib.import_module(module_path)
                for attr_name in dir(mod):
                    obj = getattr(mod, attr_name)
                    if (isinstance(obj, type)
                            and issubclass(obj, AtomicModule)
                            and obj is not AtomicModule
                            and hasattr(obj, "META")):
                        instance = obj()
                        discovered.append((category, instance))
            except Exception as e:
                print(f"  [ERR] {module_path}: {e}")

    return discovered


def validate_domains(modules: list[tuple[str, AtomicModule]]) -> list[str]:
    """domain 필드가 유효한지 사전 검증. 잘못된 모듈 ID 목록 반환."""
    bad = []
    for category, inst in modules:
        d = inst.META.domain
        if d not in VALID_DOMAINS:
            bad.append(f"{inst.META.module_id} (domain='{d}')")
    return bad


def main():
    print("=" * 60)
    print(" AI_MathMate V2 — Module Registry 일괄 등록")
    print("=" * 60)

    # 1. 디스커버리
    print("\n[1/5] 모듈 디스커버리...")
    modules = discover_modules()
    print(f"  발견: {len(modules)}개")
    for cat in MODULE_DIRS:
        count = sum(1 for c, _ in modules if c == cat)
        if count > 0:
            print(f"    {cat}: {count}")

    # 2. domain 검증
    print("\n[2/5] domain 필드 검증...")
    bad = validate_domains(modules)
    if bad:
        print(f"  [FAIL] {len(bad)}개 모듈의 domain이 잘못됨:")
        for b in bad:
            print(f"    - {b}")
        print("  → 먼저 domain 필드를 수정하세요. 중단합니다.")
        sys.exit(1)
    print("  모든 domain 유효 ✓")

    # 3. DB 초기화
    print("\n[3/5] DB 초기화 (stale 데이터 삭제)...")
    registry = ModuleRegistry.get_instance()
    registry.reset_db()
    print(f"  DB 경로: {registry.db_path}")
    print("  4개 테이블 클리어 완료 ✓")

    # 4. 순차 등록 + 호환성 테스트
    print(f"\n[4/5] {len(modules)}개 모듈 등록 시작...")
    start = time.time()
    success = 0
    fail = 0

    for i, (category, inst) in enumerate(modules, 1):
        mid = inst.META.module_id
        try:
            result = registry.register(inst)
            if result.get("registered"):
                compat = result.get("compatibility_results", {})
                n_compat = sum(1 for v in compat.values() if v == "COMPATIBLE")
                n_total = len(compat)
                bridge_info = f" bridge" if inst.META.bridge_output_keys else ""
                print(f"  [{i:2d}/{len(modules)}] ✓ {mid} ({n_compat}/{n_total} compat{bridge_info})")
                success += 1
            else:
                print(f"  [{i:2d}/{len(modules)}] ✗ {mid}: 등록 실패")
                fail += 1
        except Exception as e:
            print(f"  [{i:2d}/{len(modules)}] ✗ {mid}: {e}")
            fail += 1

    elapsed = time.time() - start

    # 5. 최종 리포트
    print("\n[5/5] 최종 리포트")
    print("=" * 60)
    print(f"  등록: {success}/{success + fail}")
    print(f"  소요: {elapsed:.1f}초")

    # DB 통계 조회
    import sqlite3
    with sqlite3.connect(registry.db_path) as conn:
        n_modules = conn.execute("SELECT COUNT(*) FROM modules").fetchone()[0]
        compat_stats = conn.execute(
            "SELECT status, COUNT(*) FROM module_compatibility GROUP BY status"
        ).fetchall()
        n_bridges = conn.execute(
            "SELECT COUNT(*) FROM module_bridge_connections"
        ).fetchone()[0]

        # 도메인 분포
        domain_dist = conn.execute(
            "SELECT domain, COUNT(*) FROM modules GROUP BY domain"
        ).fetchall()

        # 카테고리 분포
        cat_dist = conn.execute(
            "SELECT category, COUNT(*) FROM modules GROUP BY category"
        ).fetchall()

    print(f"\n  DB 모듈 수: {n_modules}")
    print(f"  카테고리별: {dict(cat_dist)}")
    print(f"  도메인별: {dict(domain_dist)}")
    print(f"\n  호환성 테스트:")
    for status, count in compat_stats:
        print(f"    {status}: {count}")
    print(f"\n  Bridge 연결: {n_bridges}")
    print("=" * 60)


if __name__ == "__main__":
    main()
