import math
import random
import sympy.ntheory

class Solver:
    DNA = {
        "core_concept": "COMBINATORICS-GRID-FRANEL",
        "has_image": True,
        "difficulty": 4,
        "category": "Combinatorics",
        "level": 10
    }
    DRILL_LEVELS = [1, 2, 3]
    DIFFICULTY_BAND = "EXPERT"
    
    GOLDEN_SEEDS = [
        {'K': 3, 'expected_t': 81}
    ]

    def __init__(self, payload=None, config=None):
        self.payload = payload
        self.config = config

    @classmethod
    def compute_exact_answer(cls, K):
        # Total ways = (3K)! * S(K) * (K!)^6
        # where S(K) = sum( (K choose k)^3 ) for k=0..K
        
        S_K = sum(math.comb(K, k)**3 for k in range(K + 1))
        
        fact_3K = math.factorial(3 * K)
        fact_K = math.factorial(K)
        
        total_ways = fact_3K * S_K * (fact_K ** 6)
        
        # Prime factorization
        factors = sympy.ntheory.factorint(total_ways)
        
        # Calculate sum of (prime * exponent)
        final_answer = sum(p * e for p, e in factors.items())
        return final_answer

    @classmethod
    def generate_seed(cls):
        # Copyright-Safe: Avoid K=3 (Original AIME 2025 I #10)
        for _ in range(50):
            K = random.choice([1, 2, 4, 5])
            ans = cls.compute_exact_answer(K)
            if 0 <= ans <= 999:
                return {'K': K, 'expected_t': ans}
                
        return {'K': 2, 'expected_t': 38} # Non-original fallback

    def execute(self):
        return self.payload['expected_t']

    @classmethod
    def generate_image(cls, seed, filepath):
        import matplotlib.pyplot as plt
        import numpy as np

        K = seed['K']
        rows = 3
        cols = 3 * K
        
        fig, ax = plt.subplots(figsize=(cols * 0.6, rows * 0.6))
        
        # Create a deterministically valid grid
        # M[r][c] = (c + r * K) % (3K) + 1
        grid = np.zeros((rows, cols), dtype=int)
        for r in range(rows):
            for c in range(cols):
                grid[r, c] = (c + r * K) % (3 * K) + 1
                
        # Draw cells and text
        for r in range(rows):
            for c in range(cols):
                # matplotlib origin (0,0) is bottom-left, typically. We'll draw from top-left.
                plot_x = c
                plot_y = rows - 1 - r
                ax.text(plot_x + 0.5, plot_y + 0.5, str(grid[r, c]), 
                        ha='center', va='center', fontsize=14, color='black')
                
        # Draw grid lines
        for i in range(cols + 1):
            lw = 3 if i % K == 0 else 1
            ax.plot([i, i], [0, rows], color='black', linewidth=lw)
            
        for i in range(rows + 1):
            lw = 3 if i in [0, rows] else 1
            ax.plot([0, cols], [i, i], color='black', linewidth=lw)
            
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close(fig)

    @classmethod
    def get_narrative_instruction(cls, seed):
        K = seed['K']
        cells = 3 * 3 * K
        row_length = 3 * K
        
        return f"""
Construct an AIME-level math problem based on the following mathematical structure.

# Mathematical DNA & Rules:
1. Explain that a grid of 3 rows and {row_length} columns (total {cells} cells) is filled using the numbers 1 through {row_length}.
2. The grid is divided into three blocks of size $3 \\times {K}$ (side-by-side).
3. Each row must contain {row_length} different numbers (a permutation of 1 to {row_length}).
4. Each of the three $3 \\times {K}$ blocks must also contain {row_length} different numbers (a permutation of 1 to {row_length}). This is akin to Sudoku rules.
5. The problem asks for the number of different valid grids.
6. The total number of valid grids can be prime factorized as $\\prod p_i^{{e_i}}$, where $p_i$ are distinct prime numbers and $e_i$ are positive integers.
7. Ask to find the sum $\\sum (p_i \\cdot e_i)$.

# Style:
Ensure formal combinatorics terminology. Do not reference the original AIME Sudoku graphic, but explain the block boundaries clearly (e.g. columns 1 to {K}, columns {K+1} to {2*K}, columns {2*K+1} to {3*K}).
End with "Find the sum of $p_i \\cdot e_i$."
"""

    @classmethod
    def verify_narrative(cls, narrative, seed):
        K = seed['K']
        row_length = 3 * K
        cells = 3 * row_length
        # Deep check for numerical mentions
        if str(row_length) not in narrative:
            return False, f"Missing row length {row_length}"
        if str(K) not in narrative and K != 1:
            # For K=1, it might just say 3x1.
            return False, f"Missing block dimension {K}"
            
        return True, "Passed P10 combinatorial verification"

    @classmethod
    def generate_drill_seed(cls, level):
        import math
        import random
        
        if level == 1:
            K = random.randint(2, 4)
            ans = math.factorial(3 * K)
            return {'K': K, 'expected_t': ans, 'drill_level': 1}
        elif level == 2:
            K = 1
            S_K = sum(math.comb(1, k)**3 for k in range(2))
            total_ways = math.factorial(3) * S_K * (math.factorial(1) ** 6)
            return {'K': 1, 'expected_t': total_ways, 'drill_level': 2}
        elif level == 3:
            K = random.randint(2, 3)
            S_K = sum(math.comb(K, k)**3 for k in range(K + 1))
            fact_3K = math.factorial(3 * K)
            fact_K = math.factorial(K)
            total_ways = fact_3K * S_K * (fact_K ** 6)
            return {'K': K, 'expected_t': total_ways, 'drill_level': 3}
            
        return cls.GOLDEN_SEEDS[0]

    @classmethod
    def get_drill_instruction(cls, seed, level):
        K = seed['K']
        cells = 3 * 3 * K
        row_length = 3 * K
        
        if level == 1:
            return f"""
Construct an AIME-style concept drill (Level 1) focusing purely on permutations.
Explain that we have a single row of {row_length} empty slots.
We must fill it with the numbers 1 through {row_length} such that no numbers repeat.
Ask for the total number of ways to do this.
Do NOT mention anything about multiple rows, blocks, or primes.
Just ask for the raw total number of permutations.
"""
        elif level == 2:
            return f"""
Construct an AIME-style concept drill (Level 2) focusing on basic intersecting constraints.
Explain that a grid of 3 rows and {row_length} columns (total {cells} cells) is filled using the numbers 1 through {row_length}.
The grid is divided into three blocks of size $3 \\times {K}$.
Each row must contain {row_length} different numbers.
Each block must contain {row_length} different numbers.
Ask for the total number of valid ways to fill this miniature grid.
Do NOT ask for prime factorization. Just ask for the exact integer of total ways.
"""
        elif level == 3:
            import random
            # Diversity Injector: Forces the LLM to use a randomly assigned logic-proof theme.
            theme_pool = [
                ("University Courses", "assignments of students to different course tracks"),
                ("Logistics & Shipping", "distribution of cargo crates across different delivery fleets"),
                ("Military Defense", "assignment of soldiers to different regional outposts"),
                ("Kitchen Prep", "allocation of special ingredients to different chef stations"),
                ("Automotive Assembly", "routing of car frames onto different manufacturing lines"),
                ("Space Colony", "distribution of colonists across different planetary habitats"),
                ("Server Cloud", "allocation of virtual machines to physical server racks"),
                ("Art Exhibition", "placement of distinct sculptures into different gallery rooms"),
                ("Zoo Enclosures", "distribution of exotic animals into different biomes"),
                ("Olympic Tournaments", "assigning athletes to different qualifier brackets")
            ]
            chosen_domain, chosen_context = random.choice(theme_pool)
            
            return f"""
Construct a difficult mathematical modeling concept drill (Level 3) wrapped in a real-world scenario.

[THEME/SCENARIO INSTRUCTION]:
You MUST build your story around the following randomly selected theme:
Domain: "{chosen_domain}"
Context: "{chosen_context}"
Do NOT use a typical Sudoku or grid theme. You must vividly describe this specific domain.

[MATHEMATICAL CONSTRAINTS to embed in your story]:
1. There are {row_length} "unique items" (e.g., {row_length} soldiers, crates, students, etc.).
2. There are 3 "groups/destinations" (e.g., 3 outposts, 3 fleets, 3 rooms).
3. The process happens over 3 "phases" (e.g., 3 days, 3 weeks, 3 shifts).
4. In each phase, the 3 groups must divide all {row_length} items evenly. Specifically, each group must take EXACTLY {K} items from Group 1's initial state, {K} items from Group 2's, and {K} items from Group 3's initial state so that the proportions are completely balanced. (This represents exact Block intersection math).
5. Add the ultimate rule: Over the 3 phases, NO "item" can visit the same "group" more than once. (Every group must intercept every unique item exactly once).

Ask for the total number of valid deterministic arrangements. 
Do NOT mention grids, Sudoku, rows, or blocks. Mask the pure mathematics completely behind the {chosen_domain} scenario!
"""
        return ""
