import sqlite3
import json
import os

DB_PATH = 'c:/AI_MathMate/amc_engine/amc_factory.db'
OUTPUT_PATH = 'c:/AI_MathMate/amc_engine/P12_All_18_Variants.md'

def format_seed_info(variables_json: str) -> str:
    try:
        v = json.loads(variables_json)
        return f"N={v.get('N')}"
    except Exception:
        return "N/A"

def export_p12():
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT narrative, correct_answer, variables
        FROM generated_problems
        WHERE problem_num = 'P12'
        ORDER BY cast(correct_answer as integer) ASC
        """
    )
    variants = cursor.fetchall()
    conn.close()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# 🏆 AIME 2025 I — P12 All 18 Generated Variants\n\n")
        f.write("> **Source:** amc_engine (GPT-4o-mini)\n")
        f.write("> **Total Generated:** 18 variants (Complete Seed Space)\n")
        f.write("> **Mathematical DNA:** `REGION-PLANE-INEQ` ($N \\equiv 3 \\pmod 6$)\n\n")
        f.write("---\n\n")

        for i, (narrative, answer, variables) in enumerate(variants, 1):
            seed_info = format_seed_info(variables)
            f.write(f"### Variant {i} (Seed: `{seed_info}`)\n\n")
            f.write(f"> {narrative.strip()}\n\n")
            f.write(f"**🔑 Answer: `{int(answer)}`**\n\n")
            f.write("---\n\n")

    print(f"Exported {len(variants)} P12 variants to {OUTPUT_PATH}")

if __name__ == "__main__":
    export_p12()
