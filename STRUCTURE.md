# 🗂 Project Structure

```text
c:\Workspaces\SKN22-3rd-4Team
├── .env                  # 환경 변수 파일
├── .gitignore
├── LICENSE
├── README.md             # 프로젝트 메인 문서
├── STRUCTURE.md          # 프로젝트 구조도 (본 파일)
├── app.py                # Streamlit 메인 애플리케이션
├── requirements.txt      # 의존성 패키지 목록
├── config/               # 설정 관련 파일
│   └── settings.py
├── data/                 # 데이터 저장소
│   ├── 10k_documents/    # 10-K 보고서 PDF/TXT
│   └── processed/        # 전처리된 CSV/JSON 데이터
├── docs/                 # 문서화 자료
│   └── TUTORIAL.md       # 상세 사용 가이드
├── fonts/                # PDF 생성용 한글 폰트
│   ├── NanumGothic.ttf
│   └── NanumGothicBold.ttf
├── models/               # ML 모델 저장소
├── scripts/              # 데이터 수집 및 유틸리티 스크립트
│   ├── collect_10k_relationships.py
│   ├── collect_top100_financials.py
│   ├── embed_10k_documents.py
│   ├── expand_to_sp500.py
│   ├── sp500_scheduler.py
│   ├── update_existing_companies.py
│   ├── upload_relationships_to_supabase.py
│   └── upload_to_supabase.py
└── src/                  # 소스 코드
    ├── core/             # 핵심 모듈
    │   ├── chat_connector.py
    │   └── input_validator.py
    ├── data/             # 데이터 클라이언트
    │   ├── finnhub_client.py
    │   ├── stock_api_client.py
    │   └── supabase_client.py
    ├── rag/              # RAG (검색 증강 생성) 로직
    │   ├── analyst_chat.py
    │   ├── data_retriever.py
    │   ├── rag_base.py
    │   ├── report_generator.py
    │   └── vector_store.py
    ├── ui/               # 사용자 인터페이스
    │   ├── helpers/
    │   └── pages/
    │       ├── calendar_page.py
    │       ├── home.py
    │       ├── insights.py
    │       └── report_page.py
    └── utils/            # 유틸리티 함수
        └── pdf_utils.py  # PDF 생성 및 차트 임베딩
```
