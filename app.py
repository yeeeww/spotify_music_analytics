"""
Spotify Music Analytics - 메인 애플리케이션
"""
import streamlit as st
import os
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="Spotify Music Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1DB954;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #1DB954;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1ed760;
    }
</style>
""", unsafe_allow_html=True)

# 메인 페이지
def main():
    # 헤더
    st.markdown('<div class="main-header">🎵 Spotify Music Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">SQL을 모르는 사용자도 자연어로 음악 데이터를 분석할 수 있는 웹 서비스</div>', unsafe_allow_html=True)
    
    # 데이터베이스 상태 확인
    db_path = Path("data/spotify.db")
    
    if not db_path.exists():
        st.warning("⚠️ 데이터베이스 파일을 찾을 수 없습니다.")
        
        with st.expander("📥 데이터베이스 설정 방법", expanded=True):
            st.markdown("""
            ### 데이터베이스를 생성하려면:
            
            1. **데이터 다운로드**
               ```bash
               python scripts/download_data.py
               ```
               Kaggle에서 Spotify Tracks Dataset을 다운로드하여 `data/raw/` 폴더에 저장하세요.
               
            2. **데이터 전처리**
               ```bash
               python scripts/preprocess_data.py
               ```
               
            3. **데이터베이스 구축**
               ```bash
               python scripts/build_database.py
               ```
            
            ### 데이터셋 정보
            - **출처**: [Kaggle - Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
            - **규모**: 114,000+ 트랙
            - **장르**: 125개
            """)
        
        st.info("💡 데이터베이스가 준비되면 페이지를 새로고침하세요.")
        return
    
    # 데이터베이스가 있는 경우
    st.success("✅ 데이터베이스가 준비되었습니다!")
    
    # 소개 섹션
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>📊 데이터 탐색</h3>
            <p>전체 데이터 미리보기, 테이블 스키마 확인, 기본 통계를 제공합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>💬 자연어 질의</h3>
            <p>한국어 질문으로 데이터를 조회하고 AI가 자동으로 SQL을 생성합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>📈 분석 리포트</h3>
            <p>AI 기반 결과 해석과 인터랙티브 차트를 제공합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 빠른 시작 가이드
    st.subheader("🚀 빠른 시작")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 자연어 질의 예시
        - "가장 인기 있는 장르 TOP 10은?"
        - "댄스 지수가 0.8 이상인 곡은?"
        - "장르별 평균 템포 비교"
        - "에너지와 댄스 지수의 상관관계는?"
        """)
    
    with col2:
        st.markdown("""
        ### 사용 방법
        1. 왼쪽 사이드바에서 원하는 페이지 선택
        2. **데이터 탐색**: 데이터 구조 파악
        3. **자연어 질의**: 질문 입력하고 결과 확인
        4. **분석 리포트**: 심층 분석 및 리포트 생성
        """)
    
    st.markdown("---")
    
    # 데이터셋 정보
    st.subheader("📚 데이터셋 정보")
    
    # 데이터베이스 정보 로드
    try:
        from modules.database import DatabaseManager
        
        db = DatabaseManager(str(db_path))
        info = db.get_database_info()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            tracks_count = info['tables'].get('tracks', {}).get('row_count', 0)
            st.metric("총 트랙 수", f"{tracks_count:,}")
        
        with col2:
            genres_count = info['tables'].get('genres', {}).get('row_count', 0)
            st.metric("장르 수", f"{genres_count:,}")
        
        with col3:
            artists_count = info['tables'].get('artists', {}).get('row_count', 0)
            st.metric("아티스트 수", f"{artists_count:,}")
        
        with col4:
            db_size = info['database_size'] / (1024 * 1024)
            st.metric("DB 크기", f"{db_size:.1f} MB")
        
        db.close()
        
    except Exception as e:
        st.error(f"데이터베이스 정보 로드 실패: {e}")
    
    st.markdown("---")
    
    # 푸터
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>Made with ❤️ using Streamlit + Gemini AI + SQLite</p>
        <p>Data Source: <a href="https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset" target="_blank">Kaggle Spotify Tracks Dataset</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

