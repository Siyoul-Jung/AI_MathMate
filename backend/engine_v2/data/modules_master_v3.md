# AI MathMate V2 — Atomic Module Registry v3

> **최종 갱신:** 2026-04-04
> **검증 방법:** AIME 기출 1065개 역방향 매핑 (Gemini 2.5 Pro) + GPT-4o 교차 검증 + 5문제 수동 검수
> **검증 데이터:** `data/problem_module_map.json` (1065 problems), `data/cross_validation_result.json`

---

## 요약

| 항목 | 값 |
|------|-----|
| 활성 모듈 | **85개** (기법 77 + meta 전략 8) |
| 기출 커버리지 | **1065/1065** (100%), 1983~2026 AIME 전 연도 |
| 기출 연도 범위 | 1983~1999 (단일 AIME, 15문제/년) + 2000~2026 (AIME I+II, 30문제/년) |
| 교차 검증 일치율 | **~95%** (Gemini vs GPT-4o, 도메인 수준) |
| 환각 모듈 제거 | 6개 제거 완료 |

### 기출 커버리지 연도별 상세

| 연도 구간 | 문제 수 | 커버리지 | 비고 |
|----------|---------|---------|------|
| 1983~1989 | 105 | 100% | 단일 AIME (15문제 × 7년) |
| 1990~1999 | 150 | 100% | 단일 AIME (15문제 × 10년) |
| 2000~2009 | 300 | 100% | AIME I+II (30문제 × 10년) |
| 2010~2019 | 300 | 100% | AIME I+II (30문제 × 10년) |
| 2020~2026 | 210 | 100% | AIME I+II (30문제 × 7년) |
| **합계** | **1065** | **100%** | |

---

## ALGEBRA (21개)

| # | module_id | 기출 등장 | 비율 | 연도 범위 | 2015+ |
|---|-----------|----------|------|----------|-------|
| 1 | `algebra_sequences_series_recurrence` | 143 | 13.4% | 1984-2026 | 38 |
| 2 | `algebra_basic_manipulation` | 111 | 10.4% | 1983-2026 | 26 |
| 3 | `algebra_systems_of_equations` | 86 | 8.1% | 1983-2025 | 21 |
| 4 | `algebra_inequalities` | 75 | 7.0% | 1983-2026 | 19 |
| 5 | `algebra_trigonometry` | 72 | 6.8% | 1983-2026 | 17 |
| 6 | `algebra_logarithms_exponents` | 61 | 5.7% | 1983-2026 | 19 |
| 7 | `algebra_complex_numbers` | 58 | 5.4% | 1983-2025 | 16 |
| 8 | `algebra_functions_and_properties` | 55 | 5.2% | 1984-2026 | 27 |
| 9 | `algebra_poly_vieta_newton` | 50 | 4.7% | 1983-2026 | 16 |
| 10 | `algebra_kinematics` | 48 | 4.5% | 1985-2026 | 13 |
| 11 | `algebra_binomial_theorem` | 33 | 3.1% | 1983-2026 | 9 |
| 12 | `algebra_poly_complex_roots` | 32 | 3.0% | 1986-2026 | 12 |
| 13 | `algebra_floor_ceiling_functions` | 24 | 2.3% | 1985-2023 | 4 |
| 14 | `algebra_roots_unity_filter` | 24 | 2.3% | 1984-2024 | 8 |
| 15 | `algebra_statistics` | 19 | 1.8% | 1984-2024 | 6 |
| 16 | `algebra_absolute_value` | 16 | 1.5% | 1983-2025 | 7 |
| 17 | `algebra_func_symmetry` | 12 | 1.1% | 1984-2024 | 4 |
| 18 | `algebra_func_equations_cauchy` | 11 | 1.0% | 1984-2020 | 3 |
| 19 | `algebra_telescoping_sum` | 10 | 0.9% | 1984-2026 | 2 |
| 20 | `algebra_matrices_determinants` | 7 | 0.7% | 1986-2018 | 1 |
| 21 | `algebra_seq_characteristic_eq` | 5 | 0.5% | 1985-2018 | 1 |

