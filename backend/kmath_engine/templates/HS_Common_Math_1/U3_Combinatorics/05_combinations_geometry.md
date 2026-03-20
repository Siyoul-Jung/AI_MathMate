---
id: "Combinations_Geometry_Master"
master_id: "STD-HIGH-06"
category: "Combinations"
title: "도형에서의 조합 응용"
type_tag: "Combinations_Geometry"
KC_tags: ["조합의 응용", "도형의 개수", "삼각형의 개수", "직선의 개수"]
required_context: "constellation_maps" # 별자리 지도, 점 연결 게임 등
description: "평면 위에 주어진 점들을 연결하여 만들 수 있는 직선, 삼각형, 사각형의 개수를 구하는 문제."

logic_setup: |
  import math
  import random

  # 1. 난이도(user_level)별 도형 배치 로직
  if user_level == 1:
      # [Level 1] 기초: 어느 세 점도 일직선 위에 없는 n개의 점 (nC2, nC3)
      n = random.randint(5, 7)
      target_expr = f"원 위에 서로 다른 {n}개의 점이 있다. 이 중 두 점을 이어 만들 수 있는 서로 다른 '직선'의 개수"
      ans_val = math.comb(n, 2)
      # SVG: 원 위에 점들을 배치
      pts = []
      for i in range(n):
          angle = 2 * math.pi * i / n
          pts.append((100 + 60*math.cos(angle), 100 + 60*math.sin(angle)))
      
  elif user_level == 2:
      # [Level 2] 기본: 한 직선 위의 점 포함 (삼각형 개수)
      # 5개 점 중 3개는 일직선 위 (5C3 - 3C3)
      target_expr = f"아래 그림과 같이 5개의 점이 있을 때, 세 점을 꼭짓점으로 하는 삼각형의 개수"
      ans_val = math.comb(5, 3) - math.comb(3, 3)
      pts = [(40, 160), (100, 160), (160, 160), (70, 60), (130, 60)]

  elif user_level == 3:
      # [Level 3] 응용: 격자점에서의 삼각형 개수 (수활북 스타일)
      # 3x3 격자점 (9C3 - 일직선 케이스 빼기)
      m, n = 3, 3
      target_expr = f"가로, 세로의 간격이 일정한 {m}x{n} 격자점 9개에서 세 점을 택하여 만들 수 있는 삼각형의 개수"
      # 전체 9C3 - (가로 3C3*3 + 세로 3C3*3 + 대각선 3C3*2)
      ans_val = math.comb(9, 3) - (3 + 3 + 2)
      pts = [(x*40 + 60, y*40 + 60) for y in range(m) for x in range(n)]

  elif user_level == 4:
      # [Level 4] 심화: 두 평행선 사이의 점 (사각형 개수)
      # 위 l선에 n개, 아래 m선에 m개 점 (nC2 * mC2)
      n_top, n_bottom = 4, 3
      target_expr = f"두 평행선 위에 각각 {n_top}개, {n_bottom}개의 점이 있다. 이 점들을 꼭짓점으로 하는 '사각행'의 개수"
      ans_val = math.comb(n_top, 2) * math.comb(n_bottom, 2)
      pts = [(x*40 + 40, 60) for x in range(n_top)] + [(x*40 + 60, 140) for x in range(n_bottom)]

  else:
      # [Level 5] 킬러: 다각형의 대각선 교점 또는 복합 격자
      # 원 위의 n개 점을 이은 대각선의 교점의 최대 개수 (nC4)
      n = random.randint(6, 8)
      target_expr = f"원 위에 서로 다른 {n}개의 점이 있다. 어느 세 대각선도 원 내부의 한 점에서 만나지 않을 때, 대각선들이 원 내부에서 만드는 교점의 최대 개수"
      ans_val = math.comb(n, 4)
      pts = [(100 + 70*math.cos(2*math.pi*i/n), 100 + 70*math.sin(2*math.pi*i/n)) for i in range(n)]

  # SVG 렌더링
  svg_pts = "".join([f'<circle cx="{p[0]}" cy="{p[1]}" r="4" fill="black" />' for p in pts])
  if user_level == 1 or user_level == 5:
      svg_pts += '<circle cx="100" cy="100" r="70" fill="none" stroke="#ccc" stroke-dasharray="4" />'

  render_vars = {
      "dynamic_svg": f'<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">{svg_pts}</svg>',
      "target_expr": target_expr,
      "ans_val": ans_val
  }
---
### [경우의 수: 조합과 도형]

다음 그림과 같이 배치된 점들을 이용하여 물음에 답하시오.

<div style="text-align: center; margin: 20px 0;">
  {{ dynamic_svg }}
</div>

**{{ target_expr }}**을 구하시오.



{% if question_type == 'multiple_choice' %}
① ${{ opt1 }}$
② ${{ opt2 }}$
③ ${{ opt3 }}$
④ ${{ opt4 }}$
⑤ ${{ opt5 }}$

{% elif question_type == 'short_answer' %}
**[정답]** ${{ ans_val }}$
{% endif %}