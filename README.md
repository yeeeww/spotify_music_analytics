# Spotify Music Analytics

SQL을 모르는 사용자도 자연어로 음악 데이터를 분석할 수 있는 웹 서비스

## 프로젝트 개요

- **목표**: 자연어 질문을 통한 Spotify 음악 데이터 분석
- **핵심 기술**: Streamlit + Gemini AI + SQLite
- **데이터셋**: Kaggle Spotify Tracks Dataset (114,000+ 트랙)

## 주요 기능

1. **데이터 탐색**: 전체 데이터 미리보기 및 통계
2. **자연어 질의**: 한국어 질문으로 데이터 조회
3. **시각화**: 인터랙티브 차트 자동 생성
4. **분석 리포트**: AI 기반 결과 해석

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd spotify_music_analytics
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env.example` 파일을 `.env`로 복사하고 Gemini API 키를 입력하세요:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
```

`.env` 파일을 열어 API 키를 입력:

```
GEMINI_API_KEY=your_actual_api_key_here
```

### 5. 데이터 준비

Kaggle에서 Spotify Tracks Dataset을 다운로드하세요:
- URL: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
- 다운로드한 `dataset.csv` 파일을 `data/raw/` 폴더에 저장

### 6. 데이터베이스 구축

```bash
python scripts/build_database.py
```

## 실행 방법

```bash
streamlit run app.py
```

브라우저에서 자동으로 열립니다 (기본: http://localhost:8501)

## 프로젝트 구조

```
spotify_music_analytics/
├── app.py                      # Streamlit 메인 앱
├── requirements.txt            # 패키지 의존성
├── .env                        # 환경 변수 (API 키)
├── README.md                   # 프로젝트 문서
├── data/
│   ├── raw/                    # 원본 데이터
│   │   └── dataset.csv
│   └── spotify.db              # SQLite 데이터베이스
├── scripts/
│   ├── build_database.py       # DB 구축 스크립트
│   └── preprocess_data.py      # 데이터 전처리
├── modules/
│   ├── __init__.py
│   ├── database.py             # DB 연결 및 쿼리
│   ├── llm.py                  # Gemini API 연동
│   └── visualization.py        # 시각화 함수
└── pages/
    ├── 1_📊_데이터_탐색.py
    ├── 2_💬_자연어_질의.py
    └── 3_📈_분석_리포트.py
```

## 사용 예시

### 자연어 질문 예시

- "가장 인기 있는 장르 TOP 10은?"
- "BTS의 모든 곡 보여줘"
- "댄스 지수가 0.8 이상인 곡은?"
- "장르별 평균 템포 비교"
- "에너지와 댄스 지수의 상관관계는?"

## 기술 스택

- **Frontend**: Streamlit
- **LLM**: Google Gemini API
- **Database**: SQLite
- **데이터 처리**: Pandas
- **시각화**: Plotly

## 라이선스

MIT License

## 참고 자료

- [Spotify Tracks Dataset - Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [Plotly Python Documentation](https://plotly.com/python/)

