import math

class Solver:
    """
    2025 AIME I Problem 6
    Isosceles trapezoid with inscribed circle radius R and area A.
    Goal: r^2 + s^2 where r, s are parallel sides.
    """

    DNA = {
        'specific_tag': 'GEOMETRY-TRAPEZOID-CIRCLE',
        'context_type': 'narrative',
        'has_image': True
    }

    def __init__(self, payload=None, config=None):
        self.payload = payload
        self.config = config

    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def solve_static(cls, radius, area):
        # h = 2*R
        h = 2 * radius
        # Area = (r+s)/2 * h => (r+s) = 2*A / h
        sum_rs = 2 * area / h
        
        # Pitot's Theorem: r + s = 2 * side (for isosceles tangential trapezoid)
        side = sum_rs / 2
        
        # Pythagorean on dropped altitude triangle: 
        # ( (r-s)/2 )^2 + h^2 = side^2
        half_diff_sq = side**2 - h**2
        diff_rs_sq = 4 * half_diff_sq
        
        # Identity: r^2 + s^2 = [ (r+s)^2 + (r-s)^2 ] / 2
        val = (sum_rs**2 + diff_rs_sq) / 2
        return round(val)

    @classmethod
    def generate_seed(cls):
        import random
        # Copyright-Safe
        SAFE_FALLBACK = {'radius': 4, 'area': 128, 'expected_t': 800}

        for _ in range(100):
            radius = random.randint(2, 6)
            # Avoid original AIME 2025 I #6 radius
            if radius == 3: radius = 5
            
            min_area = 4 * (radius**2) + 10
            area = random.randint(min_area, min_area + 200)
            
            if area % radius == 0:
                ans = cls.solve_static(radius, area)
                # Ensure not original AIME 2025 I #6: R=3, Area=72
                if radius == 3 and area == 72: continue
                
                if 0 <= ans <= 999:
                    return {
                        'radius': radius,
                        'area': area,
                        'expected_t': ans
                    }
        
        return SAFE_FALLBACK

    @classmethod
    def generate_drill_seed(cls, level):
        import random
        if level == 1:
            # Simple area given r, s, h
            h = random.randint(4, 12)
            s = random.randint(2, 10)
            r = s + random.randint(4, 20)
            return {'r': r, 's': s, 'h': h, 'expected_t': (r+s)*h//2}
        elif level == 2:
            # Side length from r, s in a tangential trapezoid
            s = random.randint(2, 10)
            r = s + random.randint(4, 20)
            return {'r': r, 's': s, 'expected_t': (r+s)//2}
        return cls.generate_seed()

    @classmethod
    def get_narrative_instruction(cls, seed):
        return f"An isosceles trapezoid has an inscribed circle of radius {seed['radius']} and area {seed['area']}. Calculate the sum of the squares of its parallel sides."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Find the area of an isosceles trapezoid with parallel sides of length {seed['r']} and {seed['s']}, and a height of {seed['h']}."
        elif level == 2:
            return f"An isosceles trapezoid has an inscribed circle. If the parallel sides have lengths {seed['r']} and {seed['s']}, find the length of each of the non-parallel sides."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def generate_image(cls, seed, path):
        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_aspect('equal')
        
        # Illustrate a trapezoid and a circle
        # Circle at (0, R)
        R = 3
        circle = plt.Circle((0, R), R, color='blue', fill=False)
        ax.add_artist(circle)
        
        # Trapezoid vertices (simplified)
        h = 2*R
        r = 15 # bottom
        s = 5  # top
        x1 = -r/2; x2 = r/2; x3 = s/2; x4 = -s/2;
        y_bot = 0; y_top = h
        
        ax.plot([x1, x2, x3, x4, x1], [y_bot, y_bot, y_top, y_top, y_bot], color='black', linewidth=2)
        ax.set_xlim(-10, 10); ax.set_ylim(-1, 7)
        ax.axis('off')
        
        plt.savefig(path, dpi=100)
        plt.close()
