import os
import sys
import argparse
import json

def scaffold(year, exam, p_id, band="MASTER"):
    """
    Creates the folder structure and boilerplate for a new AIME engine.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "amc_engine", "exams", str(year), exam, band, p_id)
    
    if os.path.exists(target_dir):
        print(f"⚠️  Target directory already exists: {target_dir}")
        return

    os.makedirs(target_dir, exist_ok=True)
    
    # 1. solver.py Boilerplate
    solver_content = f"""import random
import matplotlib.pyplot as plt
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {{
        "specific_tag": "UNKNOWN",
        "category": "Algebra",
        "context_type": "narrative",
        "level": {p_id[1:]},
        "has_image": False,
        "is_mock_ready": True
    }}
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def generate_seed(cls):
        # TODO: Implement parameter generation logic
        return {{'a': random.randint(1, 10), 'expected_t': 42}}

    @classmethod
    def get_narrative_instruction(cls, seed):
        return f"Find the value of a = {{seed['a']}}."

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {{"focus": "Basic Step", "goal": "Solve for the first variable."}}
        return super().get_drill_intent(level)
"""
    with open(os.path.join(target_dir, "solver.py"), "w", encoding="utf-8") as f:
        f.write(solver_content)

    # 2. metadata.json Boilerplate
    metadata = {
        "title": f"AIME {year} {exam} Problem {p_id[1:]}",
        "domain": "Algebra",
        "dna_tag": "UNKNOWN",
        "difficulty_band": band,
        "has_image_support": False,
        "dna_tags": ["Standard"],
        "drill_config": {
            "L1": "Basic concept check",
            "L2": "Intermediate step",
            "L3": "Full problem"
        }
    }
    with open(os.path.join(target_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    # 3. template.md Boilerplate
    template_content = """# Problem Scenario
{NARRATIVE_INSTRUCTION}
"""
    with open(os.path.join(target_dir, "template.md"), "w", encoding="utf-8") as f:
        f.write(template_content)

    print(f"✅ Scaffolded engine for {year} {exam} {p_id} in {band}")
    print(f"📍 Directory: {target_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AIME Engine Scaffolder")
    parser.add_argument("year", help="Exam year (e.g. 2024)")
    parser.add_argument("exam", help="Exam type (e.g. AIME1)")
    parser.add_argument("p_id", help="Problem ID (e.g. P01)")
    parser.add_argument("--band", default="MASTER", choices=["CHALLENGER", "EXPERT", "MASTER"])
    
    args = parser.parse_args()
    scaffold(args.year, args.exam, args.p_id, args.band)
