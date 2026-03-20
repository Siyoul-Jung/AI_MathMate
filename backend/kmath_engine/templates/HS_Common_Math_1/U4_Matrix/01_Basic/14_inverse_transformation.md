---
id: "Inverse_Transformation_Master"
category: "Matrix_Operation"
title: "역변환"
type_tag: "Inverse_Transformation"
KC_tags: ["역변환", "역행렬", "원래의 점 찾기", "역변환이 존재할 조건"]
description: "일차변환 f의 역변환 f^-1을 구하고, 이를 이용해 변환 전의 좌표나 미지수를 구하는 문제."

logic_setup: |
  from sympy import Matrix, latex, sqrt
  import random

  # 1. 난이도별 로직 분기 (5단계 엄격 분리)
  if user_level == 1:
      # [Level 1] 기초: 역변환을 나타내는 행렬 구하기 (단순 공식 적용)
      # 계산이 깔끔하도록 det=1인 행렬 설계
      a = random.randint(2, 5)
      c = random.randint(1, a-1)
      A = Matrix([[a, a*2-1], [1, 2]]) # det = 2a - (2a-1) = 1
      ans_matrix = A.inv()
      ans_val = int(sum(ans_matrix))
      target_expr = "일차변환 $f$를 나타내는 행렬이 $A = \\begin{pmatrix} 2 & 5 \\\\ 1 & 3 \\end{pmatrix}$ 일 때, 역변환 $f^{-1}$을 나타내는 행렬의 모든 성분의 합"
      # 오답: 역행렬 공식을 잘못 적용(위치 안 바꿈, 부호 실수 등)
      distractors = [sum(A), -ans_val, 0, 1]

  elif user_level == 2:
      # [Level 2] 기본: 역변환을 이용하여 원래의 점 구하기 (순수 역산)
      # f(x, y) = (x', y') 일 때 (x, y) = A^-1 * (x', y')
      a = random.randint(1, 3)
      A = Matrix([[a, 1], [a*2-1, 2]]) # det = 1
      # 원래 점 (1, 2)를 가정하고 결과점 생성
      p_x, p_y = random.randint(1, 3), random.randint(1, 3)
      p_prime = A * Matrix([p_x, p_y])
      ans_val = p_x + p_y
      target_expr = f"일차변환 $f$를 나타내는 행렬이 $A = {latex(A)}$ 일 때, $f$에 의하여 점 ({p_prime[0]}, {p_prime[1]})로 옮겨지는 점의 좌표의 합"
      # 오답: 결과점의 합(12), 단순히 행렬 A를 결과점에 곱한 결과 등
      distractors = [int(p_prime[0] + p_prime[1]), -ans_val, 0, 5]

  elif user_level == 3:
      # [Level 3] 응용: 특수 변환(회전)의 역변환 성질
      # 30도 회전의 역변환은 -30도 회전임 (기하적 이해)
      deg = random.choice([30, 60])
      
      if deg == 30:
          ans_val = sqrt(3)
          distractors = [1, 0, 2, -sqrt(3)]
      else: # 60도
          ans_val = 1
          distractors = [0, 2, sqrt(3), -1]
          
      target_expr = f"원점을 중심으로 ${deg}^\\circ$만큼 회전하는 일차변환 $f$의 역변환 $f^{{-1}}$을 나타내는 행렬의 모든 성분의 합"

  elif user_level == 4:
      # [Level 4] 심화: 합성변환의 역변환 성질 (순서 역전)
      # (g ∘ f)^-1 = f^-1 ∘ g^-1 임을 아는지 변별
      # 정수 역행렬을 위해 det=1인 행렬 생성
      def get_unimodular():
          if random.random() < 0.5:
              return Matrix([[1, random.randint(1,3)], [0, 1]])
          else:
              return Matrix([[1, 0], [random.randint(1,3), 1]])
              
      f_mat = get_unimodular()
      g_mat = get_unimodular()
      # 정답: f_inv * g_inv
      ans_matrix = f_mat.inv() * g_mat.inv()
      ans_val = int(sum(ans_matrix))
      target_expr = f"두 일차변환 $f, g$를 나타내는 행렬이 각각 $F={latex(f_mat)}, G={latex(g_mat)}$일 때, 합성변환 $g \\circ f$의 역변환을 나타내는 행렬의 모든 성분의 합"
      # 오답: 순서를 뒤집지 않은 G^-1 * F^-1, 혹은 단순 행렬의 곱 FG의 역행렬 실수
      distractors = [int(sum(g_mat.inv() * f_mat.inv())), int(sum(g_mat * f_mat)), 0, -ans_val]

  else:
      # [Level 5] 킬러: 역변환이 존재하지 않을 조건 (ad-bc=0)
      # 수활북 139p 스타일: 미지수 k의 결정
      k_ans = random.choice([2, 3, 4])
      # det = k^2 - k_ans^2 = 0
      A_elements = [ "k", k_ans**2, 1, "k" ]
      ans_val = k_ans
      target_expr = f"행렬 $A = \\begin{pmatrix} k & {k_ans**2} \\\\ 1 & k \\end{pmatrix}$ 로 나타내어지는 일차변환 $f$의 역변환이 존재하지 않도록 하는 양수 $k$의 값"
      distractors = [k_ans**2, 0, -k_ans, 1]

  # 2. LaTeX 포맷팅 (객관식 보기용)
  if not isinstance(ans_val, str) and not isinstance(ans_val, int):
      ans_val = latex(ans_val)
  
  distractors_latex = []
  for d in distractors:
      if not isinstance(d, str) and not isinstance(d, int):
          distractors_latex.append(latex(d))
      else:
          distractors_latex.append(str(d))
  distractors = distractors_latex

  # 3. 렌더링 변수
  render_vars = {
      "user_level": user_level,
      "target_expr": target_expr,
      "ans_val": ans_val
  }
---
{{ target_expr }}을 구하시오.



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