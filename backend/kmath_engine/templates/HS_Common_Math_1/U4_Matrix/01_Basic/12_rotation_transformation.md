---
id: "Rotation_Transformation_Master"
category: "Matrix_Operation"
title: "회전변환"
required_context: "coordinate_systems"
type_tag: "Rotation_Transformation"
KC_tags: ["회전변환", "회전변환 행렬", "특수각의 삼각비", "점의 회전"]
description: "원점을 중심으로 각 theta만큼 회전하는 변환 f를 나타내는 행렬과 점의 이동."

logic_setup: |
  import math
  from sympy import Matrix, latex, sin, cos, pi, sqrt
  import random

  # SVG 생성을 위한 설정
  svg_width, svg_height = 300, 250
  cx, cy = 150, 180 # 원점 위치 (화면 하단 중앙)

  # 1. 특수각 리스트 정의 (라디안 기준)
  # 엔진이 계산하기 편하도록 삼각비 값을 미리 매핑
  angles = [
      {"deg": 30, "rad": pi/6, "sin": "1/2", "cos": "sqrt(3)/2"},
      {"deg": 45, "rad": pi/4, "sin": "sqrt(2)/2", "cos": "sqrt(2)/2"},
      {"deg": 60, "rad": pi/3, "sin": "sqrt(3)/2", "cos": "1/2"},
      {"deg": 90, "rad": pi/2, "sin": "1", "cos": "0"}
  ]
  
  # 기본 시각화 변수 (Level별로 덮어씀)
  vis_angle = 60

  # 2. 난이도별 로직 분기 (5단계 엄격 분리)
  if user_level == 1:
      # [Level 1] 기초: 90도 또는 180도 회전행렬의 성분 합 (가장 기본 구조)
      deg = random.choice([90, 180, 270])
      if deg == 90: A = Matrix([[0, -1], [1, 0]])
      elif deg == 180: A = Matrix([[-1, 0], [0, -1]])
      else: A = Matrix([[0, 1], [-1, 0]])
      
      target_expr = f"원점을 중심으로 ${deg}^\circ$ 회전하는 변환을 나타내는 행렬의 모든 성분의 합"
      ans_val = sum(A)
      distractors = [2, -2, 1, -1]
      vis_angle = deg

  elif user_level == 2:
      # [Level 2] 기본: 특수각(30, 45, 60) 회전행렬의 특정 성분 찾기
      choice = random.choice(angles[:3]) # 30, 45, 60 중 하나
      target_expr = f"원점을 중심으로 ${choice['deg']}^\circ$만큼 회전하는 변환을 나타내는 행렬의 성분 $a_{{21}}$의 값"
      # a21 = sin(theta)
      ans_val = choice['sin'] 
      distractors = [choice['cos'], f"-({choice['sin']})", "1", "0"]
      vis_angle = choice['deg']

  elif user_level == 3:
      # [Level 3] 응용: 실제 점 P(x, y)를 회전시킨 후의 좌표 구하기 (실전 연산)
      # 계산이 깔끔하도록 (1, 0) 또는 (0, 1)을 특수각으로 회전
      p_x, p_y = random.choice([(2, 0), (0, 2), (4, 0)])
      # 60도 회전 시: (2*cos60, 2*sin60) = (1, sqrt(3))
      ans_val = p_x * (1/2) - p_y * (sqrt(3)/2) + p_x * (sqrt(3)/2) + p_y * (1/2) # 60도 기준
      target_expr = f"점 ({p_x}, {p_y})를 원점을 중심으로 $60^\circ$만큼 회전시킨 점의 좌표의 합"
      distractors = [p_x, p_y, 0, -1]
      vis_angle = 60

  elif user_level == 4:
      # [Level 4] 심화: 회전변환 행렬의 거듭제곱 (A^n)의 기하적 의미
      # 30도 회전 행렬을 6번 곱하면 180도 회전임
      deg = random.choice([30, 45, 60])
      if deg == 30: n = 6 # 180도
      elif deg == 45: n = 4 # 180도
      else: n = 3 # 180도
      
      ans_val = -2 # 180도 회전 행렬의 합 (-1 + 0 + 0 - 1 = -2)
      target_expr = f"원점을 중심으로 ${deg}^\circ$만큼 회전하는 변환을 나타내는 행렬을 $A$라 할 때, $A^{{{n}}}$의 모든 성분의 합"
      distractors = [0, 2, -1, 1]
      vis_angle = deg

  else:
      # [Level 5] 킬러: 좌표의 변화를 보고 회전각 theta 추론 (역산)
      # f(2, 0) = (1, sqrt(3)) -> cos(theta)=1/2, sin(theta)=sqrt(3)/2 -> theta=60
      choice = random.choice(angles[:3])
      ans_val = choice['deg']
      
      # (2, 0)을 회전시킨 점 계산
      res_x = 2 * float(eval(choice['cos'].replace('sqrt', 'math.sqrt')))
      res_y = 2 * float(eval(choice['sin'].replace('sqrt', 'math.sqrt')))
      
      # 근사치로 표현하거나 SymPy로 정확히 표현 (여기서는 텍스트로 하드코딩된 예시 대체)
      if ans_val == 60:
          pt_str = "(1, \\sqrt{3})"
      elif ans_val == 30:
          pt_str = "(\\sqrt{3}, 1)"
      else:
          pt_str = "(\\sqrt{2}, \\sqrt{2})"
          
      target_expr = f"일차변환 $f$가 원점을 중심으로 $\\theta$만큼 회전하는 변환이고, $f(2, 0) = {pt_str}$일 때, $\\theta$의 크기($0 < \\theta < 90^\circ$)"
      distractors = [x for x in [30, 45, 60, 75] if x != ans_val]
      vis_angle = ans_val

  # 3. LaTeX 포맷팅 (객관식 보기용)
  # SymPy 객체나 문자열을 LaTeX 포맷으로 변환하여 리스트 갱신
  if not isinstance(ans_val, str) and not isinstance(ans_val, int):
      ans_val = latex(ans_val)
  
  distractors_latex = []
  for d in distractors:
      if not isinstance(d, str) and not isinstance(d, int):
          distractors_latex.append(latex(d))
      else:
          distractors_latex.append(str(d))
  distractors = distractors_latex

  # 4. SVG 시각화 생성
  # 좌표축
  svg = f'<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">'
  svg += f'<line x1="20" y1="{cy}" x2="{svg_width-20}" y2="{cy}" stroke="black" stroke-width="1" marker-end="url(#arrow)" />' # x축
  svg += f'<line x1="{cx}" y1="{svg_height-20}" x2="{cx}" y2="20" stroke="black" stroke-width="1" marker-end="url(#arrow)" />' # y축
  svg += f'<text x="{svg_width-15}" y="{cy+15}" font-size="12">x</text><text x="{cx+10}" y="15" font-size="12">y</text><text x="{cx-15}" y="{cy+15}" font-size="12">O</text>'
  
  # 회전 전 점 P (예시로 (2,0) 위치인 (100, 0) 정도 사용)
  r_px = 100
  px, py = cx + r_px, cy
  svg += f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="#999" stroke-width="1" stroke-dasharray="4,4" />'
  svg += f'<circle cx="{px}" cy="{py}" r="3" fill="black" />'
  svg += f'<text x="{px+5}" y="{py+15}" font-size="12" stroke="white" stroke-width="3">P</text>'
  svg += f'<text x="{px+5}" y="{py+15}" font-size="12">P</text>'

  # 회전 후 점 P'
  rad = math.radians(vis_angle)
  px_prime = cx + r_px * math.cos(-rad) # SVG y축은 아래로 증가하므로 -rad
  py_prime = cy + r_px * math.sin(-rad)
  svg += f'<line x1="{cx}" y1="{cy}" x2="{px_prime}" y2="{py_prime}" stroke="#3b82f6" stroke-width="2" />'
  svg += f'<circle cx="{px_prime}" cy="{py_prime}" r="3" fill="#3b82f6" />'
  svg += f'<text x="{px_prime+5}" y="{py_prime-5}" font-size="12" stroke="white" stroke-width="3">P\'</text>'
  svg += f'<text x="{px_prime+5}" y="{py_prime-5}" font-size="12" fill="#3b82f6">P\'</text>'

  # 각도 표시 (Arc)
  svg += f'<path d="M {cx+30} {cy} A 30 30 0 0 0 {cx + 30*math.cos(-rad)} {cy + 30*math.sin(-rad)}" fill="none" stroke="#ef4444" stroke-width="1.5" />'
  svg += f'<text x="{cx + 40*math.cos(-rad/2)}" y="{cy + 40*math.sin(-rad/2)}" font-size="12" fill="#ef4444">{vis_angle}°</text>'
  svg += '</svg>'

  # 5. 렌더링 변수
  render_vars = {
      "user_level": user_level,
      "target_expr": target_expr,
      "ans_val": ans_val,
      "rotation_svg": svg
  }
---
{{ target_expr }}을 구하시오.

<div style="text-align: center; margin: 20px 0;">
  {{ rotation_svg }}
</div>

{% if question_type == 'multiple_choice' %}
① ${{ opt1 }}$
② ${{ opt2 }}$
③ ${{ opt3 }}$
④ ${{ opt4 }}$
⑤ ${{ opt5 }}$

{% elif question_type == 'short_answer' %}
**[정답]** ${{ ans_val }}$

{% elif question_type == 'fill_in_the_blank' %}
구하고자 하는 값은 $\square$ 이다. 빈칸에 알맞은 값을 구하시오.

**[정답]** {{ ans_val }}
{% endif %}