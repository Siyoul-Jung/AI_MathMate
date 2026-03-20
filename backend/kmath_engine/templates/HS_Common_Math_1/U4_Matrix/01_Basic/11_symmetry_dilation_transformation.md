---
id: "Symmetric_Scaling_Master"
category: "Matrix_Operation"
title: "대칭변환과 닮음변환"
type_tag: "Symmetry_Dilation_Transformation"
KC_tags: ["대칭변환", "닮음변환", "행렬의 성분", "일차변환의 기하적 의미"]
required_context: "coordinate_systems"
description: "축 대칭, 원점 대칭, 직선 대칭 및 확대/축소 변환 행렬을 다루는 문항."

logic_setup: |
  import random
  from sympy import Matrix, latex

  # 1. 소재 주입 (예: { "name": "마인크래프트 월드", "target": "스티브 캐릭터" })
  ctx = injected_context if 'injected_context' in locals() else {
      "name": "좌표평면", "target": "점 P"
  }

  # 2. 난이도별 변별력 설계 (5단계)
  if user_level == 1:
      # [Level 1] 기초: 닮음변환 (k배 확대) 행렬의 성분 합
      k = random.choice([2, 3, 5])
      A = Matrix([[k, 0], [0, k]])
      target_expr = f"{ctx['name']}에서 {ctx['target']}를 원점을 중심으로 {k}배 확대하는 변환 행렬의 모든 성분의 합"
      ans_val = 2 * k
      distractors = [k, k**2, 0, 4]

  elif user_level == 2:
      # [Level 2] 기본: x축 또는 y축 대칭변환 행렬
      type = random.choice(["x축", "y축"])
      if type == "x축":
          A = Matrix([[1, 0], [0, -1]])
          ans_val = 0
      else:
          A = Matrix([[-1, 0], [0, 1]])
          ans_val = 0
      target_expr = f"{ctx['target']}를 {type}에 대하여 대칭이동시키는 변환 행렬의 모든 성분의 합"
      distractors = [2, -2, 1, -1]

  elif user_level == 3:
      # [Level 3] 응용: 직선 y=x 또는 y=-x 대칭변환
      A = Matrix([[0, 1], [1, 0]]) # y=x 대칭 예시
      target_expr = f"{ctx['target']}를 직선 $y=x$에 대하여 대칭이동시키는 변환 행렬 $A$의 성분 $a_{{12}}$의 값"
      ans_val = 1
      distractors = [0, -1, 2, 0.5]

  elif user_level == 4:
      # [Level 4] 심화: 대칭변환과 닮음변환의 합성 (간단한 형태)
      # k배 확대 후 x축 대칭
      k = 2
      # [[1, 0], [0, -1]] * [[2, 0], [0, 2]] = [[2, 0], [0, -2]]
      ans_val = 0
      target_expr = f"{ctx['target']}를 2배 확대하고 $x$축에 대하여 대칭이동시킨 합성변환 행렬의 모든 성분의 합"
      distractors = [4, -4, 2, -2]

  else:
      # [Level 5] 킬러: 미지수를 포함한 대칭변환의 성질
      # 행렬 [[a, b], [c, d]]가 y=x 대칭일 때 a+b+c+d 의 값 등
      target_expr = f"임의의 {ctx['target']}를 직선 $y=x$에 대하여 대칭이동시키는 행렬을 $A$라 할 때, $A^{{2026}}$의 모든 성분의 합"
      # y=x 대칭은 두 번 하면 자기 자신(단위행렬)이 됨. 2026은 짝수이므로 A^2026 = E
      ans_val = 2 # 단위행렬 성분의 합 (1+0+0+1)
      distractors = [0, 1, 4, 2026]

  render_vars = {
      "ctx_name": ctx["name"],
      "target_expr": target_expr,
      "ans_val": ans_val
  }
---
### [일차변환: 대칭과 닮음]

**{{ ctx_name }}** 상의 **{{ target_expr }}**을 구하시오.



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