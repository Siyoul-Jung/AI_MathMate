# fix: Judge 에이전트 수정 프로토콜 & 알려진 버그 패턴

이 문서는 BEq 루프에서 발생하는 오류를 체계적으로 처리하는 **Judge 에이전트의 수정 프로토콜**과
개발 과정에서 발견된 알려진 버그 패턴을 정의합니다.

---

## 1. BEq 판정 결과별 처리 프로토콜

### PASS ✅
- 문항을 `variants` 테이블에 `status="VERIFIED"`로 저장합니다.
- `daps_scores` 테이블에 최종 점수를 기록합니다.
- 참신성 검증(Novelty Check)을 통과한 문항만 최종 배포합니다.

### FIX_REQUIRED ⚠️
Judge가 `fix_instruction`을 생성하여 Writer에게 전달합니다.
**수정 루프의 핵심 원칙:**
```python
# Fix History 누적 (국소 수렴 방지)
# Writer는 이전 실패 이유를 모두 알고 수정해야 합니다
fix_history.append(judge_res.fix_instruction)
writer.run(..., fix_history=fix_history)
```

**FIX_REQUIRED 원인별 수정 지침:**
| 원인 | Fix Instruction 핵심 내용 |
|---|---|
| 낮은 신뢰도 (LOW confidence) | "수학적 조건을 더 명확하게 기술하고, 불필요한 수식 생략을 없애세요." |
| 모호성 감지 (ambiguity) | "다음 모호한 표현을 해결하세요: [구체적 구절]" |
| 조건 부족 (conditions < 2) | "핵심 제약 조건(범위, 관계식)을 지문에 더 명시적으로 포함하세요." |

### FAIL ❌ (수학 오류)
수학 오류는 Writer 수정으로 해결할 수 없습니다. **즉시 루프를 종료**합니다.
```
원인: Evaluator가 도출한 답 ≠ Python Solver의 정답 (Ground Truth)
조치: Seed를 폐기하거나, Architect에게 반환하여 DAPS를 -1.5 하향 재설계
```

---

## 2. Circuit Breaker 발동 기준 (MAX_LOOP 초과)

3회 BEq 검증 실패 시 다음 Fallback 중 하나를 실행합니다:

**옵션 A: Seed 폐기 후 재시도**
```python
new_seed = module.generate_seed(difficulty_hint=target_daps - 1.5)
```

**옵션 B: Architect 재설계 요청**
```python
architect.run(target_daps=target_daps - 1.5, reason="CIRCUIT_BREAKER")
```

로그에는 반드시 `status="CIRCUIT_BREAKER"` 와 실패 이력 3회분을 기록합니다.

---

## 3. 알려진 버그 패턴 (Known Issues)

### 3.1 LaTeX 환각 패턴
LLM이 잘못된 LaTeX를 생성하는 경우:
- **`\text{circ}` 오류**: `^\\circ`로 대체 (정규식: `re.sub(r'\\text\{circ\}', r'^\\circ', text)`)
- **마크다운 코드블록 래핑**: LLM이 응답을 ` ```json ` 으로 감쌀 때, `{...}` 구간을 정규식으로 추출
- **인라인/블록 혼용**: `$...$` (인라인)과 `$$...$$` (블록)을 혼용하지 않도록 후처리 검증

### 3.2 혁신의 저주 감지 패턴
Writer가 지시를 어기고 수학적 조건을 변형하는 경우:
- **증상**: BEq 루프에서 `fix_instruction`이 매번 같은 오류를 반복 보고
- **진단**: Evaluator의 `steps`에서 Writer가 추가한 비공인 조건 확인
- **처치**: Writer 프롬프트에 "주어진 `logic_steps` 외의 수학적 조건을 추가하지 마시오"를 명시적으로 강화

### 3.3 데이터베이스 경로 오류
스탠드얼론 스크립트 실행 시 DB 경로 문제:
```python
# 항상 절대 경로 사용
DB_PATH = r'c:\AI_MathMate\backend\engine_v2\amc_factory_v2.db'
```

### 3.4 이미지 경로 오류
FastAPI의 정적 파일 디렉토리 기준 경로인지 확인 후 `image_url`을 설정합니다.