---

## COMBINATORICS (17개)

| # | module_id | 기출 등장 | 비율 | 연도 범위 | 2015+ |
|---|-----------|----------|------|----------|-------|
| 1 | `comb_count_double` | 118 | 11.1% | 1983-2026 | 45 |
| 2 | `comb_probability` | 113 | 10.6% | 1983-2026 | 50 |
| 3 | `comb_recursion_dp` | 80 | 7.5% | 1983-2026 | 30 |
| 4 | `comb_multinomial_partition` | 70 | 6.6% | 1983-2026 | 22 |
| 5 | `comb_set_theory_and_subsets` | 44 | 4.1% | 1983-2026 | 12 |
| 6 | `comb_inclusion_exclusion` | 22 | 2.1% | 1984-2024 | 9 |
| 7 | `comb_path_counting` | 20 | 1.9% | 1990-2026 | 10 |
| 8 | `comb_graph_theory` | 14 | 1.3% | 1985-2025 | 7 |
| 9 | `comb_gen_func_snake_oil` | 10 | 0.9% | 1998-2026 | 3 |
| 10 | `comb_prob_absorbing_markov` | 10 | 0.9% | 1985-2021 | 6 |
| 11 | `comb_grid_sudoku_sum` | 7 | 0.7% | 2010-2026 | 6 |
| 12 | `comb_symmetry_and_burnside` | 7 | 0.7% | 1996-2024 | 2 |
| 13 | `comb_derangement` | 6 | 0.6% | 2001-2014 | 0 |
| 14 | `comb_pairing_probability` | 6 | 0.6% | 2010-2026 | 5 |
| 15 | `comb_graph_coloring_chromatic` | 4 | 0.4% | 1985-2025 | 2 |
| 16 | `comb_catalan` | 2 | 0.2% | 1988-2006 | 0 |
| 17 | `comb_prob_transition_matrix` | 2 | 0.2% | 1985-2021 | 1 |

---

## GEOMETRY (24개)

| # | module_id | 기출 등장 | 비율 | 연도 범위 | 2015+ |
|---|-----------|----------|------|----------|-------|
| 1 | `geometry_coordinate_analytic` | 191 | 17.9% | 1983-2026 | 55 |
| 2 | `geometry_area_and_volume` | 147 | 13.8% | 1983-2026 | 48 |
| 3 | `geometry_triangle_properties` | 116 | 10.9% | 1983-2026 | 39 |
| 4 | `geometry_circle_theorems` | 82 | 7.7% | 1983-2026 | 31 |
| 5 | `geometry_solid_3d` | 77 | 7.2% | 1983-2026 | 24 |
| 6 | `geometry_trigonometry_laws` | 67 | 6.3% | 1985-2026 | 13 |
| 7 | `geometry_sim_homothety` | 64 | 6.0% | 1984-2024 | 16 |
| 8 | `geometry_polygons` | 51 | 4.8% | 1985-2026 | 21 |
| 9 | `geometry_circles_tangency` | 39 | 3.7% | 1991-2026 | 18 |
| 10 | `geometry_transformations` | 36 | 3.4% | 1983-2026 | 8 |
| 11 | `geometry_power_of_a_point` | 33 | 3.1% | 1983-2026 | 17 |
| 12 | `geometry_angle_bisector_theorem` | 27 | 2.5% | 1987-2026 | 9 |
| 13 | `geometry_triangle_centers` | 25 | 2.3% | 1986-2026 | 14 |
| 14 | `geometry_vectors` | 23 | 2.2% | 1983-2025 | 5 |
| 15 | `geometry_complex_numbers_in_geometry` | 19 | 1.8% | 1997-2026 | 5 |
| 16 | `geometry_cyclic_quadrilaterals` | 17 | 1.6% | 1991-2024 | 10 |
| 17 | `geometry_locus` | 6 | 0.6% | 1983-2024 | 1 |
| 18 | `geometry_circle_radical` | 4 | 0.4% | 2012-2019 | 3 |
| 19 | `geometry_coordinate_intersections` | 4 | 0.4% | 1991-2023 | 3 |
| 20 | `geometry_transform_inversion` | 3 | 0.3% | 2008-2017 | 1 |
| 21 | `geometry_circle_ptolemy` | 2 | 0.2% | 1991-2013 | 0 |
| 22 | `geo_parabola_rotation` | 1 | 0.1% | 2025-2025 | 1 |
| 23 | `geometry_sim_spiral` | 1 | 0.1% | 2019-2019 | 1 |
| 24 | `geo_reflection_heptagon` | 0 | 0.0% | — | 0 |

