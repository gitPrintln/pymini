# 음식/레시피 데이터 추천 함수
from transformers import pipeline

# 모델 준비
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# 사용자 입력
user_input = "가볍고 단백질 많은 음식 뭐 있을까?"

# 사전 정의한 목적 후보
labels = ["다이어트", "간식", "고단백", "스트레스 해소", "해장", "영양 보충"]

# 목적 예측
result = classifier(user_input, labels)

# 가장 가능성 높은 목적
predicted_purpose = result['labels'][0]
print(f"👉 예측된 목적: {predicted_purpose}")

# 사용자가 선호하는 재료와 각 레시피 간의 유사도 계산

# 선호도 상위 추천 함수

# 재추천 함수
