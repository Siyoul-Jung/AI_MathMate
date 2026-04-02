# ui-polish: AI MathMate V2 UI/UX 디자인 표준

이 문서는 AI MathMate V2의 프론트엔드 디자인 철학과 구현 표준을 정의합니다.
**수학 학습자의 '몰입 상태(Flow)'를 유지하는 것**이 모든 UI 결정의 최우선 기준입니다.

---

## 1. 디자인 철학 (Design Philosophy)

### 1.1 신뢰의 투명성 (Trust Through Transparency)
학습자는 문항이 어떻게 검증되었는지 볼 권리가 있습니다.
문항 카드에는 **BEq 검증 통과 뱃지**와 **DAPS 점수**를 시각화하여
"이 문항은 AI가 수학적으로 검증한 문항입니다"라는 신뢰감을 줍니다.

### 1.2 수학적 DNA 시각화 (Mathematical DNA Badge)
각 문항의 메타 정보를 다음과 같이 시각화합니다:
```
[Algebra × Number Theory]  DAPS 13.5  δ★★☆ (Heuristic: 2.0)  ✅ BEq Verified
```

---

## 2. 미적 표준 (Aesthetic Standards)

### 2.1 색상 팔레트 (Color Palette)
- **다크 테마 기반**: Zinc-900 → Zinc-800 그라디언트 배경
- **강조 색상**: Blue-500 (상호작용), Emerald-400 (정답/성공), Rose-400 (오류/경고)
- **BEq 검증 뱃지**: Emerald 계열 글로우 효과
- **DAPS 바**: 점수에 따라 Blue(Challenger) → Purple(Expert) → Gold(Master)

### 2.2 타이포그래피 (Typography)
- **기본 폰트**: Inter (UI 텍스트), JetBrains Mono (코드/시드 데이터)
- **수식**: KaTeX 렌더링, 절대로 Raw LaTeX 텍스트가 사용자에게 노출되면 안 됩니다

### 2.3 컴포넌트 스타일
- **카드**: `rounded-2xl`, `backdrop-blur-md`, `border border-zinc-700/50` (Glassmorphism)
- **버튼**: 호버 시 scale-105 + glow 효과 (subtle micro-animation)
- **드릴 레벨 표시기**: L1 → L2 → L3 진행 바 (스텝퍼 형식)

---

## 3. 수식 렌더링 표준 (Math Rendering)

- **엔진**: KaTeX (모든 수식의 최종 렌더러, MathJax 사용 금지)
- **인라인**: `$...$` → `<InlineMath>` 컴포넌트
- **블록**: `$$...$$` → `<BlockMath>` 컴포넌트 (중앙 정렬)
- **오류 방지**: KaTeX 렌더링 실패 시 Raw LaTeX를 숨기고 에러 아이콘만 표시

---

## 4. 핵심 컴포넌트 설계 (Component Design)

### 4.1 ProblemViewer (문항 뷰어)
```
┌─────────────────────────────────────────────────────────┐
│  [MASTER]  DAPS 13.5  δ★★☆  ✅ BEq Verified            │
│  Algebra × Number Theory                                 │
├─────────────────────────────────────────────────────────┤
│  [문제 지문 — KaTeX 렌더링]                              │
│                                                          │
│  Find the value of ...                                   │
│           $$\sum_{k=1}^{n} k^2 = ...$$                  │
├─────────────────────────────────────────────────────────┤
│  [답안 입력]  [___]  (0–999)        [제출] [힌트 보기]   │
└─────────────────────────────────────────────────────────┘
```

### 4.2 DrillBridge (드릴 연결 컴포넌트)
Level 1 → Level 2 → Level 3 전환은 **페이지 점프가 아닌 슈퍼 트랜지션**처럼 느껴져야 합니다:
- 레벨 업 시: 화면 중앙에서 ripple 애니메이션 후 다음 레벨 슬라이드 인
- DAPS 바가 실시간으로 올라가는 애니메이션 표시

### 4.3 MAS Provenance Panel (검증 이력 패널)
"솔루션 보기" 클릭 시 확장되는 패널:
```
🏗️ Architect: algebra.vieta 모듈 선택  (DAPS 4.5)
✍️ Writer:    지문 생성 완료 (시도 1회)
🔍 Evaluator: 역추론 답 = 567 ✅
⚖️ Judge:     BEq PASS — 원본 567 == 역추론 567
```
- 이 패널은 AI 교육 플랫폼의 차별화 포인트입니다. **학습자에게 AI가 어떻게 문제를 만들고 검증했는지 투명하게 공개**합니다.

---

## 5. 인터랙션 디자인 (Interaction Design)

- **마이크로 애니메이션**: 버튼/카드 호버 시 scale-105 + 그림자 강화
- **정답 제출**: 정답 시 confetti + 에메랄드 글로우, 오답 시 빨간 빛 + shake 애니메이션
- **모바일 대응**: 수식 블록은 가로 스크롤 허용 (`overflow-x: auto`)

---

## 6. TikZ/Asymptote 렌더링 통합 (기하 문항 전용)

GEOMETRY 도메인 문항의 도형은 SVG로 임베딩됩니다:
```html
<!-- 백엔드에서 TikZ → SVG 변환 후 정적 파일로 제공 -->
<img src="/static/problems/{variant_id}_diagram.svg"
     alt="문제 다이어그램"
     class="w-full max-w-md mx-auto my-4" />
```
- SVG는 항상 `max-width: 28rem` 제한으로 레이아웃 깨짐 방지
- 다크 모드에서 선 색상이 보이도록 SVG 내 `stroke: currentColor` 사용