> ⚠️ `geo_reflection_heptagon`: 기출 0회이나 특수 정다각형 문제 대비용으로 잠정 보류.

---

## NUMBER_THEORY (15개)

| # | module_id | 기출 등장 | 비율 | 연도 범위 | 2015+ |
|---|-----------|----------|------|----------|-------|
| 1 | `nt_diophantine_equations` | 110 | 10.3% | 1983-2026 | 33 |
| 2 | `nt_modular_arithmetic` | 103 | 9.7% | 1983-2026 | 38 |
| 3 | `nt_base_representation_and_digits` | 82 | 7.7% | 1983-2026 | 24 |
| 4 | `nt_divisibility_and_primes` | 75 | 7.0% | 1983-2025 | 27 |
| 5 | `nt_divisor_functions` | 36 | 3.4% | 1983-2026 | 11 |
| 6 | `nt_perfect_powers` | 32 | 3.0% | 1985-2023 | 8 |
| 7 | `nt_gcd_lcm` | 24 | 2.3% | 1985-2026 | 8 |
| 8 | `nt_chinese_remainder_theorem` | 12 | 1.1% | 2002-2026 | 6 |
| 9 | `nt_floor_legendre` | 8 | 0.8% | 1983-2022 | 1 |
| 10 | `nt_mod_order_primitive` | 7 | 0.7% | 2001-2024 | 5 |
| 11 | `nt_quadratic_residue` | 6 | 0.6% | 1994-2024 | 3 |
| 12 | `nt_frobenius_coin_problem` | 5 | 0.5% | 1994-2025 | 3 |
| 13 | `nt_mod_lte_lemma` | 4 | 0.4% | 2018-2024 | 4 |
| 14 | `nt_diophantine_pell` | 3 | 0.3% | 1997-2008 | 0 |
| 15 | `nt_base_divisibility` | 2 | 0.2% | 1984-2003 | 0 |

---

## META (8개) — 출제 전략 모듈

기출 태깅 대상이 아닌 **문제 생성 시 적용되는 전략 모듈**입니다.

| # | module_id | 역할 |
|---|-----------|------|
| 1 | `meta_extremal_construction` | 극단적 구성을 통한 최적화 문제 설계 |
| 2 | `meta_logic_concealer` | 풀이 중간 단계를 은폐하여 논리 도약 강제 |
| 3 | `meta_anonymization` | 변수명 익명화로 패턴 인식 차단 |
| 4 | `meta_symmetry_breaker` | 시드 값에 비대칭성 주입 |
| 5 | `meta_trace_removal` | 풀이 흔적 제거 |
| 6 | `meta_invariant_design` | 불변량 기반 문제 설계 |
| 7 | `meta_rationale_layering` | 다층 추론 구조 강제 |
| 8 | `meta_rosetta_mapping` | 도메인 간 번역 (대수→기하 표현 변환) |

---

## 제거된 모듈 (환각/과잉 세분화)

아래 모듈은 기출 1065개 역추적에서 단 한 번도 필요하지 않았던 것으로 확인되어 제거되었습니다.

