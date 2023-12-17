## chatGPT study helper web service

사용자별 chatGPT 답변 자동 카테고리 생성 및 분류 서비스

#### 📌 개발기간
2023.3 ~ 2023.12

#### 📌 개발환경
- NLP: python, hugging face, scikit-learn
- Web Backend: django
- Web Frontend: HTML, CSS, JS
- Chrome Extension: JS
- Database: Sqlite3
- Collaboration: Github, Figma, Notion

#### 📌 팀원 역할
- @NurulhudaAminuddin: Web Frontend
- @oh-bom: Web Backend, Chrome Extension
- @syi07030: NLP, Web Backend

#### 📌 시스템 플로우
<img width="612" alt="스크린샷 2023-12-17 오후 12 35 27" src="https://github.com/3H-GPT-HELPER/web/assets/58241963/b9553ff4-beaa-4d7d-98ba-9293f27e2837">


#### 📌 주요 기능
- Chrome Extension
    - 실행 시 chatGPT 각 답변마다 체크 버튼 생성
    - 사용자가 스크랩을 원하는 Q&A 답변 클릭하면 서버로 해당 데이터 전달
- chatGPT study helper server
    - 데이터 전처리
    - 토픽 모델링: LDA
    - 의미론적 유사도 분석: PromCSE
- chatGPT study helper web site
    - 사용자가 스크랩한 답변들의 메인/서브 카테고리 생성
    - 메인->서브 카테고리 진입 통해 분류된 답변 내용 확인 가능
    - 카테고리 추가, 삭제 기능
 

#### 📌 기대효과
- 가독성: 많은 질문들 중 사용자에게 유용한 Q&A 목록만 정리
- 편리성: 자동으로 질문이 속하는 카테고리로 분류
- 시간 절약: 한 눈에 정리되어 있어 원하는 내용 찾는 시간 절약
