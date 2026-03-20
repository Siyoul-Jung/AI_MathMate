---
id: "Permutations_Basic_Master"
master_id: "STD-HIGH-06"
category: "Permutations"
type_tag: "Permutations_Basic"
KC_tags: ["순열", "계승(factorial)", "이웃하는 나열", "이웃하지 않는 나열"]
required_context: "school_events"
description: "순열의 정의를 이해하고, 이웃하거나 위치가 고정된 조건하에서의 나열 수를 구하는 문제."

logic_setup: |
  import math
  import random

  # 1. 난이도(user_level)별 로직 분기
  if user_level == 1:
      # [Level 1] 기초: 단순 계승 (n!)
      # 소재: 이어달리기 순서 정하기 등
      n = random.randint(4, 6)
      target_expr = f"{ctx['name']}에 참여한 학생 {n}명을 일렬로 세워 활동 순서를 정하는 방법의 수"
      ans_val = math.factorial(n)
      distractors = [math.factorial(n-1), n * (n-1), n**2, ans_val + n]

  elif user_level == 2:
      # [Level 2] 기본: nPr (n명 중 r명을 뽑아 나열)
      # 소재: 회장, 부회장 선출 등
      n = random.randint(5, 7)
      r = 2
      target_expr = f"{ctx['name']} 위원 {n}명 중 {ctx['roles'][0]} 1명과 {ctx['roles'][1]} 1명을 선출하여 나열하는 방법의 수"
      ans_val = math.perm(n, r)
      distractors = [math.comb(n, r), n + r, n**r, math.factorial(n)]

  elif user_level == 3:
      # [Level 3] 응용: 특정 대상이 이웃하는 나열
      # 소재: 친구끼리 이웃하여 앉기
      total = 5
      neighbor_count = 2 # 이웃해야 할 묶음의 크기
      # (total - neighbor_count + 1)! * neighbor_count!
      ans_val = math.factorial(total - neighbor_count + 1) * math.factorial(neighbor_count)
      target_expr = f"남학생 3명과 여학생 2명이 일렬로 설 때, 여학생 2명이 서로 이웃하여 서는 방법의 수"
      distractors = [math.factorial(total), math.factorial(total-1), ans_val // 2, ans_val * 2]

  elif user_level == 4:
      # [Level 4] 심화: 특정 대상이 이웃하지 않는 나열
      # 전체에서 이웃하는 경우를 빼는 것이 아니라, 사이사이에 끼워 넣기 기법 사용 유도
      # 남 4명 나열(4!) 후 사이사이 5자리 중 여 2명 배치(5P2)
      n_men, n_women = 4, 2
      ans_val = math.factorial(n_men) * math.perm(n_men + 1, n_women)
      target_expr = f"남학생 4명과 여학생 2명이 일렬로 설 때, 여학생끼리는 서로 이웃하지 않도록 서는 방법의 수"
      distractors = [math.factorial(n_men + n_women) - (math.factorial(n_men)*math.factorial(n_women)), 720, 240, 120]

  else:
      # [Level 5] 킬러: 양 끝 조건 + 이웃 조건 복합
      # 특정 인물 A, B는 양 끝에 서고, 나머지 인원 중 C, D는 이웃하게 서는 경우
      # 양 끝 고정(2!) * 남은 인원(total-2) 중 묶음 처리 나열
      total = 6
      # A, B 양 끝: 2!
      # 나머지 4명 중 C, D 이웃: (4-2+1)! * 2! = 3! * 2! = 12
      # 총합: 2 * 12 = 24
      ans_val = 2 * math.factorial(total - 4 + 1) * 2
      target_expr = f"6명의 학생 A, B, C, D, E, F가 일렬로 설 때, A와 B는 양 끝에 서고 C와 D는 서로 이웃하여 서는 방법의 수"
      distractors = [48, 72, 144, 12]

  render_vars = {
      "target_expr": target_expr,
      "ans_val": ans_val
  }
---
### [경우의 수: 순열의 활용]

다음 조건에 따라 나열하는 모든 방법의 수를 구하시오.

**[조건]**
{{ target_expr }}



{% if question_type == 'multiple_choice' %}
① ${{ opt1 }}$
② ${{ opt2 }}$
③ ${{ opt3 }}$
④ ${{ opt4 }}$
⑤ ${{ opt5 }}$

{% elif question_type == 'short_answer' %}
**[정답]** ${{ ans_val }}$
{% endif %}