---
id: "Matrix_Equality_Master"
category: "Matrix_Meaning"
title: "행렬의 상등"
type_tag: "Matrix_Equality"
KC_tags: ["행렬의 상등", "연립일차방정식", "이차식의 값 계산"]
description: "두 행렬이 서로 같을 조건을 이용해 미지수를 구하는 문제. 엔진 공통 셔플링 규격 적용."

logic_setup: |
  from sympy import Matrix, latex, symbols
  import random

  x, y = symbols('x y')

  # 1. 역산(Backward Design): 정수 해 (ans_x, ans_y) 생성
  ans_x = random.randint(-5, 5)
  ans_y = random.randint(-5, 5)
  # 0이 아닌 해를 선호 (문제의 재미를 위해)
  if ans_x == 0: ans_x = random.choice([-1, 1, 2])
  if ans_y == 0: ans_y = random.choice([-2, 2, 3])

  # 2. 난이도(user_level)별 로직 분기
  if user_level == 1:
      # [Level 1] 일차방정식 (각 성분이 하나의 변수만 포함)
      # 변수가 A에만 있을 수도, A와 B 양쪽에 있을 수도 있게 함 (예: x+1 = 2x-3)
      
      # x에 대한 식 설정
      if random.random() < 0.7: # 70% 확률로 한쪽에만 변수
          c1 = random.randint(1, 5)
          expr_x_A = x + c1
          expr_x_B = ans_x + c1
      else: # 30% 확률로 양쪽에 변수 (x+c1 = 2x+c2)
          c1 = random.randint(1, 5)
          c2 = c1 - ans_x 
          expr_x_A = x + c1
          expr_x_B = 2*x + c2
          
      # y에 대한 식 설정
      if random.random() < 0.7:
          c3 = random.randint(1, 5)
          expr_y_A = y - c3
          expr_y_B = ans_y - c3
      else:
          c3 = random.randint(1, 5)
          c4 = -c3 - ans_y
          expr_y_A = y - c3
          expr_y_B = 2*y + c4

      # 행렬 구조 랜덤화 (변수 위치 섞기)
      layout = random.choice([0, 1])
      A_mat = Matrix([[0,0],[0,0]])
      B_mat = Matrix([[0,0],[0,0]])
      
      # 나머지 성분은 랜덤 상수로 채움
      for r in range(2):
          for c in range(2):
              val = random.randint(1, 9)
              A_mat[r,c] = val
              B_mat[r,c] = val
              
      if layout == 0: # 대각선 배치
          A_mat[0,0] = expr_x_A; B_mat[0,0] = expr_x_B
          A_mat[1,1] = expr_y_A; B_mat[1,1] = expr_y_B
      else: # 반대 대각선 배치
          A_mat[0,1] = expr_x_A; B_mat[0,1] = expr_x_B
          A_mat[1,0] = expr_y_A; B_mat[1,0] = expr_y_B
      
      # 질문 다양화
      q_list = ["x+y", "x-y", "xy", "2x+y", "x+2y"]
      q_type = random.choice(q_list)
      if q_type == "x+y": ans_val = ans_x + ans_y; target_expr = "x + y"
      elif q_type == "x-y": ans_val = ans_x - ans_y; target_expr = "x - y"
      elif q_type == "xy": ans_val = ans_x * ans_y; target_expr = "xy"
      elif q_type == "2x+y": ans_val = 2*ans_x + ans_y; target_expr = "2x + y"
      elif q_type == "x+2y": ans_val = ans_x + 2*ans_y; target_expr = "x + 2y"
          
      distractors = [ans_val + 1, ans_val - 1, ans_val + 2, -ans_val]

  elif user_level == 2:
      # [Level 2] 계수가 있는 일차방정식 (2x = 4, 3y = 9 등)
      c1 = random.randint(2, 4)
      k1 = random.randint(1, 5)
      
      c2 = random.randint(2, 4)
      k2 = random.randint(1, 5)
      
      # 위치 완전 랜덤
      pos_x = random.choice([(0,0), (0,1)])
      pos_y = random.choice([(1,0), (1,1)])
      
      A_mat = Matrix([[random.randint(1,5), random.randint(1,5)], [random.randint(1,5), random.randint(1,5)]])
      B_mat = A_mat.copy()
      
      A_mat[pos_x] = c1*x + k1
      B_mat[pos_x] = c1*ans_x + k1
      
      A_mat[pos_y] = c2*y + k2
      B_mat[pos_y] = c2*ans_y + k2
      
      q_case = random.choice(["2x+y", "x-2y", "x+y", "3x+y"])
      if q_case == "2x+y":
          target_expr = "2x + y"
          ans_val = 2*ans_x + ans_y
      elif q_case == "x-2y":
          target_expr = "x - 2y"
          ans_val = ans_x - 2*ans_y
      elif q_case == "x+y":
          target_expr = "x + y"
          ans_val = ans_x + ans_y
      else:
          target_expr = "3x + y"
          ans_val = 3*ans_x + ans_y
          
      distractors = [ans_val + 1, ans_val - 1, -ans_val, 0]

  elif user_level == 3:
      # [Level 3] 연립일차방정식 (x+y=a, x-y=b 형태)
      # 계수 랜덤 선택
      coeffs = random.sample([(1,1), (1,-1), (2,1), (1,2)], 2)
      
      A_mat = Matrix([[0, 0], [0, 0]])
      B_mat = Matrix([[0, 0], [0, 0]])
      
      # 기본값 채우기 (상수)
      for r in range(2):
          for c in range(2):
              val = random.randint(1, 9)
              A_mat[r,c] = val
              B_mat[r,c] = val
              
      # 식 1: 변수를 A에 넣을지 B에 넣을지 랜덤
      a1, b1 = coeffs[0]
      val1 = a1*ans_x + b1*ans_y
      if random.random() < 0.5:
          A_mat[0,0] = a1*x + b1*y
          B_mat[0,0] = val1
      else:
          A_mat[0,0] = val1
          B_mat[0,0] = a1*x + b1*y
          
      # 식 2
      a2, b2 = coeffs[1]
      val2 = a2*ans_x + b2*ans_y
      if random.random() < 0.5:
          A_mat[1,1] = a2*x + b2*y
          B_mat[1,1] = val2
      else:
          A_mat[1,1] = val2
          B_mat[1,1] = a2*x + b2*y
      
      q_case = random.choice(["xy", "x^2+y^2", "x^2-y^2"])
      if q_case == "xy":
          target_expr = "xy"
          ans_val = ans_x * ans_y
      elif q_case == "x^2+y^2":
          target_expr = "x^2 + y^2"
          ans_val = ans_x**2 + ans_y**2
      else:
          target_expr = "x^2 - y^2"
          ans_val = ans_x**2 - ans_y**2
          
      distractors = [ans_val + 1, ans_val - 1, ans_val + 10, -ans_val]

  elif user_level == 4:
      # [Level 4] 복잡한 연립방정식 (계수가 큼)
      a1, b1 = random.randint(2, 5), random.randint(2, 5)
      a2, b2 = random.randint(2, 5), random.randint(-5, -2)
      
      A_mat = Matrix([[a1*x + b1*y, random.randint(1,9)], [random.randint(1,9), a2*x + b2*y]])
      B_mat = Matrix([[a1*ans_x + b1*ans_y, A_mat[0,1]], [A_mat[1,0], a2*ans_x + b2*ans_y]])
      
      target_expr = "x + y"
      ans_val = ans_x + ans_y
      distractors = [ans_x - ans_y, ans_x * ans_y, -ans_val, ans_val + 2]

  else:
      # [Level 5] 이차식 포함 (x^2, y^2 등)
      # A = [[x^2, y], [x, y^2]] vs B = [[ans_x^2, ans_y], [ans_x, ans_y^2]]
      # x, y의 부호를 결정할 수 있도록 1차항도 같이 줌
      A_mat = Matrix([[x**2, y], [x, y**2]])
      B_mat = Matrix([[ans_x**2, ans_y], [ans_x, ans_y**2]])
      
      target_expr = random.choice(["x^3+y^3", "x^2+xy+y^2"])
      if target_expr == "x^3+y^3": ans_val = ans_x**3 + ans_y**3
      else: ans_val = ans_x**2 + ans_x*ans_y + ans_y**2
      
      distractors = [ans_val+10, ans_val-10, 0, 1]

  # 3. 렌더링 변수 내보내기 (SymPy 문자열 정제)
  render_vars = {
      "A_tex": latex(A_mat),
      "B_tex": latex(B_mat),
      "target_expr": target_expr,
      "ans_val": ans_val
  }

---
두 행렬 $A = {{ A_tex }}$, $B = {{ B_tex }}$ 에 대하여 $A = B$ 가 성립할 때, 실수 $x, y$에 대하여 ${{ target_expr }}$ 의 값을 구하시오.

{% if question_type == 'multiple_choice' %}
① ${{ opt1 }}$
② ${{ opt2 }}$
③ ${{ opt3 }}$
④ ${{ opt4 }}$
⑤ ${{ opt5 }}$

{% elif question_type == 'short_answer' %}
**[정답]** ${{ ans_val }}$

{% elif question_type == 'fill_in_the_blank' %}
구하고자 하는 식 ${{ target_expr }}$ 의 값은 $\square$ 이다. 빈칸에 알맞은 값을 구하시오.

**[정답]** {{ ans_val }}
{% endif %}