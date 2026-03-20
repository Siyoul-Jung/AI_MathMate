---
id: "Combinations_Basic_Master"
master_id: "STD-HIGH-06"
category: "Combinations"
title: "조합의 뜻과 성질"
type_tag: "Combinations_Basic"
KC_tags: ["조합", "nCr", "특정한 것을 포함하는 조합", "적어도 조건"]
required_context: "student_council"
description: "조합의 정의를 이해하고, 다양한 조건(포함/제외/적어도) 하에서 대상을 선택하는 방법의 수를 구하는 문제."

logic_setup: |
  import math
  import random

  # 1. 난이도(user_level)별 로직 분기 (5단계 엄격 분리)
  if user_level == 1:
      # [Level 1] 기초: nCr 계산 및 단순 선택
      # 소재: 동아리원 중 대표 선출
      n = random.randint(6, 9)
      r = 3
      target_expr = f"{ctx['name']} 회원 {n}명 중에서 대의원 {r}명을 선출하는 방법의 수"
      ans_val = math.comb(n, r)
      distractors = [math.perm(n, r), math.comb(n, r-1), n*r, ans_val + 1]

  elif user_level == 2:
      # [Level 2] 기본: 특정한 대상을 포함하거나 제외하는 경우
      # n명 중 r명을 뽑을 때, A는 포함하고 B는 제외하기
      # (n-2)C(r-1)
      total = random.randint(8, 10)
      pick = 4
      ans_val = math.comb(total - 2, pick - 1)
      target_expr = f"학생 {total}명 중에서 {pick}명의 위원을 뽑을 때, 특정 학생 A는 반드시 포함하고 B는 포함하지 않도록 뽑는 방법의 수"
      distractors = [math.comb(total, pick), math.comb(total-1, pick-1), math.comb(total-2, pick), 0]

  elif user_level == 3:
      # [Level 3] 응용: 그룹별 선택 (남 n명, 여 m명 중 각각 뽑기)
      # 소재: 조 편성 또는 성별 대표 뽑기
      m_count, w_count = 5, 4
      m_pick, w_pick = 2, 2
      ans_val = math.comb(m_count, m_pick) * math.comb(w_count, w_pick)
      target_expr = f"남학생 {m_count}명, 여학생 {w_count}명 중에서 남학생 {m_pick}명과 여학생 {w_pick}명을 뽑는 방법의 수"
      distractors = [math.comb(m_count+w_count, m_pick+w_pick), ans_val + 10, 60, 120]

  elif user_level == 4:
      # [Level 4] 심화: '적어도' 조건 (여사건 활용)
      # 전체에서 한쪽 성별만 뽑히는 경우 제외하기
      # 소재: 특정 성별이 적어도 한 명 포함되도록 팀 구성
      total_m, total_w = 4, 4
      pick = 3
      # 8C3 - (4C3 + 4C0 - 안 뽑히는 경우) -> 여기서는 남성팀 또는 여성팀만 되는 경우 제외
      ans_val = math.comb(total_m + total_w, pick) - (math.comb(total_m, pick) + math.comb(total_w, pick))
      target_expr = f"남학생 {total_m}명, 여학생 {total_w}명 중에서 {pick}명의 대표를 뽑을 때, 남학생과 여학생이 적어도 한 명씩은 포함되도록 뽑는 방법의 수"
      distractors = [math.comb(total_m + total_w, pick), ans_val - 2, 56, 48]

  else:
      # [Level 5] 킬러: 조합의 성질과 방정식 (nCr = nCk 활용)
      # nCr = nC(n-r) 성질이나 nCr + nCr+1 = n+1Cr+1 성질(파스칼의 삼각형) 이용
      r_val = random.randint(2, 4)
      n_val = 2 * r_val + random.randint(1, 3)
      # nCr = nC(n-r) 형태의 방정식
      target_expr = f"조합의 성질을 이용하여 등식 ${{{n_val}}}C_{{r}} = {{{n_val}}}C_{{{n_val - r_val}}}$를 만족시키는 자연수 $r$의 값들의 합"
      ans_val = r_val + (n_val - (n_val - r_val)) # 사실상 가능한 r값들의 합 로직
      ans_val = n_val # nCr = nCk 이면 r=k 또는 r+k=n 임을 이용
      distractors = [r_val, n_val - r_val, 0, 1]

  render_vars = {
      "target_expr": target_expr,
      "ans_val": ans_val
  }
---
### [경우의 수: 조합의 뜻과 활용]

다음 상황에서 대상을 선택하는 모든 방법의 수를 구하시오.

**[문제 상황]**
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