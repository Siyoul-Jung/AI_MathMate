"""
export_comparison.py
=====================
원형 문제 vs 생성 변형 비교 분석 리포트 생성기

DB에 저장된 변형 문제들을 원형 AIME 2025 I 문제와 나란히 비교하는
마크다운 리포트를 생성합니다.

사용법:
    python amc_engine/export_comparison.py
"""

import sqlite3
import json
import os

# ─────────────────────────────────────────────
# 원형 문제 데이터 (AIME 2025 I)
# AoPS: https://artofproblemsolving.com/wiki/index.php/2025_AIME_I_Problems
# ─────────────────────────────────────────────
ORIGINALS = {
    "P01": {
        "title": "Problem 1 — Number Theory (Base Representations)",
        "statement": (
            "Find the sum of all integer bases $b > 1$ for which $17_b$ is a divisor of $97_b$."
        ),
        "answer": 70,
        "topic": "Number Theory / Divisibility in Base $b$",
        "difficulty": "AIME Level 1",
    },
    "P10": {
        "title": "Problem 10 — Combinatorics / Grid Arrangements (Sudoku)",
        "statement": (
            "The 27 cells of a $3 \\times 9$ grid are filled in using the numbers $1$ through $9$ so that each row contains "
            "$9$ different numbers, and each of the three $3 \\times 3$ blocks contains $9$ different numbers, "
            "as in the first three rows of a Sudoku puzzle. The number of different ways to fill such a grid can be "
            "written as $p^a \cdot q^b \cdot r^c \cdot s^d$ where $p, q, r, s$ are distinct prime numbers and $a,b,c,d$ are positive integers. "
            "Find $p \\cdot a + q \\cdot b + r \\cdot c + s \\cdot d$."
        ),
        "answer": 81,
        "topic": "Combinatorics",
        "difficulty": "AIME Level 10",
    },
    "P11": {
        "title": "Problem 11 — Functions / Geometric Intersections (Piecewise Parabola)",
        "statement": (
            "A piecewise linear function $f$ is defined by $f(x) = x$ if $-1 \\le x < 1$, "
            "and $f(x) = 2 - x$ if $1 \\le x < 3$. Let $f(x + 4) = f(x)$ for all real numbers $x$. "
            "The parabola $x = 34y^2$ intersects the graph of $f(x)$ at finitely many points. "
            "The sum of the $y$-coordinates of all these intersection points can be expressed "
            "in the form $\\frac{a + b\\sqrt{c}}{d}$, where $c$ is squarefree. Find $a+b+c+d$."
        ),
        "answer": 259,
        "topic": "Algebra / Functions",
        "difficulty": "AIME Level 11",
    },
    "P12": {
        "title": "Problem 12 — Geometry / Inequalities (3D Convex Regions)",
        "statement": (
            "The set of points in 3-dimensional coordinate space that lie in the plane "
            "$x + y + z = 75$ whose coordinates satisfy the inequalities "
            "$x - yz < y - zx < z - xy$ forms three disjoint convex regions. "
            "Exactly one of those regions has finite area. "
            "The area of this finite region can be expressed in the form $a\\sqrt{b}$, "
            "where $a$ and $b$ are positive integers and $b$ is not divisible by the square "
            "of any prime. Find $a + b$."
        ),
        "answer": 510,
        "topic": "Geometry / Algebra / 3D Convex Regions",
        "difficulty": "AIME Level 12",
    },
    "P13": {
        "title": "Problem 13 — Combinatorics / Expected Value",
        "statement": (
            "Alex divides a disk into four quadrants with two perpendicular diameters intersecting "
            "at the center of the disk. He draws $10$ more line segments through the disk, drawing "
            "each segment by selecting two points at random on the perimeter of the disk in "
            "different quadrants and connecting these two points. Find the expected number of "
            "regions into which these $12$ line segments divide the disk."
        ),
        "answer": 167,
        "topic": "Combinatorics / Geometric Probability / Expected Value",
        "difficulty": "AIME Level 13",
    },
    "P14": {
        "title": "Problem 14 — Geometry (Fermat Point)",
        "statement": (
            "Let $ABCDE$ be a convex pentagon with $AB = 14$, $BC = 7$, $CD = 24$, $DE = 13$, "
            "$EA = 26$, and $\\angle B = \\angle E = 60^\\circ$. For each point $X$ in the plane, "
            "define $f(X) = AX + BX + CX + DX + EX$. The least possible value of $f(X)$ can be "
            "expressed as $m + n\\sqrt{p}$, where $m$ and $n$ are positive integers and $p$ is "
            "not divisible by the square of any prime. Find $m + n + p$."
        ),
        "answer": 593,
        "topic": "Geometry / Fermat Point / Distance Optimization",
        "difficulty": "AIME Level 14",
    },
    "P15": {
        "title": "Problem 15 — Number Theory (LTE / Modular Arithmetic)",
        "statement": (
            "Let $N$ denote the number of ordered triples of positive integers $(a, b, c)$ such "
            "that $a, b, c \\leq 3^7$ and $a^3 + b^3 + c^3$ is a multiple of $3^7$. Find the "
            "remainder when $N$ is divided by $1000$."
        ),
        "answer": 247,
        "topic": "Number Theory / Lifting the Exponent Lemma",
        "difficulty": "AIME Level 15",
    },
}

# ─────────────────────────────────────────────

