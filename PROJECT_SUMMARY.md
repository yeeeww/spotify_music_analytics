# 🎵 Spotify Music Analytics - 프로젝트 완료 보고서

## 📋 프로젝트 개요

**프로젝트명:** Spotify Music Analytics  
**완료일:** 2025년 12월 15일  
**목표:** SQL을 모르는 사용자도 자연어로 음악 데이터를 분석할 수 있는 웹 서비스 구축  
**핵심 기술:** Streamlit + Gemini AI + SQLite + Plotly

---

## ✅ 구현 완료 항목

### 1. 프로젝트 구조 및 의존성 ✅

- [x] 프로젝트 폴더 구조 생성
- [x] requirements.txt 작성
- [x] .gitignore 설정
- [x] README.md 작성
- [x] 라이선스 파일 (MIT)

### 2. 데이터 처리 모듈 ✅

- [x] 데이터 다운로드 가이드 스크립트
- [x] 데이터 전처리 스크립트
- [x] SQLite 데이터베이스 구축 스크립트
- [x] 데이터베이스 관리 모듈 (database.py)

### 3. AI/LLM 모듈 ✅

- [x] Gemini API 연동 (llm.py)
- [x] Text-to-SQL 기능
- [x] 결과 분석 기능
- [x] 시각화 추천 기능
- [x] 리포트 생성 기능

### 4. 시각화 모듈 ✅

- [x] 막대 그래프
- [x] 선 그래프
- [x] 산점도
- [x] 파이 차트
- [x] 히스토그램
- [x] 박스 플롯
- [x] 히트맵 (상관관계)
- [x] 자동 시각화 기능

### 5. Streamlit 웹 애플리케이션 ✅

- [x] 메인 페이지 (app.py)
- [x] 데이터 탐색 페이지
- [x] 자연어 질의 페이지
- [x] 분석 리포트 페이지
- [x] Streamlit 테마 설정

### 6. 문서화 ✅

- [x] README.md (프로젝트 소개)
- [x] setup_guide.md (설치 및 실행 가이드)
- [x] USAGE_EXAMPLES.md (사용 예시)
- [x] PROJECT_SUMMARY.md (이 문서)

---

## 📁 프로젝트 구조

```
spotify_music_analytics/
├── app.py                          # 메인 Streamlit 앱
├── requirements.txt                # Python 패키지 의존성
├── .gitignore                      # Git 무시 파일
├── .env.example                    # 환경 변수 예시
├── README.md                       # 프로젝트 소개
├── setup_guide.md                  # 설치 가이드
├── USAGE_EXAMPLES.md               # 사용 예시
├── PROJECT_SUMMARY.md              # 프로젝트 요약
├── LICENSE                         # MIT 라이선스
│
├── .streamlit/
│   └── config.toml                 # Streamlit 설정
│
├── data/
│   ├── raw/                        # 원본 데이터 (사용자가 다운로드)
│   │   └── dataset.csv             # Kaggle Spotify 데이터셋
│   ├── processed/                  # 전처리된 데이터
│   │   └── spotify_cleaned.csv     # 전처리 완료 데이터
│   └── spotify.db                  # SQLite 데이터베이스
│
├── scripts/
│   ├── download_data.py            # 데이터 검증 스크립트
│   ├── preprocess_data.py          # 데이터 전처리 스크립트
│   └── build_database.py           # 데이터베이스 구축 스크립트
│
├── modules/
│   ├── __init__.py
│   ├── database.py                 # 데이터베이스 관리 모듈
│   ├── llm.py                      # Gemini API 연동 모듈
│   └── visualization.py            # 시각화 모듈
│
└── pages/
    ├── 1_📊_데이터_탐색.py          # 데이터 탐색 페이지
    ├── 2_💬_자연어_질의.py          # 자연어 질의 페이지
    └── 3_📈_분석_리포트.py          # 분석 리포트 페이지
```

---

## 🔧 기술 스택

### Backend

- **Python 3.10+**: 메인 프로그래밍 언어
- **SQLite**: 경량 데이터베이스
- **Pandas**: 데이터 처리 및 분석

### AI/LLM

- **Google Gemini API**: Text-to-SQL 및 결과 분석
- **google-generativeai**: Gemini API Python SDK

