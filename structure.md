# MathMate Project Structure

## Core (공통 모듈)
- `core/base.py`: 문제 생성기 기본 클래스 (BaseTMaster)
- `core/math_utils.py`: 수학 연산 유틸리티

## Curriculum (교육과정 콘텐츠)
### KR (한국)
- **Middle_1-1 (중1-1)**
  - `std_11_01.py`: 소인수분해
  - `std_11_02.py`: 최대공약수와 최소공배수

### US (미국 - 예정)
- **AMC_8**
  - (추후 추가 예정)

## Configuration (설정)
- `manifest.json`: 교육과정 및 모듈 매핑 설정 파일

## System
- `manager.py`: 문제 생성 통합 관리자 (manifest.json 기반 로딩)
- `generator.py`: 메인 실행 파일

## Documentation
- `indexes/`: 표준 인덱스 리스트 (Markdown)