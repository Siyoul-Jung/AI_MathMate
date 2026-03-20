---
id: "Symmetric_Scaling_Trans_Master"
category: "Matrix_Operation"
title: "대칭변환과 닮음변환"
type_tag: "Symmetric_Scaling_Trans"
KC_tags: ["대칭변환", "닮음변환", "행렬", "일차변환"]
description: "점이나 도형을 대칭이동하거나 확대/축소하는 일차변환 행렬을 다루는 문제."

logic_setup: |
  from sympy import Matrix, latex
  import random

  # 1. 난이도별 로직 분기
  if user_level == 1:
      # [Level 1] 기본 대칭변환 (x축, y축, 원점)
      type_idx = random.randint(0, 2)
      if type_idx == 0:
          name = "x축"
          A = Matrix([[1, 0], [0, -1]])
      elif type_idx == 1:
          name = "y축"
          A = Matrix([[-1, 0], [0, 1]])
      else:
          name = "원점"
          A = Matrix([[-1, 0], [0, -1]])
      
      p_x, p_y = random.randint(1, 5), random.randint(1, 5)
      ans_pt = A * Matrix([p_x, p_y])
      ans_val = ans_pt[0] + ans_pt[1]
      target_expr = f"점 ({p_x}, {p_y})를 {name}에 대하여 대칭이동한 점의 좌표의 합"

  elif user_level == 2:
      # [Level 2] 직선 y=x, y=-x 대칭
      type_idx = random.randint(0, 1)
      if type_idx == 0:
          name = "직선 y=x"
          A = Matrix([[0, 1], [1, 0]])
      else:
          name = "직선 y=-x"
          A = Matrix([[0, -1], [-1, 0]])
          
      p_x, p_y = random.randint(-4, 4), random.randint(-4, 4)
      ans_pt = A * Matrix([p_x, p_y])
      ans_val = ans_pt[0] + ans_pt[1]
      target_expr = f"점 ({p_x}, {p_y})를 {name}에 대하여 대칭이동한 점의 좌표의 합"

  elif user_level == 3:
      # [Level 3] 닮음변환 (k배 확대/축소)
      k = random.choice([2, 3, 4, -2])
      A = Matrix([[k, 0], [0, k]])
      p_x, p_y = random.randint(1, 3), random.randint(1, 3)
      ans_pt = A * Matrix([p_x, p_y])
      ans_val = ans_pt[0] + ans_pt[1]
      target_expr = f"점 ({p_x}, {p_y})를 원점을 중심으로 {k}배 확대한 점의 좌표의 합"

  elif user_level == 4:
      # [Level 4] 대칭변환 행렬 찾기 (행렬의 성분 합)
      case = random.choice(["x_axis", "y_axis", "origin", "y_eq_x"])
      if case == "x_axis":
          A = Matrix([[1, 0], [0, -1]])
          desc = "x축에 대한 대칭변환"
      elif case == "y_axis":
          A = Matrix([[-1, 0], [0, 1]])
          desc = "y축에 대한 대칭변환"
      elif case == "origin":
          A = Matrix([[-1, 0], [0, -1]])
          desc = "원점에 대한 대칭변환"
      else:
          A = Matrix([[0, 1], [1, 0]])
          desc = "직선 y=x에 대한 대칭변환"
      
      ans_val = sum(A)
      target_expr = f"{desc}을 나타내는 행렬의 모든 성분의 합"

  else:
      # [Level 5] 합성 (대칭 + 닮음)
      k = random.randint(2, 3)
      S = Matrix([[1, 0], [0, -1]]) # x축 대칭
      K = Matrix([[k, 0], [0, k]]) # k배
      A = K * S
      p_x, p_y = random.randint(1, 3), random.randint(1, 3)
      ans_pt = A * Matrix([p_x, p_y])
      ans_val = ans_pt[0] + ans_pt[1]
      target_expr = f"점 ({p_x}, {p_y})를 x축에 대하여 대칭이동한 후, 원점을 중심으로 {k}배 확대한 점의 좌표의 합"

  render_vars = {
      "target_expr": target_expr,
      "ans_val": ans_val
  }

---
일차변환에 대하여, {{ target_expr }}을 구하시오.

**[정답]** {{ ans_val }}