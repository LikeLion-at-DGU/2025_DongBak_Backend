# 1. Python 3.13 기반 Docker 이미지 사용
FROM python:3.13

# 2. 작업 디렉토리 설정
WORKDIR /

# 3. 로컬의 Django 프로젝트 파일을 컨테이너 내부로 복사
COPY . /

# 4. 필요한 패키지 설치
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. 장고 마이그레이션 (DB 세팅)
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# 6. 컨테이너 실행 시 Django 서버 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]