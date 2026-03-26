from dotenv import load_dotenv
load_dotenv()

"""
CrewAI + Gemini 무료 티어 예제: 웹사이트 리서치 → 요약 보고서
==============================================================

실행 전 필요한 것:
  1. pip install crewai
  2. Gemini API 키 발급: https://aistudio.google.com/apikey
  3. 환경변수 설정:
     - Windows CMD:   set GEMINI_API_KEY=your-key-here
     - Windows PS:    $env:GEMINI_API_KEY="your-key-here"
     - Mac/Linux:     export GEMINI_API_KEY="your-key-here"

참고: Gemini 무료 티어는 분당 요청 수 제한이 있습니다.
     에이전트가 많으면 속도 제한에 걸릴 수 있어요.
"""

import os
from crewai import Agent, Task, Crew, Process, LLM

# ============================================================
# Gemini LLM 설정
# ============================================================

# 환경변수에서 API 키 가져오기
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    print("❌ GEMINI_API_KEY 환경변수가 설정되지 않았습니다!")
    print()
    print("설정 방법:")
    print("  Windows CMD:  set GEMINI_API_KEY=여기에_키_입력")
    print("  Windows PS:   $env:GEMINI_API_KEY=\"여기에_키_입력\"")
    print("  Mac/Linux:    export GEMINI_API_KEY=\"여기에_키_입력\"")
    print()
    print("API 키 발급: https://aistudio.google.com/apikey")
    exit(1)

# CrewAI의 LLM 객체로 Gemini 설정
# "gemini/" 접두사를 붙이면 CrewAI가 자동으로 Gemini API를 사용합니다
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",  # 무료 티어에서 사용 가능한 모델
    api_key=gemini_api_key,
    temperature=0.7,
)

print("✅ Gemini API 연결 설정 완료!")
print(f"   모델: gemini-2.0-flash (무료)")
print()


# ============================================================
# 1단계: Agent 정의 (팀원 3명) - 모두 Gemini를 두뇌로 사용
# ============================================================

# 팀원 1: 리서처
researcher = Agent(
    role="시니어 AI 리서처",
    goal="AI 에이전트 관련 최신 트렌드와 핵심 정보를 수집한다",
    backstory="""
        당신은 10년 경력의 AI 기술 리서처입니다.
        최신 기술 트렌드를 빠르게 파악하고,
        신뢰할 수 있는 정보를 정리하는 전문가입니다.
    """,
    llm=gemini_llm,  # ← Gemini 사용!
    verbose=True,
)

# 팀원 2: 분석가
analyst = Agent(
    role="기술 트렌드 분석가",
    goal="수집된 정보를 분석하여 핵심 인사이트를 도출한다",
    backstory="""
        당신은 기술 컨설팅 회사의 분석가입니다.
        복잡한 기술 정보를 비전공자도 이해할 수 있게
        정리하고 패턴을 찾아내는 것이 특기입니다.
    """,
    llm=gemini_llm,  # ← Gemini 사용!
    verbose=True,
)

# 팀원 3: 작가
writer = Agent(
    role="테크 블로그 작가",
    goal="분석 결과를 읽기 쉬운 한국어 보고서로 작성한다",
    backstory="""
        당신은 기술 블로그를 운영하는 작가입니다.
        복잡한 기술 내용을 쉽고 재미있게 풀어쓰는 능력이 있습니다.
        마크다운 형식으로 깔끔하게 작성합니다.
    """,
    llm=gemini_llm,  # ← Gemini 사용!
    verbose=True,
)


# ============================================================
# 2단계: Task 정의 (할 일 3개)
# ============================================================

# 할 일 1: 리서치
research_task = Task(
    description="""
        2025-2026년 AI 에이전트 트렌드에 대해 당신이 알고 있는 정보를 정리하세요.
        다음 내용을 포함해주세요:
        - 주요 AI 에이전트 도구들 (Claude Code, Cursor, Copilot 등)
        - 멀티 에이전트 시스템의 발전 방향
        - MCP(Model Context Protocol)의 역할
        - 개발자들이 실제로 어떻게 활용하고 있는지
        최소 10개의 핵심 포인트를 정리해주세요.
    """,
    expected_output="AI 에이전트 트렌드에 대한 상세한 리서치 결과 (최소 10개 핵심 포인트)",
    agent=researcher,
)

# 할 일 2: 분석
analysis_task = Task(
    description="""
        리서치 결과를 바탕으로 다음을 분석하세요:
        - 3가지 핵심 트렌드 도출
        - 각 트렌드가 개발자에게 미치는 영향
        - 2026년 하반기 전망
        - Python 웹 개발자가 주목해야 할 포인트
    """,
    expected_output="구조화된 트렌드 분석 결과",
    agent=analyst,
    context=[research_task],  # ← 리서치 결과를 입력으로 받음
)

# 할 일 3: 보고서 작성
writing_task = Task(
    description="""
        분석 결과를 바탕으로 한국어 보고서를 작성하세요.
        형식:
        - 제목
        - 요약 (3줄)
        - 핵심 트렌드 3가지 (각각 설명)
        - 개발자를 위한 액션 아이템
        - 마무리
        모든 내용은 한국어로 작성해주세요.
    """,
    expected_output="마크다운 형식의 한국어 보고서",
    agent=writer,
    context=[analysis_task],  # ← 분석 결과를 입력으로 받음
    output_file="report.md",
)


# ============================================================
# 3단계: Crew 구성 & 실행
# ============================================================

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AI 에이전트 트렌드 리서치 Crew 시작!")
    print("   (Gemini 2.0 Flash 무료 티어 사용)")
    print("=" * 60)
    print()
    print("👥 팀 구성:")
    print("  1. 시니어 AI 리서처 → 정보 수집")
    print("  2. 기술 트렌드 분석가 → 인사이트 도출")
    print("  3. 테크 블로그 작가 → 보고서 작성")
    print()
    print("📋 실행 순서: 리서치 → 분석 → 보고서 작성")
    print("=" * 60)
    print()

    result = crew.kickoff()

    print()
    print("=" * 60)
    print("✅ 완료! report.md 파일을 확인하세요")
    print("=" * 60)
    print()
    print(result)
