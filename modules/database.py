"""
데이터베이스 연결 및 쿼리 실행 모듈
"""
import sqlite3
import pandas as pd
from typing import Optional, List, Dict, Any
import os


class DatabaseManager:
    """SQLite 데이터베이스 관리 클래스"""
    
    def __init__(self, db_path: str = "data/spotify.db"):
        """
        Args:
            db_path: 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self.connection = None
        
    def connect(self) -> sqlite3.Connection:
        """데이터베이스 연결"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        return self.connection
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        SQL 쿼리 실행 및 결과 반환
        
        Args:
            query: 실행할 SQL 쿼리
            
        Returns:
            쿼리 결과를 담은 DataFrame
        """
        try:
            conn = self.connect()
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            raise Exception(f"쿼리 실행 오류: {str(e)}")
    
    def get_table_names(self) -> List[str]:
        """데이터베이스의 모든 테이블 이름 조회"""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        df = self.execute_query(query)
        return df['name'].tolist()
    
    def get_table_schema(self, table_name: str) -> pd.DataFrame:
        """
        테이블 스키마 정보 조회
        
        Args:
            table_name: 테이블 이름
            
        Returns:
            스키마 정보 DataFrame
        """
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def get_table_sample(self, table_name: str, limit: int = 5) -> pd.DataFrame:
        """
        테이블 샘플 데이터 조회
        
        Args:
            table_name: 테이블 이름
            limit: 조회할 행 수
            
        Returns:
            샘플 데이터 DataFrame
        """
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)
    
    def get_table_count(self, table_name: str) -> int:
        """
        테이블의 전체 행 수 조회
        
        Args:
            table_name: 테이블 이름
            
        Returns:
            전체 행 수
        """
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        df = self.execute_query(query)
        return int(df['count'].iloc[0])
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        데이터베이스 전체 정보 조회
        
        Returns:
            데이터베이스 정보 딕셔너리
        """
        tables = self.get_table_names()
        info = {
            'database_path': self.db_path,
            'database_size': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0,
            'tables': {}
        }
        
        for table in tables:
            info['tables'][table] = {
                'row_count': self.get_table_count(table),
                'schema': self.get_table_schema(table).to_dict('records')
            }
        
        return info
    
    def get_schema_for_llm(self) -> str:
        """
        LLM에게 제공할 스키마 정보를 문자열로 반환
        
        Returns:
            스키마 정보 문자열
        """
        tables = self.get_table_names()
        schema_text = "데이터베이스 스키마:\n\n"
        
        for table in tables:
            schema_df = self.get_table_schema(table)
            schema_text += f"테이블: {table}\n"
            schema_text += "컬럼:\n"
            
            for _, row in schema_df.iterrows():
                col_name = row['name']
                col_type = row['type']
                is_pk = " (PRIMARY KEY)" if row['pk'] == 1 else ""
                not_null = " NOT NULL" if row['notnull'] == 1 else ""
                schema_text += f"  - {col_name}: {col_type}{is_pk}{not_null}\n"
            
            schema_text += "\n"
        
        return schema_text
    
    def validate_query(self, query: str) -> tuple[bool, str]:
        """
        쿼리 유효성 검사 (읽기 전용)
        
        Args:
            query: 검사할 SQL 쿼리
            
        Returns:
            (유효성 여부, 오류 메시지)
        """
        # 위험한 키워드 체크
        dangerous_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE', 'TRUNCATE']
        query_upper = query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False, f"보안상 {keyword} 명령어는 사용할 수 없습니다."
        
        # 쿼리 실행 테스트
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            return True, "유효한 쿼리입니다."
        except Exception as e:
            return False, f"쿼리 오류: {str(e)}"

