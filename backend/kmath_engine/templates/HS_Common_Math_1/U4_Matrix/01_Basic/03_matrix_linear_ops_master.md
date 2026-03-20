---
id: "Matrix_Linear_Ops_Master"
category: "Matrix_Operation"
title: "행렬의 덧셈과 뺄셈"
required_context: "inventory_sales"
type_tag: "Matrix_Linear_Ops"
KC_tags: ["행렬의 덧셈과 뺄셈", "행렬의 실수배", "행렬 방정식", "연립 행렬 방정식"]
description: "행렬의 선형 연산 종합. 1~5단계 난이도 분리 및 엔진 공통 셔플링 규격 완벽 적용."

logic_setup: |
  from sympy import Matrix, latex
  import random

  # 1. 난이도별 로직 및 수식 구조 분기 (5단계 완벽 분리)
  if user_level == 1:
      # [Level 1] 기초 연산 (A + B 또는 A - B)
      A = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      B = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      op = random.choice(["+", "-"])
      expr_tex = f"A {op} B"
      ans_matrix = A + B if op == "+" else A - B
      ans_val = sum(ans_matrix)
      
      # 오답: 연산자를 반대로 착각, 단순 부호 실수
      err_matrix = A - B if op == "+" else A + B
      distractors = [sum(err_matrix), -ans_val, ans_val + 2, ans_val - 2]

  elif user_level == 2:
      # [Level 2] 실수배가 포함된 연산 (c1*A - c2*B)
      A = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      B = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      c1 = random.randint(2, 4); c2 = random.randint(2, 4)
      expr_tex = f"{c1}A - {c2}B"
      ans_matrix = c1*A - c2*B
      ans_val = sum(ans_matrix)
      
      # 오답: B에 실수배를 빼먹은 실수 (c1*A - B), 덧셈으로 착각
      err_matrix1 = c1*A - B
      err_matrix2 = c1*A + c2*B
      distractors = [sum(err_matrix1), sum(err_matrix2), -ans_val, ans_val + 3]

  elif user_level == 3:
      # [Level 3] 식의 정리 후 대입 (c1(A - c2*B) + c3*B)
      A = Matrix(2, 2, [random.randint(-4, 4) for _ in range(4)])
      B = Matrix(2, 2, [random.randint(-4, 4) for _ in range(4)])
      c1 = random.randint(2, 4); c2 = random.randint(1, 3); c3 = random.randint(2, 5)
      expr_tex = f"{c1}(A - {c2}B) + {c3}B"
      ans_matrix = c1*A + (-c1*c2 + c3)*B
      ans_val = sum(ans_matrix)
      
      # 오답: 분배법칙을 할 때 괄호 뒤쪽 항에 c1을 곱하지 않은 흔한 실수 유도
      err_matrix = c1*A + (-c2 + c3)*B
      distractors = [sum(err_matrix), -ans_val, ans_val + 4, ans_val - 4]

  elif user_level == 4:
      # [Level 4] 행렬 방정식 풀이 (c1*X - A = (c1-1)*X + c2*A - c3*B)
      A = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      B = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      c1 = random.randint(3, 5); c2 = random.randint(1, 3); c3 = random.randint(1, 3)
      expr_tex = f"{c1}X - A = {c1-1}X + {c2}A - {c3}B"
      ans_matrix = (c2+1)*A - c3*B  # 역산 설계 (깔끔한 해)
      ans_val = sum(ans_matrix)
      
      # 오답: -A를 이항할 때 부호를 반대로(+가 아닌 -) 넘긴 실수 유도
      err_matrix = (c2-1)*A - c3*B
      distractors = [sum(err_matrix), -ans_val, sum((c2+1)*A + c3*B), ans_val - 3]

  else:
      # [Level 5] 연립 행렬 방정식 (X+Y, X-Y 활용)
      X = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      Y = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      C_mat = X + Y
      D_mat = X - Y
      c1 = random.randint(2, 4); c2 = random.randint(1, 3)
      expr_tex = f"{c1}X - {c2}Y"
      ans_matrix = c1*X - c2*Y
      ans_val = sum(ans_matrix)
      
      # 오답: X와 Y의 값을 반대로 착각하여 대입한 실수 유도
      err_matrix = c1*Y - c2*X
      distractors = [sum(err_matrix), sum(c1*X + c2*Y), -ans_val, ans_val + 2]

  # 2. 렌더링 변수 내보내기 (SymPy 문자열 정제)
  render_vars = {
      "user_level": user_level,
      "expr_tex": expr_tex
  }

  if user_level <= 4:
      render_vars["A_tex"] = latex(A)
      render_vars["B_tex"] = latex(B)
  else:
      render_vars["C_tex"] = latex(C_mat)
      render_vars["D_tex"] = latex(D_mat)

---
{% if user_level <= 3 %}
두 행렬 $A = {{ A_tex }}$, $B = {{ B_tex }}$ 에 대하여 다음 식을 계산한 행렬의 모든 성분의 합을 구하시오.

$$ {{ expr_tex }} $$

{% elif user_level == 4 %}
두 행렬 $A = {{ A_tex }}$, $B = {{ B_tex }}$ 에 대하여 행렬 $X$가 다음 등식을 만족할 때, 행렬 $X$의 모든 성분의 합을 구하시오.

$$ {{ expr_tex }} $$

{% elif user_level == 5 %}
두 이차정사각행렬 $X, Y$가 다음 조건을 만족시킬 때, ${{ expr_tex }}$ 를 계산한 행렬의 모든 성분의 합을 구하시오.

$$ X + Y = {{ C_tex }}, \quad X - Y = {{ D_tex }} $$

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
주어진 조건을 만족하는 행렬의 모든 성분을 더한 값은 $\square$ 이다. 빈칸에 알맞은 값을 구하시오.

**[정답]** {{ ans_val }}
{% endif %}