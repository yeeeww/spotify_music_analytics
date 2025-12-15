"""
데이터 탐색 페이지
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# 모듈 경로 추가
sys.path.append(str(Path(__file__).parent.parent))

from modules.database import DatabaseManager
from modules.visualization import create_bar_chart, create_histogram, create_box_plot

# 페이지 설정
st.set_page_config(
    page_title="데이터 탐색 - Spotify Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 데이터 탐색")
st.markdown("데이터베이스의 구조와 내용을 탐색합니다.")

# 데이터베이스 연결
db_path = Path("data/spotify.db")

if not db_path.exists():
    st.error("❌ 데이터베이스 파일을 찾을 수 없습니다. 먼저 데이터베이스를 구축하세요.")
    st.info("메인 페이지에서 데이터베이스 설정 방법을 확인하세요.")
    st.stop()

db = DatabaseManager(str(db_path))

# 사이드바 - 테이블 선택
st.sidebar.header("테이블 선택")
tables = db.get_table_names()
selected_table = st.sidebar.selectbox("테이블", tables, index=0)

# 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["📋 데이터 미리보기", "🔍 스키마 정보", "📊 기본 통계", "📈 시각화"])

# 탭 1: 데이터 미리보기
with tab1:
    st.subheader(f"📋 {selected_table} 테이블 미리보기")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 행 수 선택
        row_count = st.slider("표시할 행 수", min_value=5, max_value=100, value=10, step=5)
    
    with col2:
        # 전체 행 수
        total_rows = db.get_table_count(selected_table)
        st.metric("전체 행 수", f"{total_rows:,}")
    
    # 데이터 로드
    try:
        df = db.get_table_sample(selected_table, limit=row_count)
        
        # 데이터 표시
        st.dataframe(df, use_container_width=True, height=400)
        
        # 다운로드 버튼
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 CSV 다운로드",
            data=csv,
            file_name=f"{selected_table}_sample.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")

# 탭 2: 스키마 정보
with tab2:
    st.subheader(f"🔍 {selected_table} 테이블 스키마")
    
    try:
        schema_df = db.get_table_schema(selected_table)
        
        # 스키마 정보를 보기 좋게 표시
        schema_display = schema_df[['name', 'type', 'notnull', 'pk']].copy()
        schema_display.columns = ['컬럼명', '데이터 타입', 'NOT NULL', 'PRIMARY KEY']
        schema_display['NOT NULL'] = schema_display['NOT NULL'].map({0: '❌', 1: '✅'})
        schema_display['PRIMARY KEY'] = schema_display['PRIMARY KEY'].map({0: '❌', 1: '✅'})
        
        st.dataframe(schema_display, use_container_width=True, height=400)
        
        # 컬럼 설명 (tracks 테이블인 경우)
        if selected_table == 'tracks':
            st.markdown("---")
            st.subheader("📖 주요 컬럼 설명")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **기본 정보**
                - `track_id`: 트랙 고유 ID
                - `track_name`: 곡 제목
                - `artists`: 아티스트명
                - `album_name`: 앨범명
                - `track_genre`: 장르
                - `popularity`: 인기도 (0-100)
                - `duration_ms`: 재생 시간 (밀리초)
                """)
            
            with col2:
                st.markdown("""
                **음악 특성**
                - `danceability`: 댄스 적합도 (0.0-1.0)
                - `energy`: 에너지 (0.0-1.0)
                - `tempo`: BPM (템포)
                - `valence`: 긍정적 분위기 (0.0-1.0)
                - `acousticness`: 어쿠스틱 정도 (0.0-1.0)
                - `instrumentalness`: 보컬 없는 정도 (0.0-1.0)
                - `speechiness`: 음성 포함 정도 (0.0-1.0)
                - `liveness`: 라이브 녹음 정도 (0.0-1.0)
                """)
        
    except Exception as e:
        st.error(f"스키마 로드 실패: {e}")

