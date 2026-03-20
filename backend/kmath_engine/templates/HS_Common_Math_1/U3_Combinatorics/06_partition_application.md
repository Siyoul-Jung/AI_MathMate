---
id: "Partition_Application_Master"
master_id: "STD-HIGH-06"
category: "Combinations"
title: "분할과 실생활 응용"
type_tag: "Partition_Application"
KC_tags: ["집합의 분할", "조 나누기", "색칠하기", "대진표 작성"]
required_context: "tournament_map" # 대진표, 지역 지도, 국가 국기 등
description: "서로 다른 대상을 조로 나누거나, 인접한 영역을 서로 다른 색으로 칠하는 방법의 수를 구하는 문제."

logic_setup: |
  import math
  import random

  # 1. 난이도(user_level)별 로직 분기
  if user_level == 1:
      # [Level 1] 기초: 단순 조 나누기 (인원수가 모두 다른 경우)
      # 6명을 1명, 2명, 3명의 세 조로 나누기 (6C1 * 5C2 * 3C3)
      n = 6
      p1, p2, p3 = 1, 2, 3
      target_expr = f"학생 {n}명을 각각 {p1}명, {p2}명, {p3}명으로 구성된 세 조로 나누는 방법의 수"
      ans_val = math.comb(n, p1) * math.comb(n-p1, p2)
      distractors = [ans_val // 2, ans_val * 2, math.comb(n, 3), 60]

  elif user_level == 2:
      # [Level 2] 기본: 인원수가 같은 조가 있는 분할
      # 6명을 2명, 2명, 2명으로 나누기 (6C2 * 4C2 * 2C2 / 3!)
      n = 6
      target_expr = f"서로 다른 종류의 꽃 {n}송이를 똑같이 {n//3}송이씩 세 묶음으로 나누는 방법의 수"
      ans_val = (math.comb(6, 2) * math.comb(4, 2)) // math.factorial(3)
      distractors = [ans_val * 6, ans_val * 3, 15, 90]

  elif user_level == 3:
      # [Level 3] 응용: 간단한 색칠하기 (일자형 또는 원형 영역)
      # 4개 영역을 4색으로 칠하기 (인접 영역 중복 불가)
      n_areas = 4
      n_colors = 4
      # 첫 번째 영역 n, 두 번째 n-1, 세 번째 n-1...
      ans_val = n_colors * (n_colors-1) * (n_colors-1) * (n_colors-1)
      target_expr = f"아래 그림과 같이 나누어진 {n_areas}개의 영역을 서로 다른 {n_colors}가지 색으로 칠하려고 한다. 인접한 영역은 서로 다른 색을 칠하는 방법의 수"
      # SVG: 일렬로 나열된 4개 칸
      shape_svg = "".join([f'<rect x="{i*40+20}" y="80" width="40" height="40" fill="none" stroke="black" />' for i in range(n_areas)])

  elif user_level == 4:
      # [Level 4] 심화: 토너먼트 대진표 작성 (수활북 스타일)
      # 6강 대진표 (결승 기준 3/3 분할 후 각각 내부 분할)
      # (6C3 / 2!) * (3C2 * 1C1) * (3C2 * 1C1)
      ans_val = (math.comb(6, 3) // 2) * math.comb(3, 2) * math.comb(3, 2)
      target_expr = f"어느 대회에 참가한 {ctx['name']} 6팀의 대진표가 아래 그림과 같을 때, 대진표를 작성하는 방법의 수"
      # SVG: 토너먼트 대진표 모양
      shape_svg = '<path d="M40 140 V100 H80 V140 M60 100 V70 H140 V100 M120 100 V140 H160 V100" fill="none" stroke="black" stroke-width="2" />'

  else:
      # [Level 5] 킬러: 복합 영역 색칠하기 (가운데 영역이 있는 형태)
      # 수활북 107쪽 '색칠하기' 고난도 변형
      # 5개 영역, 4색 사용. 가운데 영역(A)을 먼저 칠하고 나머지 결정
      n_colors = 4
      # 로직: A(4) * B(3) * C(2) * D(2) * E(2) 형태 (영역 구조에 따라 다름)
      ans_val = 4 * 3 * 2 * 2 * 2 
      target_expr = f"5개로 나누어진 지도를 서로 다른 {n_colors}가지 색으로 칠하려 한다. 같은 색을 여러 번 써도 좋으나 인접한 영역은 다른 색을 칠하는 방법의 수"
      # SVG: 중앙에 원이 있고 주변에 4개 영역이 인접한 형태
      shape_svg = '<circle cx="100" cy="100" r="30" fill="none" stroke="black" />'
      shape_svg += '<path d="M100 20 V70 M100 130 V180 M20 100 H70 M130 100 H180" stroke="black" />'

  render_vars = {
      "dynamic_svg": f'<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">{shape_svg}</svg>',
      "target_expr": target_expr,
      "ans_val": ans_val
  }
---
### [경우의 수: 분할과 색칠하기]

제시된 조건과 그림을 바탕으로 가능한 모든 방법의 수를 구하시오.

<div style="text-align: center; margin: 20px 0;">
  {{ dynamic_svg }}
</div>

**{{ target_expr }}**을 구하시오. (단, 사용 가능한 색의 수는 문제에 제시된 것과 같다.)



{% if question_type == 'multiple_choice' %}
① ${{ opt1 }}$
② ${{ opt2 }}$
③ ${{ opt3 }}$
④ ${{ opt4 }}$
⑤ ${{ opt5 }}$

{% elif question_type == 'short_answer' %}
**[정답]** ${{ ans_val }}$
{% endif %}