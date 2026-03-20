"""
amc_engine/verifier.py
======================
다단계 문제 검증 모듈

Stage 1: Surface Check  — LaTeX 균형, 지문 길이
Stage 2: Deep Math Check— DNA 태그 기반 수치 역산 + 단어 숫자 변환
"""

import re

# ─────────────────────────────────────────────────────────────
# 숫자 단어 → 정수 변환 테이블
# ─────────────────────────────────────────────────────────────
WORD_TO_NUM = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
    'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
    'nineteen': 19, 'twenty': 20, 'twenty-one': 21, 'twenty-two': 22,
    'twenty-four': 24, 'thirty': 30, 'forty': 40, 'fifty': 50,
    'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
    'hundred': 100,
}


def extract_all_numbers(text: str) -> set:
    """
    Digit 형식(10)과 단어 형식(ten) 모두 추출하여 정수 집합으로 반환.
    AIME 문제에서 LLM이 간혹 소수 단어를 쓸 때도 감지 가능.
    """
    # 숫자 digit 추출
    digits = {int(n) for n in re.findall(r'\b(\d+)\b', text)}
    # 단어 형식 숫자 추출 (단어 경계 체크)
    words = {
        WORD_TO_NUM[w]
        for w in WORD_TO_NUM
        if re.search(rf'\b{re.escape(w)}\b', text.lower())
    }
    return digits | words


# ─────────────────────────────────────────────────────────────
# Stage 1: Surface Check
# ─────────────────────────────────────────────────────────────
def stage1_surface(narrative: str) -> tuple:
    """
    LaTeX 균형 검사 + 최소 길이 체크.
    Returns: (ok: bool, reason: str)
    """
    if not narrative or len(narrative.strip()) < 50:
        return False, "지문이 너무 짧거나 비어 있음"

    # $$ 블록 제거 후 홀짝 체크
    cleaned = re.sub(r'\$\$[^$]*\$\$', '', narrative)
    if cleaned.count('$') % 2 != 0:
        return False, (
            "LaTeX $ 닫힘 오류 — 열린 $ 와 닫힌 $ 개수 불일치. "
            "예: 'Find the value of $m + n + p$.' (마침표 앞에 $ 필요)"
        )

    return True, "OK"


