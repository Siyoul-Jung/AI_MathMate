---
id: "Composite_Transformation_Master"
category: "Matrix_Operation"
title: "합성변환"
type_tag: "Composite_Transformation"
KC_tags: ["합성변환", "행렬의 곱", "변환의 순서", "합성변환의 성분"]
description: "두 일차변환 f, g의 합성을 나타내는 행렬을 구하고 점을 이동시키는 문제. 순서의 비가환성 변별."

logic_setup: |
  from sympy import Matrix, latex
  import random

  # 1. 난이도별 로직 분기 (5단계 엄격 분리)
  if user_level == 1:
      # [Level 1] 기초: 기호 f ∘ g 의 정의 (순방향 기호 해석)
      # f(A), g(B) -> f ∘ g 는 AB 임을 아는지 확인
      A = Matrix(2, 2, [random.randint(0, 3) for _ in range(4)])
      B = Matrix(2, 2, [random.randint(0, 3) for _ in range(4)])
      ans_matrix = A * B
      ans_val = int(sum(ans_matrix))
      target_expr = "합성변환 $f \circ g$를 나타내는 행렬의 모든 성분의 합"
      # 오답: BA의 합, A+B의 합 등
      distractors = [int(sum(B * A)), int(sum(A) + sum(B)), 0, 5]

  elif user_level == 2:
      # [Level 2] 기본: "A변환 후 B변환" 문장의 행렬식 변환 (역방향 문장 해석)
      # x축 대칭(f) 후 y=x 대칭(g) -> 행렬은 g * f (BA) 임을 변별
      sym_types = [
          ("x축", Matrix([[1, 0], [0, -1]])),
          ("y축", Matrix([[-1, 0], [0, 1]])),
          ("원점", Matrix([[-1, 0], [0, -1]])),
          ("직선 y=x", Matrix([[0, 1], [1, 0]]))
      ]
      t1, t2 = random.sample(sym_types, 2)
      name1, f_mat = t1
      name2, g_mat = t2
      
      ans_matrix = g_mat * f_mat 
      ans_val = int(sum(ans_matrix))
      target_expr = f"점 $P$를 {name1}에 대하여 대칭변환을 한 후, 다시 {name2}에 대하여 대칭변환을 하는 합성변환을 나타내는 행렬의 모든 성분의 합"
      # 오답: 순서를 바꾼 f*g의 합(1), 단순 합(1+1-1=1), 0
      distractors = [int(sum(f_mat * g_mat)), 1, 0, 2]

  elif user_level == 3:
      # [Level 3] 응용: 합성변환을 통한 구체적 점의 좌표 산출
      # f: 회전, g: 확대 -> (g ∘ f)(p)
      
      # 1. 변수 랜덤화
      p_x = random.randint(1, 4)
      p_y = random.randint(1, 4)
      p = Matrix([p_x, p_y])
      
      k = random.randint(2, 3) # 확대 배율
      rot_deg = random.choice([90, 180, 270]) # 회전 각도
      
      if rot_deg == 90:
          f_mat = Matrix([[0, -1], [1, 0]])
      elif rot_deg == 180:
          f_mat = Matrix([[-1, 0], [0, -1]])
      else: # 270
          f_mat = Matrix([[0, 1], [-1, 0]])
          
      g_mat = Matrix([[k, 0], [0, k]])
      
      ans_p = g_mat * f_mat * p # g(f(p))
      ans_val = int(ans_p[0] + ans_p[1])
      target_expr = f"점 ({p_x}, {p_y})를 원점을 중심으로 ${rot_deg}^\circ$ 회전시킨 후, 원점을 중심으로 {k}배 확대했을 때 옮겨진 점의 좌표의 합"
      
      # 오답: 순서 변경(f(g(p))), 회전만 적용, 확대만 적용, 부호 반대
      wp1 = f_mat * g_mat * p
      distractors = [int(wp1[0]+wp1[1]), int(sum(f_mat*p)), int(sum(g_mat*p)), -ans_val]

  elif user_level == 4:
      # [Level 4] 심화: 합성변환의 교환법칙 성립 조건 (AB = BA)
      # 특수 행렬 구조에서 미지수 관계 찾기
      a_val = random.randint(2, 4)
      # A = [[a, 1], [0, 2]], B = [[1, b], [0, 3]] -> ab+3 = b+2 -> b(a-1) = -1
      if a_val == 2: b_val = -1
      else: b_val = 0 # 로직 단순화
      ans_val = a_val + b_val
      target_expr = "두 일차변환 $f, g$를 나타내는 행렬이 각각 $A=\\begin{pmatrix} a & 1 \\\\ 0 & 2 \\end{pmatrix}, B=\\begin{pmatrix} 1 & b \\\\ 0 & 3 \\end{pmatrix}$일 때, $f \circ g = g \circ f$가 성립하도록 하는 $a+b$의 값"
      distractors = [a_val, b_val, 0, 1]

  else:
      # [Level 5] 킬러: 합성변환의 주기성과 기하적 추론
      # f: y=x 대칭(A), g: x축 대칭(B) -> g ∘ f 는 90도 회전 -> (g ∘ f)^4 = E
      case = random.choice([1, 2, 3])
      if case == 1:
          name1, name2 = "x축", "직선 y=x"
          ans_val = 4 # 90도 회전
      elif case == 2:
          name1, name2 = "x축", "y축"
          ans_val = 2 # 180도 회전 (원점대칭)
      else:
          name1, name2 = "직선 y=x", "직선 y=-x"
          ans_val = 2 # 180도 회전
          
      target_expr = f"일차변환 $f$는 {name1}에 대한 대칭변환이고, $g$는 {name2}에 대한 대칭변환이다. 합성변환 $(g \circ f)^n = E$ (단위변환)를 만족하는 최소의 자연수 $n$의 값"
      distractors = [x for x in [2, 4, 6, 8] if x != ans_val]

  # 2. 렌더링 변수
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