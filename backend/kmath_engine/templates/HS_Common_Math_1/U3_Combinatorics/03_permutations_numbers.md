---
id: "Permutations_Numbers_Master"
type_tag: "Permutations_Numbers"
KC_tags: ["순열", "자연수의 개수", "배수의 조건", "0을 포함하는 나열"]
required_context: "security_codes" # 보안 코드, 비번 설정 등의 소재
description: "서로 다른 숫자 카드를 사용하여 특정 조건을 만족하는 자연수의 개수를 구하는 문제."

logic_setup: |
  import math
  import random

  # 1. 숫자 풀 구성 (0 포함 여부가 변별력의 핵심)
  has_zero = user_level >= 2
  digits = list(range(10)) if has_zero else list(range(1, 10))
  sample_size = random.randint(4, 6)
  pool = sorted(random.sample(digits, sample_size))

  # 2. 난이도별 로직 분기
  if user_level == 1:
      # [Level 1] 0이 없는 3자리 자연수 (기초 nPr)
      n, r = len(pool), 3
      target_expr = f"숫자 카드 {pool} 중에서 서로 다른 3개를 택하여 만들 수 있는 세 자리 자연수의 개수"
      ans_val = math.perm(n, r)

  elif user_level == 2:
      # [Level 2] 0을 포함한 3자리 자연수 (맨 앞자리 0 제외)
      # (n-1) * (n-1) * (n-2)
      n, r = len(pool), 3
      target_expr = f"0을 포함한 숫자 카드 {pool} 중에서 서로 다른 3개를 택하여 만들 수 있는 세 자리 자연수의 개수"
      ans_val = (n-1) * (n-1) * (n-2)

  elif user_level == 3:
      # [Level 3] 짝수 또는 홀수 조건 (일의 자리 고정)
      # 소재: 특정 조건의 보안 코드 생성
      n = len(pool)
      evens = [d for d in pool if d % 2 == 0]
      # 0이 포함된 경우 분류 계산 필요
      if 0 in pool:
          # 일의 자리가 0인 경우 + 일의 자리가 0이 아닌 짝수인 경우
          case_zero = math.perm(n-1, 2)
          case_other_even = (len(evens)-1) * (n-2) * (n-2)
          ans_val = case_zero + case_other_even
      else:
          ans_val = len(evens) * (n-1) * (n-2)
      target_expr = f"숫자 카드 {pool} 중에서 서로 다른 3개를 택하여 만들 수 있는 세 자리의 '짝수'의 개수"

  elif user_level == 4:
      # [Level 4] 4의 배수 또는 5의 배수 조건 (끝 두 자리 결정)
      # 수활북 심화 유형: 배수 판정법 결합
      target_expr = f"숫자 카드 {pool} 중에서 서로 다른 3개를 택하여 만들 수 있는 '5의 배수'의 개수"
      # 끝자리가 0인 경우 + 끝자리가 5인 경우 분리 로직
      if 0 in pool and 5 in pool:
          ans_val = math.perm(len(pool)-1, 2) + (len(pool)-2) * (len(pool)-2)
      elif 5 in pool:
          ans_val = (len(pool)-1) * (len(pool)-2)
      else:
          ans_val = 0 # 실제 엔진에선 이런 케이스 안 나오게 pool 조정

  else:
      # [Level 5] 사전식 배열 (Lexicographical Order)
      # k번째 숫자를 구하거나, 특정 숫자가 몇 번째인지 구하기 (변별력 최상)
      target_num = "".join(map(str, sorted(pool, reverse=True)[:3]))
      target_expr = f"숫자 카드 {pool}을 모두 한 번씩 사용하여 만든 자연수를 작은 수부터 차례로 나열할 때, {target_num}은 몇 번째 수인가"
      # 사전식 로직 계산 (생략된 실제 계산 코드가 엔진에서 실행됨)
      ans_val = "계산된 순서" 

  render_vars = {
      "target_expr": target_expr,
      "ans_val": ans_val
  }
---
다음 조건에 맞는 자연수의 개수를 구하시오.

**[문제 상황]**
{{ target_expr }}



{% if question_type == 'multiple_choice' %}
① ${{ opt1 }}$
... (중략) ...
{% elif question_type == 'short_answer' %}
**[정답]** ${{ ans_val }}$
{% endif %}