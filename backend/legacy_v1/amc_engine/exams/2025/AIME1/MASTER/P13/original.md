# AIME 2025 I — Problem 13

**Source:** 2025 AIME I, Problem 13  
**Answer:** 167  
**Topic:** Combinatorics / Expected Value / Geometric Probability  
**AoPS:** https://artofproblemsolving.com/wiki/index.php/2025_AIME_I_Problems/Problem_13

---

## Problem Statement

Alex divides a disk into four quadrants with two perpendicular diameters intersecting at the center of the disk. He draws $10$ more line segments through the disk, drawing each segment by selecting two points at random on the perimeter of the disk in different quadrants and connecting these two points. Find the expected number of regions into which these $12$ line segments divide the disk.

---

## Key Mathematical Structure

Using Euler's formula $R = 1 + L + X$ where:
- $L$ = number of line segments = $2 + 10 = 12$
- $X$ = expected number of intersection points (interior)

For the 10 random chords, each pair has probability $\frac{1}{3}\left(1 + \frac{1}{m^2}\right)$ of intersecting inside the disk (where $m=2$ for 4 quadrants, so $p = \frac{1}{3}(1 + \frac{1}{4}) = \frac{5}{12}$).

Expected regions $= (m + n + 1) + \binom{n}{2} \cdot p$

**Answer: 167** (verified by competition)

---

## DNA Mapping to amc_engine

| Original | Engine Parameter |
|---|---|
| Number of diameter lines ($m=2$) | `m` |
| Number of quadrants ($2m = 4$) | `quadrants` |
| Number of random chords ($n=10$) | `n` |
| Total lines ($m+n = 12$) | `total_lines` |
| Expected number of regions | `expected_t` |
