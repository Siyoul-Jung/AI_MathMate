import os
import shutil

def cleanup():
    mod_root = r"C:\AI_MathMate\backend\engine_v2\modules"
    backup_dir = os.path.join(mod_root, "legacy_backup")
    os.makedirs(backup_dir, exist_ok=True)

    # 정예 91개에서 제외할 13개 "Extra" 파일 리스트 (상대 경로)
    # 이 파일들은 중복이거나 실험적/레거시 파일로 분류됨
    extra_files = [
        r"algebra\algebra_cyclic_ineq_plane.py",
        r"algebra\algebra_func_periodicity.py",
        r"algebra\algebra_quadratic_lattice.py",
        r"combinatorics\comb_basic_counting.py",
        r"combinatorics\comb_constrained_arrangements.py",
        r"combinatorics\comb_distributions_partitions.py",
        r"combinatorics\comb_divisibility_perm.py",
        r"combinatorics\comb_expected_value.py",
        r"combinatorics\comb_game_theory.py",
        r"combinatorics\comb_geometric_probability.py",
        r"combinatorics\comb_graph_theory.py",
        r"combinatorics\comb_inclusion_exclusion.py",
        r"combinatorics\comb_pigeonhole_principle.py"
    ]

    print("--- 파일 시스템 정리 및 백업 시작 ---")
    moved_count = 0
    for rel_path in extra_files:
        src = os.path.join(mod_root, rel_path)
        if os.path.exists(src):
            # 대상 폴더 구조 유지
            dst_subdir = os.path.join(backup_dir, os.path.dirname(rel_path))
            os.makedirs(dst_subdir, exist_ok=True)
            dst = os.path.join(dst_subdir, os.path.basename(rel_path))
            
            shutil.move(src, dst)
            print(f"✅ 이동 완료: {rel_path} ➔ legacy_backup/{rel_path}")
            moved_count += 1
        else:
            print(f"⚠️ 파일 없음 (이미 이동됨?): {rel_path}")

    print(f"\n총 {moved_count}개 파일을 legacy_backup/으로 격리했습니다.")

if __name__ == "__main__":
    cleanup()