def get_variants_from_db(cursor, p_id: str, mode: str = "MOCK", limit: int = 3):
    """DB에서 특정 문항의 변형 문제를 모드별로 최신순으로 가져옵니다."""
    cursor.execute(
        """
        SELECT narrative, correct_answer, variables, theme, drill_level
        FROM generated_problems
        WHERE exam_year = '2025' AND exam_type = 'AIME1' AND problem_num = ? AND problem_mode = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (p_id, mode, limit),
    )
    return cursor.fetchall()


def format_seed_info(variables_json: str) -> str:
    try:
        v = json.loads(variables_json)
        if "k1" in v:
            return f"k1={v.get('k1')}, k2={v.get('k2')}, CD={v.get('CD')}"
        elif "m" in v and "n" in v:
            return f"m={v.get('m')}, n={v.get('n')}"
        elif "K" in v:
            return f"K={v.get('K')}, M={v.get('M')}"
        elif "X" in v:
            return f"X={v.get('X')}, Y={v.get('Y')}, W={v.get('W')}"
        else:
            return str(v)
    except Exception:
        return "N/A"


def compare_answers(variants: list) -> str:
    """변형 문제 정답들의 분산을 분석합니다."""
    if not variants:
        return "데이터 없음"
    answers = [int(row[1]) for row in variants]
    return f"[{', '.join(str(a) for a in answers)}]"


def export_comparison(db_name="amc_factory.db", output_file="AIME_Comparison_Report.md"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, db_name)
    output_path = os.path.join(base_dir, output_file)

    if not os.path.exists(db_path):
        print(f"❌ DB 파일 없음: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ── [이 목록에 있는 문항들의 리포트를 생성합니다] ──
    PROBLEMS_TO_REPORT = ["P01", "P10", "P11", "P12", "P13", "P14", "P15"]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🏆 AI MathMate — AIME 2025 I 원형 vs 변형 비교 분석 리포트\n\n")
        f.write("> **생성 엔진:** amc_engine (GPT-4o-mini)  \n")
        f.write("> **원형 출처:** [AIME 2025 I, AoPS](https://artofproblemsolving.com/wiki/index.php/2025_AIME_I_Problems)  \n")
        f.write("> 각 문항별 원형 문제 1개 + AI 생성 변형 3개를 비교합니다.\n\n")
        f.write("---\n\n")

        summary_rows = []

        for p_id, orig in ORIGINALS.items():
            mocks = get_variants_from_db(cursor, p_id, mode="MOCK", limit=3)
            drills = get_variants_from_db(cursor, p_id, mode="DRILL", limit=10)

            f.write(f"## 📌 {p_id} — {orig['title']}\n\n")
            f.write(f"- **주제:** {orig['topic']}\n")
            f.write(f"- **난이도:** {orig['difficulty']}\n\n")

            # 원형 문제
            f.write("### 🔵 원형 문제 (Official AIME 2025 I)\n\n")
            f.write(f"> {orig['statement']}\n\n")
            f.write(f"**🔑 공식 정답: `{orig['answer']}`**\n\n")
            f.write("---\n\n")

            # 실전 변형 문제들 (MOCK)
            if not mocks:
                f.write(f"### 🔴 실전 변형 문제 (MOCK)\n\n")
                f.write("> ⚠️ 아직 생성된 실전 변형 문제가 없습니다.\n\n")
            else:
                f.write(f"### 🟢 실전 변형 문제 (MOCK) ({len(mocks)}개)\n\n")
                for i, (narrative, answer, variables, theme, lvl) in enumerate(mocks, 1):
                    seed_info = format_seed_info(variables)
                    f.write(f"#### 실전 변형 {i}\n\n")
                    f.write(f"> {narrative.strip()}\n\n")
                    f.write(f"**🔑 답: `{int(answer) if answer == int(answer) else answer}`** &nbsp;|&nbsp; ")
                    f.write(f"🌱 시드: `{seed_info}` &nbsp;|&nbsp; 🎨 테마: `{theme}`\n\n")

            # 개념 드릴 문제들 (DRILL)
            if drills:
                f.write(f"### 🛠️ 개념 드릴 문제 (DRILL)\n\n")
                for i, (narrative, answer, variables, theme, lvl) in enumerate(drills, 1):
                    seed_info = format_seed_info(variables)
                    f.write(f"#### 드릴 Level {lvl if lvl else '?'}\n\n")
                    f.write(f"> {narrative.strip()}\n\n")
                    f.write(f"**🔑 답: `{answer}`** &nbsp;|&nbsp; ")
                    f.write(f"🌱 시드: `{seed_info}` &nbsp;|&nbsp; 🎨 테마: `{theme}`\n\n")

            # 요약 행 축적
            topic_short = orig["topic"].split("/")[0].strip()
            variant_answers = compare_answers(mocks + drills)
            summary_rows.append(
                (p_id, topic_short, orig["answer"], variant_answers, len(mocks) + len(drills))
            )
            f.write("---\n\n")

        # 비교 분석 요약표
        f.write("## 📊 전체 비교 요약\n\n")
        f.write("| 문항 | 유형 | 원형 정답 | 변형 정답 목록 | 생성 수 |\n")
        f.write("|------|------|-----------|----------------|--------|\n")
        for p_id, topic, orig_ans, var_ans, count in summary_rows:
            f.write(f"| {p_id} | {topic} | `{orig_ans}` | {var_ans} | {count}개 |\n")

        f.write("\n---\n\n")
        f.write("*이 리포트는 `amc_engine/export_comparison.py`에 의해 자동 생성되었습니다.*\n")

    conn.close()
    print(f"🎉 비교 리포트 생성 완료: {output_path}")


if __name__ == "__main__":
    export_comparison()
