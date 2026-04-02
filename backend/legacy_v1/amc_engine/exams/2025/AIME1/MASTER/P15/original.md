# AIME 2025 I — 문제 15

**출처:** 2025 AIME I, Problem 15  
**정답:** 735  
**주제:** 정수론 / 지수 들어올리기 (LTE) / 조합론  
**AoPS:** https://artofproblemsolving.com/wiki/index.php/2025_AIME_I_Problems/Problem_15

---

## 문제 서술 (Problem Statement)

$1 \leq a, b, c \leq 3^6$을 만족하는 양의 정수 순서쌍 $(a, b, c)$ 중에서 $a^3 + b^3 + c^3$이 $3^7$의 배수인 것의 개수를 $N$이라 하자. $N$을 1000으로 나눈 나머지를 구하시오.

---

## 핵심 수학적 구조 (Key Mathematical Structure)

- **변수 범위**: $\{1, 2, \ldots, 3^K\}$ (원본 $K=6$, 상한 $3^6$)
- **약수 조건**: $3^M \mid a^3 + b^3 + c^3$ (원본 $M=7$)
- **풀이 기법**: $p=3$에 대한 지수 들어올리기 보조정리 (LTE Lemma) 및 재귀적 세기.
- **정답**: $N \pmod{1000} = 735$.

---

## amc_engine DNA 매핑

| 항목 | 엔진 파라미터 | 값 |
|---|---|---|
| 상한 지수 ($K=6$) | `K` | 6 |
| 약수 조건 지수 ($M=7$) | `M` | 7 |
| 모듈로 값 | `divisor` | 1000 |
| 결과값 | `expected_t` | 735 |
