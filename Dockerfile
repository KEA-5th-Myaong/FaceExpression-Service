# 베이스 이미지로 Python 3.9을 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-system-dev \
    libboost-filesystem-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 필수 패키지를 설치하기 위한 requirements.txt 파일을 복사
COPY requirements.txt .

# pip 업데이트
RUN pip install --upgrade pip

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# Flask 애플리케이션 실행
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
