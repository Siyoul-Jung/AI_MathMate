import os
import webbrowser
from manager import ProblemManager

def generate_qa_report():
    print("=== MathMate QA 리포트 생성 시작 ===")
    manager = ProblemManager()
    standards = manager.get_all_standards()
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>MathMate QA Report</title>
        <!-- KaTeX CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" integrity="sha384-n8MVd4Xs03H9q2HKtfl4PVtofDKfy96V98Dg4W+t8vBIruuMO7fUE90MrzAKSn9a" crossorigin="anonymous">
        <!-- KaTeX JS -->
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js" integrity="sha384-XjKyFAMyF36Kp3NM1rBXZ00AX8L0NVX3WqGLr1sac4f8d8i8X7U01E08Wk1y2J3y" crossorigin="anonymous"></script>
        <!-- Auto-render Extension -->
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0o4+/RRE05" crossorigin="anonymous" onload="renderMathInElement(document.body, {delimiters: [{left: '$', right: '$', display: false}]});"></script>
        <style>
            body { font-family: sans-serif; line-height: 1.6; padding: 20px; background: #f0f2f5; }
            .container { max_width: 1000px; margin: 0 auto; }
            .standard-block { background: white; padding: 20px; margin-bottom: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .type-block { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 20px; }
            .type-title { font-size: 1.2em; font-weight: bold; color: #2563eb; margin-bottom: 10px; }
            .problem-row { display: flex; gap: 20px; overflow-x: auto; padding-bottom: 10px; }
            .problem-card { min-width: 300px; max-width: 300px; background: #f8fafc; padding: 15px; border-radius: 6px; border: 1px solid #e2e8f0; }
            .q-text { font-weight: bold; margin-bottom: 10px; white-space: pre-wrap; }
            .image-box { background: white; padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin: 10px 0; text-align: center; overflow: hidden; }
            .image-box svg { max-width: 100%; height: auto; }
            .answer-box { font-size: 0.9em; color: #059669; margin-top: 5px; }
            .expl-box { font-size: 0.85em; color: #64748b; margin-top: 5px; display: none; }
            .problem-card:hover .expl-box { display: block; }
            h1 { text-align: center; color: #1e293b; }
            .meta { font-size: 0.8em; color: #94a3b8; margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MathMate QA Report</h1>
            <p style="text-align: center; color: #666;">각 유형별로 3개의 샘플을 생성하여 다양성과 시각적 품질을 점검합니다.</p>
    """

    for std in standards:
        # 학년 추정
        target_grade = "Middle_1-1"
        if "STD-12" in std: target_grade = "Middle_1-2"
        elif "STD-21" in std: target_grade = "Middle_2-1"
        elif "STD-22" in std: target_grade = "Middle_2-2"
        elif "STD-31" in std: target_grade = "Middle_3-1"
        elif "STD-32" in std: target_grade = "Middle_3-2"
        
        types = manager.list_supported_types("KR", target_grade, std)
        if not types: continue

        html_content += f'<div class="standard-block"><h2>[{std}] {target_grade}</h2>'
        
        for t_info in types:
            t_code = t_info['id']
            t_name = t_info['name']
            
            html_content += f'<div class="type-block"><div class="type-title">{t_code}: {t_name}</div>'
            html_content += '<div class="problem-row">'
            
            # 다양성 체크를 위해 3번 생성
            for i in range(3):
                try:
                    # 난이도와 유형을 섞어서 생성
                    diff = "Normal" if i == 0 else ("Hard" if i == 1 else "Easy")
                    q_type = "short_answer" if i % 2 == 0 else "multi"
                    
                    prob = manager.get_problem("KR", target_grade, std, t_code, difficulty=diff, q_type=q_type)
                    
                    if "error" in prob:
                        html_content += f'<div class="problem-card" style="color:red;">Error: {prob["error"]}</div>'
                        continue

                    html_content += f"""
                    <div class="problem-card">
                        <div class="meta">{diff} | {q_type}</div>
                        <div class="q-text">Q. {prob['question']}</div>
                    """
                    
                    if prob.get('image'):
                        html_content += f'<div class="image-box">{prob["image"]}</div>'
                        
                    if prob.get('options'):
                        html_content += '<ul style="font-size: 0.9em; padding-left: 20px; margin: 5px 0;">'
                        for opt in prob['options']:
                            html_content += f'<li>{opt}</li>'
                        html_content += '</ul>'
                        
                    # 해설 처리 (리스트인 경우 줄바꿈)
                    expl = prob['explanation']
                    if isinstance(expl, list):
                        expl_html = "<ul style='margin:0; padding-left:15px;'>" + "".join([f"<li>{e}</li>" for e in expl]) + "</ul>"
                    else:
                        expl_html = str(expl)

                    html_content += f"""
                        <div class="answer-box">A: {prob['answer']}</div>
                        <div class="expl-box">💡 {expl_html}</div>
                    </div>
                    """
                except Exception as e:
                    html_content += f'<div class="problem-card" style="color:red;">Exception: {str(e)}</div>'
            
            html_content += '</div></div>' # End problem-row & type-block
        
        html_content += '</div>' # End standard-block

    html_content += "</div></body></html>"
    
    output_path = os.path.join(os.path.dirname(__file__), "qa_report.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"리포트 생성 완료: {output_path}")
    webbrowser.open(output_path)

if __name__ == "__main__":
    generate_qa_report()