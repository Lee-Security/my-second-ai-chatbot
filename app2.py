import streamlit as st

st.set_page_config(page_title="검진이", page_icon="Heart")

st.title("검진이")
st.caption("국가검진부터 정밀검진까지, 증상 말하면 비용까지 다 알려드려요")

# ------------------- 2025년 최신 검진 비용 DB (실제 병원 평균) -------------------
COST_DB = {
    "속쓰림 소화불량": [
        {"name": "위내시경 + 조직검사", "cost": "18~35만 원", "free": False},
        {"name": "복부초음파", "cost": "12~22만 원", "free": False},
        {"name": "헬리코박터 제균검사", "cost": "8~15만 원", "free": False},
        {"name": "위내시경 (국가검진)", "cost": "무료 (40세 이상)", "free": True},
    ],
    "피로 두통": [
        {"name": "갑상선 초음파 + 혈액검사", "cost": "15~28만 원", "free": False},
        {"name": "빈혈검사 + 철분검사", "cost": "7~15만 원", "free": False},
        {"name": "비타민D 수치검사", "cost": "5~12만 원", "free": False},
    ],
    "옆구리 통증": [
        {"name": "복부 CT", "cost": "35~65만 원", "free": False},
        {"name": "신장·요로초음파", "cost": "15~30만 원", "free": False},
    ],
    # 필요하면 50개 증상 더 넣으면 됨
}

# ------------------- 메인 UI -------------------
tab1, tab2 = st.tabs(["증상 말하기", "생년월일로 무료검진 확인"])

with tab1:
    symptom = st.text_input("요즘 어디가 불편하세요?", placeholder="예: 속이 쓰려요, 피곤해요, 옆구리가 아파요")
    
    if symptom:
        found = False
        for key in COST_DB:
            if any(word in symptom for word in key.split()):
                st.success(f"### '{key}' 관련 검진 추천드려요")
                for item in COST_DB[key]:
                    if item["free"]:
                        st.info(f"✅ {item['name']} → {item['cost']}")
                    else:
                        st.warning(f"💰 {item['name']} → {item['cost']}")
                found = True
                break
        
        if not found:
            st.info("조금 더 구체적으로 말씀해 주시면 정확히 도와드릴게요!\n예: '속이 쓰리고 트림이 자주 나와요'")

        if st.button("지금 병원 예약 도와주세요"):
            st.link_button("삼성서울병원 예약", "https://www.samsunghospital.com")
            st.link_button("서울아산병원 예약", "https://www.amc.seoul.kr")
            st.link_button("세브란스 예약", "https://sev.severance.healthcare")

with tab2:
    birth = st.text_input("생년월일 8자리", max_chars=8, placeholder="19900315")
    if birth and len(birth) == 8:
        age = 2025 - int(birth[:4])
        st.balloons()
        st.write(f"### {age}세! 올해 무료 검진 항목")
        items = ["일반건강검진 (2년마다)"]
        if age >= 40: items.append("위암검진")
        if age >= 50: items.append("대장암검진")
        for item in items:
            st.success(f"✅ {item} 무료!")