
---

# [Specification Document] Hybrid AI Math Tutoring System

## 1. System Overview & Core Philosophy

* **Goal:** Provide a dynamic, interactive high school math learning platform.
* **Core Architecture:** * **Python Symbolic Engine (SymPy):** Handles deterministic math logic, problem generation, and exact answer verification.
* **LLM (Tutor Engine):** Handles pedagogical dialogue, error diagnosis based on step-logic, and interactive hinting.


* **Operating Principle:** "Code is the Problem." Instead of static DB entries, use Python templates to generate infinite parametric problems.

---

## 2. Technical Stack (Requirement)

* **Language:** Python 3.10+
* **Math Library:** `SymPy` (Symbolic Mathematics)
* **AI Model:** GPT-4o or Claude 3.5 Sonnet (via API)
* **Formula Rendering:** KaTeX (Frontend) / LaTeX (Backend)
* **Database:** PostgreSQL (Relational data & Student Logs)

---

## 3. Module Specification

### M1. Parametric Problem Generator (Python)


```python
class MathProblemGenerator:
    """
    Interface for generating parametric math problems.
    Must ensure 'clean' answers (integers/simple fractions).
    """
    def generate_quadratic_problem(self, difficulty_level):
        # Step 1: Inverse design for clean answers
        # Step 2: Extract 'Solving Steps' for LLM guidance
        # Returns: { problem_latex, answer, logic_steps: [] }
        pass

```

* **Logic Steps Structure:**
1. `step_id`: Sequential ID.
2. `description`: Human-readable logic (e.g., "Substitute into Discriminant").
3. `target_expr`: The symbolic expression expected at this stage.
4. `concept_id`: Mapping to national achievement standards.



### M2. LLM Diagnostic Prompt (Tutor Engine)

AI 개발 에이전트가 시스템 프롬프트에 주입해야 할 로직입니다.

> **Role:** You are a meta-cognitive math tutor.
> **Input:** `Logic_Steps` (from M1), `Student_Input` (Handwriting OCR/LaTeX).
> **Task:** > 1. Compare Student_Input against Logic_Steps sequentially.
> 2. Identify the FIRST point of failure (Break-point).
> 3. Categorize error: `CONCEPT` (Wrong logic) vs `CALC` (Calculation error).
> **Constraint:** > - **NEVER** give the final answer.
> * **ALWAYS** provide a hint only for the current failed step.
> * **PRIORITIZE** conceptual errors over calculation errors.
> 
> 

---

## 4. Data Model (ERD for AI Implementation)

### Table: `Achievement_Standards`

* `std_code` (PK): NCIC/AMC Standard ID.
* `prerequisites` (Array): Parent concepts for diagnostic backtracking.

### Table: `Student_Step_Log` (The 'Brain' of Analysis)

* `log_id` (PK)
* `student_id` (FK)
* `step_type`: `CONCEPT` | `CALC` | `STRATEGY`
* `success_status`: `自力(Self)`, `힌트후(Hinted)`, `실패(Fail)`
* `timestamp`: For calculating 'Thinking Time'.

---

## 5. User Autonomy & Recovery Workflow

AI는 다음 흐름을 보장하도록 인터페이스를 코딩해야 합니다.

1. **Diagnostic Feedback:** 사용자가 문제를 완료하면, AI는 `Student_Step_Log`를 집계하여 "취약 성취기준 리스트"를 대시보드에 업데이트합니다.
2. **Self-Correction Menu:** * 사용자 화면에 "취약점 보완하기" 섹션 노출.
* 사용자가 특정 성취기준 클릭 시 -> `M1. Generator`에 해당 `concept_id`를 전달하여 유사 유형 문제 세트 즉시 생성.
* 시스템은 강제로 문제를 배정하지 않으며, 사용자의 'Trigger'에 의해서만 작동함.



---

## 6. Implementation Roadmap for AI Agent (Prompt to AI)

AI 에이전트에게 다음 순서로 코딩을 지시하세요:

1. **Phase 1:** `SymPy`를 사용하여 고등 공통수학 '이차방정식' 단원의 파라메트릭 생성기(`M1`)를 코딩하라. 정답은 항상 정수가 나오도록 역산 설계하라.
2. **Phase 2:** 생성기에서 나온 `logic_steps`를 읽어 학생의 오답을 진단하는 FastAPI 엔드포인트와 LLM 프롬프트를 연동하라.
3. **Phase 3:** `Student_Step_Log`를 기반으로 특정 성취기준의 숙련도를 계산하는 분석 모듈을 작성하라.
4. **Phase 4:** 분석된 숙련도가 낮은 단원을 사용자가 클릭했을 때 다시 `Phase 1`을 호출하는 순환 구조를 완성하라.

---

## 7. UI/UX Design Strategy (Minimalist Studio)

* **Visual Concept:** "Minimalist Studio" - Focus on immersion and intelligence.
* **Color Palette:**
    * **Background:** Soft White (`#F8FAFC`) for Day, Dark Navy (`#0F172A`) for Night.
    * **Primary:** Electric Blue (`#3B82F6`) for emphasis and AI interaction.
* **Typography:**
    * **Math:** KaTeX for elegant formula rendering.
    * **Text:** Inter or Pretendard for maximum readability.
* **Component Design:**
    * **Step-by-Step Card UI:** Progressive disclosure (Hint -> Logic -> Solution).
    * **AMC Exam Mode:** Timer and clean "paper-like" layout.
    * **Dark Mode:** Optimized for eye comfort using slate tones rather than pure black.