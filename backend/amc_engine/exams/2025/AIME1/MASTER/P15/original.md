# AIME 2025 I — Problem 15

**Source:** 2025 AIME I, Problem 15  
**Answer:** 247  
**Topic:** Number Theory / Lifting the Exponent / Combinatorics  
**AoPS:** https://artofproblemsolving.com/wiki/index.php/2025_AIME_I_Problems/Problem_15

---

## Problem Statement

Let $N$ denote the number of ordered triples of positive integers $(a, b, c)$ such that $a, b, c \leq 3^7$ and $a^3 + b^3 + c^3$ is a multiple of $3^7$. Find the remainder when $N$ is divided by $1000$.

---

## Key Mathematical Structure

- Variables constrained to $\{1, 2, \ldots, 3^7\}$ (i.e., $K=7$, upper bound $3^K$)
- Divisibility condition: $3^M \mid a^3 + b^3 + c^3$ where $M=7$
- Solution uses Lifting the Exponent (LTE) Lemma for $p=3$
- Recursive structure: $T(k, m) = 2 \cdot 3^{3k-m} + T(k-1, m-3)$
- The answer $N \mod 1000 = 247$

**Answer: 247** (verified by competition)

---

## DNA Mapping to amc_engine

| Original | Engine Parameter |
|---|---|
| Exponent in upper bound ($K=7$) | `K` |
| Divisibility exponent ($M=7$) | `M` |
| Modulus ($1000$) | `divisor` |
| $N \mod 1000$ | `expected_t = 247` |
