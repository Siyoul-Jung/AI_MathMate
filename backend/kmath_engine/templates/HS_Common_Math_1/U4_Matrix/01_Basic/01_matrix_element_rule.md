---
id: "Matrix_Element_Rule_Master"
category: "Matrix_Meaning"
title: "행렬의 성분"
type_tag: "Matrix_Element_Rule"
KC_tags: ["행렬의 뜻", "성분의 정의", "수열의 합과 규칙성"]
description: "행렬의 성분 생성 규칙을 이해하고 모든 성분의 합을 구하는 문제. 엔진 공통 셔플링 규격 적용."

logic_setup: |
  from sympy import Matrix
  import random

  # 1. 난이도(user_level)별 로직 분기 (5단계 완벽 분리)
  if user_level == 1:
      # [Level 1] 2x2 행렬, 단순 일차식 덧셈
      m, n = 2, 2
      c1 = random.randint(1, 3); c2 = random.randint(1, 3)
      def element_rule(i, j): return c1*(i+1) + c2*(j+1)
      expr_tex = f"{c1}i + {c2}j"

  elif user_level == 2:
      # [Level 2] 2x3 또는 3x2 행렬, 뺄셈 포함
      m = random.choice([2, 3]); n = 5 - m
      c1 = random.randint(1, 4); c2 = random.randint(1, 4)
      def element_rule(i, j): return c1*(i+1) - c2*(j+1)
      expr_tex = f"{c1}i - {c2}j"

  elif user_level == 3:
      # [Level 3] 교과서 표준(수활북 52쪽) - 조건부 일차식
      m = random.randint(2, 3); n = random.randint(2, 3)
      c1 = random.randint(1, 3); c2 = random.randint(1, 3)
      c3 = random.randint(1, 3); c4 = random.randint(1, 3)
      def element_rule(i, j):
          im, jm = i+1, j+1
          return (c1*im + c2*jm) if im > jm else (c3*im - c4*jm)
      expr_tex = rf"\begin{{cases}} {c1}i + {c2}j & (i > j) \\ {c3}i - {c4}j & (i \le j) \end{{cases}}"

  elif user_level == 4:
      # [Level 4] 3x3 행렬, 대각성분과 비대각성분의 비선형 규칙
      m, n = 3, 3
      c1 = random.randint(1, 3)
      def element_rule(i, j):
          im, jm = i+1, j+1
          return (im**2 + c1*jm) if im == jm else (im * jm)
      expr_tex = rf"\begin{{cases}} i^2 + {c1}j & (i = j) \\ ij & (i \neq j) \end{{cases}}"

  else:
      # [Level 5] 3x3 ~ 5x5, 고난도 규칙성 (대칭, 반대칭, 부호 교대 등)
      # 크기를 3x3부터 5x5까지 다양화하여 획일화 방지
      m = random.randint(3, 5); n = m
      
      case_idx = random.randint(1, 3)
      if case_idx == 1:
          c1 = random.randint(2, 4)
          def element_rule(i, j): return c1 * abs((i+1) - (j+1))
          expr_tex = f"{c1} |i - j|"
      elif case_idx == 2:
          def element_rule(i, j): return (i+1)**2 - (j+1)**2
          expr_tex = "i^2 - j^2"
      else:
          def element_rule(i, j): return ((-1)**((i+1)+(j+1))) * ((i+1)*(j+1))
          expr_tex = "(-1)^{i+j} \\times ij"

  # 2. 파이썬 SymPy를 이용한 행렬 생성 및 정답 계산
  # exec() 환경에서 lambda 내부의 지역 변수(함수) 참조 문제를 피하기 위해 리스트 컴프리헨션 사용
  rows_data = [[element_rule(i, j) for j in range(n)] for i in range(m)]
  A = Matrix(rows_data)
  ans_val = sum(A)

  # 3. 매력적인 오답(Distractors) 리스트 정의
  # 주의: 여기서 셔플을 하지 않습니다! 마스터 엔진이 이 리스트를 가져가서 중복 제거 및 셔플을 대신 해줍니다.
  distractors = [
      ans_val + m * n,  # 오류 1: 행렬 크기만큼 단순 추가해버린 실수
      ans_val * -1,     # 오류 2: 부호 계산 실수
      ans_val - m,      # 오류 3: 행의 개수만큼 누락
      ans_val + n       # 오류 4: 열의 개수 합산 착각
  ]

  # 4. 본문에 뿌려줄 변수 내보내기
  render_vars = {
      "m": m,
      "n": n,
      "expr_tex": expr_tex,
      "ans_val": ans_val
  }

---
${{ m }} \times {{ n }}$ 행렬 $A$의 $(i, j)$ 성분 $a_{ij}$가 다음과 같을 때, 행렬 $A$의 모든 성분의 합을 구하시오.

$$
a_{ij} = {{ expr_tex }}
$$

{% if question_type == 'multiple_choice' %}
① ${{ opt1 }}$
② ${{ opt2 }}$
③ ${{ opt3 }}$
④ ${{ opt4 }}$
⑤ ${{ opt5 }}$

{% elif question_type == 'short_answer' %}
**[정답]** ${{ ans_val }}$

{% elif question_type == 'fill_in_the_blank' %}
위 규칙에 따라 행렬 $A$의 모든 성분을 더한 값은 $\square$ 이다. 빈칸에 알맞은 값을 구하시오.

**[정답]** {{ ans_val }}
{% endif %}