# MathMate 시스템 명세서 (System Specification)

> **Note**: This document serves as the root pointer for the Spec-Driven Development (SDD) process. Detailed specifications, plans, and tasks are managed in the `specs/` directory.

## 1. Project Constitution
See memory/constitution.md for the core architectural principles and immutable rules governing this project.

## 2. Active Specifications

### Feature: Initial Implementation (v1.0)
- **Specification**: specs/001-initial-implementation/spec.md
- **Implementation Plan**: specs/001-initial-implementation/plan.md
- **Task List**: specs/001-initial-implementation/tasks.md

## 3. Directory Structure

```text
c:\AI_MathMate\
├── core\                  # Core logic & utilities
├── curriculum\            # Content generation modules
├── frontend\              # Next.js application
├── memory\                # Project constitution & context
├── specs\                 # SDD specifications & plans
├── manager.py             # Module loader
├── server.py              # API server
└── manifest.json          # Configuration
```

## 4. 확장 가이드 (Extension Guide)

새로운 수학 단원을 추가하려면 다음 단계를 따릅니다.

1.  **모듈 생성**: `curriculum/` 하위 적절한 경로에 `std_{code}.py` 파일을 생성합니다.
2.  **클래스 구현**: `BaseTMaster`를 상속받는 클래스(예: `T99_Master`)를 작성하고 `generate` 메서드를 구현합니다.
    - `MathUtils`나 `GeometryUtils`를 활용하여 로직을 작성합니다.
    - 난이도(`difficulty`)와 문제 형식(`q_type`)에 따른 분기 처리를 포함합니다.
3.  **설정 등록**: `manifest.json` 파일에 새로운 성취기준 ID와 파일 경로를 추가합니다.
4.  **프론트엔드 갱신**: `frontend/app/page.tsx`의 `allStandards` 배열에 새 성취기준 정보를 추가합니다.

## 5. 디렉토리 구조 (Directory Structure)
```text
c:\AI_MathMate\
├── core\                  # 핵심 공통 모듈
├── curriculum\            # 교육과정별 문제 생성 로직
├── frontend\              # Next.js 웹 애플리케이션
├── indexes\               # 교육과정 인덱스 명세 (Markdown)
├── manager.py             # 모듈 로더 및 관리자
├── server.py              # API 서버
├── manifest.json          # 모듈 매핑 설정
├── requirements.txt       # Python 의존성 목록
└── SPEC.md                # 시스템 명세서 (본 파일)
```