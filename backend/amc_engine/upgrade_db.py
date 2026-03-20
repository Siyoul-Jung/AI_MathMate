import sqlite3
import os

def clean_aime_data(db_name="amc_factory.db"):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
    
    if not os.path.exists(db_path):
        print("❌ DB 파일을 찾을 수 없습니다.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # exam_type이 'AIME1'인 데이터만 골라서 삭제
    cursor.execute("DELETE FROM generated_problems WHERE exam_type = 'AIME1'")
    deleted_count = cursor.rowcount  # 몇 개가 지워졌는지 확인

    conn.commit()
    conn.close()

    print(f"✨ 청소 완료! 총 {deleted_count}개의 AIME 테스트 데이터가 DB에서 영구 삭제되었습니다.")
    print("기존 AMC 12A 데이터는 안전하게 보존되어 있습니다.")

if __name__ == "__main__":
    clean_aime_data()