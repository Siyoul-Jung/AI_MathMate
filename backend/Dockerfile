FROM python:3.11-slim

WORKDIR /app

# 이미지 생성을 위한 시스템 라이브러리 설치 (matplotlib 등 필요시)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 및 DB 복사
COPY . .

# 정적 이미지 저장을 위한 디렉토리 보장
RUN mkdir -p images

EXPOSE 8088

# .env 파일 관리는 docker-compose 또는 환경변수 직접 주입 추천
CMD ["python", "main.py"]
