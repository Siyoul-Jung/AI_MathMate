---
id: "Matrix_Non_Commutative_Master"
category: "Matrix_Operation"
title: "행렬의 곱셈 성질"
type_tag: "Matrix_Non_Commutative"
KC_tags: ["행렬의 곱셈", "비가환성", "곱셈 공식의 적용", "행렬 방정식"]
description: "행렬 곱셈에서 교환법칙이 성립하지 않음을 이용한 곱셈 공식 전개 함정 문제."

logic_setup: |
  from sympy import Matrix, latex
  import random

  # 1. 비가환성(AB != BA)을 만족하는 두 행렬 A, B를 안전하게(무한루프 방지) 생성
  while True:
      A = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      B = Matrix(2, 2, [random.randint(-3, 3) for _ in range(4)])
      # 조건: 교환법칙이 성립하지 않아야 하고, 영행렬 등 특이 케이스 배제
      if A * B != B * A and A.det() != 0 and B.det() != 0:
          break

  # 2. 난이도별(user_level) 로직 분기 및 오답(Distractors) 설계
  if user_level == 1:
      # [Level 1] 기초: 단순 행렬의 곱셈 연산 (함정 없음)
      target_expr = "AB"
      ans_matrix = A * B
      ans_val = sum(ans_matrix)
      
      # 오답: BA를 계산한 결과, 행렬 성분끼리 단순 곱한 결과 등
      err_matrix_ba = B * A
      distractors = [sum(err_matrix_ba), sum(A) * sum(B), -ans_val, ans_val + 2]

  elif user_level == 2:
      # [Level 2] 기본: AB와 BA가 다름을 직접 확인 (AB - BA)
      target_expr = "AB - BA"
      ans_matrix = A * B - B * A
      ans_val = sum(ans_matrix)
      
      # 오답: 교환법칙이 성립한다고 착각하여 0을 고르도록 유도
      distractors = [0, sum(A * B), sum(B * A), -ans_val if ans_val != 0 else 4]

  elif user_level == 3:
      # [Level 3] 응용(교과서 핵심): (A+B)^2 의 올바른 전개
      target_expr = "(A+B)^2"
      ans_matrix = (A + B)**2
      ans_val = sum(ans_matrix)
      
      # 오답: A^2 + 2AB + B^2 (완전제곱식 착각), A^2 + B^2 착각
      err_matrix_1 = A**2 + 2*A*B + B**2
      err_matrix_2 = A**2 + B**2
      distractors = [sum(err_matrix_1), sum(err_matrix_2), -ans_val, ans_val + 3]

  elif user_level == 4:
      # [Level 4] 심화: (A+B)(A-B) 의 올바른 전개
      target_expr = "(A+B)(A-B)"
      ans_matrix = (A + B) * (A - B)
      ans_val = sum(ans_matrix)
      
      # 오답: A^2 - B^2 (합차공식 착각), (A-B)(A+B) 착각
      err_matrix_1 = A**2 - B**2
      err_matrix_2 = (A - B) * (A + B)
      distractors = [sum(err_matrix_1), sum(err_matrix_2), -ans_val, ans_val - 2]

  else:
      # [Level 5] 킬러/AMC: 곱셈 공식을 행렬 방정식으로 비틀어 출제
      # (A+B)^2 = A^2 + X + B^2 를 만족하는 X를 구하시오. (정답: AB + BA)
      target_expr = "X"
      ans_matrix = A * B + B * A
      ans_val = sum(ans_matrix)
      
      # 오답: 교환법칙이 성립한다고 착각하여 2AB나 2BA를 고르도록 유도
      err_matrix_1 = 2 * A * B
      err_matrix_2 = 2 * B * A
      distractors = [sum(err_matrix_1), sum(err_matrix_2), 0, -ans_val if ans_val != 0 else 5]

  # 3. 렌더링 변수 내보내기
  render_vars = {
      "user_level": user_level,
      "A_tex": latex(A),
      "B_tex": latex(B),
      "target_expr": target_expr
  }

---
{% if user_level <= 4 %}
두 이차정사각행렬 $A = {{ A_tex }}$, $B = {{ B_tex }}$ 에 대하여 
다음 식을 계산한 행렬의 모든 성분의 합을 구하시오.

$$ {{ target_expr }} $$

{% else %}
두 이차정사각행렬 $A = {{ A_tex }}$, $B = {{ B_tex }}$ 에 대하여 
행렬 $X$가 다음 등식을 만족시킬 때, 행렬 $X$의 모든 성분의 합을 구하시오.

$$ (A+B)^2 = A^2 + X + B^2 $$

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
구하고자 하는 행렬의 모든 성분을 더한 값은 $\square$ 이다. 빈칸에 알맞은 값을 구하시오.

**[정답]** {{ ans_val }}
{% endif %}