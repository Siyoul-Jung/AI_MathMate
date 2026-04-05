"""
AI_MathMate V2 — 6. 교차 검증: GPT-4o 독립 태깅
Gemini 2.5 Pro가 태깅한 problem_module_map.json의 신뢰성을 검증합니다.

[방법]
- GPT-4o에게 모듈 목록을 제공하지 않고, 자유 서술로 기법을 추출
- 자유 서술 결과를 91개 모듈에 자동 매핑
- Gemini(Google) 태깅 vs GPT-4o(OpenAI) 태깅 일치율 계산
- 편향 분리: 서로 다른 회사 모델로 교차 검증

[실행]
  python 6_cross_validate_claude.py
  → data/cross_validation_result.json
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "engine_v2" / "data"
PROBLEMS_PATH = DATA_DIR / "aime_problems_text.json"
GEMINI_MAP_PATH = DATA_DIR / "problem_module_map.json"
OUTPUT_PATH = DATA_DIR / "cross_validation_result.json"

load_dotenv(BASE_DIR / ".env")

# ── 모듈 태그 매핑 테이블 (자유 서술 → module_id) ────────────────
# 각 모듈의 핵심 키워드를 정의하여 Claude 자유 서술과 매칭
MODULE_KEYWORDS = {
    # Algebra
    "algebra_absolute_value": ["absolute value", "piecewise", "distance on number line"],
    "algebra_basic_manipulation": ["factoring", "expansion", "exponent laws", "rational expression", "algebraic manipulation", "rationalizing expressions", "quadratic equations", "polynomial equations", "number manipulation", "ratio and proportion", "linear equations", "fraction simplification", "difference of squares", "polynomial division", "polynomial evaluation"],
    "algebra_binomial_theorem": ["binomial theorem", "binomial expansion", "pascal", "binomial coefficient"],
    "algebra_complex_numbers": ["complex number", "complex plane", "de moivre", "imaginary", "argand"],
    "algebra_floor_ceiling_functions": ["floor function", "ceiling function", "greatest integer", "fractional part"],
    "algebra_func_equations_cauchy": ["functional equation", "cauchy", "function equation"],
    "algebra_func_symmetry": ["function symmetry", "even function", "odd function", "symmetric function"],
    "algebra_functions_and_properties": ["function properties", "domain", "range", "composition", "inverse function"],
    "algebra_inequalities": ["inequality", "am-gm", "cauchy-schwarz", "power mean", "jensen", "inequalities", "optimization", "geometric optimization"],
    "algebra_kinematics": ["rate", "speed", "distance", "time", "work problem", "mixture", "kinematics", "relative motion"],
    "algebra_logarithms_exponents": ["logarithm", "exponent", "change of base", "log property"],
    "algebra_matrices_determinants": ["matrix", "determinant", "eigenvalue", "linear algebra"],
    "algebra_poly_complex_roots": ["polynomial root", "complex root", "conjugate pair", "root of polynomial"],
    "algebra_poly_vieta_newton": ["vieta", "newton sum", "symmetric polynomial", "power sum", "elementary symmetric", "symmetric sums"],
    "algebra_roots_unity_filter": ["roots of unity", "unity filter", "cyclotomic", "primitive root of unity"],
    "algebra_seq_characteristic_eq": ["characteristic equation", "linear recurrence", "homogeneous recurrence"],
    "algebra_sequences_series_recurrence": ["sequence", "series", "recurrence", "arithmetic progression", "geometric progression", "telescoping", "summation techniques", "consecutive sums", "recursive functions", "summation", "approximation techniques"],
    "algebra_statistics": ["mean", "median", "variance", "standard deviation", "weighted average"],
    "algebra_systems_of_equations": ["system of equations", "simultaneous", "substitution", "elimination", "system of linear equations"],
    "algebra_telescoping_sum": ["telescoping", "collapsing sum", "partial fraction decomposition"],
    "algebra_trigonometry": ["trigonometric equation", "trig identity", "sin cos tan", "double angle", "half angle", "trigonometric identities", "trigonometry", "trigonometric ratios"],
    # Geometry
    "geo_complex_bisector_tangency": ["bisector tangency", "perpendicular bisector tangent"],
    "geo_parabola_rotation": ["parabola rotation", "conic rotation"],
    "geo_reflection_heptagon": ["heptagon", "regular 7-gon"],
    "geo_trapezoid_inscribed": ["inscribed trapezoid", "tangential trapezoid"],
    "geometry_angle_bisector_theorem": ["angle bisector", "bisector theorem", "incenter ratio"],
    "geometry_area_and_volume": ["area", "volume", "surface area", "cross section", "geometric optimization", "geometric dissection", "inscribed figures"],
    "geometry_center_euler_ninepoint": ["euler line", "nine point", "circumcenter orthocenter"],
    "geometry_circle_isogonal_symmedian": ["isogonal", "symmedian", "isogonal conjugate"],
    "geometry_circle_ptolemy": ["ptolemy", "cyclic quadrilateral diagonal"],
    "geometry_circle_radical": ["radical axis", "radical center", "power of a point circle"],
    "geometry_circle_theorems": ["inscribed angle", "central angle", "chord", "secant", "tangent line", "circle geometry", "circle properties", "circle inscription", "tangent-segment theorem", "circle tangency properties", "tangent properties", "circle tangency", "arc length calculation", "geometry of circles", "circle packing"],
    "geometry_circles_tangency": ["tangent circle", "internally tangent", "externally tangent", "descartes circle"],
    "geometry_complex_numbers_in_geometry": ["complex number geometry", "rotation complex", "geometric transformation complex"],
    "geometry_coordinate_analytic": ["coordinate geometry", "analytic geometry", "distance formula", "slope", "midpoint", "line equation", "line intersection", "plane geometry", "intersection of curves", "ellipse properties", "lattice points"],
    "geometry_coordinate_intersections": ["curve intersection", "system of curve", "parabola line"],
    "geometry_cyclic_quadrilaterals": ["cyclic quadrilateral", "concyclic", "ptolemy theorem"],
    "geometry_locus": ["locus", "set of points satisfying"],
    "geometry_polygons": ["polygon", "regular polygon", "diagonal", "interior angle sum", "n-gon"],
    "geometry_power_of_a_point": ["power of a point", "intersecting chord", "secant tangent"],
    "geometry_sim_homothety": ["similarity", "homothety", "dilation", "similar triangle", "ratio of similarity", "symmetry analysis", "symmetry"],
    "geometry_sim_spiral": ["spiral similarity", "rotation dilation"],
    "geometry_solid_3d": ["3d geometry", "solid geometry", "polyhedron", "tetrahedron", "cube", "sphere", "cone", "cylinder", "cross-section", "geometry of solids", "volume ratios"],
    "geometry_transform_inversion": ["inversion", "inversive geometry", "circle inversion"],
    "geometry_transformations": ["reflection", "rotation", "translation", "transformation"],
    "geometry_triangle_centers": ["incenter", "circumcenter", "orthocenter", "centroid", "triangle center"],
    "geometry_triangle_properties": ["triangle", "law of cosines", "law of sines", "heron", "stewart", "cevian", "median", "altitude", "pythagorean theorem", "geometric properties", "incircle properties", "trapezoid properties", "angle chasing", "ceva's theorem", "mass points", "perpendicular lines", "parallel lines"],
    "geometry_trigonometry_laws": ["law of cosines", "law of sines", "trigonometry geometry", "sine rule", "cosine rule"],
    "geometry_vectors": ["vector", "dot product", "cross product", "vector geometry"],
    # Number Theory
    "nt_base_divisibility": ["base conversion divisibility", "divisibility in base"],
    "nt_base_representation_and_digits": ["base representation", "digit", "decimal expansion", "number base", "binary", "digit sum", "base conversion", "decimal approximations", "decimal representation", "consecutive integers"],
    "nt_chinese_remainder_theorem": ["chinese remainder", "crt", "simultaneous congruence"],
    "nt_diophantine_equations": ["diophantine", "integer solution", "pell equation", "linear diophantine"],
    "nt_diophantine_pell": ["pell equation", "continued fraction", "fundamental solution"],
    "nt_diophantine_vieta_jumping": ["vieta jumping", "markov equation"],
    "nt_discrete_log": ["discrete logarithm", "primitive root index"],
    "nt_divisibility_and_primes": ["prime", "divisibility", "factorization", "fundamental theorem arithmetic"],
    "nt_divisor_functions": ["divisor", "number of divisors", "sum of divisors", "tau", "sigma"],
    "nt_floor_legendre": ["floor function number theory", "legendre formula", "p-adic valuation", "largest power dividing factorial"],
    "nt_frobenius_coin_problem": ["frobenius", "coin problem", "chicken mcnugget", "sylvester-frobenius"],
    "nt_gcd_lcm": ["gcd", "lcm", "euclidean algorithm", "greatest common divisor"],
    "nt_mod_lte_lemma": ["lifting the exponent", "lte lemma", "v_p"],
    "nt_mod_order_primitive": ["multiplicative order", "primitive root", "order modulo"],
    "nt_modular_arithmetic": ["modular arithmetic", "congruence", "mod", "remainder", "fermat little", "euler totient", "wilson", "number theory", "inverses", "cyclic groups", "order of elements", "factorial properties", "integer properties", "parity analysis"],
    "nt_perfect_powers": ["perfect square", "perfect cube", "perfect power"],
    "nt_quadratic_residue": ["quadratic residue", "legendre symbol", "quadratic reciprocity"],
    # Combinatorics
    "comb_catalan": ["catalan number", "ballot problem", "dyck path", "parenthesization"],
    "comb_count_double": ["double counting", "handshaking lemma", "overcounting", "combinatorial counting", "combinatorial enumeration", "combinatorial geometry", "combinatorial design", "complementary counting", "counting solutions", "combinatorial paths"],
    "comb_derangement": ["derangement", "subfactorial", "no fixed point permutation"],
    "comb_gen_func_snake_oil": ["generating function", "snake oil", "formal power series"],
    "comb_graph_coloring_chromatic": ["graph coloring", "chromatic number", "chromatic polynomial"],
    "comb_graph_theory": ["graph theory", "euler path", "hamilton", "tournament", "directed graph", "adjacency"],
    "comb_grid_sudoku_sum": ["grid counting", "latin square", "sudoku"],
    "comb_inclusion_exclusion": ["inclusion-exclusion", "inclusion exclusion", "sieve", "overcounting correction", "parity arguments", "parity analysis"],
    "comb_multinomial_partition": ["multinomial", "partition", "distributing", "stars and bars", "permutations", "permutation counting", "circular permutations", "permutations with restrictions", "permutations with repetition", "permutation", "combinatorial coefficients"],
    "comb_pairing_probability": ["pairing", "matching", "lexicographic"],
    "comb_path_counting": ["lattice path", "grid path", "catalan path", "path counting"],
    "comb_prob_absorbing_markov": ["markov chain", "absorbing state", "random walk"],
    "comb_prob_transition_matrix": ["transition matrix", "state diagram", "stochastic"],
    "comb_probability": ["probability", "conditional probability", "bayes", "expected value", "geometric probability"],
    "comb_recursion_dp": ["recursion", "dynamic programming", "recurrence relation counting", "memoization"],
    "comb_set_theory_and_subsets": ["subset", "power set", "set theory", "cardinality"],
    "comb_symmetry_and_burnside": ["burnside", "polya", "symmetry counting", "group action", "orbit"],
}


def match_techniques_to_modules(techniques: list[str]) -> list[str]:
    """Claude의 자유 서술 기법을 module_id에 매핑."""
    matched = []
    for tech in techniques:
        tech_lower = tech.lower()
        best_module = None
        best_score = 0

        for module_id, keywords in MODULE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in tech_lower)
            if score > best_score:
                best_score = score
                best_module = module_id

        if best_module and best_score > 0:
            matched.append(best_module)
        else:
            # 키워드 매칭 실패 시 도메인이라도 매칭
            matched.append(f"UNMATCHED:{tech[:50]}")

    return matched


def run_gpt4o_batch(client: OpenAI, problems: list[dict], batch_num: int, total_batches: int) -> list[dict]:
    """GPT-4o에 배치 전송하여 자유 태깅."""
    print(f"\n🔍 [Batch {batch_num}/{total_batches}] {len(problems)} problems...")

    problems_text = ""
    for p in problems:
        problems_text += f"\n---\n**{p['problem_id']}** (Answer: {p['answer']})\n{p['question']}\n"

    prompt = f"""당신은 AIME 수학 올림피아드 분석가입니다.
