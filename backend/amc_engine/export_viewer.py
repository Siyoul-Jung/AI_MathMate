import sqlite3
import os
import json

def export_to_markdown(db_name="amc_factory.db", output_file="AIME_I_01_Results.md"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, db_name)
    output_path = os.path.join(base_dir, output_file)

    if not os.path.exists(db_path):
        print(f"❌ DB 파일을 찾을 수 없습니다: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT theme, narrative, correct_answer, variables
        FROM generated_problems
        WHERE exam_type = 'AIME1'
        ORDER BY id DESC
    ''')
    rows = cursor.fetchall()

    if not rows:
        print("📭 출력할 문항이 없습니다.")
        conn.close()
        return

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 🏆 AI MathMate - AIME I Generated Problems\n\n")
        f.write("---\n\n")

        for i, row in enumerate(rows):
            theme, narrative, answer, variables = row
            try:
                var_dict = json.loads(variables)
                # P13 특유의 변수 m, n이 있으면 테마를 강제로 Expected Value로 설정
                if 'm' in var_dict and 'n' in var_dict:
                    theme = "Expected Value"
                    seed_info = f"m = {var_dict.get('m')}, n = {var_dict.get('n')}"
                elif 'k1' in var_dict:
                    theme = "Geometry Optimization"
                    seed_info = f"k1 = {var_dict.get('k1')}, k2 = {var_dict.get('k2')}"
                else:
                    seed_info = "Seed data available"
            except:
                seed_info = "Parsing error"

            f.write(f"### Problem {i+1} \n")
            f.write(f"*(Theme: {theme})*\n\n")
            f.write(f"> {narrative.strip()}\n\n")
            f.write(f"**🔑 Answer:** `{int(answer)}`\n\n")
            f.write(f"*⚙️ Engine Seed: {seed_info}*\n\n")
            f.write("---\n\n")

    conn.close()
    print(f"🎉 통일된 포맷으로 추출 완료: {output_path}")

if __name__ == "__main__":
    export_to_markdown()