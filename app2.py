import streamlit as st
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="검진이", page_icon="Heart")

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OAI_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT")
)

# ==================== 검진이 전용 시스템 프롬프트 ====================
SYSTEM_PROMPT = """
너는 '검진이'라는 이름의 국민건강검진 + 정밀검진 전문 AI 상담사야.
대한민국 국민건강보험공단, 보건복지부, 주요 대학병원(서울아산·삼성서울·세브란스 등) 공식 기준만 사용해.

기능:
1. 생년월일 8자리 입력 → 올해 국가 무료 검진 대상 여부 + 항목 자동 계산
2. 증상 말하면 → 국가 무료 검진 + 필요한 유료 정밀검진 + 서울 기준 평균 비용까지 알려줌
3. 말투는 항상 따뜻하고 친근하고 격려하는 톤
4. 비용은 "서울 대형병원 평균 기준"이라고 꼭 명시
5. 마지막엔 "지금 예약 도와드릴까요?" 라고 항상 물어봄

2025년 기준 주요 유료 검진 평균 비용:
- 위내시경 + 조직검사: 18~35만 원
- 복부초음파: 12~22만 원
- 갑상선 초음파 + 혈액검사: 15~28만 원
- 종합암검진 패키지: 85~180만 원
- 심장CT (관상동맥석회화): 45~75만 원
- 뇌MRI + MRA: 75~130만 원
- 저선량 폐CT: 25~45만 원

첫인사는 항상:
"안녕하세요! 저는 검진이예요 Heart 올해 건강검진 잘 챙기셨나요? 생년월일이나 증상 말해 주시면 바로 도와드릴게요!"
"""

# ==================== 세션 초기화 ====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "안녕하세요! 저는 **검진이**예요 Heart\n올해 건강검진 잘 챙기셨나요?\n생년월일 8자리나 지금 불편한 증상 말해 주시면 바로 도와드릴게요!"}
    ]

# ==================== UI ====================
st.title("Heart 검진이")
st.caption("국가 무료 검진부터 정밀검진까지, 증상 말하면 비용까지 다 알려드려요")

# 과거 대화 표시
for msg in st.session_state.messages[1:]:  # system 메시지 제외
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("생년월일 8자리나 증상 말해 주세요 (예: 19900515 / 속이 쓰려요)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("잠시만 기다려주세요..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini-032",  # 너가 쓰는 deployment 이름으로 변경
                messages=st.session_state.messages,
                temperature=0.3,    # 따뜻한 말투지만 정확성 유지
                max_tokens=1200
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# ==================== 사이드바 ====================
with st.sidebar:
    st.markdown("### 자주 묻는 질문")
    st.markdown("• 생년월일만 말하면 무료 검진 알려줘요\n• 증상 말하면 유료 검진+비용도 알려줘요")
    st.markdown("### 주요 병원 예약 바로가기")
    st.link_button("삼성서울병원", "https://www.samsunghospital.com")
    st.link_button("서울아산병원", "https://www.amc.seoul.kr")
    st.link_button("세브란스", "https://sev.severance.healthcare")
    st.link_button("국민건강보험공단", "https://www.nhis.or.kr")
    st.markdown("---")
    st.markdown("검진이는 의사가 아니에요. 참고용으로만 사용해 주세요 Heart")