각 문제를 풀기 위해 필요한 '원자적 수학 기법(Atomic Mathematical Technique)'을 1~3개 추출하세요.

[원자적 기법의 정의]
- 하나의 수학 정리, 공식, 또는 테크닉 단위입니다.
- 표면적 스토리텔링은 무시하고, 풀이의 뼈대가 되는 핵심 기법만 추출합니다.
- 너무 넓은 분류("대수학")는 안 되고, 너무 좁은 분류("3차 방정식의 판별식")도 안 됩니다.
- 적절한 단위 예시: "비에타 공식과 대칭 다항식", "포함-배제 원리", "좌표 해석 기하"
- 4대 도메인: algebra, geometry, number_theory, combinatorics

[세분화 수준 가이드]
- "다항식" ← 너무 넓음
- "비에타 공식 + 뉴턴 합" ← 적절 (관련 기법을 하나로 묶음)
- "2차 비에타" ← 너무 좁음
- "원의 성질" ← 너무 넓음
- "멱(Power of a Point) 정리" ← 적절
- "내접원의 반지름 공식" ← 너무 좁음

[문제 목록]
{problems_text}

[응답 형식 — 반드시 JSON 배열만]
[
  {{"problem_id": "1983_AIME_P1", "techniques": ["technique name 1", "technique name 2"], "domain_primary": "combinatorics"}},
  ...
]

