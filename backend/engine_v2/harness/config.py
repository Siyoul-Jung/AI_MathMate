"""Harness 설정값 — 기법 이름 검사 목록 및 결과 저장 경로."""
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "data" / "harness_results"

# Writer 지문에서 검출할 수학 기법 이름 목록
# 이 단어가 narrative에 포함되면 기법 은폐 실패로 판정
TECHNIQUE_WORDS = [
    "snake oil", "vieta", "inclusion-exclusion", "shoelace",
    "derangement", "catalan", "chinese remainder", "law of cosines",
    "law of sines", "heron", "euler", "burnside", "fermat",
    "ptolemy", "brahmagupta", "stewart", "ceva", "menelaus",
    "power of a point", "radical axis", "angle bisector theorem",
    "pigeonhole", "generating function", "markov",
]
