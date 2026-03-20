---
id: "Matrix_Linear_Systems_Master"
category: "Matrix_Operation"
title: "연립일차방정식과 행렬"
required_context: "inventory_sales"
type_tag: "Matrix_Linear_Systems"
KC_tags: ["연립일차방정식의 행렬 표현", "역행렬을 이용한 해 구하기", "부정/불능 조건"]
description: "연립일차방정식을 행렬식 AX=B로 변환하고 역행렬을 이용해 해를 구하는 문제."

logic_setup: |
  from sympy import Matrix, latex
  import random

  # 1. 역산(Backward Design): 정수 해 (ans_x, ans_y)를 먼저 결정
  ans_x = random.randint(-3, 3)
  ans_y = random.randint(-3, 3)

  # 2. 난이도별 로직 분기 (5단계 완벽 분리)
  if user_level == 1:
      # [Level 1] 기초: 행렬 표현의 이해 (연립방정식 -> 행렬 변환)
      # 수활북 86p 01번 스타일
      a, b, c, d = random.sample(range(1, 6), 4)
      A_mat = Matrix([[a, b], [c, d]])
      B_mat = Matrix([[a*ans_x + b*ans_y], [c*ans_x + d*ans_y]])
      target_expr = "A" # 행렬 A의 성분을 묻거나 행렬식 자체를 묻기
      ans_val = sum(A_mat)

  elif user_level == 2:
      # [Level 2] 기본: 역행렬이 주어졌을 때 해 구하기
      # AX = B에서 A^-1를 알려주고 X를 구하게 함
      # det(A) = 1인 행렬 생성
      a_val = random.randint(1, 3)
      c_val = random.randint(1, 3)
      A = Matrix([[a_val, 1], [a_val*c_val - 1, c_val]]) # det = ac - (ac-1) = 1
      A_inv = A.inv()
      B_mat = Matrix([[ans_x + 2*ans_y], [ans_x + 3*ans_y]])
      target_expr = "x + y"
      ans_val = ans_x + ans_y
      distractors = [ans_x - ans_y, -ans_val, ans_val + 1, ans_val - 1]

  elif user_level == 3:
      # [Level 3] 응용: 직접 역행렬을 구해 해 구하기 (수활북 88p)
      # ad-bc = 1인 행렬로 설계하여 정수 역행렬 유도
      a = random.randint(2, 5)
      d = random.randint(2, 5)
      b, c = 1, a*d - 1
      A_mat = Matrix([[a, b], [c, d]])
      B_val = Matrix([[a*ans_x + b*ans_y], [c*ans_x + d*ans_y]])
      target_expr = "xy"
      ans_val = ans_x * ans_y
      distractors = [ans_x + ans_y, -ans_val, 0, ans_val + 2]

  elif user_level == 4:
      # [Level 4] 심화: 해가 존재하지 않거나 무수히 많을 조건 (D=0)
      # 수활북 89p 03번 스타일
      k_ans = random.randint(1, 5)
      # (k-1)x + 2y = 0, 3x + (k-2)y = 0 형태 (제차 연립방정식)
      # det = (k-1)(k-2) - 6 = k^2 - 3k - 4 = 0 -> (k-4)(k+1)=0
      k_list = [4, -1]
      ans_val = random.choice(k_list)
      target_expr = "k"
      distractors = [0, 1, 2, -ans_val]

  else:
      # [Level 5] 킬러/AMC: 실생활 상황을 행렬 방정식으로 세워 풀기
      # 수활북 87p 창의/융합 스타일 (가격과 개수)
      items = ["사과", "배"]
      p1, p2 = random.choice([(1000, 1500), (500, 800), (1200, 2000)])
      # x + y = total_count, p1*x + p2*y = total_price
      ans_x, ans_y = random.randint(3, 7), random.randint(3, 7)
      total_count = ans_x + ans_y
      total_price = p1*ans_x + p2*ans_y
      ans_val = ans_x # 사과의 개수를 구하라
      target_expr = f"{items[0]}의 개수"
      distractors = [ans_y, total_count, (total_price//1000), ans_x + 1]

  # 3. 렌더링 변수 처리
  render_vars = {
      "user_level": user_level,
      "target_expr": target_expr
  }
  if user_level == 1:
      render_vars["eq_tex"] = rf"\begin{{cases}} {a}x + {b}y = {B_mat[0]} \\ {c}x + {d}y = {B_mat[1]} \end{{cases}}"
  elif user_level == 2:
      render_vars["A_inv_tex"] = latex(A_inv)
      render_vars["B_tex"] = latex(B_mat)
  elif user_level == 3:
      render_vars["A_tex"] = latex(A_mat)
      render_vars["B_tex"] = latex(B_val)
  elif user_level == 4:
      render_vars["eq_tex"] = rf"\begin{{cases}} (k-1)x + 2y = 0 \\ 3x + (k-2)y = 0 \end{{cases}}"
  elif user_level == 5:
      render_vars["context"] = f"{items[0]}와 {items[1]}를 합하여 {total_count}개 사고 {total_price}원을 지불하였다."
      render_vars["price_info"] = f"{items[0]} 한 개의 가격은 {p1}원, {items[1]} 한 개의 가격은 {p2}원이다."

---
{% if user_level == 1 %}
다음 연립일차방정식을 행렬을 이용하여 $\begin{pmatrix} a & b \\ c & d \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} k_1 \\ k_2 \end{pmatrix}$ 와 같이 나타낼 때, 행렬 $A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$ 의 모든 성분의 합을 구하시오.

$$ {{ eq_tex }} $$

{% elif user_level == 2 %}
행렬 $A$의 역행렬 $A^{-1} = {{ A_inv_tex }}$ 가 주어지고, $A \begin{pmatrix} x \\ y \end{pmatrix} = {{ B_tex }}$ 일 때, ${{ target_expr }}$ 의 값을 구하시오.

{% elif user_level == 3 %}
연립방정식 ${{ A_tex }} \begin{pmatrix} x \\ y \end{pmatrix} = {{ B_tex }}$ 의 해를 $x, y$라 할 때, ${{ target_expr }}$ 의 값을 구하시오.

{% elif user_level == 4 %}
$x, y$에 대한 연립방정식 ${{ eq_tex }}$ 가 $x=0, y=0$ 이외의 해를 갖도록 하는 실수 ${{ target_expr }}$ 의 값을 구하시오.

{% elif user_level == 5 %}
{{ context }} {{ price_info }} 이 상황을 행렬을 이용하여 해결할 때, {{ target_expr }}를 구하시오.

{% endif %}

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