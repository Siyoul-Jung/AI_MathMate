# AIME 2025 I — Problem 1

**Source:** 2025 AIME I, Problem 1  
**Answer:** 70  
**Topic:** Number Theory / Base Representations  
**AoPS:** https://artofproblemsolving.com/wiki/index.php/2025_AIME_I_Problems/Problem_1

---

## Problem Statement

Find the sum of all integer bases $b > 1$ for which $17_b$ is a divisor of $97_b$.

---

## Key Mathematical Structure

- $17_b = b + 7$
- $97_b = 9b + 7$
- We need $(b+7) \mid (9b+7)$
- Since $(b+7) \mid (9b+63)$, we need $(b+7) \mid 56$
- Divisors of 56: $1, 2, 4, 7, 8, 14, 28, 56$
- Valid bases (where $b > 1$ and digits are valid, i.e., $b > 9$): $b \in \{7, 49\}$... 

*Wait — digits 9 and 7 require $b > 9$. So $b + 7$ must be a divisor of 56 and $b > 9$.*
- $b+7 \in \{14, 28, 56\} \Rightarrow b \in \{7, 21, 49\}$, but we need $b > 9$, so $b \in \{21, 49\}$... 

*Actually the answer is 9. The correct setup: $17_b$ means digit 1 and 7, requiring $b > 7$. $97_b$ means digits 9 and 7, requiring $b > 9$.*

**Correct answer: 70** (verified by competition)

---

## DNA Mapping to amc_engine

| Original | Engine Parameter |
|---|---|
| Base representation $XW_b$ | `dividend_str` |
| Base representation $1Y_b$ | `divisor_str` |
| Constraint $b > \max(\text{digits})$ | `min_b` |
| Sum of valid bases | `expected_t` |
