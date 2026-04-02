# amc_engine/config/themes.py

"""
AIME-Professional Theme Registry.
Categorized narrative hooks to ensure high-finesse problem generation.
"""

AIME_THEME_REGISTRY = {
    "LOGISTICS": [
        "Network packet routing across three primary nodes",
        "Bandwidth allocation for satellite communication channels",
        "Inventory distribution across multi-tier storage facilities",
        "Optimizing transport routes for emergency medical supplies",
        "Worker shift assignments in a 24-hour pharmaceutical lab",
        "Assigning varying security clearance levels to research staff",
        "Energy load balancing across high-voltage power grids",
        "Sorting algorithmic tasks into priority processing queues"
    ],
    "SCIENTIFIC": [
        "Observing quantum state transitions in a controlled vacuum",
        "Analyzing radioactive decay sequences in rare isotopes",
        "Mapping genetic sequence mutations in a large population study",
        "Calculating equilibrium constants in a complex chemical reaction",
        "Measuring gravitational lensing effects in a distant star cluster",
        "Tracking microbial population growth in varying nutrient cultures",
        "Calibrating precision optics for deep-space observation",
        "Modeling fluid dynamics in high-pressure volcanic vents"
    ],
    "ABSTRACT": [
        "Finding ordered triples of integers satisfying modular properties",
        "Analyzing the distribution of coefficients in a high-degree polynomial",
        "Constructing sets of elements under strict algebraic constraints",
        "Defining a transformation mapping on a lattice of points",
        "Investigating divisibility patterns in a sequence of primes",
        "Determining the sum of residues for a functional equation",
        "Evaluating the convergence of a discrete numerical series",
        "Partitioning a set into non-empty subsets with specific sums"
    ],
    "RECONSTRUCTED_CLASSIC": [
        "Arranging tiles on a hexagonal grid under adjacency rules",
        "Moving a game piece on a coordinate plane with restricted steps",
        "Filling a 3D matrix with integers such that layer sums are constant",
        "Counting sequences of coin flips with no consecutive heads",
        "Assigning colors to a graph representing a spatial map",
        "Distributing distinct balls into numbered urns with constraints",
        "Walking along the edges of a dodecahedron from vertex to vertex",
        "Seating people around a circular table with specific intervals"
    ]
}

# Mapping: Which Categories are appropriate for which DNA Categories
DNA_THEME_MAPPING = {
    "Combinatorics": ["LOGISTICS", "RECONSTRUCTED_CLASSIC", "ABSTRACT"],
    "Algebra": ["ABSTRACT", "SCIENTIFIC", "LOGISTICS"],
    "Number Theory": ["ABSTRACT", "SCIENTIFIC", "LOGISTICS"],
    "Geometry": ["RECONSTRUCTED_CLASSIC", "ABSTRACT", "SCIENTIFIC"],
}
