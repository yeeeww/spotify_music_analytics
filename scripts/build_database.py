"""
SQLite 데이터베이스 구축 스크립트
"""
import pandas as pd
import sqlite3
import os
from pathlib import Path


def create_database(csv_path: str, db_path: str):
    """
    전처리된 CSV 파일로부터 SQLite 데이터베이스 생성
    
    Args:
        csv_path: 전처리된 CSV 파일 경로
        db_path: 생성할 데이터베이스 파일 경로
    """
    print("데이터 로딩 중...")
    df = pd.read_csv(csv_path)
    
    print(f"데이터 크기: {df.shape}")
    print(f"컬럼: {df.columns.tolist()}")
    
    # 데이터베이스 연결
    print(f"\n데이터베이스 생성 중: {db_path}")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 기존 DB 파일이 있으면 삭제
    if os.path.exists(db_path):
        os.remove(db_path)
        print("기존 데이터베이스 삭제됨")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. tracks 테이블 생성 (메인 테이블)
    print("\ntracks 테이블 생성 중...")
    df.to_sql('tracks', conn, if_exists='replace', index=False)
    
    # 인덱스 생성 (성능 향상)
    print("인덱스 생성 중...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_track_id ON tracks(track_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_artists ON tracks(artists)")
    
    if 'track_genre' in df.columns:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_genre ON tracks(track_genre)")
    
    if 'popularity' in df.columns:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_popularity ON tracks(popularity)")
    
    conn.commit()
    
    # 2. genres 테이블 생성 (정규화)
    if 'track_genre' in df.columns:
        print("\ngenres 테이블 생성 중...")
        genres_df = df[['track_genre']].drop_duplicates().reset_index(drop=True)
        genres_df.columns = ['genre_name']
        genres_df.insert(0, 'genre_id', range(1, len(genres_df) + 1))
        genres_df.to_sql('genres', conn, if_exists='replace', index=False)
        print(f"총 {len(genres_df)}개 장르")
    
    # 3. artists 테이블 생성 (간단한 버전)
    print("\nartists 테이블 생성 중...")
    # 아티스트는 세미콜론으로 구분되어 있을 수 있음
    all_artists = []
    for artists_str in df['artists'].dropna().unique():
        # 세미콜론이나 쉼표로 구분된 경우 처리
        if ';' in str(artists_str):
            artist_list = [a.strip() for a in str(artists_str).split(';')]
        elif ',' in str(artists_str):
            artist_list = [a.strip() for a in str(artists_str).split(',')]
        else:
            artist_list = [str(artists_str).strip()]
        
        all_artists.extend(artist_list)
    
    unique_artists = sorted(set(all_artists))
    artists_df = pd.DataFrame({
        'artist_id': range(1, len(unique_artists) + 1),
        'artist_name': unique_artists
    })
    artists_df.to_sql('artists', conn, if_exists='replace', index=False)
    print(f"총 {len(artists_df)}개 아티스트")
    
    # 4. albums 테이블 생성
    if 'album_name' in df.columns:
        print("\nalbums 테이블 생성 중...")
        albums_df = df[['album_name']].drop_duplicates().reset_index(drop=True)
        albums_df.columns = ['album_name']
        albums_df.insert(0, 'album_id', range(1, len(albums_df) + 1))
        albums_df.to_sql('albums', conn, if_exists='replace', index=False)
        print(f"총 {len(albums_df)}개 앨범")
    
    # 5. 통계 뷰 생성
    print("\n통계 뷰 생성 중...")
    
    # 장르별 통계 뷰
    if 'track_genre' in df.columns:
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS genre_stats AS
        SELECT 
            track_genre,
            COUNT(*) as track_count,
            AVG(popularity) as avg_popularity,
            AVG(danceability) as avg_danceability,
            AVG(energy) as avg_energy,
            AVG(tempo) as avg_tempo,
            AVG(valence) as avg_valence
        FROM tracks
        GROUP BY track_genre
        ORDER BY track_count DESC
        """)
    
    # 인기도별 통계 뷰
    if 'popularity' in df.columns:
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS popularity_stats AS
        SELECT 
            CASE 
                WHEN popularity >= 80 THEN 'Very High (80-100)'
                WHEN popularity >= 60 THEN 'High (60-79)'
                WHEN popularity >= 40 THEN 'Medium (40-59)'
                WHEN popularity >= 20 THEN 'Low (20-39)'
                ELSE 'Very Low (0-19)'
            END as popularity_range,
            COUNT(*) as track_count,
            AVG(danceability) as avg_danceability,
            AVG(energy) as avg_energy
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
        """)
    
    conn.commit()
    
    # 데이터베이스 정보 출력
    print("\n=== 데이터베이스 생성 완료 ===")
    print(f"파일 경로: {db_path}")
    print(f"파일 크기: {os.path.getsize(db_path) / (1024*1024):.2f} MB")
    
    # 테이블 목록
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n생성된 테이블: {[t[0] for t in tables]}")
    
    # 각 테이블의 행 수
    print("\n테이블별 행 수:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]}: {count:,}개")
    
    # 뷰 목록
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
    views = cursor.fetchall()
    if views:
        print(f"\n생성된 뷰: {[v[0] for v in views]}")
    
    conn.close()
    print("\n데이터베이스 생성이 완료되었습니다!")


if __name__ == "__main__":
    # 경로 설정
    project_root = Path(__file__).parent.parent
    csv_file = project_root / "data" / "processed" / "spotify_cleaned.csv"
    db_file = project_root / "data" / "spotify.db"
    
    if not csv_file.exists():
        print(f"오류: {csv_file} 파일을 찾을 수 없습니다.")
        print("\n먼저 데이터 전처리를 실행하세요:")
        print("python scripts/preprocess_data.py")
    else:
        create_database(str(csv_file), str(db_file))

