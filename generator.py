from manager import ProblemManager

if __name__ == "__main__":
    # 통합 관리자 인스턴스 생성
    manager = ProblemManager()
    
    print("=== 한국 중등 1-1 수학 문제 생성 테스트 ===")

    # 1. 소인수분해 (STD-11-01)
    print("\n[STD-11-01] 소인수분해의 이해")
    print(f"지원 유형: {manager.list_supported_types('KR', 'Middle_1-1', 'STD-11-01')}")
    
    print("\n--- T01: 소수와 합성수 (Easy) ---")
    print(manager.get_problem("KR", "Middle_1-1", "STD-11-01", "T01", difficulty="Easy"))

    print("\n--- T09: 제곱수 만들기 (Hard) ---")
    print(manager.get_problem("KR", "Middle_1-1", "STD-11-01", "T09", difficulty="Hard"))
    
    # 2. 최대공약수와 최소공배수 (STD-11-02)
    print("\n[STD-11-02] 최대공약수와 최소공배수")
    
    print("\n--- T13: 최대공약수 활용 (Normal) ---")
    print(manager.get_problem("KR", "Middle_1-1", "STD-11-02", "T13"))

    # 3. 정수와 유리수 (STD-11-03)
    print("\n[STD-11-03] 정수와 유리수")
    
    print("\n--- T16: 정수와 유리수의 분류 ---")
    print(manager.get_problem("KR", "Middle_1-1", "STD-11-03", "T16"))

    # 4. 유리수의 사칙계산 (STD-11-04)
    print("\n[STD-11-04] 유리수의 사칙계산")
    
    print("\n--- T21: 유리수의 덧셈/뺄셈 ---")
    print(manager.get_problem("KR", "Middle_1-1", "STD-11-04", "T21"))

    # 5. 문자의 사용과 식의 값 (STD-11-05)
    print("\n[STD-11-05] 문자의 사용과 식의 값")
    
    print("\n--- T29: 문자를 사용한 식 세우기 ---")
    print(manager.get_problem("KR", "Middle_1-1", "STD-11-05", "T29"))