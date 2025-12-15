"""
Spotify 데이터셋 전처리 스크립트
"""
import pandas as pd
import os
from pathlib import Path


def preprocess_spotify_data(input_path: str, output_path: str):
    """
    Spotify 데이터셋 전처리
    
    Args:
        input_path: 원본 CSV 파일 경로
        output_path: 전처리된 CSV 파일 저장 경로
    """
    print("데이터 로딩 중...")
    df = pd.read_csv(input_path)
    
    print(f"원본 데이터 크기: {df.shape}")
    print(f"컬럼: {df.columns.tolist()}")
    
    # 1. 중복 제거
    print("\n중복 제거 중...")
    before_dup = len(df)
    df = df.drop_duplicates(subset=['track_id'], keep='first')
    print(f"중복 제거: {before_dup - len(df)}개 행 제거")
    
    # 2. 결측치 처리
    print("\n결측치 확인...")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    # track_name, artists가 없는 행 제거
    df = df.dropna(subset=['track_name', 'artists'])
    
    # 숫자형 컬럼의 결측치는 중앙값으로 대체
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"{col}: 결측치를 중앙값({median_val})으로 대체")
    
    # 3. 데이터 타입 최적화
    print("\n데이터 타입 최적화 중...")
    
    # duration_ms를 초 단위로도 추가
    if 'duration_ms' in df.columns:
        df['duration_sec'] = (df['duration_ms'] / 1000).round(2)
    
    # 4. 이상치 제거 (선택적)
    print("\n이상치 확인...")
    
    # popularity는 0-100 범위
    if 'popularity' in df.columns:
        df = df[(df['popularity'] >= 0) & (df['popularity'] <= 100)]
    
    # 음악 특성은 0-1 범위 (일부 예외 있음)
    feature_cols = ['danceability', 'energy', 'speechiness', 'acousticness', 
                   'instrumentalness', 'liveness', 'valence']
    for col in feature_cols:
        if col in df.columns:
            df = df[(df[col] >= 0) & (df[col] <= 1)]
    
    # 5. 인덱스 리셋
    df = df.reset_index(drop=True)
    
    print(f"\n전처리 완료! 최종 데이터 크기: {df.shape}")
    
    # 저장
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"저장 완료: {output_path}")
    
    # 기본 통계
    print("\n=== 기본 통계 ===")
    print(f"총 트랙 수: {len(df):,}")
    print(f"고유 아티스트 수: {df['artists'].nunique():,}")
    if 'track_genre' in df.columns:
        print(f"고유 장르 수: {df['track_genre'].nunique():,}")
    if 'album_name' in df.columns:
        print(f"고유 앨범 수: {df['album_name'].nunique():,}")
    
    return df


if __name__ == "__main__":
    # 경로 설정
    project_root = Path(__file__).parent.parent
    input_file = project_root / "data" / "raw" / "dataset.csv"
    output_file = project_root / "data" / "processed" / "spotify_cleaned.csv"
    
    if not input_file.exists():
        print(f"오류: {input_file} 파일을 찾을 수 없습니다.")
        print("\nKaggle에서 데이터셋을 다운로드하세요:")
        print("https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset")
        print(f"\n다운로드한 dataset.csv 파일을 {input_file.parent} 폴더에 저장하세요.")
    else:
        preprocess_spotify_data(str(input_file), str(output_file))

