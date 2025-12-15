"""
Spotify 데이터셋 다운로드 가이드 및 검증 스크립트
"""
import os
from pathlib import Path


def check_data_file():
    """데이터 파일 존재 여부 확인"""
    project_root = Path(__file__).parent.parent
    data_file = project_root / "data" / "raw" / "dataset.csv"
    
    print("=" * 60)
    print("Spotify Tracks Dataset 다운로드 가이드")
    print("=" * 60)
    
    if data_file.exists():
        print(f"\n✅ 데이터 파일을 찾았습니다: {data_file}")
        
        # 파일 크기 확인
        file_size = os.path.getsize(data_file) / (1024 * 1024)  # MB
        print(f"   파일 크기: {file_size:.2f} MB")
        
        # 간단한 검증
        try:
            import pandas as pd
            df = pd.read_csv(data_file, nrows=5)
            print(f"   행 수 (샘플): {len(df)}")
            print(f"   컬럼 수: {len(df.columns)}")
            print(f"   컬럼: {df.columns.tolist()[:5]}...")
            
            print("\n✅ 데이터 파일이 정상적으로 로드됩니다.")
            print("\n다음 단계를 진행하세요:")
            print("1. python scripts/preprocess_data.py")
            print("2. python scripts/build_database.py")
            
        except Exception as e:
            print(f"\n⚠️  파일 검증 중 오류 발생: {e}")
            print("   파일이 손상되었을 수 있습니다. 다시 다운로드하세요.")
    
    else:
        print(f"\n❌ 데이터 파일을 찾을 수 없습니다: {data_file}")
        print("\n다운로드 방법:")
        print("-" * 60)
        print("1. Kaggle 웹사이트 방문:")
        print("   https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset")
        print("\n2. 'Download' 버튼 클릭하여 dataset.csv 다운로드")
        print("\n3. 다운로드한 파일을 다음 경로에 저장:")
        print(f"   {data_file.parent}")
        print("\n또는 Kaggle API 사용:")
        print("-" * 60)
        print("pip install kaggle")
        print("kaggle datasets download -d maharshipandya/-spotify-tracks-dataset")
        print(f"unzip -o spotify-tracks-dataset.zip -d {data_file.parent}")
        print("-" * 60)
        
        # 폴더 생성
        data_file.parent.mkdir(parents=True, exist_ok=True)
        print(f"\n📁 폴더가 생성되었습니다: {data_file.parent}")


if __name__ == "__main__":
    check_data_file()

