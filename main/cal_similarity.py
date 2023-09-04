#pip install promcse
#from promcse import PromCSE
import joblib
#from .views import extract_topic
from django.contrib.auth.models import User
from user.models import UserCategory

model = joblib.load('/Users/hgy/Desktop/hgy/EWHA/2023_1(4)/Final_project/3H/main/promcse_model.pkl')
#받은 쿼리와 기존의 토픽들 간 거리 비교
def cal_similarity(request, answer_str):
    THRESHOLD = 0.5
    userCategories=UserCategory.objects.filter(user_id__user_id=request.user.user_id)
    scores = [] #dictionary
    model.build_index(userCategories, use_faiss=False)
    results = model.search(answer_str)
    for i, result in enumerate(results):
        print("Retrieval results for query: {}".format(answer_str[i]))
        for sentence, score in result:
            print("    {}  (cosine similarity: {:.4f})".format(sentence, score))
            scores.add(score)
        print("")
    # 기존 category에 내용 추가
    if max(scores) >= THRESHOLD:
        category = results.index(max(scores))[0]
        return {'existed': category}
    # 새로운 category 생성
    else:
        return {'new': answer_str}