모든 {len(problems)}개 문제에 대해 빠짐없이 응답하세요."""

    for attempt in range(1, 4):
        try:
            t0 = time.time()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a math olympiad analyst. Always respond with valid JSON only. No markdown, no explanation."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )
            dur = time.time() - t0

            raw = response.choices[0].message.content
            if raw.startswith("```json"):
                raw = raw.split("```json")[-1].split("```")[0].strip()

            parsed = json.loads(raw)
            # GPT-4o 응답 형태 정규화
            if isinstance(parsed, list):
                results = parsed
            elif isinstance(parsed, dict):
                # {"results": [...]} 또는 {"problems": [...]} 형태
                for key in ["results", "problems", "data"]:
                    if key in parsed and isinstance(parsed[key], list):
                        results = parsed[key]
                        break
                else:
                    # 값 중 첫 번째 리스트를 찾음
                    results = []
                    for v in parsed.values():
                        if isinstance(v, list) and v and isinstance(v[0], dict):
                            results = v
                            break
            else:
                print(f"  ⚠️  Unexpected type: {type(parsed)}")
                results = []

            # 유효성 검증: dict이고 problem_id가 있는 항목만
            results = [r for r in results if isinstance(r, dict) and "problem_id" in r]

            if not results:
                print(f"  ⚠️  Attempt {attempt}: 유효한 결과 0개, 재시도...")
                time.sleep(3)
                continue

            print(f"  ✅ {len(results)} problems tagged in {dur:.1f}s")
            return results

        except Exception as e:
            print(f"  ⚠️  Attempt {attempt}: {e}")
            if attempt < 3:
                time.sleep(5)

    print(f"  ❌ 3회 시도 모두 실패")
    return []


def compare_results(gemini_map: dict, claude_tags: list[dict]) -> dict:
    """Gemini vs Claude 일치율 분석."""
    # Gemini mappings를 dict로
    gemini_dict = {}
    for m in gemini_map["mappings"]:
        gemini_dict[m["problem_id"]] = set(m["modules_used"])

    total = 0
    exact_match = 0
    partial_match = 0
    no_match = 0
    unmatched_count = 0

    by_difficulty = {"easy": [0, 0], "medium": [0, 0], "hard": [0, 0]}  # [match, total]
    by_era = {}

    details = []

    for ct in claude_tags:
        pid = ct["problem_id"]
        if pid not in gemini_dict:
            continue

        total += 1
        gemini_mods = gemini_dict[pid]
        claude_techniques = ct.get("techniques", [])
        claude_mods = set(match_techniques_to_modules(claude_techniques))

        # UNMATCHED 제거 후 비교
        claude_clean = {m for m in claude_mods if not m.startswith("UNMATCHED:")}
        unmatched_count += len(claude_mods) - len(claude_clean)

        overlap = gemini_mods & claude_clean
        if overlap == gemini_mods or overlap == claude_clean:
            exact_match += 1
            match_type = "exact"
        elif overlap:
            partial_match += 1
            match_type = "partial"
        else:
            no_match += 1
            match_type = "none"

        # 난이도별
        pnum = int(pid.split("_P")[-1]) if "_P" in pid else 0
        if pnum <= 5:
            diff = "easy"
        elif pnum <= 10:
            diff = "medium"
        else:
            diff = "hard"
        by_difficulty[diff][1] += 1
        if match_type in ("exact", "partial"):
            by_difficulty[diff][0] += 1

        # 시대별
        year = int(pid.split("_")[0])
        era = f"{(year // 10) * 10}s"
        if era not in by_era:
            by_era[era] = [0, 0]
        by_era[era][1] += 1
        if match_type in ("exact", "partial"):
            by_era[era][0] += 1

        details.append({
            "problem_id": pid,
            "gemini": list(gemini_mods),
            "claude_raw": claude_techniques,
            "claude_mapped": list(claude_mods),
            "match_type": match_type,
        })

    agreement = (exact_match + partial_match) / total * 100 if total else 0

    return {
        "total_compared": total,
        "exact_match": exact_match,
        "partial_match": partial_match,
        "no_match": no_match,
        "agreement_pct": round(agreement, 2),
        "unmatched_techniques": unmatched_count,
        "by_difficulty": {k: round(v[0] / v[1] * 100, 1) if v[1] else 0 for k, v in by_difficulty.items()},
        "by_era": {k: round(v[0] / v[1] * 100, 1) if v[1] else 0 for k, v in sorted(by_era.items())},
        "details": details,
    }


def main():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Load problems
    with open(PROBLEMS_PATH, encoding="utf-8") as f:
        all_problems = json.load(f)
    print(f"📄 문제 로드: {len(all_problems)}개")

    # Load existing Claude results if resuming
    claude_tags = []
    if OUTPUT_PATH.exists():
        with open(OUTPUT_PATH, encoding="utf-8") as f:
            existing = json.load(f)
        claude_tags = existing.get("claude_tags", [])
        print(f"📂 기존 결과 로드: {len(claude_tags)}개")

    tagged_ids = {t["problem_id"] for t in claude_tags}
    remaining = [p for p in all_problems if p["problem_id"] not in tagged_ids]
    print(f"📦 남은 문제: {len(remaining)}개")

    # Batch: 15 problems per batch (GPT-4o json_object 안정성 확보)
    BATCH_SIZE = 15
    batches = [remaining[i:i + BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]
    total_batches = len(batches)

    for i, batch in enumerate(batches, 1):
        results = run_gpt4o_batch(client, batch, i, total_batches)

        if len(results) < len(batch) * 0.5:
            # 배치 실패 → 개별 문제 단위로 폴백
            tagged_in_batch = {r["problem_id"] for r in results}
            failed = [p for p in batch if p["problem_id"] not in tagged_in_batch]
            print(f"  🔄 {len(failed)}개 문제 개별 재시도...")
            for p in failed:
                single = run_gpt4o_batch(client, [p], 0, 0)
                results.extend(single)
                time.sleep(0.5)

        claude_tags.extend(results)

        # 중간 저장
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump({"claude_tags": claude_tags}, f, ensure_ascii=False, indent=2)
        print(f"  💾 중간 저장 ({len(claude_tags)}개 누적)")

        time.sleep(1)

    # 최종 비교
    print("\n" + "=" * 70)
    print("📊 교차 검증 분석")
    print("=" * 70)

    with open(GEMINI_MAP_PATH, encoding="utf-8") as f:
        gemini_map = json.load(f)

    analysis = compare_results(gemini_map, claude_tags)

    print(f"\n비교 대상: {analysis['total_compared']}개")
    print(f"완전 일치: {analysis['exact_match']}개")
    print(f"부분 일치: {analysis['partial_match']}개")
    print(f"불일치:    {analysis['no_match']}개")
    print(f"일치율:    {analysis['agreement_pct']}%")

    print(f"\n난이도별:")
    for k, v in analysis["by_difficulty"].items():
        print(f"  {k}: {v}%")

    print(f"\n시대별:")
    for k, v in analysis["by_era"].items():
        print(f"  {k}: {v}%")

    # 최종 저장
    final = {
        "claude_tags": claude_tags,
        "analysis": analysis,
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 교차 검증 완료! → {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