# 탭 3: 기본 통계
with tab3:
    st.subheader(f"📊 {selected_table} 테이블 기본 통계")
    
    try:
        # 전체 데이터 로드 (통계용)
        query = f"SELECT * FROM {selected_table}"
        df = db.execute_query(query)
        
        # 숫자형 컬럼 통계
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        if numeric_cols:
            st.markdown("### 숫자형 컬럼 통계")
            
            # 통계 선택
            selected_cols = st.multiselect(
                "통계를 볼 컬럼 선택",
                numeric_cols,
                default=numeric_cols[:5] if len(numeric_cols) >= 5 else numeric_cols
            )
            
            if selected_cols:
                stats_df = df[selected_cols].describe().T
                stats_df = stats_df.round(2)
                st.dataframe(stats_df, use_container_width=True)
        
        # 문자형 컬럼 통계
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if text_cols:
            st.markdown("### 문자형 컬럼 통계")
            
            selected_text_col = st.selectbox("컬럼 선택", text_cols)
            
            if selected_text_col:
                col1, col2 = st.columns(2)
                
                with col1:
                    unique_count = df[selected_text_col].nunique()
                    st.metric("고유 값 개수", f"{unique_count:,}")
                
                with col2:
                    null_count = df[selected_text_col].isnull().sum()
                    st.metric("결측치 개수", f"{null_count:,}")
                
                # 빈도수 TOP 10
                st.markdown(f"#### {selected_text_col} 빈도수 TOP 10")
                value_counts = df[selected_text_col].value_counts().head(10)
                value_counts_df = pd.DataFrame({
                    selected_text_col: value_counts.index,
                    '개수': value_counts.values
                })
                
                st.dataframe(value_counts_df, use_container_width=True)
                
                # 막대 그래프
                fig = create_bar_chart(value_counts_df, selected_text_col, '개수',
                                      title=f"{selected_text_col} 빈도수 TOP 10")
                st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"통계 계산 실패: {e}")

# 탭 4: 시각화
with tab4:
    st.subheader(f"📈 {selected_table} 테이블 시각화")
    
    try:
        # 전체 데이터 로드
        query = f"SELECT * FROM {selected_table} LIMIT 1000"
        df = db.execute_query(query)
        
        st.info("💡 성능을 위해 최대 1,000개 행만 시각화합니다.")
        
        # 시각화 타입 선택
        viz_type = st.selectbox(
            "시각화 타입",
            ["히스토그램", "박스 플롯", "막대 그래프"]
        )
        
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if viz_type == "히스토그램":
            if numeric_cols:
                col = st.selectbox("컬럼 선택", numeric_cols)
                nbins = st.slider("구간 수", min_value=10, max_value=100, value=30)
                
                fig = create_histogram(df, col, title=f"{col} 분포", nbins=nbins)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("숫자형 컬럼이 없습니다.")
        
        elif viz_type == "박스 플롯":
            if numeric_cols:
                col1, col2 = st.columns(2)
                
                with col1:
                    y_col = st.selectbox("Y축 (숫자)", numeric_cols)
                
                with col2:
                    x_col = st.selectbox("X축 (카테고리, 선택사항)", ["없음"] + text_cols)
                
                x_val = None if x_col == "없음" else x_col
                
                fig = create_box_plot(df, x_val, y_col, title=f"{y_col} 박스 플롯")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("숫자형 컬럼이 없습니다.")
        
        elif viz_type == "막대 그래프":
            if text_cols and numeric_cols:
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("X축 (카테고리)", text_cols)
                
                with col2:
                    y_col = st.selectbox("Y축 (숫자)", numeric_cols)
                
                # 데이터 집계
                agg_df = df.groupby(x_col)[y_col].mean().reset_index()
                agg_df = agg_df.nlargest(20, y_col)
                
                fig = create_bar_chart(agg_df, x_col, y_col,
                                      title=f"{x_col}별 평균 {y_col} (TOP 20)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("적절한 컬럼이 없습니다.")
        
    except Exception as e:
        st.error(f"시각화 생성 실패: {e}")

# 데이터베이스 연결 종료
db.close()

