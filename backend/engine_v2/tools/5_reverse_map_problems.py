"""
AI_MathMate V2 — 5. 역방향 문제-모듈 매핑 (Reverse Map)

기존 추출 방식의 검증을 위해, **문제 → 모듈** 방향으로 역추적합니다.
PDF의 각 문제를 읽고, 우리 89개 활성 모듈 중 어떤 것이 필요한지 태깅합니다.

[기존 vs 신규]
  기존 (2_extract_chunks.py): PDF → "기법 추출" → module_id 목록 (LLM 주관)
  신규 (이 스크립트):         PDF + 모듈 목록 → "문제별 태깅" → problem-module 매핑 (검증 가능)

[검증 가능성]
  출력: "1983_AIME_P1 → [algebra_polynomials_vieta, nt_modular_arithmetic]"
  → 사람이 1983 AIME P1 원문을 보고 "맞다/틀리다" 판단 가능

[실행]
  python 5_reverse_map_problems.py
  → data/problem_module_map.json 생성
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "engine_v2" / "data"
CACHE_PATH = DATA_DIR / "pdf_cache.json"
OUTPUT_PATH = DATA_DIR / "problem_module_map.json"

load_dotenv(BASE_DIR / ".env")

# ── 연도별 시험 구성 ────────────────────────────────────────────
# 1983~1999: AIME 1회 (15문제/년) → 255문제
# 2000~2026: AIME I + II (30문제/년) → 810문제
# 합계: ~1065문제
def build_problem_list() -> list[str]:
    """전체 AIME 문제 ID 목록 생성 (~1065개)."""
    problems = []
    for year in range(1983, 2000):
        for p in range(1, 16):
            problems.append(f"{year}_AIME_P{p}")
    for year in range(2000, 2027):
        for part in ["I", "II"]:
            for p in range(1, 16):
                problems.append(f"{year}_AIME_{part}_P{p}")
    return problems


def load_active_modules() -> list[dict]:
    """현재 활성 모듈 목록을 파일 시스템에서 로드."""
    modules_dir = BASE_DIR / "engine_v2" / "modules"
    module_list = []

    for category in ["algebra", "combinatorics", "geometry", "number_theory", "meta"]:
        cat_dir = modules_dir / category
        if not cat_dir.exists():
            continue
        for py_file in cat_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            module_id = py_file.stem
            module_list.append({
                "module_id": module_id,
                "category": category,
            })

    return module_list


def reverse_map_chunk(
    client, pdf_file, start_year: int, end_year: int,
    module_ids: list[str], chunk_index: int
) -> list[dict]:
    """
    특정 연도 범위의 문제들에 대해, 각 문제가 사용하는 모듈을 태깅합니다.
    """
    print(f"\n🔍 [Chunk {chunk_index}] {start_year}~{end_year}년 역방향 매핑 시작...")

    module_list_str = "\n".join(f"  - {mid}" for mid in sorted(module_ids))

    prompt = f"""당신은 AIME 수학 올림피아드 분석가입니다.
첨부된 PDF는 1983~2026 모든 AIME 기출문제 모음집입니다.

[작업]
**{start_year}년부터 {end_year}년까지** 출제된 모든 AIME 문제를 하나씩 읽고,
각 문제를 풀기 위해 반드시 필요한 수학적 기법(모듈)을 아래 목록에서 선택하세요.

[사용 가능한 모듈 목록 (총 {len(module_ids)}개)]
{module_list_str}

[규칙]
1. 각 문제에 대해 1~3개의 모듈을 선택하세요. (핵심 기법만)
2. 위 목록에 적절한 모듈이 없으면 "UNMAPPED"라고 표기하고 어떤 기법이 필요한지 설명하세요.
3. 문제를 실제로 읽고 풀이 전략을 판단한 후 태깅하세요. 추측하지 마세요.
4. {start_year}년부터 {end_year}년까지의 문제만 분석하세요.
5. 문제 번호 형식:
   - 1999년 이전: "1983_AIME_P1" ~ "1983_AIME_P15"
   - 2000년 이후: "2000_AIME_I_P1" ~ "2000_AIME_I_P15", "2000_AIME_II_P1" ~ "2000_AIME_II_P15"

