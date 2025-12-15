"""
Gemini API 연동 모듈
"""
import google.generativeai as genai
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


class GeminiLLM:
    """Gemini API를 사용한 LLM 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: Gemini API 키 (None이면 환경변수에서 로드)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("Gemini API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
        
        # Gemini API 설정
        genai.configure(api_key=self.api_key)
        # 가장 가벼운 무료 모델 사용 (quota 절약)
        # gemini-flash-lite-latest: 빠르고 무료 한도가 넉넉함
        try:
            self.model = genai.GenerativeModel('gemini-flash-lite-latest')
        except:
            try:
                # 대안: gemini-2.0-flash-lite
                self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
            except:
                # 최종 대안
                self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def text_to_sql(self, question: str, schema: str) -> str:
        """
        자연어 질문을 SQL 쿼리로 변환
        
        Args:
            question: 사용자의 자연어 질문
            schema: 데이터베이스 스키마 정보
            
        Returns:
            생성된 SQL 쿼리
        """
        prompt = f"""당신은 SQL 전문가입니다. 사용자의 자연어 질문을 SQLite 쿼리로 변환해주세요.

{schema}

중요한 규칙:
1. SELECT 쿼리만 생성하세요 (INSERT, UPDATE, DELETE, DROP 등은 절대 사용 금지)
2. 쿼리는 반드시 실행 가능한 SQLite 문법을 따라야 합니다
3. 테이블과 컬럼 이름은 스키마에 있는 것만 사용하세요
4. 한국어 질문을 정확히 이해하고 적절한 SQL로 변환하세요
5. 필요한 경우 JOIN, GROUP BY, ORDER BY 등을 적절히 사용하세요
6. LIMIT를 사용하여 결과를 제한하는 것이 좋습니다 (기본 100개)
7. 키워드는 대문자로 작성하세요 (SELECT, FROM, WHERE, LIMIT 등)
8. 세미콜론(;)은 사용하지 마세요
9. 응답은 SQL 쿼리만 출력하세요 (설명이나 다른 텍스트, 코드 블록 없이)

사용자 질문: {question}

SQL 쿼리:"""

        try:
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            
            # 코드 블록 제거
            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            elif sql_query.startswith("```"):
                sql_query = sql_query[3:]
            
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]
            
            return sql_query.strip()
        
        except Exception as e:
            error_msg = str(e)
            
            # Quota 초과 에러 처리
            if "429" in error_msg or "quota" in error_msg.lower():
                raise Exception(
                    "⚠️ API 사용 한도를 초과했습니다.\n\n"
                    "해결 방법:\n"
                    "1. 새 API 키 발급: https://aistudio.google.com/app/apikey\n"
                    "2. .env 파일에 새 키 입력 후 앱 재시작\n"
                    "3. 또는 1시간 후 다시 시도\n\n"
                    f"상세 오류: {error_msg}"
                )
            
            # Rate limit 에러 처리
            if "rate" in error_msg.lower() and "limit" in error_msg.lower():
                raise Exception(
                    "⚠️ 요청 속도 제한에 걸렸습니다.\n\n"
                    "잠시 후 다시 시도해주세요 (약 1분).\n\n"
                    f"상세 오류: {error_msg}"
                )
            
            # 기타 에러
            raise Exception(f"SQL 생성 오류: {error_msg}")
    
    def analyze_results(self, question: str, query: str, results_df) -> str:
        """
        쿼리 결과를 분석하고 인사이트 제공
        
        Args:
            question: 원래 질문
            query: 실행된 SQL 쿼리
            results_df: 쿼리 결과 DataFrame
            
        Returns:
            분석 결과 텍스트
        """
        # 결과 요약
        result_summary = f"총 {len(results_df)}개의 결과가 조회되었습니다.\n\n"
        
        if len(results_df) > 0:
            # 상위 5개 행만 포함
            result_preview = results_df.head(5).to_string()
        else:
            result_preview = "결과가 없습니다."
        
        prompt = f"""다음은 사용자의 질문과 그에 대한 SQL 쿼리 결과입니다.
결과를 분석하고 주요 인사이트를 한국어로 제공해주세요.

사용자 질문: {question}

실행된 SQL: {query}

결과 미리보기:
{result_preview}

다음 형식으로 분석해주세요:
1. 결과 요약 (간단히)
2. 주요 발견사항 (2-3개)
3. 추가 분석 제안 (있다면)

분석:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            return f"분석 생성 중 오류가 발생했습니다: {str(e)}"
    
    def suggest_visualization(self, results_df, question: str) -> Dict[str, Any]:
        """
        쿼리 결과에 적합한 시각화 방법 제안
        
        Args:
            results_df: 쿼리 결과 DataFrame
            question: 원래 질문
            
        Returns:
            시각화 제안 딕셔너리
        """
        if len(results_df) == 0:
            return {"type": "none", "message": "시각화할 데이터가 없습니다."}
        
        # 컬럼 정보
        columns = results_df.columns.tolist()
        dtypes = results_df.dtypes.to_dict()
        
        # 숫자형 컬럼과 문자형 컬럼 구분
        numeric_cols = [col for col, dtype in dtypes.items() if dtype in ['int64', 'float64']]
        text_cols = [col for col, dtype in dtypes.items() if dtype == 'object']
        
        # 기본 규칙 기반 제안
        if len(numeric_cols) >= 2:
            # 산점도 추천
            return {
                "type": "scatter",
                "x": numeric_cols[0],
                "y": numeric_cols[1],
                "title": f"{numeric_cols[0]} vs {numeric_cols[1]}"
            }
        elif len(text_cols) >= 1 and len(numeric_cols) >= 1:
            # 막대 그래프 추천
            return {
                "type": "bar",
                "x": text_cols[0],
                "y": numeric_cols[0],
                "title": f"{text_cols[0]}별 {numeric_cols[0]}"
            }
        elif len(numeric_cols) == 1:
            # 히스토그램 추천
            return {
                "type": "histogram",
                "x": numeric_cols[0],
                "title": f"{numeric_cols[0]} 분포"
            }
        else:
            return {
                "type": "table",
                "message": "테이블 형태로 표시하는 것이 적합합니다."
            }
    
    def generate_report(self, question: str, query: str, results_df, analysis: str) -> str:
        """
        전체 분석 리포트 생성
        
        Args:
            question: 원래 질문
            query: 실행된 SQL 쿼리
            results_df: 쿼리 결과 DataFrame
            analysis: 분석 결과
            
        Returns:
            마크다운 형식의 리포트
        """
        report = f"""# 데이터 분석 리포트

## 질문
{question}

## 실행된 쿼리
```sql
{query}
```

## 결과 요약
- 총 결과 수: {len(results_df)}개
- 컬럼 수: {len(results_df.columns)}개
- 컬럼 목록: {', '.join(results_df.columns.tolist())}

## 분석
{analysis}

## 데이터 미리보기
"""
        
        if len(results_df) > 0:
            report += results_df.head(10).to_markdown(index=False)
        else:
            report += "결과가 없습니다."
        
        report += "\n\n---\n*Generated by Spotify Music Analytics*"
        
        return report