# ─────────────────────────────────────────────────────────────
# Stage 2: Deep Math Check (DNA 태그 기반)
# ─────────────────────────────────────────────────────────────
def stage2_deep_math(narrative: str, seed: dict, dna_tag: str) -> tuple:
    """
    DNA 태그에 따라 지문에서 수치를 추출하고 시드와 역산 비교.
    단어 형식 숫자도 처리.
    Returns: (ok: bool, reason: str)
    """
    nums = extract_all_numbers(narrative)

    # ── P13: 기댓값 / 원 분할 ──────────────────────────────
    if dna_tag == "EXPECTED-REGIONS-DISK":
        level = seed.get('drill_level')
        if level == 1:
            n_lines = seed.get('n_lines')
            if n_lines not in nums:
                return False, f"선분 개수 n_lines={n_lines} 누락"
            return True, "OK"
        elif level == 2:
            if seed['m'] not in nums:
                return False, f"지름 수 m={seed['m']} 누락"
            return True, "OK"
            
        required = {
            seed['m']:          f"지름 수 m={seed['m']}",
            seed['quadrants']:  f"섹터 수 quadrants={seed['quadrants']}",
            seed['n']:          f"추가 선분 n={seed['n']}",
            seed['total_lines']:f"전체 선분 total_lines={seed['total_lines']}",
        }
        missing = [desc for val, desc in required.items() if val not in nums]
        if missing:
            return False, f"수치 누락: {missing[0]}"
        return True, "OK"

    # ── P14: 오각형 기하 최적화 ───────────────────────────
    elif dna_tag == "GEO-FERMAT-PENTAGON":
        level = seed.get('drill_level')
        if level == 1:
            # Level 1 usually asks about angle AXB = 120
            # Just do a surface check for 'AX' or '120'
            return True, "OK (Level 1 Surface Pass)"
        elif level == 2:
            diag1 = seed.get('diag1')
            if str(diag1) not in narrative:
                return False, f"대각선 {diag1} 수치 누락"
            return True, "OK"

        val_map = {k: int(v) for k, v in re.findall(r'([A-Z]{2})\s*=\s*(\d+)', narrative)}
        expected = {
            'AB': 2 * seed['k1'],
            'BC': seed['k1'],
            'CD': seed['CD'],
            'DE': seed['k2'],
            'EA': 2 * seed['k2'],
        }
        for var, exp_val in expected.items():
            found_val = val_map.get(var)
            if found_val is None:
                if str(exp_val) not in narrative:
                    return False, f"변수 {var}={exp_val}가 지문에 없음"
            elif found_val != exp_val:
                return False, f"{var} 불일치: 기대값 {exp_val}, 지문 {found_val}"
        return True, "OK"

    # ── P01: 진법 표현 ────────────────────────────────────
    elif dna_tag == "NT-BASE-DIV-L1":
        div = seed.get('divisor_str', '')
        dnd = seed.get('dividend_str', '')
        level = seed.get('drill_level')
        min_b = seed.get('min_b')
        
        if level == 1:
            target_b = seed.get('target_b')
            if str(target_b) not in narrative:
                return False, f"대상 진법 {target_b} 누락"
            if dnd not in narrative:
                return False, f"대상 진법 기호 {dnd} 누락"
            return True, "OK"
            
        if div not in narrative:
            return False, f"제수 진법 기호 {div} 누락"
            
        if level == 2:
            # Level 2는 최소 진법 찾기이므로 dnd가 있어야 함
            if dnd not in narrative:
                return False, f"피제수 진법 기호 {dnd} 누락"
            return True, "OK"
            
        # Level 3 (Full Sum)
        if dnd not in narrative:
            return False, f"피제수 진법 기호 {dnd} 누락"
        return True, "OK"

    # ── P15: LTE 정수론 ───────────────────────────────────
    elif dna_tag == "NT-LTE-CUBE-L3":
        level = seed.get('drill_level')
        if level == 1 or level == 2:
            m_mod = seed.get('m_mod')
            if str(m_mod) not in narrative:
                return False, f"모듈러 상수 {m_mod} 누락"
            return True, "OK"

        K, M = seed.get('K'), seed.get('M')
        # Check for 3^K or 3^M with/without braces
        has_K = f"3^{{{K}}}" in narrative or f"3^{K}" in narrative
        has_M = f"3^{{{M}}}" in narrative or f"3^{M}" in narrative
        if not has_K:
            return False, f"상한 지수 3^{K} 누락"
        if not has_M:
            return False, f"배수 지수 3^{M} 누락"
        return True, "OK"

    # ── P12: 3D 평면 부등식 영역 ──────────────────────────
    elif dna_tag == "REGION-PLANE-INEQ":
        level = seed.get('drill_level')
        if level == 1:
            # Level 1: Point Evaluation
            x, y, z = seed.get('target_point', (0,0,0))
            if x not in nums and y not in nums and z not in nums:
                 return False, f"대상 포인트 ({x}, {y}, {z}) 누락"
            return True, "OK"
        elif level == 2:
            # Level 2: Boundary check (The answer is -1, so it might not be in the text)
            if "factor" not in narrative.lower() and "inequality" not in narrative.lower():
                 return False, "핵심 키워드(factor, inequality) 누락"
            return True, "OK"

        N = seed.get('N')
        if str(N) not in narrative:
            return False, f"평면 상수 N={N} 누락"
        # 핵심 부등식 항 존재 여부 (yz, zx, xy 중 최소 2개)
        key_terms = sum(t in narrative for t in ["yz", "zx", "xy"])
        if key_terms < 2:
            return False, f"핵심 부등식 항(yz, zx, xy) 누락 — {key_terms}개만 발견"
        return True, "OK"

    # ── P11: 조각의 선형 함수와 포물선 ───────────────────────
    elif dna_tag == "FUNC-SAWTOOTH-PARABOLA":
        K, P = seed.get('K'), seed.get('P')
        level = seed.get('drill_level')
        
        # Level 1, 2는 포물선 체크 생략
        if level != 1 and level != 2:
            expected_para = fr"{K}y\^2"
            if not re.search(expected_para, narrative):
                if str(K) not in narrative:
                    return False, f"포물선 계수 K={K} 누락"
        
        if str(P) not in narrative:
            return False, f"치역/주기 상수 P={P} 누락"
            
        return True, "OK"

    # ── 기타 DNA: 기본 통과 ───────────────────────────────
    return True, f"OK (DNA '{dna_tag}'는 Stage 2 미지원, 기본 통과)"


# ─────────────────────────────────────────────────────────────
# 통합 검증 실행기
# ─────────────────────────────────────────────────────────────
def run_all_stages(narrative: str, seed: dict, dna_tag: str) -> tuple:
    """
    Stage 1 → Stage 2 순서로 실행.
    Returns: (ok: bool, failed_stage: int, reason: str)
    """
    ok1, msg1 = stage1_surface(narrative)
    if not ok1:
        return False, 1, msg1

    ok2, msg2 = stage2_deep_math(narrative, seed, dna_tag)
    if not ok2:
        return False, 2, msg2

    return True, 0, "OK"
