"""
자연어 질의 페이지
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# 모듈 경로 추가
sys.path.append(str(Path(__file__).parent.parent))

from modules.database import DatabaseManager
from modules.llm import GeminiLLM
from modules.visualization import auto_visualize

# 페이지 설정
st.set_page_config(
    page_title="자연어 질의 - Spotify Analytics",
    page_icon="💬",
    layout="wide"
)

st.title("💬 자연어 질의")
st.markdown("한국어로 질문하면 AI가 자동으로 SQL을 생성하고 결과를 보여줍니다.")

# 데이터베이스 연결
db_path = Path("data/spotify.db")

if not db_path.exists():
    st.error("❌ 데이터베이스 파일을 찾을 수 없습니다.")
    st.stop()

# 세션 상태 초기화
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

if 'llm' not in st.session_state:
    try:
        st.session_state.llm = GeminiLLM()
    except ValueError as e:
        st.error(f"❌ {e}")
        st.info("💡 `.env` 파일에 `GEMINI_API_KEY`를 설정하세요.")
        st.stop()

db = DatabaseManager(str(db_path))
llm = st.session_state.llm

# 사이드바 - 예시 질문
st.sidebar.header("💡 예시 질문")
example_questions = [
    "가장 인기 있는 장르 TOP 10은?",
    "댄스 지수가 0.8 이상인 곡은?",
    "장르별 평균 템포를 보여줘",
    "에너지가 높은 곡 TOP 20",
    "인기도가 80 이상인 곡의 평균 특성은?",
    "가장 긴 곡과 가장 짧은 곡은?",
    "장르별 곡 개수를 보여줘",
    "템포가 120 이상인 곡 중 인기 있는 곡은?",
    "어쿠스틱 지수가 높은 장르는?",
    "라이브 녹음 비율이 높은 곡들은?"
]

selected_example = st.sidebar.selectbox(
    "예시 선택",
    ["직접 입력"] + example_questions
)

# 메인 영역
st.markdown("### 질문 입력")

# 질문 입력
if selected_example == "직접 입력":
    question = st.text_area(
        "질문을 입력하세요",
        height=100,
        placeholder="예: 가장 인기 있는 장르 TOP 10은?"
    )
else:
    question = st.text_area(
        "질문을 입력하세요",
        value=selected_example,
        height=100
    )

col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    submit_button = st.button("🔍 질의 실행", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ 초기화", use_container_width=True)

if clear_button:
    st.session_state.query_history = []
    st.rerun()

# 질의 실행
if submit_button and question:
    with st.spinner("AI가 SQL을 생성하고 있습니다..."):
        try:
            # 1. 스키마 정보 가져오기
            schema = db.get_schema_for_llm()
            
            # 2. Text-to-SQL
            sql_query = llm.text_to_sql(question, schema)
            
            # 3. SQL 유효성 검사
            is_valid, message = db.validate_query(sql_query)
            
            if not is_valid:
                st.error(f"❌ 쿼리 유효성 검사 실패: {message}")
                st.code(sql_query, language="sql")
                st.stop()
            
            # 4. 쿼리 실행
            with st.spinner("쿼리를 실행하고 있습니다..."):
                results_df = db.execute_query(sql_query)
            
            # 5. 결과 분석
            with st.spinner("결과를 분석하고 있습니다..."):
                analysis = llm.analyze_results(question, sql_query, results_df)
            
            # 6. 히스토리에 추가
            st.session_state.query_history.insert(0, {
                'question': question,
                'sql': sql_query,
                'results': results_df,
                'analysis': analysis
            })
            
            st.success("✅ 질의가 성공적으로 실행되었습니다!")
            
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")
            st.stop()

# 결과 표시
if st.session_state.query_history:
    st.markdown("---")
    st.markdown("## 📊 결과")
    
    # 최신 결과 표시
    latest = st.session_state.query_history[0]
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs(["💬 분석", "📋 데이터", "📊 시각화", "🔍 SQL"])
    
    # 탭 1: AI 분석
    with tab1:
        st.markdown("### 🤖 AI 분석")
        st.markdown(latest['analysis'])
        
        # 기본 정보
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("결과 행 수", f"{len(latest['results']):,}")
        
        with col2:
            st.metric("컬럼 수", len(latest['results'].columns))
        
        with col3:
            if len(latest['results']) > 0:
                st.metric("데이터 크기", f"{latest['results'].memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # 탭 2: 데이터 테이블
    with tab2:
        st.markdown("### 📋 데이터 테이블")
        
        if len(latest['results']) > 0:
            # 페이지네이션
            page_size = st.selectbox("페이지당 행 수", [10, 25, 50, 100], index=1)
            total_pages = (len(latest['results']) - 1) // page_size + 1
            
            if total_pages > 1:
                page = st.slider("페이지", 1, total_pages, 1)
                start_idx = (page - 1) * page_size
                end_idx = start_idx + page_size
                display_df = latest['results'].iloc[start_idx:end_idx]
            else:
                display_df = latest['results']
            
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # 다운로드 버튼
            csv = latest['results'].to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 전체 결과 CSV 다운로드",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )
        else:
            st.info("결과가 없습니다.")
    
    # 탭 3: 시각화
    with tab3:
        st.markdown("### 📊 시각화")
        
        if len(latest['results']) > 0:
            try:
                fig = auto_visualize(latest['results'], latest['question'])
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"시각화 생성 실패: {e}")
                st.info("데이터를 테이블 형태로 확인하세요.")
        else:
            st.info("시각화할 데이터가 없습니다.")
    
    # 탭 4: SQL 쿼리
    with tab4:
        st.markdown("### 🔍 생성된 SQL 쿼리")
        st.code(latest['sql'], language="sql")
        
        # SQL 수정 및 재실행
        st.markdown("#### ✏️ SQL 수정 및 재실행")
        edited_sql = st.text_area(
            "SQL 쿼리를 수정할 수 있습니다",
            value=latest['sql'],
            height=150
        )
        
        if st.button("🔄 수정된 쿼리 실행"):
            try:
                # 유효성 검사
                is_valid, message = db.validate_query(edited_sql)
                
                if not is_valid:
                    st.error(f"❌ {message}")
                else:
                    # 쿼리 실행
                    new_results = db.execute_query(edited_sql)
                    
                    # 히스토리에 추가
                    st.session_state.query_history.insert(0, {
                        'question': latest['question'] + " (수정됨)",
                        'sql': edited_sql,
                        'results': new_results,
                        'analysis': "수정된 쿼리 결과입니다."
                    })
                    
                    st.success("✅ 쿼리가 성공적으로 실행되었습니다!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")
    
    # 히스토리
    if len(st.session_state.query_history) > 1:
        st.markdown("---")
        st.markdown("## 📜 질의 히스토리")
        
        for idx, item in enumerate(st.session_state.query_history[1:], 1):
            with st.expander(f"{idx}. {item['question'][:50]}..."):
                st.markdown(f"**질문:** {item['question']}")
                st.code(item['sql'], language="sql")
                st.markdown(f"**결과:** {len(item['results'])}개 행")

else:
    # 초기 화면
    st.info("💡 위에서 질문을 입력하거나 사이드바의 예시 질문을 선택하세요.")
    
    # 스키마 정보 표시
    with st.expander("📚 데이터베이스 스키마 보기"):
        schema = db.get_schema_for_llm()
        st.text(schema)

# 데이터베이스 연결 종료
db.close()

