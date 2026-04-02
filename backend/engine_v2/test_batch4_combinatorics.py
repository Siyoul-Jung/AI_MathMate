import sys
import os
from pathlib import Path

# backend 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine_v2.modules.combinatorics.combinatorics_counting_principles import CombinatoricsCountingPrinciplesModule
from engine_v2.modules.combinatorics.combinatorics_permutations_combinations import CombinatoricsPermutationsCombinationsModule
from engine_v2.modules.combinatorics.combinatorics_binomial_coefficients import CombinatoricsBinomialCoefficientsModule
from engine_v2.modules.combinatorics.combinatorics_inclusion_exclusion import CombinatoricsInclusionExclusionModule
from engine_v2.modules.combinatorics.combinatorics_pigeonhole_principle import CombinatoricsPigeonholePrincipleModule
from engine_v2.modules.combinatorics.combinatorics_probability_basics import CombinatoricsProbabilityBasicsModule
from engine_v2.modules.combinatorics.combinatorics_expected_value import CombinatoricsExpectedValueModule
from engine_v2.modules.combinatorics.combinatorics_geometric_probability import CombinatoricsGeometricProbabilityModule
from engine_v2.modules.combinatorics.combinatorics_recursion_relations import CombinatoricsRecursionRelationsModule
from engine_v2.modules.combinatorics.combinatorics_generating_functions import CombinatoricsGeneratingFunctionsModule
from engine_v2.modules.combinatorics.combinatorics_graph_theory_basics import CombinatoricsGraphTheoryBasicsModule
from engine_v2.modules.combinatorics.combinatorics_game_theory_basics import CombinatoricsGameTheoryBasicsModule
from engine_v2.modules.combinatorics.combinatorics_partitions_numbers import CombinatoricsPartitionsNumbersModule
from engine_v2.modules.combinatorics.combinatorics_invariant_principle import CombinatoricsInvariantPrincipleModule

modules = [
    CombinatoricsCountingPrinciplesModule(),
    CombinatoricsPermutationsCombinationsModule(),
    CombinatoricsBinomialCoefficientsModule(),
    CombinatoricsInclusionExclusionModule(),
    CombinatoricsPigeonholePrincipleModule(),
    CombinatoricsProbabilityBasicsModule(),
    CombinatoricsExpectedValueModule(),
    CombinatoricsGeometricProbabilityModule(),
    CombinatoricsRecursionRelationsModule(),
    CombinatoricsGeneratingFunctionsModule(),
    CombinatoricsGraphTheoryBasicsModule(),
    CombinatoricsGameTheoryBasicsModule(),
    CombinatoricsPartitionsNumbersModule(),
    CombinatoricsInvariantPrincipleModule()
]

output_file = "backend/engine_v2/test_batch4_combinatorics_output.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("=== Batch 4 (Combinatorics) 14 Modules Full Test ===\n\n")
    for m in modules:
        f.write(f"[{m.META.name}] ({m.META.module_id})\n")
        try:
            for i in range(5):
                seed = m.generate_seed(difficulty_hint=10.0 + i)
                answer = m.execute(seed)
                valid_ans, reason_ans = m.validate_answer(answer)
                f.write(f"  Trial {i+1}: Seed={seed}, Ans={answer} ({'✅' if valid_ans else '❌'})\n")
            f.write("-" * 50 + "\n")
        except Exception as e:
            f.write(f"  ❌ ALERT: Error in module: {e}\n")
            f.write("-" * 50 + "\n")

print(f"Test completed. Results saved to {output_file}")
