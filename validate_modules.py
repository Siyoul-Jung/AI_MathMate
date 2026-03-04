import sys
import traceback
import os
from manager import ProblemManager

def validate_all_modules():
    print("=== MathMate 모듈 일괄 검증 시작 ===")
    manager = ProblemManager()
    
    # 0. 데이터 무결성 검사 (Logic Steps 파편화 확인)
    logic_steps_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "logic_steps")
    if os.path.exists(logic_steps_dir):
        fragmented = [f for f in os.listdir(logic_steps_dir) if f.startswith("STD-") and f.endswith(".json")]
        if fragmented:
            print(f"⚠️  [Warning] 파편화된 Logic Steps 파일 {len(fragmented)}개가 발견되었습니다. 'organize_logic_steps.py'를 실행하여 정리해주세요.")

    report = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "errors": []
    }
    
    # Registry 구조: {curriculum: {grade: {standard: {t_code: master}}}}
    for curriculum, grades in manager.registry.items():
        for grade, standards in grades.items():
            for std, types in standards.items():
                if not types:
                    continue
                
                print(f"\n[{curriculum} > {grade} > {std}] ({len(types)}개 유형)")
                
                for t_code in types.keys():
                    report["total"] += 1
                    
                    try:
                        # 1. 주관식 생성 테스트
                        res_short = manager.get_problem(curriculum, grade, std, t_code, q_type="short_answer")
                        if "error" in res_short:
                            raise Exception(f"주관식 생성 실패: {res_short['error']}")
                        if not res_short.get("question") or not str(res_short.get("answer")):
                            raise Exception("주관식 필수 필드 누락")
                            
                        # 2. 객관식 생성 테스트
                        res_multi = manager.get_problem(curriculum, grade, std, t_code, q_type="multi")
                        if "error" in res_multi:
                            raise Exception(f"객관식 생성 실패: {res_multi['error']}")
                        if not res_multi.get("options") or len(res_multi["options"]) < 2:
                            raise Exception("객관식 보기(options) 누락 또는 부족")
                        
                        print(f"  ✅ {t_code}: OK")
                        report["success"] += 1
                        
                    except Exception as e:
                        print(f"  ❌ {t_code}: {str(e)}")
                        report["failed"] += 1
                        report["errors"].append(f"[{std}-{t_code}] {str(e)}")
                        # traceback.print_exc() # 상세 에러 필요시 주석 해제

    print("\n=== 검증 결과 요약 ===")
    print(f"총 유형: {report['total']}")
    print(f"성공: {report['success']}")
    print(f"실패: {report['failed']}")
    
    if report["errors"]:
        print("\n[실패 목록]")
        for err in report["errors"]:
            print(err)

if __name__ == "__main__":
    validate_all_modules()
