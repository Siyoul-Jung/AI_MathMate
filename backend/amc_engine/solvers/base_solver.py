import abc

class BaseSolver(abc.ABC):
    """모든 AMC Solver의 근간이 되는 추상 클래스"""
    
    def __init__(self, variables, constraints):
        self.vars = variables
        self.constraints = constraints
    
    @abc.abstractmethod
    def check_constraints(self):
        """수학적 제약 조건(Constraints)을 확인합니다. [cite: 16-18, 211-213]"""
        pass

    @abc.abstractmethod
    def solve(self):
        """실제 정답(Value)을 연산합니다."""
        pass
    
    def execute(self):
        """제약 조건 확인 후 정답을 반환하는 실행 흐름"""
        is_valid, msg = self.check_constraints()
        if not is_valid:
            raise ValueError(f"Constraint Violation: {msg}") [cite: 16-18, 211-213]
        return self.solve()