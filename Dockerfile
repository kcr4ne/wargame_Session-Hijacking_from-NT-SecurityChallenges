# 파이썬 공식 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리를 /app으로 설정
WORKDIR /app

# 현재 디렉터리의 모든 파일과 디렉터리를 컨테이너의 /app으로 복사
# .dockerignore 파일을 사용해 불필요한 파일 제외 가능
COPY . .

# requirements.txt 복사 및 의존성 설치 (requirements.txt가 복사되었으므로 별도 COPY 불필요)
RUN pip install --no-cache-dir -r requirements.txt

# 2003번 포트 노출
EXPOSE 2003

# 컨테이너 시작 시 app.py 실행
CMD ["python", "app.py"]