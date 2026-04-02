# AIME 2025 I — Problem 12

**Source:** 2025 AIME I, Problem 12  
**Answer:** 510  
**Topic:** Geometry / Algebra / Convex Regions in 3D  
**AoPS:** https://artofproblemsolving.com/wiki/index.php/2025_AIME_I_Problems/Problem_12

---

## Problem Statement

The set of points in 3-dimensional coordinate space that lie in the plane $x + y + z = 75$ whose coordinates satisfy the inequalities $x - yz < y - zx < z - xy$ forms three disjoint convex regions. Exactly one of those regions has finite area. The area of this finite region can be expressed in the form $a\sqrt{b}$, where $a$ and $b$ are positive integers and $b$ is not divisible by the square of any prime. Find $a + b$.

---

## Key Mathematical Structure

**Step 1 — Decompose the inequality chain:**

$$x - yz < y - zx < z - xy$$

- Left inequality: $x - yz < y - zx \Rightarrow (x-y) + z(x-y) < 0 \Rightarrow (x-y)(1+z) < 0$
- Right inequality: $y - zx < z - xy \Rightarrow (y-z) + x(y-z) < 0 \Rightarrow (y-z)(1+x) < 0$

**Step 2 — Classify regions by sign of $(1+x)$ and $(1+z)$:**

| $(1+z)$ | $(1+x)$ | Result |
|---|---|---|
| $> 0$ | $> 0$ | $x < y < z$ — **FINITE triangle** |
| $< 0$ | $< 0$ | $x > y$ AND $y > z$, but $x < -1, z < -1 \Rightarrow y > 77$ contradicts $y < x$ — **EMPTY** |
| $> 0$ | $< 0$ | $x < y$ AND $y > z$ — infinite region |
| $< 0$ | $> 0$ | $x > y$ AND $y < z$ — infinite region |

→ Exactly **3 disjoint regions** (Case 2 is empty).

**Step 3 — Compute finite triangle vertices (on plane $x+y+z=75$):**

| Boundary intersection | Vertex |
|---|---|
| $x=y$ ∩ $y=z$ | $(25, 25, 25)$ |
| $x=y$ ∩ $x=-1$ | $(-1, -1, 77)$ |
| $y=z$ ∩ $x=-1$ | $(-1, 38, 38)$ |

**Step 4 — Compute area via cross product:**

$$\vec{AB} = 26(-1,-1,2), \quad \vec{AC} = 13(-2,1,1)$$

$$\vec{AB} \times \vec{AC} = -1014(1,1,1), \quad |\vec{AB} \times \vec{AC}| = 1014\sqrt{3}$$

$$\text{Area} = \frac{1014\sqrt{3}}{2} = 507\sqrt{3}$$

**Answer: $507 + 3 = 510$** ✅

---

## General Formula (Engine DNA)

For plane $x + y + z = N$ with $N \equiv 3 \pmod{6}$:

$$\text{Answer} = \frac{(N+3)^2}{12} + 3$$

---

## DNA Mapping to amc_engine

| Original | Engine Parameter |
|---|---|
| Plane constant ($N = 75$) | `N` |
| Answer ($a + b$) | `expected_t` |
