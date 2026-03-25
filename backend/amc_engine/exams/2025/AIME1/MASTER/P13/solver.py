import random
import re
import math
import matplotlib.pyplot as plt
import numpy as np
import os

class Solver:
    DNA = {
        "context_type": "combinatorics_geometry",
        "category": "Combinatorics / Geometry",
        "specific_tag": "EXPECTED-REGIONS-DISK",
        "has_image": True,
        "level": 13
    }
    DRILL_LEVELS = [1, 2, 3]
    DIFFICULTY_BAND = "MASTER"

    # 테마 카테고리: LLM이 이 중 하나를 받아 자유롭게 시나리오를 창작
    THEME_CATEGORIES = [
        "science lab / biology research",
        "cooking / culinary arts",
        "urban planning / architecture",
        "visual art / design / stained glass",
        "technology / engineering / circuit design",
        "sports / games / competition",
        "transportation / navigation",
        "nature / ecology / environmental science",
        "music / performance / theater",
        "astronomy / space exploration",
    ]

    def __init__(self, payload=None, config=None):
        self.payload = payload or {}

    def execute(self):
        return float(self.payload.get('expected_t', 0))

    @classmethod
    def generate_drill_seed(cls, level):
        import math
        seed = cls.generate_seed()
        seed['drill_level'] = level
        
        if level == 1:
            # Level 1: Basic Euler Region Count (No probability)
            k = random.randint(5, 12)
            # 1 + k + k(k-1)/2 regions for k lines in general position
            ans = 1 + k + (k * (k - 1) // 2)
            seed['n_lines'] = k
            seed['expected_t'] = float(ans)
        elif level == 2:
            # Level 2: Probability logic check
            m = seed['m']
            p_inter = (1 / 3) * (1 + 1 / (m ** 2))
            seed['expected_t'] = float(1 + m**2) # This is 3m^2 * P
        else:
            # Level 3: Full AIME logic
            pass
            
        return seed

    @classmethod
    def generate_seed(cls):
        # Original AIME 2025 I #13 logic. 
        # Avoid original m=10 (diameters)
        for _ in range(200):
            m = random.randint(4, 25) 
            if m == 10: continue
            
            n = random.randint(5, 80)
            quadrants = 2 * m
            total_lines = m + n

            p_inter = (1 / 3) * (1 + 1 / (m ** 2))
            expected_t = int(round((m + n + 1) + (n * (n - 1) / 2) * p_inter))
            
            if 0 < expected_t < 1000:
                return {
                    'm': m, 'quadrants': quadrants, 'n': n,
                    'total_lines': total_lines, 'expected_t': expected_t
                }
        return {'m': 6, 'quadrants': 12, 'n': 30, 'total_lines': 36, 'expected_t': 185}

    @classmethod
    def generate_image(cls, seed, filepath):
        """Generates a circle with chords representing the problem."""
        fig, ax = plt.subplots(figsize=(6, 6))
        circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
        ax.add_artist(circle)
        
        m = seed.get('m', 10)
        n = seed.get('n', 10)
        
        # Draw diameters
        for i in range(m):
            angle = math.pi * i / m
            ax.plot([-math.cos(angle), math.cos(angle)], 
                    [-math.sin(angle), math.sin(angle)], 
                    color='gray', linestyle='--', alpha=0.5)
            
        # Draw some sample chords (n might be too many)
        sample_n = min(n, 12)
        for _ in range(sample_n):
            a1, a2 = random.uniform(0, 2*math.pi), random.uniform(0, 2*math.pi)
            ax.plot([math.cos(a1), math.cos(a2)], 
                    [math.sin(a1), math.sin(a2)], 
                    color='blue', alpha=0.7)
            
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.title(f"Disk Partitioning (m={m}, n={n})")
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(fig)

    @classmethod
    def get_drill_instruction(cls, seed, level):
        m, q, n = seed['m'], seed['quadrants'], seed.get('n_lines', seed['n'])
        
        if level == 1:
            return (
                f"Construct a foundational geometry drill problem.\n"
                f"A circular disk is partitioned by {n} distinct line segments.\n"
                "No two segments are parallel, and no three segments intersect at the same point.\n"
                "Find the maximum number of regions the disk is divided into."
            )
        elif level == 2:
            return (
                f"Construct a combinatorial probability problem.\n"
                f"A circle is divided into {q} equal sectors by {m} diameters.\n"
                "Two chords are drawn such that their endpoints are chosen uniformly at random from the boundary, "
                "with the constraint that the two endpoints of EACH chord must lie in different sectors.\n"
                f"Let $P$ be the probability that these two chords intersect. Calculate $3 \cdot {m}^2 \cdot P$."
            )
        else:
            category = random.choice(cls.THEME_CATEGORIES)
            return (
                f"Construct an advanced expected value problem wrapped in the theme of [{category}].\n"
                f"Scenario: A circular area is divided into {q} equal sectors by {m} diameters.\n"
                f"Additionally, {seed['n']} chords are drawn such that each chord's endpoints lie in DIFFERENT sectors.\n"
                f"In total, there are {seed['total_lines']} line segments. "
                "Find the expected number of regions formed within the circle."
            )

    @classmethod
    def get_narrative_instruction(cls, seed):
        m, q, n = seed['m'], seed['quadrants'], seed['n']
        category = random.choice(cls.THEME_CATEGORIES)
        return (
            f"Write an official AIME competition problem with theme [{category}].\n"
            f"Disk divided into {q} sectors by {m} diameters. {n} additional lines with endpoints in different sectors.\n"
            "Find the expected number of regions."
        )

    @classmethod
    def verify_narrative(cls, narrative, seed):
        """
        Legacy interface — 실제 검증은 verifier.py의 stage1/stage2가 담당.
        pipeline_manager가 verifier를 직접 호출하면 이 메서드는 사용되지 않음.
        하위 호환성을 위해 유지.
        """
        vals = [seed['m'], seed['quadrants'], seed['n'], seed['total_lines']]
        lower = narrative.lower()
        for v in vals:
            if str(v) not in lower:
                return False, f"Value {v} missing"
        if not any(w in lower for w in ["different", "distinct", "separate"]):
            return False, "Missing crucial constraint"
        return True, "OK"