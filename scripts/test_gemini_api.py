"""
Gemini API 연결 및 사용 가능한 모델 확인 스크립트
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 환경 변수 로드
load_dotenv()

def test_gemini_api():
    """Gemini API 키 확인 및 사용 가능한 모델 출력"""
    
    # API 키 확인
    api_key = os.getenv("GEMINI_API_KEY")
    
    print("=" * 60)
    print("Gemini API 테스트")
    print("=" * 60)
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("\n❌ API 키가 설정되지 않았습니다!")
        print("\n해결 방법:")
        print("1. .env 파일을 열어주세요")
        print("2. GEMINI_API_KEY=실제_API_키 형식으로 입력")
        print("3. API 키 발급: https://aistudio.google.com/app/apikey")
        return
    
    print(f"\n✅ API 키 발견: {api_key[:10]}...{api_key[-4:]}")
    
    # API 설정
    try:
        genai.configure(api_key=api_key)
        print("✅ API 설정 완료")
    except Exception as e:
        print(f"❌ API 설정 실패: {e}")
        return
    
    # 사용 가능한 모델 목록
    print("\n📋 사용 가능한 모델 목록:")
    print("-" * 60)
    
    try:
        models = genai.list_models()
        
        text_generation_models = []
        for model in models:
            # generateContent를 지원하는 모델만 필터링
            if 'generateContent' in model.supported_generation_methods:
                text_generation_models.append(model.name)
                print(f"✅ {model.name}")
                print(f"   설명: {model.display_name}")
                print(f"   지원 메서드: {', '.join(model.supported_generation_methods)}")
                print()
        
        if not text_generation_models:
            print("❌ 사용 가능한 텍스트 생성 모델이 없습니다.")
            return
        
        print(f"\n총 {len(text_generation_models)}개의 텍스트 생성 모델 발견")
        
        # 첫 번째 모델로 테스트
        print("\n" + "=" * 60)
        print("모델 테스트")
        print("=" * 60)
        
        test_model_name = text_generation_models[0].replace('models/', '')
        print(f"\n테스트 모델: {test_model_name}")
        
        model = genai.GenerativeModel(test_model_name)
        response = model.generate_content("Hello! Please respond with 'API is working!'")
        
        print(f"\n✅ 테스트 성공!")
        print(f"응답: {response.text}")
        
        print("\n" + "=" * 60)
        print("권장 설정")
        print("=" * 60)
        print(f"\nmodules/llm.py 파일에서 다음 모델을 사용하세요:")
        print(f"self.model = genai.GenerativeModel('{test_model_name}')")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("\n문제 해결:")
        print("1. API 키가 유효한지 확인")
        print("2. 인터넷 연결 확인")
        print("3. google-generativeai 패키지 업데이트:")
        print("   pip install --upgrade google-generativeai")


if __name__ == "__main__":
    test_gemini_api()

