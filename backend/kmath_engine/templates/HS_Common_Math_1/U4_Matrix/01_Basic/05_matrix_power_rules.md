---
id: "Matrix_Power_Rules_Master"
category: "Matrix_Operation"
title: "행렬의 거듭제곱"
required_context: "state_transition"
type_tag: "Matrix_Power_Rules"
KC_tags: ["행렬의 거듭제곱", "주기성", "단위행렬", "수열의 규칙성"]
description: "행렬의 거듭제곱을 통해 규칙성을 찾아내고 $A^n$의 성분을 구하는 문제."

logic_setup: |
  from sympy import Matrix, latex, eye
  import random

  # 1. 난이도별 규칙성 유형 분기
  if user_level == 1:
      # [Level 1] 기초: A^2 또는 A^3의 단순 계산
      A = Matrix([[1, random.randint(1, 3)], [0, 1]])
      n = random.randint(2, 3)
      ans_matrix = A**n
      target_expr = f"A^{n}"

  elif user_level == 2:
      # [Level 2] 기본: 특수 행렬의 거듭제곱 (A^n의 성분 유추)
      # k가 1씩 커지는 규칙 (등차)
      k = random.randint(2, 4)
      A = Matrix([[1, k], [0, 1]])
      n = random.randint(10, 50)
      ans_matrix = A**n # 결과는 [[1, k*n], [0, 1]]
      target_expr = f"A^{{{n}}}"

  elif user_level == 3:
      # [Level 3] 응용: 주기성을 가진 행렬 (A^2 = I 또는 A^2 = -I)
      # 수활북 102쪽 06번 스타일
      A = Matrix([[0, 1], [-1, 0]]) # A^2 = -E, A^4 = E 주기
      n = random.choice([40, 80, 100, 200])
      ans_matrix = A**n # 결과는 단위행렬 E 또는 -E
      target_expr = f"A^{{{n}}}"

  elif user_level == 4:
      # [Level 4] 심화: A^2 = A (멱등행렬) 성질 활용
      # (E + A)^n 을 전개하여 규칙 찾기
      k = random.randint(2, 5)
      A = Matrix([[1, 0], [k, 0]]) # A^2 = A 만족
      n = random.randint(5, 10)
      # (E + A)^n = E + (2^n - 1)A 형태 등
      E = eye(2)
      ans_matrix = (E + A)**n 
      target_expr = f"(E + A)^{{{n}}}"

  else:
      # [Level 5] 킬러/AMC: 복합 규칙성 및 대각성분의 합(Trace)
      # 특정 거듭제곱의 합(Sigma)을 구하는 문제
      A = Matrix([[1, 1], [0, 1]])
      # A + A^2 + ... + A^n 구하기 (n은 5~10 사이 랜덤)
      n = random.randint(5, 10)
      ans_matrix = sum([A**i for i in range(1, n+1)])
      target_expr = rf"\sum_{{k=1}}^{{{n}}} A^k"

  # 2. 결과 처리
  ans_val = sum(ans_matrix)
  
  # 3. 매력적인 오답 설계
  if user_level <= 2:
      # 성분을 각각 n제곱하는 흔한 실수 유도
      err_matrix = Matrix([[A[0,0]**n, A[0,1]**n], [A[1,0]**n, A[1,1]**n]])
      distractors = [sum(err_matrix), ans_val + n, ans_val - n, 0]
  else:
      # 주기를 잘못 계산하거나 단위를 착각하는 실수
      distractors = [ans_val + 1, 0, sum(A), ans_val * 2]

  render_vars = {
      "A_tex": latex(A),
      "target_expr": target_expr,
      "n": n if 'n' in locals() else 10
  }

---
이차정사각행렬 $A = {{ A_tex }}$ 와 단위행렬 $E$ 에 대하여 
다음 식 ${{ target_expr }}$ 을 계산한 행렬의 모든 성분의 합을 구하시오.

{% if question_type == 'multiple_choice' %}
① ${{ opt1 }}$
② ${{ opt2 }}$
③ ${{ opt3 }}$
④ ${{ opt4 }}$
⑤ ${{ opt5 }}$

{% elif question_type == 'short_answer' %}
**[정답]** ${{ ans_val }}$

{% elif question_type == 'fill_in_the_blank' %}
규칙성을 찾아 계산한 행렬의 모든 성분의 합은 $\square$ 이다. 빈칸에 알맞은 값을 구하시오.

**[정답]** {{ ans_val }}
{% endif %}