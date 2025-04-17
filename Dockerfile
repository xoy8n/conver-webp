FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 시스템 의존성 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 필요한 패키지 설치
RUN pip install --no-cache-dir pillow>=10.0.0

# 애플리케이션 코드 복사
COPY server.py .

# 스크립트 실행 권한 부여
RUN chmod +x server.py

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1

# MCP 서버 실행
CMD ["python", "server.py"] 