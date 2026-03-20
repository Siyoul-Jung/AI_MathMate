---
id: "Matrix_Real_Life_Master"
category: "Matrix_Operation"
title: "행렬의 실생활 활용"
required_context: "inventory_sales"
type_tag: "Real_Life_Modeling"
KC_tags: ["실생활 데이터 행렬 변환", "행렬의 곱셈", "총합 연산"]
description: "실생활 데이터를 행렬로 나타내고 곱셈을 통해 총합을 구하는 문제."

logic_setup: |
  import random
  from sympy import Matrix, latex

  # 1. Context 설정
  if 'injected_context' in locals() and injected_context:
      if isinstance(injected_context, list):
          ctx = random.choice(injected_context)
      else:
          ctx = injected_context
  else:
      # Fallback: 기본값도 랜덤하게 생성하여 다양성 확보
      p1, p2 = random.randint(10, 50) * 100, random.randint(10, 50) * 100
      ctx = {"name": "가게", "items": ["품목A", "품목B"], "prices": [p1, p2], "unit": "개"}

  # Jinja2 dict.items() 메서드 충돌 방지
  ctx['products'] = ctx.get('items', ["품목A", "품목B"])

  # 가격 랜덤화 (기본 가격의 80% ~ 120% 범위, 100원 단위 반올림)
  base_prices = ctx.get("prices", [1000, 2000])
  random_prices = [round(p * random.uniform(0.8, 1.2), -2) for p in base_prices]
  ctx['prices'] = [int(p) for p in random_prices]

  # 2. 판매 데이터 생성 (2x2 행렬 P)
  # sales_data[지점][품목]
  sales_data = [[random.randint(5, 50) for _ in range(2)] for _ in range(2)]
  P = Matrix(sales_data)
  
  # 3. 가격 데이터 생성 (2x1 행렬 Q)
  Q = Matrix(ctx['prices'])
  
  # 4. 결과 계산 (P * Q = R)
  # R[0] = A지점 매출, R[1] = B지점 매출
  R = P * Q
  
  # 질문 대상을 지점 A(0) 또는 B(1) 중 랜덤 선택
  target_idx = random.randint(0, 1)
  target_name = ["A 지점", "B 지점"][target_idx]
  ans_val = R[target_idx, 0]

  # 5. 오답 설계
  distractors = [
      sum(sales_data[target_idx]) * sum(ctx['prices']), # 가격과 수량을 통째로 더해서 곱하는 실수
      R[1-target_idx, 0], # 다른 지점의 매출액을 정답으로 착각
      ans_val + 500,
      ans_val - 500
  ]

  render_vars = {
      "ctx": ctx,
      "s": sales_data,
      "target_name": target_name,
      "ans_val": ans_val
  }
---
어느 **{{ ctx.name }}**의 A 지점과 B 지점에서 하루 동안 판매된 **{{ ctx.products[0] }}**와 **{{ ctx.products[1] }}**의 판매량은 다음 표와 같다.

<div style="width: 100%; display: flex; justify-content: center; margin: 20px 0;">
  <table style="border-collapse: collapse; width: 80%; max-width: 500px; text-align: center; border: 1px solid #ddd; font-size: 0.95rem;">
    <thead>
      <tr style="background-color: #f3f4f6; border-bottom: 2px solid #e5e7eb;">
        <th style="padding: 10px; border: 1px solid #e5e7eb;">지점</th>
        <th style="padding: 10px; border: 1px solid #e5e7eb;">{{ ctx.products[0] }}</th>
        <th style="padding: 10px; border: 1px solid #e5e7eb;">{{ ctx.products[1] }}</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 10px; border: 1px solid #e5e7eb; font-weight: bold; background-color: #f9fafb;">A 지점</td>
        <td style="padding: 10px; border: 1px solid #e5e7eb;">{{ s[0][0] }}</td>
        <td style="padding: 10px; border: 1px solid #e5e7eb;">{{ s[0][1] }}</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #e5e7eb; font-weight: bold; background-color: #f9fafb;">B 지점</td>
        <td style="padding: 10px; border: 1px solid #e5e7eb;">{{ s[1][0] }}</td>
        <td style="padding: 10px; border: 1px solid #e5e7eb;">{{ s[1][1] }}</td>
      </tr>
    </tbody>
  </table>
</div>

또한, {{ ctx.products[0] }} 한 개의 가격은 {{ ctx.prices[0] }}원, {{ ctx.products[1] }} 한 개의 가격은 {{ ctx.prices[1] }}원이다. 
이 판매 데이터를 행렬 $P = \begin{pmatrix} {{ s[0][0] }} & {{ s[0][1] }} \\ {{ s[1][0] }} & {{ s[1][1] }} \end{pmatrix}$ 와 가격 행렬 $Q = \begin{pmatrix} {{ ctx.prices[0] }} \\ {{ ctx.prices[1] }} \end{pmatrix}$ 의 곱으로 나타낼 때, **{{ target_name }}**의 총 매출액을 구하시오.

{% if question_type == 'multiple_choice' %}
① {{ opt1 }}원
② {{ opt2 }}원
③ {{ opt3 }}원
④ {{ opt4 }}원
⑤ {{ opt5 }}원

{% elif question_type == 'short_answer' %}
**[정답]** {{ ans_val }}원

{% elif question_type == 'fill_in_the_blank' %}
구하고자 하는 총 매출액은 $\square$원 이다. 빈칸에 알맞은 값을 구하시오.

**[정답]** {{ ans_val }}
{% endif %}