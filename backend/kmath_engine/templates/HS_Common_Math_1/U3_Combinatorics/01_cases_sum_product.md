---
id: "Cases_Sum_Product_Master"
master_id: "STD-HIGH-06"
category: "Cases_Basics"
title: "합의 법칙과 곱의 법칙"
type_tag: "Cases_Sum_Product"
KC_tags: ["합의 법칙", "곱의 법칙", "약수의 개수", "사건의 가짓수"]
required_context: "unit_sales"
description: "사건이 일어나는 모든 경우의 수를 합의 법칙과 곱의 법칙을 이용해 구하는 문제."

logic_setup: |
  import random

  # 1. 난이도(user_level)별 로직 분기 (5단계 엄격 분리)
  if user_level == 1:
      # [Level 1] 기초: 단순 합의 법칙 (A 또는 B를 선택하는 경우)
      # 소재: 매점 메뉴 선택 등
      n1 = random.randint(3, 5) # 첫 번째 카테고리 아이템 수
      n2 = random.randint(3, 5) # 두 번째 카테고리 아이템 수
      item1 = ctx['items'][0]
      item2 = ctx['items'][1]
      target_expr = f"{ctx['name']}에서 {item1} {n1}종류와 {item2} {n2}종류 중 하나를 선택하는 방법의 수"
      ans_val = n1 + n2
      distractors = [n1 * n2, abs(n1 - n2), n1, n2]

  elif user_level == 2:
      # [Level 2] 기본: 단순 곱의 법칙 (A와 B를 연이어 선택하는 경우)
      # 소재: 세트 메뉴 구성 등
      n1 = random.randint(2, 4)
      n2 = random.randint(3, 5)
      item1 = ctx['items'][0]
      item2 = ctx['items'][1]
      target_expr = f"{ctx['name']}에서 {item1} {n1}종류 중 하나와 {item2} {n2}종류 중 하나를 각각 골라 세트를 만드는 방법의 수"
      ans_val = n1 * n2
      distractors = [n1 + n2, n1**2, n2**2, n1 * n2 - 1]

  elif user_level == 3:
      # [Level 3] 응용: 약수의 개수 (소인수분해와 곱의 법칙)
      # 수활북 스타일: 숫자의 성질 이용
      p1, p2 = 2, 3
      a = random.randint(2, 4)
      b = random.randint(1, 3)
      num = (p1**a) * (p2**b)
      target_expr = f"자연수 ${num}$의 양의 약수의 개수"
      ans_val = (a + 1) * (b + 1)
      distractors = [a * b, a + b, (a + 1) + (b + 1), num // 2]

  elif user_level == 4:
      # [Level 4] 심화: 조건이 붙은 합과 곱의 혼합
      # 예: 1~N까지 자연수 중 특정 숫자의 배수 또는 다른 숫자의 배수 (포함배제)
      limit = random.choice([50, 100])
      k1, k2 = 3, 4 # 예: 3의 배수 또는 4의 배수
      count1 = limit // k1
      count2 = limit // k2
      count_both = limit // (k1 * k2 // 1) # 최소공배수 배수
      target_expr = f"$1$부터 ${limit}$까지의 자연수 중에서 ${k1}$의 배수 또는 ${k2}$의 배수의 개수"
      ans_val = count1 + count2 - count_both
      distractors = [count1 + count2, count1 + count2 + count_both, limit // k1, limit // k2]

  else:
      # [Level 5] 킬러: 방정식의 해의 개수 (노가다 분류 + 합의 법칙)
      # ax + by = c 를 만족하는 자연수 x, y의 순서쌍 (최상위 변별력)
      c = random.randint(15, 25)
      a, b = 2, 3
      count = 0
      for i in range(1, c//a + 1):
          for j in range(1, c//b + 1):
              if a*i + b*j <= c: # 부등식으로 난이도 상향
                  count += 1
      target_expr = f"부등식 ${a}x + {b}y \\le {c}$를 만족시키는 자연수 $x, y$의 순서쌍 $(x, y)$의 개수"
      ans_val = count
      distractors = [count + 2, count - 2, count * 2, 0]

  render_vars = {
      "target_expr": target_expr,
      "ans_val": ans_val
  }
---
다음 상황에서 발생하는 모든 경우의 수를 구하시오.

**[상황]**
{{ target_expr }}



{% if question_type == 'multiple_choice' %}
① ${{ opt1 }}$
② ${{ opt2 }}$
③ ${{ opt3 }}$
④ ${{ opt4 }}$
⑤ ${{ opt5 }}$

{% elif question_type == 'short_answer' %}
**[정답]** ${{ ans_val }}$

{% elif question_type == 'fill_in_the_blank' %}
구하고자 하는 경우의 수는 $\square$ 가지이다. 빈칸에 알맞은 수를 쓰시오.

**[정답]** {{ ans_val }}
{% endif %}