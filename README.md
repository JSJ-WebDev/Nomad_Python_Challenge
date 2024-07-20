# Job Search Aggregator

이 프로젝트는 Nomad Coder Python Challenge의 졸업 과제로 제작된 Job Search Aggregator입니다. 여러 구직 사이트에서 동시에 일자리를 검색할 수 있는 웹 애플리케이션입니다.

## 기능

- 사용자가 입력한 키워드로 여러 구직 사이트에서 동시에 일자리 검색
- 검색 결과를 사이트별로 분류하여 표시
- 각 일자리에 대한 상세 정보 제공 (직무, 회사, 설명, 링크)

## 지원하는 구직 사이트

- Berlin Startup Jobs
- We Work Remotely
- Web3 Career

## 기술 스택

- Backend: Python, Flask
- Frontend: HTML, CSS
- Web Scraping: BeautifulSoup4, Requests

## 설치 및 실행 방법

1. 이 저장소를 클론합니다:
   ```
   git clone https://github.com/your-username/job-search-aggregator.git
   ```

2. 프로젝트 디렉토리로 이동합니다:
   ```
   cd job-search-aggregator
   ```

3. 필요한 패키지를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

4. 애플리케이션을 실행합니다:
   ```
   python app.py
   ```

5. 웹 브라우저에서 `http://localhost:5000`으로 접속하여 애플리케이션을 사용합니다.

## 프로젝트 구조

- `app.py`: Flask 애플리케이션과 웹 스크래핑 로직
- `templates/`: HTML 템플릿 파일들
  - `index.html`: 메인 검색 페이지
  - `results.html`: 검색 결과 페이지
- `static/`: CSS 파일
  - `styles.css`: 애플리케이션 스타일

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`).
3. 변경 사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`).
5. Pull Request를 생성합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 연락처

프로젝트 관리자 - [jsj970220@gmail.com]
