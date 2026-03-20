import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

class High12_1_SetDef_Master(BaseTMaster):
    """
    고등 공통수학 - 집합 (집합의 뜻과 표현, 부분집합)
    """
    def __init__(self):
        super().__init__("High12_1", "집합의 뜻과 부분집합")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # A = {x | x is a divisor of n}
        n = random.choice([6, 8, 10, 12, 15, 16, 18, 20, 24])
        
        divisors = []
        for i in range(1, n + 1):
            if n % i == 0:
                divisors.append(i)
        
        count = len(divisors)
        num_subsets = 2 ** count
        
        q_type_internal = random.choice(["elements", "subsets"])
        
        if q_type_internal == "elements":
            # 원소의 합 구하기
            ans = sum(divisors)
            q_text = f"집합 $A = \\{{ x | x \\text{{는 }} {n} \\text{{의 양의 약수}} \\}}$ 일 때, 집합 $A$의 모든 원소의 합을 구하시오."
            expl = [
                f"${n}$의 양의 약수는 {', '.join(map(str, divisors))} 입니다.",
                f"따라서 모든 원소의 합은 ${sum(divisors)}$ 입니다."
            ]
            logic_steps = self.get_logic_steps("High12_1_elements", n=n)
            
        else:
            # 부분집합의 개수
            ans = num_subsets
            q_text = f"집합 $A = \\{{ x | x \\text{{는 }} {n} \\text{{의 양의 약수}} \\}}$ 일 때, 집합 $A$의 부분집합의 개수를 구하시오."
            expl = [
                f"${n}$의 양의 약수는 {', '.join(map(str, divisors))} 이므로 원소의 개수 $n(A) = {count}$ 입니다.",
                f"부분집합의 개수는 $2^{{{count}}} = {num_subsets}$ 입니다."
            ]
            logic_steps = self.get_logic_steps("High12_1_subsets", n=n, count=count)

        data = {
            "question": q_text,
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "strategy": "조건제시법으로 주어진 집합의 원소를 먼저 나열해봅니다."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 10) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High12_2_SetOp_Master(BaseTMaster):
    """
    고등 공통수학 - 집합 (집합의 연산)
    """
    def __init__(self):
        super().__init__("High12_2", "집합의 연산")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # U = {1, 2, ..., 10}
        U = set(range(1, 11))
        
        # A, B are random subsets of U
        size_a = random.randint(3, 5)
        size_b = random.randint(3, 5)
        
        A = set(random.sample(list(U), size_a))
        B = set(random.sample(list(U), size_b))
        
        op = random.choice(["union", "intersection", "difference_ab", "difference_ba"])
        
        if op == "union":
            res = A | B
            op_sym = "A \\cup B"
            op_name = "합집합"
        elif op == "intersection":
            res = A & B
            op_sym = "A \\cap B"
            op_name = "교집합"
        elif op == "difference_ab":
            res = A - B
            op_sym = "A - B"
            op_name = "차집합"
        else:
            res = B - A
            op_sym = "B - A"
            op_name = "차집합"
            
        # Format sets for display
        def format_set(s):
            return "\\{" + ", ".join(map(str, sorted(list(s)))) + "\\}"
            
        A_str = format_set(A)
        B_str = format_set(B)
        res_str = format_set(res)
        
        # If empty set
        if not res:
            res_str = "\\emptyset"
            
        logic_steps = self.get_logic_steps("High12_2", op_name=op_name)
        
        data = {
            "question": f"두 집합 $A = {A_str}, B = {B_str}$ 에 대하여, ${op_sym}$ 를 구하시오.",
            "answer": f"${res_str}$",
            "explanation": [
                f"$A = {A_str}$",
                f"$B = {B_str}$",
                f"${op_sym}$ 은 {op_name}을 의미하므로",
                f"구하는 집합은 ${res_str}$ 입니다."
            ],
            "logic_steps": logic_steps,
            "strategy": "벤 다이어그램을 그리거나 원소를 나열하여 연산 결과를 찾습니다."
        }
        
        if q_type == "multi":
            # Distractors
            options_set = {res_str}
            
            # Wrong operations
            options_set.add(format_set(A | B))
            options_set.add(format_set(A & B))
            options_set.add(format_set(A - B))
            options_set.add(format_set(B - A))
            
            if "\\emptyset" not in options_set:
                 options_set.add("\\emptyset")
                 
            # Ensure 4 options
            options = list(options_set)
            if len(options) > 4: options = random.sample(options, 4)
            if res_str not in options: options[0] = res_str
            
            options = [f"${o}$" if not o.startswith("$") else o for o in options]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
