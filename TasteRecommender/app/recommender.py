# 음식/레시피 데이터 추천 함수
from transformers import pipeline
from .models import recipes

# 모델 준비
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# 사용자 입력
user_input = "가볍고 단백질 많은 음식 뭐 있을까?"

# 사전 정의한 목적 후보
labels = ["다이어트", "간식", "고단백", "영양 보충", "단백질 보충", "한식", "채식", "즉석식품", "명절음식"]

test_input = "가볍고 단백질 많은 음식 뭐 있을까?"
result = classifier(test_input, labels)
for label, score in zip(result['labels'], result['scores']):
    print(f"{label}: {score:.3f}")

# 목적 예측
def recommend_by_input(user_input):
    result = classifier(user_input, labels)
    best_score = result['scores'][0]
    predicted_purpose = result['labels'][0]

    # 신뢰도 임계값 (0.4는 임의 설정, 조정 가능)
    if best_score < 0.4:
        print("❗️적합한 추천 목적을 찾을 수 없습니다.")
        return None, []

    recommended = [r for r in recipes if predicted_purpose == r['목적']]
    return predicted_purpose, recommended

# 예시 실행
purpose, recommended_recipes = recommend_by_input(user_input)

# 가장 가능성 높은 목적
if purpose:
    print(f"👉 예측된 목적: {purpose}")
    print("\n🍽 추천 레시피:")
    if recommended_recipes:
        for r in recommended_recipes:
            print(f"- {r['음식명']}")
    else:
        print("추천할 레시피가 없습니다.")
else:
    print("입력에 맞는 추천 결과가 없습니다.")

# 레시피 필터링 (목적에 맞는 것만)
# recommended_recipes = [r for r in recipes if predicted_purpose in r['목적']]

# 결과 출력
print("\n🍽 추천 레시피:")
if recommended_recipes:
    for r in recommended_recipes:
        print(f"- {r['음식명']}")
else:
    print("추천할 레시피가 없습니다.")

# 사용자 입력함수
def recommend_by_input(user_input, threshold=0.05):
    result = classifier(user_input, labels)
    selected_labels = [label for label, score in zip(result['labels'], result['scores']) if score > threshold]
    print(f"Selected purposes by threshold {threshold}: {selected_labels}")
    best_score = result['scores'][0]
    predicted_purpose = result['labels'][0]

    # 신뢰도 임계값 설정 (예: 0.4)
    if best_score < 0.4:
        return None, []  # 신뢰도 낮으면 추천 없음 처리

    recommended = [r for r in recipes if predicted_purpose == r['목적'] in selected_labels]
    return predicted_purpose, recommended

# 사용자가 선호하는 재료와 각 레시피 간의 유사도 계산

# 선호도 상위 추천 함수

# 재추천 함수
