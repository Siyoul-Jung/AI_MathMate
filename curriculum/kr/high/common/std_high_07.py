import random
from core.base import BaseTMaster

class High07_1_MatrixOp_Master(BaseTMaster):
    """
    고등 공통수학 - 행렬 (행렬의 덧셈, 뺄셈, 실수배)
    """
    def __init__(self):
        super().__init__("High07_1", "행렬의 연산")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 2x2 행렬 A, B 생성
        def gen_matrix():
            return [[random.randint(-5, 5) for _ in range(2)] for _ in range(2)]
        
        A = gen_matrix()
        B = gen_matrix()
        k = random.randint(2, 4) * random.choice([-1, 1])
        
        op_type = random.choice(["add", "sub", "scalar"])
        
        if op_type == "add":
            # A + B
            res = [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]
            q_expr = "A + B"
            expl_op = "각 성분끼리 더합니다."
        elif op_type == "sub":
            # A - B
            res = [[A[i][j] - B[i][j] for j in range(2)] for i in range(2)]
            q_expr = "A - B"
            expl_op = "각 성분끼리 뺍니다."
        else:
            # kA
            res = [[k * A[i][j] for j in range(2)] for i in range(2)]
            q_expr = f"{k}A"
            expl_op = f"각 성분에 {k}를 곱합니다."
            
        # 행렬 포맷팅 (LaTeX pmatrix)
        def mat_to_tex(M):
            return f"\\begin{{pmatrix}} {M[0][0]} & {M[0][1]} \\\\ {M[1][0]} & {M[1][1]} \\end{{pmatrix}}"
            
        A_tex = mat_to_tex(A)
        B_tex = mat_to_tex(B)
        res_tex = mat_to_tex(res)
        
        question = f"두 행렬 $A = {A_tex}, B = {B_tex}$ 에 대하여, ${q_expr}$ 를 구하시오."
        if op_type == "scalar":
            question = f"행렬 $A = {A_tex}$ 에 대하여, ${q_expr}$ 를 구하시오."
            
        logic_steps = self.get_logic_steps("High07_1", op=expl_op)
        
        data = {
            "question": question,
            "answer": f"${res_tex}$",
            "explanation": [
                f"행렬의 연산 성질에 따라 {expl_op}",
                f"계산하면: ${res_tex}$"
            ],
            "logic_steps": logic_steps,
            "strategy": "행렬의 덧셈과 뺄셈은 같은 위치의 성분끼리 계산하고, 실수배는 모든 성분에 실수를 곱합니다."
        }
        
        if q_type == "multi":
            # 오답 생성
            options_set = {f"${res_tex}$"}
            while len(options_set) < 4:
                # 임의의 오답 행렬
                fake = [[res[i][j] + random.randint(-2, 2) for j in range(2)] for i in range(2)]
                options_set.add(f"${mat_to_tex(fake)}$")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High07_2_MatrixMul_Master(BaseTMaster):
    """
    고등 공통수학 - 행렬 (행렬의 곱셈)
    """
    def __init__(self):
        super().__init__("High07_2", "행렬의 곱셈")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 2x2 행렬 A, B
        def gen_matrix():
            return [[random.randint(-3, 3) for _ in range(2)] for _ in range(2)]
            
        A = gen_matrix()
        B = gen_matrix()
        
        # AB 계산
        # C[i][j] = sum(A[i][k] * B[k][j])
        res = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    res[i][j] += A[i][k] * B[k][j]
                    
        def mat_to_tex(M):
            return f"\\begin{{pmatrix}} {M[0][0]} & {M[0][1]} \\\\ {M[1][0]} & {M[1][1]} \\end{{pmatrix}}"
            
        A_tex = mat_to_tex(A)
        B_tex = mat_to_tex(B)
        res_tex = mat_to_tex(res)
        
        logic_steps = self.get_logic_steps("High07_2")
        
        data = {
            "question": f"두 행렬 $A = {A_tex}, B = {B_tex}$ 에 대하여, $AB$ 를 구하시오.",
            "answer": f"${res_tex}$",
            "explanation": [
                "행렬의 곱셈은 앞 행렬의 행과 뒤 행렬의 열의 성분을 차례로 곱하여 더합니다.",
                f"(1행 1열): ${A[0][0]}\\times{B[0][0]} + {A[0][1]}\\times{B[1][0]} = {res[0][0]}$",
                f"(1행 2열): ${A[0][0]}\\times{B[0][1]} + {A[0][1]}\\times{B[1][1]} = {res[0][1]}$",
                f"(2행 1열): ${A[1][0]}\\times{B[0][0]} + {A[1][1]}\\times{B[1][0]} = {res[1][0]}$",
                f"(2행 2열): ${A[1][0]}\\times{B[0][1]} + {A[1][1]}\\times{B[1][1]} = {res[1][1]}$",
                f"따라서 $AB = {res_tex}$"
            ],
            "logic_steps": logic_steps,
            "strategy": "행렬의 곱셈 AB는 A의 행벡터와 B의 열벡터의 내적을 성분으로 갖습니다. 교환법칙이 성립하지 않음에 주의하세요."
        }
        
        if q_type == "multi":
            options_set = {f"${res_tex}$"}
            # 오답: BA (교환법칙 성립 안함)
            res_ba = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        res_ba[i][j] += B[i][k] * A[k][j]
            options_set.add(f"${mat_to_tex(res_ba)}$")
            
            while len(options_set) < 4:
                fake = [[res[i][j] + random.randint(-3, 3) for j in range(2)] for i in range(2)]
                options_set.add(f"${mat_to_tex(fake)}$")
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)