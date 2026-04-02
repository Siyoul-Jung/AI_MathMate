import os
import sys
import json

# Add backend to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from amc_engine.pipeline_manager import ProblemFactory
from amc_engine.generators.generator_llm import generate_variant_with_gemini

def prototype_p15_logic():
    factory = ProblemFactory()
    year, exam, p_id = "2025", "AIME1", "P15"
    
    print(f"--- 🎲 Generating P15 Mock Variant ---")
    # Silence the factory's stdout if possible, or just let it print
    variant = factory.process_new_variant(year, exam, p_id, mode="MOCK")
    
    if not variant:
        print("❌ Generation failed.")
        return

    explanation = variant['5_solution']['step_by_step']
    if isinstance(explanation, list):
        explanation = "\n".join(explanation)

    print(f"\n--- 🧠 Analyzing Explanation for Logic Steps ---")
    analysis_prompt = f"""
    [SYSTEM ROLE: AIME PEDAGOGY ANALYST]
    Analyze the following AIME solution (Problem 15 level) and extract a sequence of SUBSTANTIVE mathematical logic steps required to solve it.
    
    [STRICT RULES]
    1. EXCLUDE TRIVIAL FINAL STEPS: Do not create a separate step for "Calculate the final answer modulo 1000" or simple arithmetic formatting.
    2. REDUCTIVE SUB-PROBLEMS: Each step must be a standalone mathematical bridge that simplifies the core problem (e.g. Base Conversion, Modular Lifting, Symmetry Application).
    3. PEDAGOGICAL VALUE: Only include steps that would make for a meaningful "Drill" question for a student.
    
    [SOLUTION]
    {explanation}
    
    [OUTPUT FORMAT (JSON)]
    {{
      "summary": "High-level summary of the solution logic",
      "logic_steps": [
        {{ 
          "step_id": 1, 
          "description": "Short pedagogical description", 
          "concept": "Mathematical concept",
          "goal": "Specific goal for a Drill question"
        }}
      ]
    }}
    """

    
    result = generate_variant_with_gemini(analysis_prompt)
    try:
        analysis = json.loads(result)
        
        output_data = {
            "variant_id": variant.get('engine_id'),
            "seed": variant.get('4_solver_payload'),
            "narrative": variant.get('3_presentation', {}).get('problem_statement'),
            "analysis": analysis
        }
        
        print("\n=== [PROTOTYPE RESULT] ===")
        print(json.dumps(output_data, indent=2, ensure_ascii=False))
        
        # Save results for artifact
        with open("tmp_prototype_result.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"❌ Analysis parsing failed: {e}")
        print(result)

if __name__ == "__main__":
    prototype_p15_logic()
