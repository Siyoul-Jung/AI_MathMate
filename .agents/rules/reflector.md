# reflector: Evaluator 에이전트 역추론 표준

이 문서는 **Evaluator 에이전트**의 역할, 행동 원칙, 그리고 코드 품질 기준을 정의합니다.
Evaluator는 BEq(양방향 등가성) 검증의 핵심 실행자입니다.

---

## 1. Evaluator 에이전트의 핵심 역할

Evaluator는 **완전히 새로운 학생**처럼 행동해야 합니다.

```
입력: narrative (LaTeX 지문 텍스트만)
원칙: seed, correct_answer, logic_steps를 절대 참조하지 않음
출력: extracted_answer, confidence, conditions, steps, ambiguity
```

**이것이 BEq 검증의 핵심입니다:**
"지문 하나만 보고도 정답에 도달할 수 있는가?"라는 질문에 답합니다.
이 질문에 YES가 나와야 진짜 잘 쓰인 AIME 문항입니다.

---

## 2. 역추론 품질 기준

### 2.1 올바른 역추론의 3요소

| 요소 | 기준 |
|---|---|
| 조건 추출 | 지문에서 수학적 조건 최소 2개 이상 명시적 추출 |
| 풀이 단계 | 논리적으로 연결된 3단계 이상의 추론 경로 |
| 신뢰도 | `HIGH`: 지문이 충분히 명확함 / `LOW`: 모호함 감지 |

### 2.2 Evaluator 결과 스키마

```python
{
    "extracted_answer": int,        # 역추론으로 도출한 최종 수치 (0-999)
    "confidence": "HIGH" | "LOW",   # 지문 명확성 판단
    "conditions": list[str],        # 추출한 수학적 조건들
    "steps": list[str],             # 풀이 단계 (Judge의 솔루션으로 등록됨)
    "ambiguity": str,               # 모호한 표현 (없으면 빈 문자열)
}
```

---

## 3. 코드 품질 기준 (Python & LaTeX)

### Python 표준
- 모든 함수 시그니처에 **타입 힌트(Type Hints)** 필수
- API 관련 로직은 `async def` 비동기 함수 사용
- 스탠드얼론 스크립트는 CWD 문제 방지를 위해 **절대 경로** 사용

### LaTeX 표준 (CRITICAL — 렌더링 일관성 핵심)

| 표현 | 올바른 방식 | 금지 방식 |
|---|---|---|
| 각도(도) | `^\\circ` | `\\text{circ}`, `extcirc` |
| 곱셈 | `\\times` | `*`, 암묵적 공백 |
| 삼각형 | `\\triangle` | `△` (유니코드) |
| 집합 원소 합 | `\\sum_{i=1}^{n}` | `sum(i=1 to n)` |
| 인라인 수식 | `$...$` | 텍스트 내 백슬래시 나체 |
| 블록 수식 | `$$...$$` | `: math: `, 기타 마크업 |

---

## 4. 프론트엔드 표준 (React/TypeScript)

- **컴포넌트**: 명시적 `FC` 타입의 Functional Components 사용
- **상태 관리**: `useState`, `useEffect` 훅 + Context API (필요시)
- **스타일**: Tailwind CSS — Slate/Zinc 기반 다크 테마 일관성 유지
- **아이콘**: `lucide-react` 통일 사용
- **수식**: 모든 수학 표현은 `KaTeX`로 렌더링, Raw LaTeX 노출 금지

---

## 5. DSPy 도입 준비 (파일럿 계획)

Evaluator 에이전트는 향후 DSPy 파일럿의 첫 번째 대상입니다.
준비 조건:
1. **`mas_logs` 300개 이상** 축적 (Writer 실행 성공 이력)
2. **Metric 함수**: `Judge.run()`이 이미 결정론적 채점기 역할 수행 → 별도 구현 불필요
3. **출력 포맷 고정**: Evaluator의 출력을 위 스키마로 엄격히 고정한 뒤 DSPy 연결
