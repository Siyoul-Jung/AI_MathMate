---
id: "Graph_Matrix_Master"
category: "Matrix_Meaning"
title: "그래프와 행렬"
type_tag: "Graph_Matrix"
required_context: "network_connectivity"
KC_tags: ["그래프의 행렬 표현", "인접행렬", "차수의 합", "경로의 수"]

logic_setup: |
  from sympy import Matrix, latex
  import random
  import math

  if 'injected_context' in locals() and injected_context:
      if isinstance(injected_context, list):
          ctx = random.choice(injected_context)
      else:
          ctx = injected_context
  else:
      ctx = {"name": "지점", "nodes": ["A", "B", "C", "D", "E", "F"]}

  # [Level별 변별력 설계 - 랜덤화 적용]
  if user_level == 1: # 기초: 점 3~4개, 모든 성분의 합
      size = random.choice([3, 4])
      density = 0.7
      target_type = "SUM_ALL"
  elif user_level == 2: # 기본: 점 4~5개, 특정 점의 차수
      size = random.choice([4, 5])
      density = 0.5
      target_type = "NODE_DEGREE"
  elif user_level == 3: # 응용: 점 5개, M^2의 성분 (경로 2개)
      size = 5
      density = 0.5
      target_type = "M_SQUARE_ELEMENT"
  elif user_level == 4: # 심화: 점 5개, M^2의 대각성분의 합
      size = 5
      density = 0.4
      target_type = "M_SQUARE_TRACE"
  else: # 킬러: 점 5~6개, M^3 관련 (길이 3 경로)
      size = random.choice([5, 6])
      density = 0.4
      target_type = random.choice(["M_CUBE_ELEMENT", "M_CUBE_TRACE"])

  active_nodes = ctx["nodes"][:size]
  
  # 그래프 생성 (최소 간선 보장)
  while True:
      adj = [[0]*size for _ in range(size)]
      edge_count = 0
      for i in range(size):
          for j in range(i+1, size):
              if random.random() < density: 
                  adj[i][j] = adj[j][i] = 1
                  edge_count += 1
      if edge_count >= size - 1: # 너무 빈약한 그래프 방지
          break
          
  M = Matrix(adj)

  # 정답 로직 분기
  if target_type == "SUM_ALL":
      target_expr = "인접행렬 $M$의 모든 성분의 합"
      ans_val = sum(M)
      
  elif target_type == "NODE_DEGREE":
      idx = random.randint(0, size-1)
      target_expr = f"점 {active_nodes[idx]}와 연결된 변의 개수"
      ans_val = sum(M.row(idx))
      
  elif target_type == "M_SQUARE_ELEMENT":
      M2 = M**2
      i, j = random.sample(range(size), 2)
      target_expr = f"행렬 $M^2$의 ({i+1}, {j+1}) 성분의 값"
      ans_val = M2[i, j]
      
  elif target_type == "M_SQUARE_TRACE":
      target_expr = "한 점에서 출발하여 변을 2개 지나 다시 자기 자신으로 돌아오는 경로의 총 수"
      ans_val = sum((M**2).diagonal())
      
  elif target_type == "M_CUBE_ELEMENT":
      M3 = M**3
      i, j = random.sample(range(size), 2)
      target_expr = f"행렬 $M^3$의 ({i+1}, {j+1}) 성분의 값"
      ans_val = M3[i, j]
      
  else: # M_CUBE_TRACE
      target_expr = "한 점에서 출발하여 변을 3개 지나 다시 자기 자신으로 돌아오는 경로의 총 수"
      ans_val = sum((M**3).diagonal())

  # 오답 생성
  distractors = []
  while len(distractors) < 4:
      d = ans_val + random.randint(-10, 10)
      if d != ans_val and d >= 0 and d not in distractors:
          distractors.append(d)

  # SVG 생성 (레이아웃 개선)
  r, cx, cy = 80, 150, 150 # 반지름과 중심점 조정 (300x300 캔버스의 정중앙)
  svg_nodes, svg_edges = "", ""
  coords = [(cx + r*math.cos(2*math.pi*i/size), cy + r*math.sin(2*math.pi*i/size)) for i in range(size)]
  for i in range(size):
      # Label position: Push outward from center to avoid edge overlap
      lx = cx + (coords[i][0] - cx) * 1.45
      ly = cy + (coords[i][1] - cy) * 1.45 + 5 

      svg_nodes += f'<circle cx="{coords[i][0]}" cy="{coords[i][1]}" r="10" fill="#4A90E2" stroke="white" stroke-width="2"/>'
      # Text Halo (흰색 테두리로 가독성 확보)
      svg_nodes += f'<text x="{lx}" y="{ly}" font-size="14" text-anchor="middle" font-weight="bold" stroke="white" stroke-width="4">{active_nodes[i]}</text>'
      # Main Text
      svg_nodes += f'<text x="{lx}" y="{ly}" font-size="14" text-anchor="middle" font-weight="bold" fill="#334155">{active_nodes[i]}</text>'
      for j in range(i + 1, size):
          if adj[i][j] == 1:
              svg_edges += f'<line x1="{coords[i][0]}" y1="{coords[i][1]}" x2="{coords[j][0]}" y2="{coords[j][1]}" stroke="#94a3b8" stroke-width="2"/>'

  # HTML Matrix Generation for Layout (Use spans to avoid nested div issues in ProblemViewer)
  rows_html = ""
  for row in adj:
      rows_html += "<tr>" + "".join([f'<td style="padding: 4px 8px; text-align: center; font-family: serif;">{x}</td>' for x in row]) + "</tr>"
  
  M_html = f'''
  <span style="display: inline-flex; align-items: stretch; vertical-align: middle; margin-left: 10px;">
    <span style="width: 6px; border-left: 2px solid black; border-top: 2px solid black; border-bottom: 2px solid black; margin-right: 0px;"></span>
    <table style="border-collapse: collapse; font-size: 1rem;">
      {rows_html}
    </table>
    <span style="width: 6px; border-right: 2px solid black; border-top: 2px solid black; border-bottom: 2px solid black; margin-left: 0px;"></span>
  </span>
  '''

  render_vars = {
      "ctx_name": ctx["name"], "M_tex": latex(M), "M_html": M_html, "target_expr": target_expr, "ans_val": ans_val,
      "dynamic_svg": f'<svg width="300" height="300" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">{svg_edges}{svg_nodes}</svg>'
  }
---
어느 **{{ ctx_name }}**의 연결 관계를 나타낸 그래프와 그 인접행렬 $M$이 다음과 같다.

<div style="display: grid; grid-template-columns: auto auto; align-items: center; justify-content: center; gap: 30px; margin: 20px 0;">
  <div>
    {{ dynamic_svg }}
  </div>
  <div style="display: flex; align-items: center; font-size: 1.2rem; font-family: serif;">
    <span>M =</span>
    {{ M_html }}
  </div>
</div>

이 그래프에서 **{{ target_expr }}**을 구하시오.

{% if question_type == 'multiple_choice' %}
① {{ opt1 }}
② {{ opt2 }}
③ {{ opt3 }}
④ {{ opt4 }}
⑤ {{ opt5 }}

{% elif question_type == 'short_answer' %}
**[정답]** {{ ans_val }}

{% elif question_type == 'fill_in_the_blank' %}
구하고자 하는 값은 $\square$ 이다. 빈칸에 알맞은 값을 구하시오.

**[정답]** {{ ans_val }}
{% endif %}
