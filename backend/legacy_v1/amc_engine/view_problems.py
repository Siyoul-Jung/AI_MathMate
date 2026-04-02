import sqlite3
import json
import os

def view_saved_problems():
    # DB 경로 설정 (amc_engine 폴더 내부)
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amc_factory.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, narrative, correct_answer, theme FROM generated_problems")
    rows = cursor.fetchall()

    print(f"\n{'='*60}")
    print(f"📚 현재 DB에 저장된 AMC 변형 문제 목록 (총 {len(rows)}개)")
    print(f"{'='*60}")

    for row in rows:
        p_id, narrative, ans, theme = row
        print(f"\n[문제 {p_id}번] (분야: {theme} | 정답: {ans})")
        print("-" * 50)
        print(narrative)
        print("-" * 50)

    conn.close()

if __name__ == "__main__":
    view_saved_problems()