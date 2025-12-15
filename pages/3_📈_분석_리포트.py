"""
분석 리포트 페이지
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys
from datetime import datetime

# 모듈 경로 추가
sys.path.append(str(Path(__file__).parent.parent))

from modules.database import DatabaseManager
from modules.llm import GeminiLLM
from modules.visualization import (
    create_bar_chart, create_histogram, create_box_plot,
    create_scatter_plot, create_heatmap, create_pie_chart
)

# 페이지 설정
st.set_page_config(
    page_title="분석 리포트 - Spotify Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 분석 리포트")
st.markdown("데이터에 대한 종합적인 분석 리포트를 생성합니다.")

# 데이터베이스 연결
db_path = Path("data/spotify.db")

if not db_path.exists():
    st.error("❌ 데이터베이스 파일을 찾을 수 없습니다.")
    st.stop()

db = DatabaseManager(str(db_path))

# 세션 상태 초기화
if 'llm' not in st.session_state:
    try:
        st.session_state.llm = GeminiLLM()
    except ValueError as e:
        st.error(f"❌ {e}")
        st.info("💡 `.env` 파일에 `GEMINI_API_KEY`를 설정하세요.")
        st.stop()

llm = st.session_state.llm

# 사이드바 - 리포트 타입 선택
st.sidebar.header("📋 리포트 설정")

report_type = st.sidebar.selectbox(
    "리포트 타입",
    ["전체 데이터 개요", "장르 분석", "음악 특성 분석", "인기도 분석", "커스텀 분석"]
)

# 메인 영역
if report_type == "전체 데이터 개요":
    st.header("📊 전체 데이터 개요")
    
    with st.spinner("데이터를 분석하고 있습니다..."):
        try:
            # 기본 통계
            query = "SELECT COUNT(*) as total_tracks FROM tracks"
            total_tracks = db.execute_query(query)['total_tracks'][0]
            
            query = "SELECT COUNT(DISTINCT artists) as total_artists FROM tracks"
            total_artists = db.execute_query(query)['total_artists'][0]
            
            query = "SELECT COUNT(DISTINCT track_genre) as total_genres FROM tracks"
            total_genres = db.execute_query(query)['total_genres'][0]
            
            # 메트릭 표시
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("총 트랙 수", f"{total_tracks:,}")
            
            with col2:
                st.metric("총 아티스트 수", f"{total_artists:,}")
            
            with col3:
                st.metric("총 장르 수", f"{total_genres:,}")
            
            st.markdown("---")
            
            # 인기도 분포
            st.subheader("🎯 인기도 분포")
            query = "SELECT popularity FROM tracks WHERE popularity IS NOT NULL"
            popularity_df = db.execute_query(query)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_histogram(popularity_df, 'popularity', 
                                      title="인기도 분포", nbins=50)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # 인기도 통계
                st.markdown("#### 통계")
                stats = popularity_df['popularity'].describe()
                stats_df = pd.DataFrame({
                    '통계': ['평균', '표준편차', '최소값', '25%', '중앙값', '75%', '최대값'],
                    '값': [
                        f"{stats['mean']:.2f}",
                        f"{stats['std']:.2f}",
                        f"{stats['min']:.0f}",
                        f"{stats['25%']:.0f}",
                        f"{stats['50%']:.0f}",
                        f"{stats['75%']:.0f}",
                        f"{stats['max']:.0f}"
                    ]
                })
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # 음악 특성 분포
            st.subheader("🎵 음악 특성 분포")
            
            features = ['danceability', 'energy', 'valence', 'acousticness', 
                       'instrumentalness', 'speechiness']
            
            query = f"SELECT {', '.join(features)} FROM tracks LIMIT 10000"
            features_df = db.execute_query(query)
            
            # 박스 플롯
            fig = create_box_plot(features_df.melt(var_name='특성', value_name='값'),
                                 '특성', '값', title="음악 특성 분포")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # 상관관계 분석
            st.subheader("🔗 음악 특성 상관관계")
            
            query = """
            SELECT danceability, energy, valence, acousticness, 
                   instrumentalness, speechiness, tempo, loudness
            FROM tracks 
            LIMIT 5000
            """
            corr_df = db.execute_query(query)
            
            fig = create_heatmap(corr_df, title="음악 특성 상관관계")
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")

elif report_type == "장르 분석":
    st.header("🎸 장르 분석")
    
    with st.spinner("장르 데이터를 분석하고 있습니다..."):
        try:
            # 장르별 트랙 수
            st.subheader("📊 장르별 트랙 수 TOP 20")
            
            query = """
            SELECT track_genre, COUNT(*) as count
            FROM tracks
            GROUP BY track_genre
            ORDER BY count DESC
            LIMIT 20
            """
            genre_count_df = db.execute_query(query)
            
            fig = create_bar_chart(genre_count_df, 'track_genre', 'count',
                                  title="장르별 트랙 수 TOP 20")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # 장르별 평균 인기도
            st.subheader("⭐ 장르별 평균 인기도 TOP 20")
            
            query = """
            SELECT track_genre, AVG(popularity) as avg_popularity, COUNT(*) as count
            FROM tracks
            GROUP BY track_genre
            HAVING count >= 100
            ORDER BY avg_popularity DESC
            LIMIT 20
            """
            genre_pop_df = db.execute_query(query)
            
            fig = create_bar_chart(genre_pop_df, 'track_genre', 'avg_popularity',
                                  title="장르별 평균 인기도 TOP 20 (100곡 이상)")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # 장르별 음악 특성
            st.subheader("🎵 장르별 음악 특성")
            
            # 특정 장르 선택
            genres = db.execute_query("SELECT DISTINCT track_genre FROM tracks ORDER BY track_genre")['track_genre'].tolist()
            selected_genres = st.multiselect(
                "비교할 장르 선택 (최대 5개)",
                genres,
                default=genres[:5] if len(genres) >= 5 else genres
            )
            
            if selected_genres:
                genre_filter = "', '".join(selected_genres)
                query = f"""
                SELECT track_genre,
                       AVG(danceability) as avg_danceability,
                       AVG(energy) as avg_energy,
                       AVG(valence) as avg_valence,
                       AVG(tempo) as avg_tempo,
                       AVG(acousticness) as avg_acousticness
                FROM tracks
                WHERE track_genre IN ('{genre_filter}')
                GROUP BY track_genre
                """
                genre_features_df = db.execute_query(query)
                
                # 데이터 표시
                st.dataframe(genre_features_df.round(3), use_container_width=True, hide_index=True)
                
                # 막대 그래프
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = create_bar_chart(genre_features_df, 'track_genre', 'avg_danceability',
                                          title="장르별 평균 댄스 지수")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = create_bar_chart(genre_features_df, 'track_genre', 'avg_energy',
                                          title="장르별 평균 에너지")
                    st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")

elif report_type == "음악 특성 분석":
    st.header("🎼 음악 특성 분석")
    
    with st.spinner("음악 특성을 분석하고 있습니다..."):
        try:
            # 특성 선택
            feature = st.selectbox(
                "분석할 특성 선택",
                ['danceability', 'energy', 'valence', 'tempo', 'acousticness',
                 'instrumentalness', 'speechiness', 'liveness', 'loudness']
            )
            
            feature_names = {
                'danceability': '댄스 적합도',
                'energy': '에너지',
                'valence': '긍정도',
                'tempo': '템포 (BPM)',
                'acousticness': '어쿠스틱',
                'instrumentalness': '악기 연주',
                'speechiness': '음성 포함',
                'liveness': '라이브 녹음',
                'loudness': '음량 (dB)'
            }
            
            st.subheader(f"📊 {feature_names[feature]} 분석")
            
            # 데이터 로드
            query = f"SELECT {feature}, popularity, track_genre FROM tracks WHERE {feature} IS NOT NULL LIMIT 10000"
            feature_df = db.execute_query(query)
            
            # 분포
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_histogram(feature_df, feature, 
                                      title=f"{feature_names[feature]} 분포")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_box_plot(feature_df, None, feature,
                                     title=f"{feature_names[feature]} 박스 플롯")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # 인기도와의 관계
            st.subheader(f"⭐ {feature_names[feature]}와 인기도의 관계")
            
            fig = create_scatter_plot(feature_df.sample(min(1000, len(feature_df))),
                                     feature, 'popularity',
                                     title=f"{feature_names[feature]} vs 인기도",
                                     color='track_genre')
            st.plotly_chart(fig, use_container_width=True)
            
            # 상관계수
            correlation = feature_df[[feature, 'popularity']].corr().iloc[0, 1]
            st.metric("상관계수", f"{correlation:.3f}")
            
            if abs(correlation) > 0.3:
                st.success(f"✅ {feature_names[feature]}와 인기도 사이에 {'양의' if correlation > 0 else '음의'} 상관관계가 있습니다.")
            else:
                st.info(f"ℹ️ {feature_names[feature]}와 인기도 사이에 뚜렷한 상관관계가 없습니다.")
            
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")

elif report_type == "인기도 분석":
    st.header("⭐ 인기도 분석")
    
    with st.spinner("인기도 데이터를 분석하고 있습니다..."):
        try:
            # 인기도 구간별 분석
            st.subheader("📊 인기도 구간별 트랙 수")
            
            query = """
            SELECT 
                CASE 
                    WHEN popularity >= 80 THEN 'Very High (80-100)'
                    WHEN popularity >= 60 THEN 'High (60-79)'
                    WHEN popularity >= 40 THEN 'Medium (40-59)'
                    WHEN popularity >= 20 THEN 'Low (20-39)'
                    ELSE 'Very Low (0-19)'
                END as popularity_range,
                COUNT(*) as count
            FROM tracks
            GROUP BY popularity_range
            ORDER BY 
                CASE 
                    WHEN popularity >= 80 THEN 1
                    WHEN popularity >= 60 THEN 2
                    WHEN popularity >= 40 THEN 3
                    WHEN popularity >= 20 THEN 4
                    ELSE 5
                END
            """
            pop_range_df = db.execute_query(query)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_bar_chart(pop_range_df, 'popularity_range', 'count',
                                      title="인기도 구간별 트랙 수")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_pie_chart(pop_range_df, 'popularity_range', 'count',
                                      title="인기도 구간 비율")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # 인기 곡 TOP 20
            st.subheader("🏆 인기 곡 TOP 20")
            
            query = """
            SELECT track_name, artists, popularity, danceability, energy
            FROM tracks
            ORDER BY popularity DESC
            LIMIT 20
            """
            top_tracks_df = db.execute_query(query)
            
            st.dataframe(top_tracks_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # 인기도 구간별 음악 특성
            st.subheader("🎵 인기도 구간별 평균 음악 특성")
            
            query = """
            SELECT 
                CASE 
                    WHEN popularity >= 80 THEN 'Very High'
                    WHEN popularity >= 60 THEN 'High'
                    WHEN popularity >= 40 THEN 'Medium'
                    WHEN popularity >= 20 THEN 'Low'
                    ELSE 'Very Low'
                END as popularity_range,
                AVG(danceability) as avg_danceability,
                AVG(energy) as avg_energy,
                AVG(valence) as avg_valence,
                AVG(tempo) as avg_tempo
            FROM tracks
            GROUP BY popularity_range
            ORDER BY 
                CASE 
                    WHEN popularity >= 80 THEN 1
                    WHEN popularity >= 60 THEN 2
                    WHEN popularity >= 40 THEN 3
                    WHEN popularity >= 20 THEN 4
                    ELSE 5
                END
            """
            pop_features_df = db.execute_query(query)
            
            st.dataframe(pop_features_df.round(3), use_container_width=True, hide_index=True)
            
            # 시각화
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_bar_chart(pop_features_df, 'popularity_range', 'avg_danceability',
                                      title="인기도별 평균 댄스 지수")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_bar_chart(pop_features_df, 'popularity_range', 'avg_energy',
                                      title="인기도별 평균 에너지")
                st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")

elif report_type == "커스텀 분석":
    st.header("🔧 커스텀 분석")
    
    st.markdown("원하는 분석을 자유롭게 설정하세요.")
    
    # 분석 설정
    col1, col2 = st.columns(2)
    
    with col1:
        # X축 선택
        x_type = st.selectbox("X축 타입", ["카테고리", "숫자"])
        
        if x_type == "카테고리":
            x_col = st.selectbox("X축 컬럼", ['track_genre', 'artists', 'album_name'])
        else:
            x_col = st.selectbox("X축 컬럼", 
                               ['popularity', 'danceability', 'energy', 'tempo', 
                                'valence', 'acousticness'])
    
    with col2:
        # Y축 선택
        y_col = st.selectbox("Y축 컬럼",
                           ['popularity', 'danceability', 'energy', 'tempo',
                            'valence', 'acousticness', 'duration_ms'])
    
    # 차트 타입
    if x_type == "카테고리":
        chart_type = st.selectbox("차트 타입", ["막대 그래프", "박스 플롯"])
    else:
        chart_type = st.selectbox("차트 타입", ["산점도", "히스토그램"])
    
    # 필터
    with st.expander("🔍 필터 설정 (선택사항)"):
        use_filter = st.checkbox("필터 사용")
        
        if use_filter:
            filter_col = st.selectbox("필터 컬럼", ['track_genre', 'popularity'])
            
            if filter_col == 'track_genre':
                genres = db.execute_query("SELECT DISTINCT track_genre FROM tracks ORDER BY track_genre")['track_genre'].tolist()
                filter_values = st.multiselect("장르 선택", genres, default=genres[:5])
                # f-string 내에서 백슬래시를 사용할 수 없으므로 먼저 join
                joined_genres = "', '".join(filter_values)
                filter_condition = f"track_genre IN ('{joined_genres}')"
            else:
                min_pop = st.slider("최소 인기도", 0, 100, 0)
                filter_condition = f"popularity >= {min_pop}"
        else:
            filter_condition = "1=1"
    
    # 분석 실행
    if st.button("📊 분석 실행", type="primary"):
        with st.spinner("분석 중..."):
            try:
                if x_type == "카테고리":
                    # 집계 쿼리
                    query = f"""
                    SELECT {x_col}, AVG({y_col}) as avg_{y_col}, COUNT(*) as count
                    FROM tracks
                    WHERE {filter_condition} AND {x_col} IS NOT NULL AND {y_col} IS NOT NULL
                    GROUP BY {x_col}
                    ORDER BY avg_{y_col} DESC
                    LIMIT 20
                    """
                    df = db.execute_query(query)
                    
                    if chart_type == "막대 그래프":
                        fig = create_bar_chart(df, x_col, f'avg_{y_col}',
                                              title=f"{x_col}별 평균 {y_col}")
                    else:
                        # 박스 플롯용 원본 데이터
                        query = f"""
                        SELECT {x_col}, {y_col}
                        FROM tracks
                        WHERE {filter_condition} AND {x_col} IS NOT NULL AND {y_col} IS NOT NULL
                        LIMIT 5000
                        """
                        df = db.execute_query(query)
                        fig = create_box_plot(df, x_col, y_col,
                                             title=f"{x_col}별 {y_col} 분포")
                
                else:
                    # 숫자형 데이터
                    query = f"""
                    SELECT {x_col}, {y_col}
                    FROM tracks
                    WHERE {filter_condition} AND {x_col} IS NOT NULL AND {y_col} IS NOT NULL
                    LIMIT 5000
                    """
                    df = db.execute_query(query)
                    
                    if chart_type == "산점도":
                        fig = create_scatter_plot(df, x_col, y_col,
                                                 title=f"{x_col} vs {y_col}")
                    else:
                        fig = create_histogram(df, x_col, title=f"{x_col} 분포")
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 데이터 테이블
                st.markdown("### 📋 데이터")
                st.dataframe(df, use_container_width=True)
                
                # AI 분석
                if st.checkbox("🤖 AI 분석 받기"):
                    with st.spinner("AI가 분석하고 있습니다..."):
                        analysis = llm.analyze_results(
                            f"{x_col}와 {y_col}의 관계 분석",
                            query,
                            df
                        )
                        st.markdown("### 🤖 AI 분석")
                        st.markdown(analysis)
                
            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")

# 리포트 다운로드
st.sidebar.markdown("---")
st.sidebar.subheader("📥 리포트 다운로드")

if st.sidebar.button("📄 리포트 생성"):
    with st.spinner("리포트를 생성하고 있습니다..."):
        try:
            # 간단한 마크다운 리포트 생성
            report_content = f"""# Spotify Music Analytics 리포트

생성 날짜: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 리포트 타입: {report_type}

---

*이 리포트는 Spotify Music Analytics에서 자동 생성되었습니다.*
"""
            
            st.sidebar.download_button(
                label="📥 마크다운 다운로드",
                data=report_content,
                file_name=f"spotify_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
            
            st.sidebar.success("✅ 리포트가 생성되었습니다!")
            
        except Exception as e:
            st.sidebar.error(f"리포트 생성 실패: {e}")

# 데이터베이스 연결 종료
db.close()