[응답 형식 — JSON 배열]
[
  {{
    "problem_id": "1983_AIME_P1",
    "modules_used": ["algebra_polynomials_vieta", "algebra_systems_of_equations"],
    "unmapped_skills": "",
    "difficulty_estimate": 3
  }},
  {{
    "problem_id": "1983_AIME_P15",
    "modules_used": ["UNMAPPED"],
    "unmapped_skills": "Projective geometry / cross-ratio not covered by any module",
    "difficulty_estimate": 9
  }}
]
"""

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            t0 = time.time()
            response = client.models.generate_content(
                model="gemini-2.5-pro",  # 수학 추론 정밀도 최우선 (일회성 작업)
                contents=[pdf_file, prompt],
                config=GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,  # 최소 환각
                ),
            )
            duration = time.time() - t0

            raw_text = response.text
            if raw_text is None:
                print(f"  ⚠️  [시도 {attempt}/{max_retries}] response.text=None, 재시도...")
                time.sleep(10)
                continue

            if raw_text.startswith("```json"):
                raw_text = raw_text.split("```json")[-1].split("```")[0].strip()

            results = json.loads(raw_text)
            print(f"  ✅ 매핑 완료! ({len(results)}개 문제) - {duration:.1f}초")
            return results

        except Exception as e:
            print(f"  ⚠️  [시도 {attempt}/{max_retries}] 오류: {e}")
            if attempt < max_retries:
                time.sleep(10)

    print(f"  ❌ {max_retries}회 시도 모두 실패")
    return []


def analyze_results(all_mappings: list[dict], module_ids: list[str]):
    """매핑 결과 분석: 커버리지, 공백, 과잉 모듈 식별."""
    print("\n" + "=" * 70)
    print("📊 역방향 매핑 분석 결과")
    print("=" * 70)

    total_problems = len(all_mappings)
    unmapped_problems = [m for m in all_mappings if "UNMAPPED" in m.get("modules_used", [])]
    unmapped_skills: dict[str, int] = {}
    module_usage: dict[str, int] = {}

    for m in all_mappings:
        for mod in m.get("modules_used", []):
            if mod != "UNMAPPED":
                module_usage[mod] = module_usage.get(mod, 0) + 1
        skill = m.get("unmapped_skills", "")
        if skill:
            unmapped_skills[skill] = unmapped_skills.get(skill, 0) + 1

    # 커버리지
    coverage = (total_problems - len(unmapped_problems)) / total_problems * 100 if total_problems else 0
    print(f"\n전체 문제 수: {total_problems}")
    print(f"매핑 성공: {total_problems - len(unmapped_problems)}개 ({coverage:.1f}%)")
    print(f"UNMAPPED: {len(unmapped_problems)}개")

    # 가장 많이 사용된 모듈 Top 20
    print(f"\n🏆 모듈 사용 빈도 Top 20:")
    for mid, cnt in sorted(module_usage.items(), key=lambda x: -x[1])[:20]:
        pct = cnt / total_problems * 100
        print(f"  {mid:45s} {cnt:3d}회 ({pct:.1f}%)")

    # 한 번도 사용 안 된 모듈 (잉여)
    unused = [mid for mid in module_ids if mid not in module_usage]
    if unused:
        print(f"\n⚠️  한 번도 사용되지 않은 모듈 ({len(unused)}개):")
        for mid in sorted(unused):
            print(f"  - {mid}")

    # UNMAPPED 기법 목록 (공백)
    if unmapped_skills:
        print(f"\n🚨 모듈 공백 — UNMAPPED 기법 목록:")
        for skill, cnt in sorted(unmapped_skills.items(), key=lambda x: -x[1]):
            print(f"  [{cnt}회] {skill}")

    return {
        "total_problems": total_problems,
        "coverage_pct": round(coverage, 2),
        "unmapped_count": len(unmapped_problems),
        "unused_modules": unused,
        "unmapped_skills": unmapped_skills,
        "module_usage": module_usage,
    }


# ── 연대 블록 (2_extract_chunks.py와 동일) ───────────────────────
YEAR_CHUNKS = [
    (1983, 1989),
    (1990, 1996),
    (1997, 2001),
    (2002, 2006),
    (2007, 2011),
    (2012, 2016),
    (2017, 2021),
    (2022, 2026),
]


def main():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # PDF 로드
    if not CACHE_PATH.exists():
        print("❌ pdf_cache.json 없음. 1_upload_pdf.py를 먼저 실행하세요.")
        return
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        cache = json.load(f)
    pdf_file = client.files.get(name=cache["file_name"])
    print(f"📄 PDF 로드: {cache['display_name']}")

    # 활성 모듈 목록
    active_modules = load_active_modules()
    module_ids = [m["module_id"] for m in active_modules]
    print(f"📦 활성 모듈: {len(module_ids)}개")

    # 이미 부분 완료된 결과가 있으면 이어서 진행
    all_mappings = []
    if OUTPUT_PATH.exists():
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
        all_mappings = existing.get("mappings", [])
        mapped_ids = {m["problem_id"] for m in all_mappings}
        print(f"📂 기존 매핑 로드: {len(all_mappings)}개 문제")
    else:
        mapped_ids = set()

    # 이미 매핑된 연도 집합 계산
    mapped_years = set()
    for m in all_mappings:
        y = int(m["problem_id"].split("_")[0])
        mapped_years.add(y)

    # 연대별 역방향 매핑
    for i, (sy, ey) in enumerate(YEAR_CHUNKS, 1):
        # 해당 연대의 모든 연도가 이미 매핑되었는지 확인
        chunk_years = set(range(sy, ey + 1))
        if chunk_years.issubset(mapped_years):
            print(f"\n⏭️  [Chunk {i}] {sy}~{ey}년 이미 매핑됨. 건너뜁니다.")
            continue

        chunk_results = reverse_map_chunk(client, pdf_file, sy, ey, module_ids, i)
        all_mappings.extend(chunk_results)

        # 중간 저장 (안전 장치)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump({"mappings": all_mappings}, f, ensure_ascii=False, indent=2)
        print(f"  💾 중간 저장 완료 ({len(all_mappings)}개 누적)")

        time.sleep(3)  # API rate limit

    # 최종 분석
    analysis = analyze_results(all_mappings, module_ids)

    # 최종 저장
    final_output = {
        "mappings": all_mappings,
        "analysis": analysis,
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 역방향 매핑 완료! → {OUTPUT_PATH.name}")
    print(f"   커버리지: {analysis['coverage_pct']}%")
    print(f"   UNMAPPED: {analysis['unmapped_count']}개 문제")
    print(f"   미사용 모듈: {len(analysis['unused_modules'])}개")


if __name__ == "__main__":
    main()
