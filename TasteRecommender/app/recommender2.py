from sentence_transformers import SentenceTransformer, util
from .models import recipes

# 한국어 SBERT 모델 로드 (HuggingFace 허브에서 불러옴)
model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")

# 사용자 입력
user_input = "가볍고 단백질 많은 음식 뭐 있을까?"

# 사전 정의한 목적 후보
labels = ["식단관리", "간식", "고단백", "영양 보충", "단백질 보충", "한식", "채식", "즉석식품", "명절음식"]

# # 1. 사용자 입력과 목적들을 임베딩
# input_embedding = model.encode(user_input, convert_to_tensor=True)
# label_embeddings = model.encode(labels, convert_to_tensor=True)

# # 2. 유사도 계산
# cosine_scores = util.cos_sim(input_embedding, label_embeddings)

# # 3. 가장 유사한 목적 선택
# best_match_index = cosine_scores.argmax()
# predicted_purpose = labels[best_match_index]
# score = cosine_scores[0][best_match_index].item()

# print(f"🔍 예측된 목적: {predicted_purpose} (유사도: {score:.4f})")

# # 4. 레시피 추천
# recommended = [r for r in recipes if r['목적'] == predicted_purpose]

# # 5. 결과 출력
# print("\n🍽 추천 레시피:")
# if recommended:
#     for r in recommended:
#         print(f"- {r['음식명']}")
# else:
#     print("추천할 레시피가 없습니다.")

def recommend_by_input(user_input, threshold=0.35):
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    label_embeddings = model.encode(labels, convert_to_tensor=True)

    cosine_scores = util.cos_sim(input_embedding, label_embeddings)
    best_index = cosine_scores.argmax()
    predicted_purpose = labels[best_index]
    best_score = cosine_scores[0][best_index].item()

    if best_score < threshold:
        return None, []

    recommended = [r for r in recipes if r['목적'] == predicted_purpose]
    return predicted_purpose, recommended