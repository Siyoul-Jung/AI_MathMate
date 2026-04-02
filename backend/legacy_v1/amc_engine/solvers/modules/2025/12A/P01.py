import random
import re

class Solver:
    # 1. 이 유형 전용 테마 풀
    THEMES = ["Fintech", "Bio-medical", "Quantum Computing", "Deep Learning", "Chemical Engineering", "Supply Chain"]

    def __init__(self, payload=None, config=None):
        self.payload = payload or {}
        self.config = config or {}

    @classmethod
    def generate_seed(cls):
        while True:
            v1 = round(random.uniform(2.0, 15.0), 1)
            v2 = round(random.uniform(v1 * 1.5, v1 * 4.0), 1)
            delay = round(random.choice([0.25, 0.5, 0.75, 1.0, 1.25, 1.5]), 2)
            
            relative_v = v2 - v1
            catch_up_time = (v1 * delay) / relative_v
            total_t = delay + catch_up_time
            
            if total_t.is_integer() or (total_t * 4).is_integer():
                return {
                    'v1': v1,
                    'v2': v2,
                    'delay': delay,
                    'expected_t': round(total_t, 2)
                }

    def execute(self):
        v1 = self.payload.get('v1')
        v2 = self.payload.get('v2')
        delay = self.payload.get('delay')
        relative_v = v2 - v1
        catch_up_time = (v1 * delay) / relative_v
        return round(delay + catch_up_time, 2)

    # 2. 이 유형 전용 프롬프트 인젝션
    @classmethod
    def get_injection_prompt(cls, seed, selected_theme):
        import json
        return f"""
\n\n==================================================
🚨 [SYSTEM RULE: STRICT DATA INTEGRITY] 🚨
1. YOU MUST USE THESE NUMBERS AS-IS: {json.dumps(seed)}
2. DO NOT USE FRACTIONS. USE DECIMAL NUMBERS IN THE STATEMENT.
3. CONTEXT: Create a professional scenario in the field of "{selected_theme}".
4. PROHIBITION: NO VEHICLES, NO SUBMARINES, NO PHYSICAL DISTANCE.
   Focus on 'Processing Rates' or 'Resource Accumulation' (e.g., data, cells, money).
==================================================
"""

    # 3. 이 유형 전용 지문 검증 로직
    @classmethod
    def verify_narrative(cls, narrative, seed):
        found_nums = [float(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", narrative)]
        for target in [seed.get('v1'), seed.get('v2'), seed.get('delay')]:
            if not any(abs(target - found) < 0.01 for found in found_nums):
                return False, f"수치 누락/변형 감지: {target}"
        return True, "OK"