| module_id | 제거 사유 | 제거일 |
|-----------|----------|--------|
| `geo_complex_bisector_tangency` | 기출 0회 — 환각 추출 | 2026-04-04 |
| `geo_trapezoid_inscribed` | 기출 0회 — 다른 기하 모듈로 커버 | 2026-04-04 |
| `geometry_center_euler_ninepoint` | 기출 0회 — AIME 범위 밖 | 2026-04-04 |
| `geometry_circle_isogonal_symmedian` | 기출 0회 — USAMO급 | 2026-04-04 |
| `nt_diophantine_vieta_jumping` | 기출 0회 — IMO급 | 2026-04-04 |
| `nt_discrete_log` | 기출 0회 — 대학 정수론 | 2026-04-04 |

---

## 수정 이력

| 날짜 | 변경 | 비고 |
|------|------|------|
| 2026-04-04 | v3 초기 생성 | 기출 1065개 역추적 + GPT-4o 교차 검증 기반 |
| 2026-04-04 | 환각 모듈 6개 제거 | 91 → 85개 |
| 2026-04-04 | `comb_inclusion_exclusion` 신규 | 기출 UNMAPPED 3회 발견으로 추가 |
| 2026-04-04 | `comb_graph_theory` 신규 | 기출 UNMAPPED 2회 발견으로 추가 |
| 2026-04-04 | 3문제 Gemini 오류 수동 수정 | 2002 I P14, 2008 II P10, 2012 II P14 |

---

## 모듈 추가/삭제 기준

### 추가 기준
1. 기출 역방향 매핑에서 **UNMAPPED가 3회 이상** 등장하는 기법
2. 기존 모듈의 `tags`와 **Jaccard 유사도 < 0.3**인 새로운 기법
3. Bridge 체이닝에서 **공백을 메우는** 연결 모듈

### 삭제 기준
1. 기출 역방향 매핑에서 **등장 0회** + 다른 모듈로 완전 대체 가능
2. 교차 검증에서 **두 모델 모두 해당 모듈을 선택하지 않음**
3. `modules_master_v3.md`에 제거 사유 기록 필수

### 병합 기준
1. 두 모듈의 기출 공출현율(co-occurrence) > 80%
2. Bridge 관계가 아닌 단순 중복

---

## 교차 검증 현황 및 향후 방향

### 완료된 검증 (2026-04-04)

| 단계 | 방법 | 결과 |
|------|------|------|
| 1차 태깅 | Gemini 2.5 Pro + PDF | 1065개 전량 매핑 |
| 2차 교차 | GPT-4o + 문제 텍스트 (자유 서술, 모듈 목록 미제공) | 1065개 전량 |
| 키워드 매핑 | GPT-4o 자유 서술 → MODULE_KEYWORDS 테이블로 91개 모듈 자동 매핑 | 보완 완료 |
| 수동 검수 | 도메인 불일치 5문제 원문 대조 | Gemini 2승, GPT-4o 3승 → 3건 수정 |
| 태그 병합 | Gemini + GPT-4o 유효 태그 union | 666개 문제 보강 |

### 현재 일치율

```
전체:     78.7% (키워드 매핑 기준)
도메인 수준: ~95% (같은 도메인 내 세분화 차이 허용 시)

난이도별:
  P1~P5 (쉬움):   84.2%
  P6~P10 (중간):  78.3%
  P11~P15 (어려움): 73.5%  ← 고난도에서 해석 갈림이 자연스러움
```

### 불일치 원인 분석 (227건)

| 원인 | 비율 | 해소 방법 | 현재 상태 |
|------|------|----------|----------|
| 키워드 매핑 테이블 누락 | 78% | MODULE_KEYWORDS 수동 보완 | ⚠️ 임시 해소 |
| 같은 도메인 내 세분화 차이 | 20% | 태그 병합 (union) | ✅ 완료 |
| 진짜 도메인 불일치 | 2% | 원문 대조 수동 검수 | ✅ 5건 완료 |

