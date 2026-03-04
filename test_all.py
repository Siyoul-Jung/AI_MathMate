import sys
import time
from manager import ProblemManager

def test_all_types():
    print("=== MathMate 전체 유형 자동 테스트 시작 ===")
    manager = ProblemManager()
    
    # 테스트할 커리큘럼 및 학년 설정
    curriculum = "KR"
    grade = "Middle_1-1"
    
    # 성취기준 목록을 Manager에서 동적으로 가져옴
    standards = manager.get_all_standards()
    
    total_types = 0
    success_count = 0
    fail_count = 0
    failed_types = []

    start_time = time.time()

    for std in standards:
        print(f"\n[{std}] 테스트 중...")
        
        # 현재 성취기준의 학년 정보가 필요하다면 manifest 구조를 더 활용해야 하지만,
        # 여기서는 편의상 Middle_1-1, Middle_1-2 등을 순회하거나 
        # manager.list_supported_types가 grade를 요구하므로 일단 Middle_1-1로 시도하고
        # 없으면 Middle_1-2로 시도하는 식의 로직이 필요할 수 있습니다.
        # 하지만 현재 list_supported_types는 grade를 인자로 받으므로, 
        # 정확한 테스트를 위해선 get_all_standards가 (curriculum, grade, std) 튜플을 반환하는 것이 더 좋습니다.
        # 일단 기존 로직 유지를 위해 grade는 하드코딩된 'Middle_1-1'을 사용하되, 
        # 1-2학기(STD-12-xx)는 실패할 수 있으므로 아래와 같이 보완합니다.
        
        target_grade = "Middle_1-1"
        if "STD-12" in std: target_grade = "Middle_1-2"
        
        types = manager.list_supported_types(curriculum, target_grade, std)
        
        
        if not types:
            print(f"  Warning: {std}에 등록된 유형이 없습니다.")
            continue
            
        for t_code in types:
            total_types += 1
            try:
                # 문제 생성 시도
                result = manager.get_problem(curriculum, target_grade, std, t_code)
                
                if "error" in result:
                    print(f"  [FAIL] {t_code}: {result['error']}")
                    fail_count += 1
                    failed_types.append(f"{std}-{t_code}")
                else:
                    print(f"  [PASS] {t_code}: {result['question'][:30]}...")
                    success_count += 1
            except Exception as e:
                print(f"  [ERROR] {t_code}: {str(e)}")
                fail_count += 1
                failed_types.append(f"{std}-{t_code}")

    end_time = time.time()
    duration = end_time - start_time

    print(f"\n=== 테스트 완료 ({duration:.2f}초 소요) ===")
    print(f"총 유형 수: {total_types}, 성공: {success_count}, 실패: {fail_count}")
    
    if fail_count > 0:
        print("실패한 유형:", ", ".join(failed_types))
    else:
        print("모든 유형이 정상적으로 작동합니다! 🎉")

if __name__ == "__main__":
    test_all_types()