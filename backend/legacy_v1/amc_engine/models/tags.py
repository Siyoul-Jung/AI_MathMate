from enum import Enum

class MathCategory(str, Enum):
    ALGEBRA = "Algebra"
    COMBINATORICS = "Combinatorics"
    GEOMETRY = "Geometry"
    NUMBER_THEORY = "Number Theory"
    LOGIC = "Logic"
    PROBABILITY = "Probability"

class ContextType(str, Enum):
    NARRATIVE = "narrative"
    ABSTRACT = "abstract"

class AIMELevel(int, Enum):
    CHALLENGER = 5    # P01-P05
    EXPERT = 10      # P06-P10
    MASTER = 15      # P11-P15