### "같은 기법, 다른 이름" 문제 — 근본 해결 방향

현재 MODULE_KEYWORDS 테이블은 **문자열 일치 기반**이라 한계가 있습니다:
```
등록된 키워드:   "vieta", "newton sum", "symmetric polynomial"
매칭 성공:       "Vieta's formulas" → ✅ (부분 문자열 "vieta" 일치)
매칭 실패:       "relations between roots and coefficients" → ❌ (같은 기법인데 표현이 다름)
→ 새 표현이 나올 때마다 수동 추가 필요 = 확장 불가능
```

**근본 해결: 임베딩 기반 의미론적 매핑**
```
[현재] 키워드 매칭:    "roots and coefficients" ∉ keywords → UNMATCHED
[개선] 임베딩 매칭:    embed("roots and coefficients") ≈ embed("vieta formulas") → cosine=0.92 → ✅ 매핑
```

구현 방향:
1. 각 모듈의 `name + description + tags`를 임베딩 벡터로 변환 (OpenAI `text-embedding-3-small`)
2. GPT-4o 자유 서술 기법을 같은 모델로 임베딩
3. cosine similarity > 0.75이면 해당 모듈에 매핑
4. MODULE_KEYWORDS 수동 관리 불필요 → 모듈 META만 잘 작성하면 자동 매칭

**예상 효과:** 키워드 매핑 78.7% → 임베딩 매핑 시 90%+ (수동 보완 없이)
**비용:** 1065개 × 3 기법 × $0.00002/embedding = ~$0.06 (무시 수준)
**시점:** 다음 교차 검증 라운드 실행 시 `6_cross_validate_claude.py`의 `match_techniques_to_modules()` 교체

### 향후 추가 교차 검증 방향

#### 방향 1: 제3 모델 추가 (다수결 투표)
- **시점:** 일치율이 85% 미만으로 유지될 때
- **모델:** Claude Opus (Anthropic API 별도 가입 필요, ~$15)
- **방법:** 같은 1065개를 Claude에게 자유 서술 태깅 → 3모델 다수결
- **현재 판단:** 불필요 — 도메인 수준 95% 합의이므로 3번째 모델의 추가 가치 낮음

#### 방향 2: 실행 기반 증명 (가장 강력)
- **시점:** 모듈 코드(execute/verify_with_sympy)가 안정화된 후
- **방법:** 기출 문제의 실제 정답(0~999)이 공개되어 있으므로:
  1. 각 기출 문제에 대해 매핑된 모듈 조합으로 seed를 생성
  2. `module.execute(seed) == 공식 정답`인지 확인
  3. 성공 → 해당 매핑이 수학적으로 증명됨
- **현실적 제약:** 기출 문제의 구체적 수치를 seed로 변환하는 작업이 필요 (대규모)
- **추천:** 대표 기출 50개(난이도별 10개씩 × 5구간)로 파일럿 실행

#### 방향 3: 시간 감쇠 가중치 검증
- **시점:** Bridge 확장 및 DAPS 보정 완료 후
- **방법:** 2015년 이후 기출의 모듈 사용 빈도 vs 전체 빈도 비교
  - 최근 빈도가 높은 모듈: 트렌드 상승 → Architect 가중치 상향
  - 최근 빈도가 0인 모듈: 트렌드 하락 → 감점 또는 비활성화 후보
- **데이터:** 이미 `2015+` 열에 수치 있음

#### 방향 4: AoPS Ground Truth 접근
- **시점:** AoPS 크롤링 허용되거나, 인간 전문가 태깅 데이터 확보 시
- **방법:** AoPS 위키의 인간 전문가 카테고리 태그와 1:1 대조
- **현재 제약:** AoPS 403 차단, 공개 데이터셋에 태그 미포함
- **우회:** AIME 코치/수학 교사에게 50문제 샘플 태깅 의뢰 (가장 신뢰도 높음)