### Frontend

- **Streamlit**: 웹 애플리케이션 프레임워크
- **Plotly**: 인터랙티브 시각화

### 기타

- **python-dotenv**: 환경 변수 관리
- **openpyxl**: Excel 파일 처리 (선택사항)

---

## 🎯 주요 기능

### 1. 데이터 탐색 📊

- **테이블 미리보기**: 데이터베이스의 모든 테이블 확인
- **스키마 정보**: 컬럼 구조 및 데이터 타입 확인
- **기본 통계**: 숫자형/문자형 컬럼의 통계 정보
- **시각화**: 히스토그램, 박스 플롯, 막대 그래프
- **CSV 다운로드**: 조회 결과 다운로드

### 2. 자연어 질의 💬

- **Text-to-SQL**: 한국어 질문을 SQL로 자동 변환
- **쿼리 실행**: 생성된 SQL 자동 실행
- **AI 분석**: 결과에 대한 AI 기반 인사이트
- **자동 시각화**: 결과에 적합한 차트 자동 생성
- **SQL 수정**: 생성된 SQL 수정 및 재실행
- **질의 히스토리**: 이전 질의 기록 관리

**지원하는 질문 예시:**

- "가장 인기 있는 장르 TOP 10은?"
- "댄스 지수가 0.8 이상인 곡은?"
- "장르별 평균 템포를 보여줘"
- "에너지와 댄스 지수의 상관관계는?"
- "인기도가 80 이상인 곡의 평균 특성은?"

### 3. 분석 리포트 📈

- **전체 데이터 개요**: 전체 통계 및 분포
- **장르 분석**: 장르별 트랙 수, 인기도, 음악 특성
- **음악 특성 분석**: 개별 특성의 분포 및 상관관계
- **인기도 분석**: 인기도 구간별 분석
- **커스텀 분석**: 사용자 정의 분석 설정
- **리포트 다운로드**: 마크다운 형식 리포트 생성

---

## 📊 데이터베이스 스키마

### tracks 테이블 (메인)

| 컬럼명           | 타입    | 설명                       |
| ---------------- | ------- | -------------------------- |
| track_id         | TEXT    | 트랙 고유 ID               |
| track_name       | TEXT    | 곡 제목                    |
| artists          | TEXT    | 아티스트명                 |
| album_name       | TEXT    | 앨범명                     |
| track_genre      | TEXT    | 장르                       |
| popularity       | INTEGER | 인기도 (0-100)             |
| duration_ms      | INTEGER | 재생 시간 (밀리초)         |
| duration_sec     | FLOAT   | 재생 시간 (초)             |
| danceability     | FLOAT   | 댄스 적합도 (0.0-1.0)      |
| energy           | FLOAT   | 에너지 (0.0-1.0)           |
| tempo            | FLOAT   | BPM                        |
| valence          | FLOAT   | 긍정도 (0.0-1.0)           |
| acousticness     | FLOAT   | 어쿠스틱 정도 (0.0-1.0)    |
| instrumentalness | FLOAT   | 악기 연주 정도 (0.0-1.0)   |
| speechiness      | FLOAT   | 음성 포함 정도 (0.0-1.0)   |
| liveness         | FLOAT   | 라이브 녹음 정도 (0.0-1.0) |
| loudness         | FLOAT   | 음량 (dB)                  |
| key              | INTEGER | 음계 (0-11)                |
| mode             | INTEGER | 메이저(1)/마이너(0)        |
| time_signature   | INTEGER | 박자 (3-7)                 |

### genres 테이블

| 컬럼명     | 타입    | 설명         |
| ---------- | ------- | ------------ |
| genre_id   | INTEGER | 장르 ID (PK) |
| genre_name | TEXT    | 장르명       |

### artists 테이블

| 컬럼명      | 타입    | 설명             |
| ----------- | ------- | ---------------- |
| artist_id   | INTEGER | 아티스트 ID (PK) |
| artist_name | TEXT    | 아티스트명       |

### albums 테이블

| 컬럼명     | 타입    | 설명         |
| ---------- | ------- | ------------ |
| album_id   | INTEGER | 앨범 ID (PK) |
| album_name | TEXT    | 앨범명       |

