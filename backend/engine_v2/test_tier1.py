import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine_v2.modules.algebra.algebra_polynomials_vieta import AlgebraPolynomialsVietaModule
from engine_v2.modules.geometry.geometry_circles_tangency import GeometryCirclesTangencyModule
from engine_v2.modules.number_theory.nt_power_congruence import NTPowerCongruenceModule
from engine_v2.modules.combinatorics.comb_path_counting import CombPathCountingModule
from engine_v2.modules.algebra.algebra_sequences_series_recurrence import AlgebraSequencesSeriesRecurrenceModule

modules = [
    AlgebraPolynomialsVietaModule(),
    GeometryCirclesTangencyModule(),
    NTPowerCongruenceModule(),
    CombPathCountingModule(),
    AlgebraSequencesSeriesRecurrenceModule()
]

with open("backend/engine_v2/test_tier1_output.txt", "w", encoding="utf-8") as f:
    f.write("=== Tier 1 Modules (5 Core) Seed Generation Test ===\n\n")
    for m in modules:
        f.write(f"[{m.META.name}] ({m.META.module_id})\n")
        try:
            seed = m.generate_seed(difficulty_hint=12.0)
            valid_seed, reason_seed = m.validate_seed(seed)
            answer = m.execute(seed)
            valid_ans, reason_ans = m.validate_answer(answer)
            steps = m.get_logic_steps(seed)
            
            f.write(f" - Seed: {seed}\n")
            f.write(f" - Seed Validation: {'✅' if valid_seed else '❌'} {reason_seed}\n")
            f.write(f" - Calculated Answer: {answer}\n")
            f.write(f" - Answer Validation: {'✅' if valid_ans else '❌'} {reason_ans}\n")
            f.write(f" - Logic Steps: {len(steps)} steps generated.\n")
            f.write("-" * 50 + "\n")
        except Exception as e:
            f.write(f" - ❌ 로직 실행 에러 발생: {e}\n")
            f.write("-" * 50 + "\n")
