## [PROBLEM DNA: {specific_tag}]

### 1. MATHEMATICAL CORE
- Points $(x, y, z)$ in 3D space on the plane $x + y + z = {N}$
- Satisfying the inequality chain: $x - yz < y - zx < z - xy$
- Equivalent to: $(x-y)(1+z) < 0$ AND $(y-z)(1+x) < 0$
- Three disjoint convex regions result; the finite one is a triangle.
- Finite triangle vertices: $({N}/3, {N}/3, {N}/3)$, $(-1, -1, {N}+2)$, $(-1, ({N}+1)/2, ({N}+1)/2)$
- Area = $\frac{({N}+3)^2\sqrt{3}}{12}$

### 2. STYLE & NARRATIVE GUIDELINE
{NARRATIVE_INSTRUCTION}
- **CRITICAL**: Do NOT mention any "figures", "graphs", "diagrams", or "as shown in the image" in the problem text. This is a text-only problem.

### 3. REQUIRED PAYLOAD
- N: {N}, expected_t: {expected_t}

---
*⚙️ Engine Seed: N={N}*
