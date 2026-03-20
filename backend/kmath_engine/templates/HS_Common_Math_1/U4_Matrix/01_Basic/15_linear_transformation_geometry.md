---
id: "Linear_Trans_Geometry_Master"
category: "Matrix_Operation"
title: "일차변환과 도형"
type_tag: "Linear_Transformation_Geometry"
required_context: "geometric_objects"
KC_tags: ["도형의 이동", "직선의 변환", "원의 변환", "자취의 방정식", "넓이의 변화"]
description: "일차변환 f에 의해 직선이나 원이 어떤 도형으로 옮겨지는지 구하는 최고난도 유형."

logic_setup: |
  from sympy import Matrix, latex, symbols, solve
  import random
  import math

  if 'injected_context' in locals() and injected_context:
      if isinstance(injected_context, list):
          ctx = random.choice(injected_context)
      else:
          ctx = injected_context
  else:
      ctx = {"name": "물체", "context": "이동"}

  # [원본 로직 유지 및 레벨별 시각화 결합]
  if user_level == 1:
      # [Level 1] 기초: y=mx 이동 (2배 확대)
      m = random.randint(2, 4)
      A = Matrix([[2, 0], [0, 2]])
      ans_val = m
      target_expr = f"직선 $y = {m}x$가 행렬 $A = \\begin{pmatrix} 2 & 0 \\\\ 0 & 2 \\end{pmatrix}$에 의해 옮겨진 새로운 직선의 기울기"
      distractors = [2*m, m/2, 0, 1]
      # 시각화: 원점을 지나는 직선
      shape_svg = f'<line x1="100" y1="100" x2="150" y2="{100-50*m}" stroke="red" stroke-width="2" />'

  elif user_level == 2:
      # [Level 2] 기본: x=1 직선 k배 확대
      k = random.randint(2, 4)
      A = Matrix([[k, 0], [0, 1]])
      ans_val = k
      target_expr = f"직선 $x = 1$이 행렬 $A = \\begin{pmatrix} {k} & 0 \\\\ 0 & 1 \\end{pmatrix}$에 의해 옮겨진 직선의 방정식이 $x = a$일 때, $a$의 값"
      distractors = [1, 0, k+1, k**2]
      # 시각화: 세로선 x=1 (격자 한 칸을 20px로 가정)
      shape_svg = f'<line x1="{100+20*k}" y1="20" x2="{100+20*k}" y2="180" stroke="red" stroke-width="2" />'

  elif user_level == 3:
      # [Level 3] 응용: 일반 직선 (y=x+2) 역행렬 대입
      k = random.randint(1, 3)
      A = Matrix([[1, k], [0, 1]])
      # y = x + 2 -> x' = x+ky, y' = y -> x = x'-ky', y = y' -> y' = (x'-ky') + 2 -> (1+k)y' = x' + 2 -> y' = 1/(1+k) x' + ...
      ans_val = f"1/{1+k}"
      target_expr = f"직선 $y = x + 2$가 행렬 $A = \\begin{pmatrix} 1 & {k} \\\\ 0 & 1 \\end{pmatrix}$에 의해 옮겨진 새로운 직선의 기울기"
      distractors = ["1", "2", "0", "-1"]
      # 시각화: 기울기 1/2인 직선
      shape_svg = '<line x1="20" y1="140" x2="180" y2="60" stroke="red" stroke-width="2" />'

  elif user_level == 4:
      # [Level 4] 심화: 원의 이동 (중심 2,0 -> 0,2)
      p_x, p_y = random.choice([(2, 0), (0, 2), (1, 1)])
      A = Matrix([[0, 1], [1, 0]])
      ans_x_p, ans_y_p = p_y, p_x
      ans_val = ans_x_p + ans_y_p
      target_expr = f"중심이 ({p_x}, {p_y})이고 반지름이 1인 원이 행렬 $A = \\begin{pmatrix} 0 & 1 \\\\ 1 & 0 \\end{pmatrix}$에 의해 옮겨진 새로운 원의 중심의 $x$좌표와 $y$좌표의 합"
      distractors = [p_x + p_y, 1, 0, 4]
      # 시각화: 중심이 (0, 2)인 원 (y축 위로 40px 이동)
      shape_svg = '<circle cx="100" cy="60" r="20" fill="none" stroke="red" stroke-width="2" />'

  else:
      # [Level 5] 킬러: 넓이 변화율 (det A)
      k1, k2 = random.randint(2, 3), random.randint(2, 4)
      A = Matrix([[k1, 0], [0, k2]])
      ans_val = k1 * k2
      target_expr = f"반지름의 길이가 1인 원이 행렬 $A = \\begin{pmatrix} {k1} & 0 \\\\ 0 & {k2} \\end{pmatrix}$에 의해 옮겨진 도형의 넓이가 $n\\pi$일 때, $n$의 값"
      distractors = [k1+k2, k1**2, k2**2, 1]
      # 시각화: 타원 (장축 60, 단축 40)
      shape_svg = f'<ellipse cx="100" cy="100" rx="{20*k1}" ry="{20*k2}" fill="none" stroke="red" stroke-width="2" />'

  # [검토 포인트] 축/격자 로직 추가
  grid_svg = '<path d="M0 100 H200 M100 0 V200" stroke="#888" stroke-width="1.5" />' # 메인축
  for i in range(0, 201, 20): # 보조 격자선
      grid_svg += f'<line x1="{i}" y1="0" x2="{i}" y2="200" stroke="#eee" stroke-width="0.5" />'
      grid_svg += f'<line x1="0" y1="{i}" x2="200" y2="{i}" stroke="#eee" stroke-width="0.5" />'

  render_vars = {
      "ctx_name": ctx["name"],
      "ctx_context": ctx["context"],
      "target_expr": target_expr,
      "ans_val": ans_val,
      "dynamic_svg": f'<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="background:white;">{grid_svg}{shape_svg}</svg>'
  }
---
### [실생활 모델링: 일차변환과 도형]

**{{ ctx_name }}**과 관련된 물리적 상황을 좌표평면 위에 나타내면 다음과 같다. 빨간색 실선은 일차변환 $f$에 의해 옮겨진 도형의 궤적을 나타낸다.

<div style="text-align: center; margin: 20px 0;">
  {{ dynamic_svg }}
</div>

**{{ ctx_context }}**를 고려할 때, {{ target_expr }}을 구하시오. (단, 모든 격자 한 칸의 간격은 1이다.)



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