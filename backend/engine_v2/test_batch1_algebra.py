import sys
import json
import os
from pathlib import Path

# backend 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine_v2.modules.algebra.algebra_absolute_value import AlgebraAbsoluteValueModule
from engine_v2.modules.algebra.algebra_basic_manipulation import AlgebraBasicManipulationModule
from engine_v2.modules.algebra.algebra_binomial_theorem import AlgebraBinomialTheoremModule
from engine_v2.modules.algebra.algebra_complex_numbers import AlgebraComplexNumbersModule
from engine_v2.modules.algebra.algebra_floor_ceiling_functions import AlgebraFloorCeilingFunctionsModule
from engine_v2.modules.algebra.algebra_functions_and_properties import AlgebraFunctionsAndPropertiesModule
from engine_v2.modules.algebra.algebra_inequalities import AlgebraInequalitiesModule
from engine_v2.modules.algebra.algebra_kinematics import AlgebraKinematicsModule
from engine_v2.modules.algebra.algebra_logarithms_exponents import AlgebraLogarithmsExponentsModule
from engine_v2.modules.algebra.algebra_matrices_determinants import AlgebraMatricesDeterminantsModule
from engine_v2.modules.algebra.algebra_polynomials_vieta import AlgebraPolynomialsVietaModule
from engine_v2.modules.algebra.algebra_sequences_series_recurrence import AlgebraSequencesSeriesRecurrenceModule
from engine_v2.modules.algebra.algebra_statistics import AlgebraStatisticsModule
from engine_v2.modules.algebra.algebra_systems_of_equations import AlgebraSystemsOfEquationsModule
from engine_v2.modules.algebra.algebra_trigonometry import AlgebraTrigonometryModule

modules = [
    AlgebraAbsoluteValueModule(),
    AlgebraBasicManipulationModule(),
    AlgebraBinomialTheoremModule(),
    AlgebraComplexNumbersModule(),
    AlgebraFloorCeilingFunctionsModule(),
    AlgebraFunctionsAndPropertiesModule(),
    AlgebraInequalitiesModule(),
    AlgebraKinematicsModule(),
    AlgebraLogarithmsExponentsModule(),
    AlgebraMatricesDeterminantsModule(),
    AlgebraPolynomialsVietaModule(),
    AlgebraSequencesSeriesRecurrenceModule(),
    AlgebraStatisticsModule(),
    AlgebraSystemsOfEquationsModule(),
    AlgebraTrigonometryModule()
]

output_file = "backend/engine_v2/test_batch1_algebra_output.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("=== Batch 1 (Algebra) 15 Modules Full Test ===\n\n")
    for m in modules:
        f.write(f"[{m.META.name}] ({m.META.module_id})\n")
        try:
            # Test 5 times for each to check stability
            for i in range(5):
                seed = m.generate_seed(difficulty_hint=10.0 + i)
                valid_seed, reason_seed = m.validate_seed(seed)
                answer = m.execute(seed)
                valid_ans, reason_ans = m.validate_answer(answer)
                steps = m.get_logic_steps(seed)
                
                f.write(f"  Trial {i+1}: Seed={seed}, Ans={answer} ({'✅' if valid_ans else '❌'})\n")
            f.write("-" * 50 + "\n")
        except Exception as e:
            f.write(f"  ❌ ALERT: Error in module: {e}\n")
            f.write("-" * 50 + "\n")

print(f"Test completed. Results saved to {output_file}")
