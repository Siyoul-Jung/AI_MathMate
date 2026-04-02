import sys
import os
from pathlib import Path

# backend 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine_v2.modules.number_theory.number_theory_modular_arithmetic import NumberTheoryModularArithmeticModule
from engine_v2.modules.number_theory.number_theory_prime_factorization import NumberTheoryPrimeFactorizationModule
from engine_v2.modules.number_theory.number_theory_divisibility_rules import NumberTheoryDivisibilityRulesModule
from engine_v2.modules.number_theory.number_theory_gcd_lcm_properties import NumberTheoryGcdLcmPropertiesModule
from engine_v2.modules.number_theory.number_theory_chinese_remainder_theorem import NumberTheoryChineseRemainderTheoremModule
from engine_v2.modules.number_theory.number_theory_diophantine_equations import NumberTheoryDiophantineEquationsModule
from engine_v2.modules.number_theory.number_theory_euler_totient_phi import NumberTheoryEulerTotientPhiModule
from engine_v2.modules.number_theory.number_theory_base_conversions import NumberTheoryBaseConversionsModule
from engine_v2.modules.number_theory.number_theory_fermat_little_theorem import NumberTheoryFermatLittleTheoremModule
from engine_v2.modules.number_theory.number_theory_arithmetic_functions import NumberTheoryArithmeticFunctionsModule

modules = [
    NumberTheoryModularArithmeticModule(),
    NumberTheoryPrimeFactorizationModule(),
    NumberTheoryDivisibilityRulesModule(),
    NumberTheoryGcdLcmPropertiesModule(),
    NumberTheoryChineseRemainderTheoremModule(),
    NumberTheoryDiophantineEquationsModule(),
    NumberTheoryEulerTotientPhiModule(),
    NumberTheoryBaseConversionsModule(),
    NumberTheoryFermatLittleTheoremModule(),
    NumberTheoryArithmeticFunctionsModule()
]

output_file = "backend/engine_v2/test_batch3_number_theory_output.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("=== Batch 3 (Number Theory) 10 Modules Full Test ===\n\n")
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
