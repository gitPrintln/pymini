from sentence_transformers import SentenceTransformer, util
from .models import recipes

# 한국어 SBERT 모델 로드 (HuggingFace 허브에서 불러옴)
model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")

# 사용자 입력
user_input = "가볍고 단백질 많은 음식 뭐 있을까?"

# 사전 정의한 목적 후보
labels = ["식단관리", "간식", "고단백", "영양 보충", "단백질 보충", "한식", "채식", "즉석식품", "명절음식"]


def recommend_by_input(user_input, threshold=0.3):
    # 입력 임베딩
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    # 목적 임베딩
    label_embeddings = model.encode(labels, convert_to_tensor=True)

    # 코사인 유사도 계산 (1 x N)
    cosine_scores = util.cos_sim(input_embedding, label_embeddings)[0]
    
    # 임계값 넘는 목적(라벨) 골라내기, (라벨, 점수) 튜플 리스트
    selected = [(labels[i], cosine_scores[i].item()) for i in range(len(labels)) if cosine_scores[i] > threshold]
    if not selected:
        return {}
    
    # 유사도 높은 순 정렬
    selected.sort(key=lambda x: x[1], reverse=True)
    best_purpose, best_score = selected[0]

    recommended = [r for r in recipes if r['목적'] == best_purpose]

    return best_purpose, recommended