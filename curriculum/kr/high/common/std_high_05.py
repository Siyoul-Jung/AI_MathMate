import random
from core.base import BaseTMaster

class High05_1_AbsIneq_Master(BaseTMaster):
    """
    고등 공통수학 - 여러 가지 부등식 (절댓값 기호를 포함한 일차부등식)
    """
    def __init__(self):
        super().__init__("High05_1", "절댓값 부등식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # |x - a| < b  or  |x - a| > b
        a = random.randint(-5, 5)
        b = random.randint(1, 9)
        
        ineq_type = random.choice(["less", "greater"])
        
        if ineq_type == "less":
            # |x - a| < b  =>  -b < x - a < b  =>  a-b < x < a+b
            lower = a - b
            upper = a + b
            question = f"$|x - {a}| < {b}$" if a >= 0 else f"$|x + {abs(a)}| < {b}$"
            answer = f"${lower} < x < {upper}$"
            
            logic_steps = self.get_logic_steps("High05_1_less", a=a, b=b, lower=lower, upper=upper)
            
            explanation = [
                f"절댓값의 성질에 의해 $-{b} < x - {a} < {b}$",
                f"각 변에 {a}를 더하면 ${a-b} < x < {a+b}$",
                f"따라서 해는 ${lower} < x < {upper}$"
            ]
        else:
            # |x - a| > b  =>  x - a < -b or x - a > b  =>  x < a-b or x > a+b
            lower = a - b
            upper = a + b
            question = f"$|x - {a}| > {b}$" if a >= 0 else f"$|x + {abs(a)}| > {b}$"
            answer = f"$x < {lower}$ 또는 $x > {upper}$"
            
            logic_steps = self.get_logic_steps("High05_1_greater", a=a, b=b, lower=lower, upper=upper)
            
            explanation = [
                f"절댓값의 성질에 의해 $x - {a} < -{b}$ 또는 $x - {a} > {b}$",
                f"각 부등식을 풀면 $x < {a-b}$ 또는 $x > {a+b}$",
                f"따라서 해는 ${answer}$"
            ]

        data = {
            "question": f"다음 부등식을 푸시오.\n{question}",
            "answer": answer,
            "explanation": explanation,
            "logic_steps": logic_steps,
            "strategy": "절댓값 기호 안의 식의 범위를 나누거나, |X| < a ⇔ -a < X < a 성질을 이용합니다."
        }
        
        if q_type == "multi":
            # 오답 생성
            options_set = {answer}
            while len(options_set) < 4:
                fa = a + random.randint(-2, 2)
                fb = b + random.randint(-1, 2)
                if fb <= 0: fb = 1
                
                if ineq_type == "less":
                    fake_ans = f"${fa-fb} < x < {fa+fb}$"
                else:
                    fake_ans = f"$x < {fa-fb}$ 또는 $x > {fa+fb}$"
                options_set.add(fake_ans)
            
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High05_2_QuadIneq_Master(BaseTMaster):
    """
    고등 공통수학 - 여러 가지 부등식 (이차부등식)
    """
    def __init__(self):
        super().__init__("High05_2", "이차부등식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # (x - alpha)(x - beta) > 0 or < 0
        alpha = random.randint(-5, 5)
        beta = random.randint(-5, 5)
        while alpha == beta: beta = random.randint(-5, 5)
        
        if alpha > beta: alpha, beta = beta, alpha
        
        # 전개: x^2 - (alpha+beta)x + alpha*beta
        b = -(alpha + beta)
        c = alpha * beta
        
        ineq_type = random.choice(["less", "greater"])
        
        expr = f"x^2"
        if b > 0: expr += f" + {b}x"
        elif b < 0: expr += f" - {abs(b)}x"
        
        if c > 0: expr += f" + {c}"
        elif c < 0: expr += f" - {abs(c)}"
        
        if ineq_type == "less":
            # < 0 => 사이값
            question = f"${expr} < 0$"
            answer = f"${alpha} < x < {beta}$"
            logic_steps = self.get_logic_steps("High05_2_less", alpha=alpha, beta=beta)
            explanation = [
                f"좌변을 인수분해하면 $(x - {alpha})(x - {beta}) < 0$",
                f"이차항의 계수가 양수이고 0보다 작으므로 두 근 사이의 범위입니다.",
                f"따라서 ${alpha} < x < {beta}$"
            ]
        else:
            # > 0 => 가장자리값
            question = f"${expr} > 0$"
            answer = f"$x < {alpha}$ 또는 $x > {beta}$"
            logic_steps = self.get_logic_steps("High05_2_greater", alpha=alpha, beta=beta)
            explanation = [
                f"좌변을 인수분해하면 $(x - {alpha})(x - {beta}) > 0$",
                f"이차항의 계수가 양수이고 0보다 크므로 큰 근보다 크거나 작은 근보다 작습니다.",
                f"따라서 ${answer}$"
            ]

        data = {
            "question": f"다음 이차부등식을 푸시오.\n{question}",
            "answer": answer,
            "explanation": explanation,
            "logic_steps": logic_steps,
            "strategy": "이차방정식의 해를 구한 뒤, 그래프의 개형을 그려 부등호 방향에 맞는 범위를 찾습니다."
        }
        
        if q_type == "multi":
            options_set = {answer}
            while len(options_set) < 4:
                fa = alpha + random.randint(-1, 1)
                fb = beta + random.randint(-1, 1)
                if fa >= fb: fa, fb = fb - 1, fa + 1
                
                if ineq_type == "less":
                    if random.random() < 0.5: fake = f"$x < {fa}$ 또는 $x > {fb}$"
                    else: fake = f"${fa} < x < {fb}$"
                else:
                    if random.random() < 0.5: fake = f"${fa} < x < {fb}$"
                    else: fake = f"$x < {fa}$ 또는 $x > {fb}$"
                options_set.add(fake)
                
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)