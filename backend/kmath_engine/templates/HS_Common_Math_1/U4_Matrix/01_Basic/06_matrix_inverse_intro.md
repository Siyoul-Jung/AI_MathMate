---
id: "Matrix_Inverse_Intro_Master"
category: "Matrix_Operation"
title: "역행렬의 뜻"
type_tag: "Matrix_Inverse_Intro"
KC_tags: ["역행렬의 정의", "단위행렬", "역행렬이 존재할 조건", "판별식 D"]
description: "역행렬의 정의(AX=E)를 이해하고, 행렬이 역행렬을 가질 조건을 판별하는 문제."

logic_setup: |
  from sympy import Matrix, latex, solve, Symbol
  import random

  # 1. 난이도별 로직 분기
  if user_level == 1:
      # [Level 1] 기초: 역행렬의 정의 (AX = E를 만족하는 X 찾기)
      # 계산이 쉬운 정수 역행렬을 가진 A 생성
      k = random.randint(1, 3)
      A = Matrix([[1, k], [1, k+1]]) # det = 1
      ans_matrix = A.inv()
      ans_val = sum(ans_matrix)
      target_expr = "A^{-1}"
      # 오답: 단순 부호 반전, 성분의 역수 취하기 등
      distractors = [sum(A), -ans_val, 1/sum(A) if sum(A)!=0 else 5, ans_val + 2]

  elif user_level == 2:
      # [Level 2] 기본: 역행렬 공식 적용 (2x2 행렬의 직접 계산)
      a, d = random.randint(1, 3), random.randint(1, 3)
      b, c = 1, a*d - 1 # ad-bc = 1이 되도록 설계 (정수 해 보장)
      A = Matrix([[a, b], [c, d]])
      ans_matrix = A.inv()
      ans_val = sum(ans_matrix)
      target_expr = "A^{-1}"
      # 오답: ad-bc 분모 계산 실수, a와 d의 위치를 안 바꿈
      distractors = [a+b+c+d, sum(Matrix([[d, -b], [-c, a]])), -ans_val, 0]

  elif user_level == 3:
      # [Level 3] 응용: 역행렬이 존재하지 않을 조건 (D = 0)
      # 수활북 84쪽 스타일: k의 값 찾기
      k_ans = random.randint(-5, 5)
      c1 = random.randint(1, 3)
      # (k-c1)*1 - 2*3 = 0 형태 등으로 설계
      A_elements = [f"k - {c1}", 2, 3, 1]
      A_mat_val = Matrix([[k_ans - c1, 2], [3, 1]]) # det = 0이 되는 k_ans
      ans_val = k_ans
      target_expr = "k"
      # 오답: ad+bc=0으로 계산, 이항 부호 실수
      distractors = [-k_ans, k_ans + c1, k_ans * 2, 0]

  elif user_level == 4:
      # [Level 4] 심화: 역행렬이 존재하기 위한 모든 k의 합 (이차방정식 융합)
      # det(A)가 k에 관한 이차식인 경우
      k1, k2 = random.randint(-3, 1), random.randint(2, 5)
      # (k-k1)(k-k2) = k^2 - (k1+k2)k + k1k2
      A_tex = rf"\begin{{pmatrix}} k & {k1*k2} \\ 1 & k - {k1+k2} \end{{pmatrix}}"
      ans_val = k1 + k2 # 근과 계수의 관계
      target_expr = r"\text{역행렬이 존재하지 않도록 하는 모든 } k \text{의 합}"
      distractors = [k1 * k2, -(k1 + k2), 0, k1 + k2 + 1]

  else:
      # [Level 5] 킬러/교과서 심화: 역행렬의 성질 (AB = E 활용)
      # A와 B의 관계를 통해 (AB)^{-1} 등을 유도 (수활북 105쪽 응용)
      A = Matrix([[1, 2], [0, 1]])
      B_inv = Matrix([[random.randint(1, 3), 1], [1, random.randint(2, 4)]])
      # (AB)^-1 = B^-1 A^-1 계산
      ans_matrix = B_inv * A.inv()
      ans_val = sum(ans_matrix)
      target_expr = "(AB)^{-1}"
      # 오답: A^-1 B^-1 (순서 착각), AB 계산 후 합산 등
      err_matrix = A.inv() * B_inv
      distractors = [sum(err_matrix), sum(A*B_inv.inv()), -ans_val, 1]

  # 2. 렌더링 변수 처리
  render_vars = {
      "user_level": user_level,
      "target_expr": target_expr
  }
  if user_level == 3:
      render_vars["A_elements"] = A_elements
  elif user_level == 4:
      render_vars["A_custom_tex"] = A_tex
  else: # Covers levels 1, 2, 5
      render_vars["A_tex"] = latex(A)

---
{% if user_level <= 2 or user_level == 5 %}
이차정사각행렬 $A = {{ A_tex }}$ 에 대하여 ${{ target_expr }}$ 의 모든 성분의 합을 구하시오.

{% elif user_level == 3 %}
행렬 $A = \begin{pmatrix} {{ A_elements[0] }} & {{ A_elements[1] }} \\ {{ A_elements[2] }} & {{ A_elements[3] }} \end{pmatrix}$ 의 역행렬이 존재하지 않도록 하는 실수 ${{ target_expr }}$ 의 값을 구하시오.

{% elif user_level == 4 %}
행렬 $A = {{ A_custom_tex }}$ 의 역행렬이 존재하지 않도록 하는 ${{ target_expr }}$ 을 구하시오.

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