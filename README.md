# CrewAI 멀티 에이전트 리서치 시스템

3명의 AI 에이전트가 협업하여 AI 트렌드 보고서를 자동 생성하는 프로젝트입니다.

## 어떻게 동작하나요?

```
사람: "AI 에이전트 트렌드 보고서 만들어줘"
  │
  ▼
┌──────────────────────────────────────────┐
│              Crew (에이전트 팀)            │
│                                          │
│  ① 리서처 ──→ ② 분석가 ──→ ③ 작가      │
│     정보 수집    인사이트     보고서       │
│                  도출        작성         │
└──────────────────────────────────────────┘
  │
  ▼
reports/report_20260327_140523.md (최종 보고서)
```

각 에이전트는 이전 에이전트의 결과를 `context`로 받아서 작업합니다.

## 기술 스택

- **CrewAI** — 멀티 에이전트 오케스트레이션 프레임워크
- **Google Gemini 2.5 Flash** — LLM (무료 티어)
- **Python 3.12**

## 시작하기

### 1. 클론 & 가상환경

```bash
git clone https://github.com/YOUR_USERNAME/crewai-research.git
cd crewai-research

python -m venv venv
source venv/Scripts/activate    # Windows (Git Bash)
# source venv/bin/activate      # Mac/Linux
```

### 2. 패키지 설치

```bash
pip install crewai "crewai[google-genai]" python-dotenv
```

### 3. 환경변수 설정

[Google AI Studio](https://aistudio.google.com/apikey)에서 API 키를 발급받고 `.env` 파일을 만드세요:

```bash
cp .env.example .env
# .env 파일을 열어서 발급받은 키 입력
```

### 4. 실행

```bash
python main_gemini.py
```

실행하면 터미널에 각 에이전트의 작업 과정이 출력되고, 완료되면 `reports/` 폴더에 타임스탬프가 붙은 보고서가 생성됩니다.

```
reports/
├── report_20260327_140523.md
├── report_20260328_090015.md
└── ...
```

## 보고서 스타일 변경

`main_gemini.py`에서 작가 에이전트의 스타일을 바꿀 수 있습니다. 기본 블로그 스타일 외에 2가지 옵션이 주석으로 준비되어 있어요:

- **기본** — 테크 블로그 보고서
- **옵션 1** — 9시 뉴스 앵커 대본
- **옵션 2** — IT 팟캐스트 대화체

기본 `writer`와 `writing_task`를 주석 처리하고, 원하는 옵션의 주석을 풀면 됩니다.

## 프로젝트 구조

```
crewai-research/
├── main_gemini.py     # 메인 코드 (에이전트, 태스크, 크루 정의)
├── reports/           # 생성된 보고서들 (실행할 때마다 누적)
│   ├── report_20260327_140523.md
│   └── ...
├── .env               # API 키 (git에 올라가지 않음)
├── .env.example       # 환경변수 템플릿
├── .gitignore
└── README.md
```

## 참고

- Gemini 무료 티어는 분당 요청 수 제한이 있습니다 (RPM: 5, RPD: 20)
- 에이전트 3명 기준 1회 실행에 약 3~5분 소요
- 할당량 초과 시 잠시 후 다시 실행하면 됩니다