# 🚀 빠른 시작 가이드

Spotify Music Analytics를 5분 안에 시작하세요!

---

## ⚡ 빠른 설치 (5분)

### 1단계: 패키지 설치 (1분)

```bash
# 가상환경 생성 및 활성화 (Windows)
python -m venv venv
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2단계: API 키 설정 (1분)

1. **Gemini API 키 발급**

   - 🔗 https://makersuite.google.com/app/apikey 접속
   - Google 계정으로 로그인
   - "Create API Key" 클릭
   - API 키 복사

2. **환경 변수 설정**
   - `.env.example` 파일을 `.env`로 복사
   - `.env` 파일을 열어 API 키 입력:
   ```
   GEMINI_API_KEY=여기에_발급받은_API_키_붙여넣기
   ```

### 3단계: 데이터 준비 (3분)

```bash
# 1. 데이터 다운로드 가이드 실행
python scripts/download_data.py
```

**Kaggle에서 데이터 다운로드:**

1. 🔗 https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
2. "Download" 버튼 클릭
3. `dataset.csv` 파일을 `data/raw/` 폴더에 저장

```bash
# 2. 데이터 전처리 (1-2분 소요)
python scripts/preprocess_data.py

# 3. 데이터베이스 구축 (1-2분 소요)
python scripts/build_database.py
```

### 4단계: 앱 실행 (10초)

```bash
streamlit run app.py
```

브라우저가 자동으로 열립니다! 🎉

---

## 🎯 첫 번째 질의 해보기

### 1. 자연어 질의 페이지로 이동

왼쪽 사이드바에서 **"💬 자연어 질의"** 클릭

### 2. 질문 입력

다음 질문 중 하나를 입력해보세요:

```
가장 인기 있는 장르 TOP 10은?
```

또는

```
댄스 지수가 0.8 이상인 곡은?
```

### 3. 결과 확인

- 🤖 **AI 분석 탭**: AI가 분석한 인사이트
- 📋 **데이터 탭**: 쿼리 결과 테이블
- 📊 **시각화 탭**: 자동 생성된 차트
- 🔍 **SQL 탭**: 생성된 SQL 쿼리

---

## 📊 데이터 탐색하기

### 1. 데이터 탐색 페이지로 이동

왼쪽 사이드바에서 **"📊 데이터 탐색"** 클릭

### 2. 테이블 선택

사이드바에서 `tracks` 테이블 선택

### 3. 탭 둘러보기

- **📋 데이터 미리보기**: 실제 데이터 확인
- **🔍 스키마 정보**: 테이블 구조 확인
- **📊 기본 통계**: 통계 정보 확인
- **📈 시각화**: 차트 생성

---

## 📈 분석 리포트 생성하기

### 1. 분석 리포트 페이지로 이동

왼쪽 사이드바에서 **"📈 분석 리포트"** 클릭

### 2. 리포트 타입 선택

사이드바에서 다음 중 선택:

- **전체 데이터 개요**: 전체 통계 및 분포
- **장르 분석**: 장르별 상세 분석
- **음악 특성 분석**: 개별 특성 분석
- **인기도 분석**: 인기도 기반 분석
- **커스텀 분석**: 직접 설정

### 3. 결과 확인 및 다운로드

- 차트와 테이블로 결과 확인
- 사이드바에서 "📄 리포트 생성" 클릭하여 다운로드

---

## 💡 유용한 질문 예시

### 기본 질문

```
가장 인기 있는 장르 TOP 10은?
댄스 지수가 0.8 이상인 곡은?
장르별 평균 템포를 보여줘
에너지가 높은 곡 TOP 20
```

### 조건부 질문

```
인기도가 80 이상인 곡의 평균 특성은?
템포가 120 이상인 곡 중 인기 있는 곡은?
어쿠스틱 지수가 높은 장르는?
```

### 비교 질문

```
장르별 평균 에너지를 비교해줘
pop과 rock의 음악 특성 차이는?
인기도가 높은 곡과 낮은 곡의 특성 차이는?
```

---

## 🐛 문제 해결

### 문제: "데이터베이스 파일을 찾을 수 없습니다"

**해결:**

```bash
python scripts/download_data.py
python scripts/preprocess_data.py
python scripts/build_database.py
```

### 문제: "Gemini API 키가 설정되지 않았습니다"

**해결:**

1. `.env` 파일이 프로젝트 루트에 있는지 확인
2. `.env` 파일에 `GEMINI_API_KEY=실제키` 형식으로 입력
3. 앱 재시작

### 문제: "ModuleNotFoundError"

**해결:**

```bash
pip install -r requirements.txt
```

### 문제: 포트가 이미 사용 중

**해결:**

```bash
streamlit run app.py --server.port 8502
```

---

## 🎓 다음 단계

### 더 배우기

- 📖 [setup_guide.md](setup_guide.md) - 상세 설치 가이드
- 📚 [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - 사용 예시 모음
- 📋 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 프로젝트 전체 요약

### 고급 기능

- SQL 쿼리 직접 수정하기
- 커스텀 분석 설정하기
- 리포트 생성 및 다운로드

### 문제 발생 시

- GitHub Issues에 문제 보고
- 문서 참조
- 커뮤니티 질문

---

## ✅ 체크리스트

설치 완료 확인:

- [ ] Python 3.10+ 설치됨
- [ ] 가상환경 생성 및 활성화
- [ ] 패키지 설치 완료
- [ ] Gemini API 키 설정
- [ ] 데이터셋 다운로드
- [ ] 데이터 전처리 완료
- [ ] 데이터베이스 구축 완료
- [ ] 앱 실행 성공
- [ ] 첫 번째 질의 성공

모두 체크되었다면 준비 완료! 🎉

---

**Happy Analyzing! 🎵**

문제가 있으면 [setup_guide.md](setup_guide.md)의 문제 해결 섹션을 참조하세요.
