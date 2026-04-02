# Database Modeling Structure

AI_MathMate 프로젝트는 SQLite 기반의 **AIME Engine Factory** 전용 아키텍처를 사용합니다. 핵심 데이터베이스는 [backend/amc_engine/amc_factory.db](file:///c:/AI_MathMate/backend/amc_engine/amc_factory.db)이며, 문항 생성 엔진과 그로부터 파생된 수천 개의 변체(variants)를 효율적으로 관리하도록 설계되었습니다.

## 핵심 테이블 구조

### 1. `engines` (엔진 레지스트리)
각 AIME 기출문항의 로직을 담고 있는 **Solver 엔진**의 메타데이터를 관리합니다.
- [engine_id](file:///c:/AI_MathMate/backend/amc_engine/pipeline_manager.py#67-69): 고유 식별자 (예: `AIME1-2025-P01`)
- `dna_tag`: 엔진의 고유 특성 태그
- `category`: 수학 분류 (Algebra, Geometry 등)
- `difficulty_band`: 난이도 그룹 (Challenger, Expert, Master)
- `has_image_support`: 이미지 생성 가능 여부

### 2. [variants](file:///c:/AI_MathMate/backend/scripts/equalize_aime_variants.py#14-71) (문항 변체)
엔진이 동적으로 생성한 **실제 문항 데이터**가 저장되는 핵심 테이블입니다.
- [id](file:///c:/AI_MathMate/backend/amc_engine/pipeline_manager.py#67-69): 고유 ID
- [engine_id](file:///c:/AI_MathMate/backend/amc_engine/pipeline_manager.py#67-69): 소속 엔진 (외래키 역할)
- `mode`: `MOCK` (실전 모의고사) 또는 `DRILL` (유형 반복 학습)
- `drill_level`: 학습 단계 (L1~L3)
- [narrative](file:///c:/AI_MathMate/backend/amc_engine/exams/2025/AIME1/EXPERT/P08/solver.py#86-91): 생성된 LaTeX 문제 지문
- `seed_key`: 재현 가능한 생성을 위한 시드 값
- `variables_json`: 문제에 사용된 동적 변수 값들
- `solution_json`: 단계별 풀이 과정
- `correct_answer`: 최종 정답
- `image_url`: 생성된 이미지 파일 경로

### 3. `generated_problems` (레거시/통합 테이블)
과거 버전 또는 특정 서비스 레이어에서 사용되는 백업용 문항 테이블입니다.

### 4. `refill_status` (백그라운드 작업 상태)
엔진별 문항 공급(Refill) 파이프라인의 현재 상태를 추적합니다.

## 데이터 워크플로우
1. **Engine Scaffolder**: 기출문항 분석 후 `engines` 테이블에 등록.
2. **Variant Generation**: [Solver](file:///c:/AI_MathMate/backend/amc_engine/exams/2025/AIME1/MASTER/P11/solver.py#10-261) 클래스의 [generate_seed()](file:///c:/AI_MathMate/backend/amc_engine/exams/2025/AIME1/EXPERT/P06/solver.py#32-44)와 [execute()](file:///c:/AI_MathMate/backend/amc_engine/exams/2025/AIME1/MASTER/P11/solver.py#134-136)를 통해 고유한 문항 생성.
3. **Storage**: 생성된 데이터는 [variants](file:///c:/AI_MathMate/backend/scripts/equalize_aime_variants.py#14-71) 테이블에 JSON 형태로 저장되어 프론트엔드에 즉시 서빙.
4. **Pipeline Manager**: 데이터베이스의 문항 수가 부족할 경우 `refill_status`를 확인하여 자동으로 [variants](file:///c:/AI_MathMate/backend/scripts/equalize_aime_variants.py#14-71)를 추가 생성.
