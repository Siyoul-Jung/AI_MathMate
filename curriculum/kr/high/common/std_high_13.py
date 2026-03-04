import random
from core.base import BaseTMaster
from core.math_utils import MathUtils

class High13_1_Proposition_Master(BaseTMaster):
    """
    고등 공통수학 - 명제 (명제와 조건, 진리집합)
    """
    def __init__(self):
        super().__init__("High13_1", "명제와 진리집합")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        U = list(range(1, 11))
        case = random.choice(["multiple", "divisor", "inequality"])
        
        if case == "multiple":
            k = random.randint(2, 5)
            cond_str = f"$x$는 ${k}$의 배수이다"
            truth_set = [x for x in U if x % k == 0]
        elif case == "divisor":
            k = random.choice([6, 8, 10, 12])
            cond_str = f"$x$는 ${k}$의 약수이다"
            truth_set = [x for x in U if k % x == 0]
        else:
            k = random.randint(3, 8)
            cond_str = f"$x \\ge {k}$"
            truth_set = [x for x in U if x >= k]
            
        truth_set.sort()
        ans_str = "\\{" + ", ".join(map(str, truth_set)) + "\\}"
        logic_steps = self.get_logic_steps("High13_1", cond=cond_str)
        
        data = {
            "question": f"전체집합 $U = \\{{1, 2, \\dots, 10\\}}$ 에 대하여, 조건 '$p$: {cond_str}' 의 진리집합을 구하시오.",
            "answer": f"${ans_str}$",
            "explanation": [f"조건을 만족하는 원소는 {', '.join(map(str, truth_set))} 입니다.", f"따라서 진리집합 $P = {ans_str}$"],
            "logic_steps": logic_steps,
            "strategy": "진리집합은 전체집합의 원소 중에서 해당 조건을 참이 되게 하는 원소들의 집합입니다."
        }
        
        if q_type == "multi":
            options_set = {ans_str}
            while len(options_set) < 4:
                fake_set = truth_set[:]
                if random.random() < 0.5 and len(fake_set) > 0:
                    fake_set.pop(random.randint(0, len(fake_set)-1))
                else:
                    candidates = [x for x in U if x not in fake_set]
                    if candidates: fake_set.append(random.choice(candidates))
                fake_set.sort()
                options_set.add("\\{" + ", ".join(map(str, fake_set)) + "\\}")
            options = [f"${o}$" for o in list(options_set)]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High13_2_Logic_Master(BaseTMaster):
    """
    고등 공통수학 - 명제 (명제의 참/거짓, 대우)
    """
    def __init__(self):
        super().__init__("High13_2", "명제의 참/거짓과 대우")

    def generate(self, difficulty="Normal", q_type="multi"):
        propositions = [
            {"p": "$x = 2$", "q": "$x^2 = 4$", "truth": True, "expl": "$x=2$이면 제곱하면 $4$가 됩니다."},
            {"p": "$x^2 = 4$", "q": "$x = 2$", "truth": False, "expl": "$x=-2$일 수도 있으므로 거짓입니다."},
            {"p": "$x$는 $4$의 배수", "q": "$x$는 $2$의 배수", "truth": True, "expl": "$4$의 배수는 모두 $2$의 배수입니다."},
            {"p": "$x$는 $2$의 배수", "q": "$x$는 $4$의 배수", "truth": False, "expl": "$x=2$는 $2$의 배수이지만 $4$의 배수가 아닙니다."},
            {"p": "$x > 3$", "q": "$x > 1$", "truth": True, "expl": "$3$보다 큰 수는 $1$보다 큽니다."},
            {"p": "$x > 1$", "q": "$x > 3$", "truth": False, "expl": "$x=2$는 $1$보다 크지만 $3$보다 크지 않습니다."},
            {"p": "$x$는 $6$의 배수", "q": "$x$는 $3$의 배수", "truth": True, "expl": "$6$의 배수는 $3$의 배수입니다."},
            {"p": "$x$는 $3$의 배수", "q": "$x$는 $6$의 배수", "truth": False, "expl": "$x=3$은 $3$의 배수이지만 $6$의 배수가 아닙니다."}
        ]
        
        if q_type == "short_answer":
            target = random.choice(propositions)
            p_str, q_str = target["p"], target["q"]
            def negate(s):
                if "=" in s: return s.replace("=", "\\neq")
                if ">" in s: return s.replace(">", "\\le")
                if "<" in s: return s.replace("<", "\\ge")
                if "배수" in s: return s + "가 아니다"
                return "not " + s
            ans = f"{negate(q_str)}이면 {negate(p_str)}이다"
            data = {
                "question": f"명제 '{p_str}이면 {q_str}이다'의 대우를 말하시오.",
                "answer": ans,
                "explanation": f"대우는 결론을 부정하여 가정으로, 가정을 부정하여 결론으로 보낸 명제입니다.",
                "logic_steps": self.get_logic_steps("High13_2_contrapositive"),
                "strategy": "대우: ~q -> ~p"
            }
            return self._format_response(data, q_type, difficulty)

        target_truth = random.choice([True, False])
        q_text = "다음 명제 중 참인 것은?" if target_truth else "다음 명제 중 거짓인 것은?"
        
        ans_prop = random.choice([p for p in propositions if p["truth"] == target_truth])
        # distractors 샘플링 시 모집단 크기 문제 해결을 위해 propositions 확장함
        distractors = random.sample([p for p in propositions if p["truth"] != target_truth], 3)
        options_props = distractors + [ans_prop]
        random.shuffle(options_props)
        
        data = {
            "question": q_text,
            "options": [f"{p['p']}이면 {p['q']}이다" for p in options_props],
            "answer": f"{ans_prop['p']}이면 {ans_prop['q']}이다",
            "explanation": f"'{ans_prop['p']}이면 {ans_prop['q']}이다' : {ans_prop['expl']}",
            "logic_steps": self.get_logic_steps("High13_2_truth"),
            "strategy": "반례가 하나라도 있으면 거짓입니다."
        }
        return self._format_response(data, q_type, difficulty)