### 뷰 (Views)

- **genre_stats**: 장르별 통계 (트랙 수, 평균 특성)
- **popularity_stats**: 인기도 구간별 통계

---

## 🚀 설치 및 실행 방법

### 1. 환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. API 키 설정

1. `.env.example`을 `.env`로 복사
2. Gemini API 키 발급: https://makersuite.google.com/app/apikey
3. `.env` 파일에 API 키 입력

```
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. 데이터 준비

```bash
# 1. 데이터 검증
python scripts/download_data.py

# 2. Kaggle에서 데이터셋 다운로드
# https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
# dataset.csv를 data/raw/ 폴더에 저장

# 3. 데이터 전처리
python scripts/preprocess_data.py

# 4. 데이터베이스 구축
python scripts/build_database.py
```

### 4. 앱 실행

```bash
streamlit run app.py
```

브라우저에서 http://localhost:8501 접속

---

## 📈 성능 및 최적화

### 데이터베이스

- **인덱스**: track_id, artists, track_genre, popularity
- **뷰**: 자주 사용하는 집계 쿼리 사전 계산
- **최적화**: 쿼리 결과 제한 (LIMIT 사용)

### 시각화

- **샘플링**: 대용량 데이터는 샘플링하여 표시
- **캐싱**: Streamlit 캐싱 활용
- **지연 로딩**: 필요할 때만 데이터 로드

### AI/LLM

- **프롬프트 최적화**: 효율적인 SQL 생성
- **오류 처리**: 유효성 검사 및 재시도
- **보안**: 읽기 전용 쿼리만 허용

---

## 🔒 보안 고려사항

### SQL Injection 방지

- 위험한 키워드 차단 (DROP, DELETE, INSERT, UPDATE 등)
- 쿼리 유효성 검사
- 읽기 전용 쿼리만 허용

### API 키 보안

- `.env` 파일로 환경 변수 관리
- `.gitignore`에 `.env` 추가
- API 키 노출 방지

---

## 🐛 알려진 제한사항

1. **데이터 크기**: 매우 큰 결과는 성능 저하 가능
2. **LLM 정확도**: 복잡한 질문은 SQL 생성 실패 가능
3. **언어 지원**: 현재 한국어만 지원
4. **오프라인**: 인터넷 연결 필요 (Gemini API)

---

## 🔮 향후 개선 사항

### 기능 추가

- [ ] 다국어 지원 (영어, 일본어 등)
- [ ] 사용자 계정 및 인증
- [ ] 쿼리 즐겨찾기 기능
- [ ] 대시보드 커스터마이징
- [ ] 실시간 데이터 업데이트
- [ ] 더 많은 차트 타입

### 성능 개선

- [ ] 데이터베이스 캐싱
- [ ] 비동기 쿼리 실행
- [ ] 결과 페이지네이션
- [ ] 이미지 캐싱

### AI 개선

- [ ] 더 정교한 프롬프트 엔지니어링
- [ ] 쿼리 검증 강화
- [ ] 자연어 이해 향상
- [ ] 다른 LLM 지원 (OpenAI, Claude 등)

---

## 📚 참고 자료

### 데이터셋

- [Kaggle - Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
- [Spotify Audio Features Documentation](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)

### 기술 문서

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

---

## 👨‍💻 개발자

**프로젝트 개발자**: [Your Name]  
**개발 기간**: 2025년 12월  
**연락처**: [Your Email]

---

## 🎉 프로젝트 완료!

Spotify Music Analytics 프로젝트가 성공적으로 완료되었습니다!

### 구현된 기능 요약:

✅ 데이터 전처리 및 데이터베이스 구축  
✅ Gemini AI 기반 Text-to-SQL  
✅ 3개의 주요 페이지 (데이터 탐색, 자연어 질의, 분석 리포트)  
✅ 7가지 시각화 타입  
✅ AI 기반 결과 분석  
✅ 완전한 문서화

### 다음 단계:

1. Kaggle에서 데이터셋 다운로드
2. Gemini API 키 발급 및 설정
3. 데이터베이스 구축
4. 앱 실행 및 테스트

**Happy Analyzing! 🎵**
