"""
AI_MathMate V2 — 3D Mathematical Test Harness
모든 원자 모듈(Atomic Module)을 대상으로 3차원 수학적 검증을 수행합니다.
(1차원: 타입 매칭, 2차원: 에러 방지/불변성 유지, 3차원: AIME 정답 범위 및 속도)
"""

import time
import argparse
from typing import List, Type
from collections import defaultdict

# 필요 로드 대기 (절대 경로 사용)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from engine_v2.module_registry import ModuleRegistry
from engine_v2.modules.base_module import AtomicModule

class ModuleTestHarness:
    def __init__(self, iterations_per_daps: int = 100):
        self.iterations = iterations_per_daps
        self.daps_targets = [4.0, 9.0, 14.0] # Challenge, Expert, Master 난이도 시드
        self.registry = ModuleRegistry.get_instance()

    def run_test(self, module: AtomicModule) -> dict:
        """단일 모듈에 대해 3차원 스트레스 테스트를 수행합니다."""
        print(f"\\n🧪 [Test] 모듈 검증 시작: {module.META.module_id} ({module.META.name})")
        
        results = {
            "module_id": module.META.module_id,
            "status": "PASS",
            "errors": [],
            "avg_seed_time_ms": 0.0,
            "avg_exec_time_ms": 0.0
        }

        total_seed_time = 0.0
        total_exec_time = 0.0
        total_runs = 0

        for target_daps in self.daps_targets:
            for i in range(self.iterations):
                total_runs += 1
                
                # ── 1. 시드 생성 및 시간 측정 ──
                start_time = time.perf_counter()
                try:
                    seed = module.generate_seed(difficulty_hint=target_daps)
                except Exception as e:
                    results["errors"].append(f"[DAPS {target_daps}] generate_seed 예외 발생: {e}")
                    results["status"] = "FAIL"
                    continue
                seed_time = (time.perf_counter() - start_time) * 1000
                total_seed_time += seed_time

                # ── 2. 1차원 검증: 정적 스키마(Bounds, Types) 체크 ──
                is_valid, err_msg = module.validate_seed(seed)
                if not is_valid:
                    results["errors"].append(f"[DAPS {target_daps}] 스키마 위반 (Seed: {seed}): {err_msg}")
                    results["status"] = "FAIL"
                    continue

                # ── 3. 2차원 & 3차원 검증: 연산 무결성 및 AIME 범위 ──
                start_time = time.perf_counter()
                try:
                    answer = module.execute(seed)
                except Exception as e:
                    results["errors"].append(f"[DAPS {target_daps}] execute 예외 발생 (Seed: {seed}): {e}")
                    results["status"] = "FAIL"
                    continue
                exec_time = (time.perf_counter() - start_time) * 1000
                total_exec_time += exec_time

                if not isinstance(answer, int) or not (0 <= answer <= 999):
                    results["errors"].append(f"[DAPS {target_daps}] 정답 0~999 이탈! Answer: {answer} (Seed: {seed})")
                    results["status"] = "FAIL"
                
                # 타임아웃 경고 (모듈 1개가 100ms 이상 걸리면 심각한 병목)
                if seed_time > 100.0 or exec_time > 100.0:
                    results["errors"].append(f"[DAPS {target_daps}] 타임아웃 경고! Seed 시간: {seed_time:.1f}ms, Exec 시간: {exec_time:.1f}ms")
                    results["status"] = "WARNING" if results["status"] == "PASS" else "FAIL"

        if total_runs > 0:
            results["avg_seed_time_ms"] = total_seed_time / total_runs
            results["avg_exec_time_ms"] = total_exec_time / total_runs

        self._print_results(results, total_runs)
        return results

    def _print_results(self, res: dict, runs: int):
        status_color = "✅ PASS" if res["status"] == "PASS" else ("⚠️ WARNING" if res["status"] == "WARNING" else "❌ FAIL")
        print(f"  결과: {status_color} (테스트 횟수: {runs})")
        print(f"  성능: Seed 평균 {res['avg_seed_time_ms']:.2f}ms | Exec 평균 {res['avg_exec_time_ms']:.2f}ms")
        
        if res["errors"]:
            print("  [발견된 문제점]")
            # 에러가 너무 많으면 상위 5개만 출력
            for err in res["errors"][:5]:
                print(f"    - {err}")
            if len(res["errors"]) > 5:
                print(f"    ... (외 {len(res['errors']) - 5}건의 동일 에러 생략)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AIME 3D Test Harness")
    parser.add_argument("--module_id", type=str, help="특정 모듈 ID만 테스트 (생략 시 등록된 전체 테스트)")
    parser.add_argument("--iterations", type=int, default=100, help="DAPS 난이도별 시드 생성 횟수 (기본 100)")
    args = parser.parse_args()

    # 테스트를 위한 임시 모듈 로드 (실제로는 registry가 모든 파일을 탐색하여 자동 등록해야함)
    # 현재는 수동으로 3개 정도만 올려서 테스터 가동을 확인합니다.
    try:
        from engine_v2.modules.algebra.algebra_quadratic_lattice import AlgebraQuadraticLatticeModule
        ModuleRegistry.get_instance().register(AlgebraQuadraticLatticeModule())
    except ImportError as e:
        print(f"ImportError P04: {e}")

    try:
        from engine_v2.modules.geometry.geo_parabola_rotation import GeoParabolaRotationModule
        ModuleRegistry.get_instance().register(GeoParabolaRotationModule())
    except ImportError as e:
        print(f"ImportError P09: {e}")

    try:
        from engine_v2.modules.geometry.geo_trapezoid_inscribed import GeoTrapezoidInscribedModule
        ModuleRegistry.get_instance().register(GeoTrapezoidInscribedModule())
    except ImportError as e:
        print(f"ImportError P06: {e}")

    try:
        from engine_v2.modules.algebra.algebra_cyclic_ineq_plane import AlgebraCyclicIneqPlaneModule
        ModuleRegistry.get_instance().register(AlgebraCyclicIneqPlaneModule())
    except ImportError as e:
        print(f"ImportError P12: {e}")

    try:
        from engine_v2.modules.geometry.geo_reflection_heptagon import GeoReflectionHeptagonModule
        ModuleRegistry.get_instance().register(GeoReflectionHeptagonModule())
    except ImportError as e:
        print(f"ImportError P02: {e}")

    try:
        from engine_v2.modules.combinatorics.comb_grid_sudoku_sum import CombGridSudokuSumModule
        ModuleRegistry.get_instance().register(CombGridSudokuSumModule())
    except ImportError as e:
        print(f"ImportError P10: {e}")

    try:
        from engine_v2.modules.combinatorics.comb_pairing_probability import CombPairingProbabilityModule
        ModuleRegistry.get_instance().register(CombPairingProbabilityModule())
    except ImportError as e:
        print(f"ImportError P07: {e}")

    try:
        from engine_v2.modules.combinatorics.comb_divisibility_perm import CombDivisibilityPermModule
        ModuleRegistry.get_instance().register(CombDivisibilityPermModule())
    except ImportError as e:
        print(f"ImportError P05: {e}")

    try:
        from engine_v2.modules.combinatorics.comb_multinomial_partition import CombMultinomialPartitionModule
        ModuleRegistry.get_instance().register(CombMultinomialPartitionModule())
    except ImportError as e:
        print(f"ImportError P03: {e}")

    try:
        from engine_v2.modules.number_theory.nt_base_divisibility import NTBaseDivisibilityModule
        ModuleRegistry.get_instance().register(NTBaseDivisibilityModule())
    except ImportError as e:
        print(f"ImportError NT: {e}")

    try:
        from engine_v2.modules.number_theory.nt_power_congruence import NTPowerCongruenceModule
        ModuleRegistry.get_instance().register(NTPowerCongruenceModule())
    except ImportError:
        pass

    harness = ModuleTestHarness(iterations_per_daps=args.iterations)
    registry = ModuleRegistry.get_instance()
    
    modules_to_test = []
    if args.module_id:
        mod = registry.get_module(args.module_id)
        if mod: modules_to_test.append(mod)
        else: print(f"❌ 모듈을 찾을 수 없습니다: {args.module_id}")
    else:
        # DB(Registry)에 등록된 모든 모듈
        modules_to_test = [registry.get_module(mid) for mid in registry.list_modules()]

    if not modules_to_test:
        print("⚠️ 테스트할 모듈이 하나도 등록되지 않았습니다.")
        sys.exit(1)

    fail_count = 0
    for mod in modules_to_test:
        res = harness.run_test(mod)
        if res["status"] == "FAIL":
            fail_count += 1

    print("\\n" + "="*50)
    print(f"🎯 최종 결과: 전체 {len(modules_to_test)}개 중 {fail_count}개 실패.")
    if fail_count > 0:
        sys.exit(1)
