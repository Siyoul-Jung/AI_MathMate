---
id: "Linear_Transformation_Intro_Master"
category: "Matrix_Operation"
title: "일차변환"
type_tag: "Linear_Transformation"
KC_tags: ["일차변환의 정의", "행렬과 점의 대응", "변환된 좌표 구하기", "고정점"]
description: "일차변환 f가 행렬 A에 의해 정의될 때, 점의 이동(순방향/역방향)과 미지수 결정."

logic_setup: |
  from sympy import Matrix, latex
  import random

  # 정수 해 유도를 위한 기본 좌표 설정
  ans_x, ans_y = random.randint(-3, 3), random.randint(-3, 3)
  if ans_x == 0 and ans_y == 0: ans_x, ans_y = 1, 2

  # 1. 난이도별 로직 분기 (5단계 엄격 분리)
  if user_level == 1:
      # [Level 1] 기초: 행렬 A와 점 P를 주고 결과점 P' 구하기 (순방향 연산)
      A = Matrix([[random.randint(1, 3), 1], [0, random.randint(1, 2)]])
      p_x, p_y = random.randint(1, 4), random.randint(1, 4)
      ans_point = A * Matrix([p_x, p_y])
      ans_val = int(ans_point[0] + ans_point[1])
      target_expr = f"점 ({p_x}, {p_y})가 옮겨지는 점의 좌표의 합"
      # 오답: 행렬 성분 합과 점의 합을 단순히 더함, 혹은 부호 실수
      distractors = [sum(A) + p_x + p_y, ans_val + 2, -ans_val, 0]

  elif user_level == 2:
      # [Level 2] 기본: 결과점 P'를 보고 원래 점 P 찾기 (역방향 연산)
      # 계산 편의를 위해 det=1인 행렬 사용 (역행렬 암산 가능 수준)
      k = random.randint(1, 3)
      A = Matrix([[k+1, 1], [k, 1]]) # det = k+1 - k = 1
      p_prime = A * Matrix([ans_x, ans_y])
      ans_val = ans_x + ans_y
      target_expr = f"일차변환 f에 의해 점 ({p_prime[0]}, {p_prime[1]})로 옮겨지는 원래 점의 좌표의 합"
      # 오답: 결과점의 좌표 합을 그대로 답함, 부호 실수
      distractors = [int(p_prime[0] + p_prime[1]), -ans_val, ans_val + 3, 1]

  elif user_level == 3:
      # [Level 3] 응용: 단위 벡터 (1,0), (0,1)의 대응을 통해 행렬 A 완성하기
      # f(1,0)=(a,c), f(0,1)=(b,d) -> A = [[a,b],[c,d]]
      a, c = random.randint(1, 4), random.randint(-3, 3)
      b, d = random.randint(-3, 3), random.randint(1, 4)
      A = Matrix([[a, b], [c, d]])
      ans_val = a + b + c + d
      target_expr = "일차변환 $f$를 나타내는 행렬 $A$의 모든 성분의 합"
      # 오답: 행과 열을 바꿔서 합산, 혹은 특정 성분 누락
      distractors = [a + c, b + d, a + b, 0]

  elif user_level == 4:
      # [Level 4] 심화: 일반적인 두 점의 대응으로 행렬 A 구하기 (연립방정식)
      # f(1, 1) = v1, f(1, -1) = v2 를 만족하는 A 도출
      a = random.randint(1, 3)
      A = Matrix([[a, 1], [1, a+1]])
      p_v = A * Matrix([1, 1])
      q_v = A * Matrix([1, -1])
      ans_val = int(sum(A))
      target_expr = "일차변환 $f$를 나타내는 행렬 $A$의 모든 성분의 합"
      # 오답: 대입 과정에서의 계산 실수 유도
      distractors = [int(sum(p_v) + sum(q_v)), -ans_val, 10, 5]

  else:
      # [Level 5] 킬러: 고정점(Fixed Point) 존재 조건 (det(A-E)=0)
      # f(P)=P 를 만족하는 P(x,y) != (0,0) 가 존재하도록 하는 k 찾기
      k_ans = random.choice([2, 4, 5])
      # det([[k-1, 2], [1, 3-1]]) = 2(k-1) - 2 = 0 -> k=2
      A_elements = [k_ans, 2, 1, 3]
      ans_val = k_ans
      target_expr = "실수 $k$의 값"
      # 오답: det(A)=0으로 계산, 혹은 k-1 대신 k 대입 실수
      distractors = [1, 0, k_ans + 2, -k_ans]

  # 2. 렌더링 변수 사전 구성
  render_vars = {
      "user_level": user_level,
      "target_expr": target_expr,
      "ans_val": ans_val
  }

  # 각 케이스별 필요한 수식 텍스트 추가
  if user_level in [1, 2]:
      render_vars["A_tex"] = latex(A)
  elif user_level == 3:
      render_vars["p1_tex"] = f"({a}, {c})"
      render_vars["p2_tex"] = f"({b}, {d})"
  elif user_level == 4:
      render_vars["cond1"] = f"f(1, 1) = ({p_v[0]}, {p_v[1]})"
      render_vars["cond2"] = f"f(1, -1) = ({q_v[0]}, {q_v[1]})"
  elif user_level == 5:
      render_vars["A_elements"] = A_elements

---
{% if user_level == 1 %}
일차변환 $f$를 나타내는 행렬이 $A = {{ A_tex }}$ 일 때, {{ target_expr }}을 구하시오.

{% elif user_level == 2 %}
일차변환 $f$를 나타내는 행렬이 $A = {{ A_tex }}$ 일 때, {{ target_expr }}을 구하시오.

{% elif user_level == 3 %}
일차변환 $f$에 의하여 두 점 $(1, 0)$, $(0, 1)$ 이 각각 두 점 {{ p1_tex }}, {{ p2_tex }} 로 옮겨질 때, {{ target_expr }}을 구하시오.

{% elif user_level == 4 %}
일차변환 $f$에 대하여 ${{ cond1 }}$, ${{ cond2 }}$ 가 성립할 때, {{ target_expr }}을 구하시오.

{% elif user_level == 5 %}
행렬 $A = \begin{pmatrix} k & 2 \\ 1 & 3 \end{pmatrix}$ 로 나타내어지는 일차변환 $f$에 대하여, $f(P) = P$ 를 만족하는 점 $P$ 중 원점 $O$ 가 아닌 점이 존재하도록 하는 {{ target_expr }}을 구하시오.

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