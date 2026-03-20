import random

class ProblemTemplate:
    """
    교과서나 문제집의 전형적인 유형(Template)을 관리하는 클래스입니다.
    문장 구조(Skeleton)는 고정하고, 변수(Variables)만 제약 조건에 맞춰 생성합니다.
    """
    def __init__(self, 
                 question_format: str, 
                 variable_gen_func: callable, 
                 answer_calc_func: callable,
                 explanation_format: str = "",
                 logic_step_gen_func: callable = None,
                 options_gen_func: callable = None):
        """
        :param question_format: 문제 문장 템플릿 (예: "y가 x에 정비례하고 x={x}일 때...")
        :param variable_gen_func: 변수 딕셔너리를 반환하는 함수 (제약 조건 로직 포함)
        :param answer_calc_func: 변수를 받아 정답을 계산하는 함수
        :param explanation_format: 해설 템플릿
        :param logic_step_gen_func: 로직 스텝 생성 함수 (옵션)
        :param options_gen_func: 객관식 보기 생성 함수 (옵션)
        """
        self.q_fmt = question_format
        self.v_gen = variable_gen_func
        self.a_calc = answer_calc_func
        self.e_fmt = explanation_format
        self.ls_gen = logic_step_gen_func
        self.opt_gen = options_gen_func

    def generate(self, q_type="short_answer"):
        # 1. 제약 조건이 반영된 변수 생성
        variables = self.v_gen()
        
        # 2. 정답 계산
        answer = self.a_calc(variables)
        
        # 3. 데이터 조립
        data = {
            "question": self.q_fmt.format(**variables),
            "answer": answer,
            "explanation": self.e_fmt.format(**variables, answer=answer),
            "logic_steps": self.ls_gen(variables) if self.ls_gen else [],
            "variables": variables
        }

        # 4. 객관식 보기 생성 (필요 시)
        if q_type == "multi" and self.opt_gen:
            data["options"] = self.opt_gen(answer, variables)
            
        return data