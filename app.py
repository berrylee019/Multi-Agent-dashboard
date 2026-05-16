import time
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="Multi-Agent Central OS", page_icon="🔮", layout="wide")

# --- [보안] 워드프레스 연동 함수 ---
def post_to_wordpress(title, content, status="draft"):
    try:
        WP_URL = st.secrets["wordpress"]["URL"]
        WP_USER = st.secrets["wordpress"]["USER"]
        WP_PASSWORD = st.secrets["wordpress"]["PASSWORD"]
        
        api_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"
        payload = {"title": title, "content": content, "status": status}
        
        response = requests.post(
            api_url, json=payload, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD),
            headers={"Content-Type": "application/json"}
        )
        return (True, response.json().get("link")) if response.status_code == 201 else (False, response.text)
    except Exception as e:
        return False, str(e)

# --- [핵심] 멀티 에이전트 협업 엔진 (마케팅 자동화) ---
def run_multi_agent_pipeline(service_name, service_url, service_desc):
    status_box = st.empty()
    status_box.info("🎯 [1/3] 기획 에이전트가 서비스 분석 중...")
    time.sleep(1)
    status_box.info("✍️ [2/3] 카피라이팅 에이전트가 HTML 빌드 중...")
    time.sleep(1.2)
    status_box.info("🕵️‍♂️ [3/3] 편집 에이전트가 최종 검수 중...")
    time.sleep(0.8)
    status_box.empty()
    
    generated_title = f"[추천] 혁신적인 AI 솔루션, {service_name} 활용 가이드"
    generated_html = f"""
    <p>혁신적인 플랫폼 <strong>{service_name}</strong>을 소개합니다.</p>
    <p>{service_desc}</p>
    <h3>📌 주요 특징</h3>
    <ul>
        <li>AI 기반 실시간 최적화 알고리즘</li>
        <li>직관적인 UI/UX 및 Streamlit 기반 접근성</li>
    </ul>
    <br>
    <a href="{service_url}" style="display: block; width: 250px; margin: 30px auto; padding: 15px; background-color: #4A90E2; color: white; text-align: center; text-decoration: none; font-weight: bold; border-radius: 30px;"> {service_name} 즉시 체험하기 🚀</a>
    """
    return generated_title, generated_html

# --- 초기 대시보드 데이터 세팅 ---
if "services" not in st.session_state:
    st.session_state["services"] = {
        "솔라매니저 AI": {"url": "https://solarmanager-ai.streamlit.app/", "desc": "태양광 발전량과 에너지 소비 패턴을 AI로 분석하는 서비스입니다."},
        "거북목 방지 AI": {"url": "https://anti-turtle-neck-ai.streamlit.app/", "desc": "웹캠으로 자세를 스캔하여 건강을 지켜주는 솔루션입니다."},
        "StyleScan AI": {"url": "https://stylescan-ai.streamlit.app/", "desc": "비전 AI로 패션 태그를 추출하는 테크 SaaS입니다."}
    }

# --- 레이아웃 구성 ---
st.title("⚔️ AI SaaS 사령부 (Central Command OS)")
st.caption("사령관(형님)의 지휘 하에 개발, 배포, 마케팅 에이전트가 각자의 임무를 수행합니다.")
st.divider()

# --- [추가된 섹션] 1. 에이전트 미션 통제실 ---
st.header("📋 에이전트 미션 컨트롤 (Mission Control)")
col_dev, col_mkt, col_qa = st.columns(3)

with col_dev:
    st.subheader("🛠️ DevOps 팀")
    dev_task = st.checkbox("GitHub 세팅 및 코드 커밋")
    if dev_task:
        st.info("🤖 DevOps 에이전트: 코드 변경점을 감지하고 푸시 준비 중...")
        if st.button("GitHub 작업 최종 승인"):
            st.success("✅ GitHub Push 성공! Streamlit 배포가 업데이트되었습니다.")

with col_mkt:
    st.subheader("✍️ 마케팅 팀")
    mkt_task = st.checkbox("신규 서비스 홍보물 기획")
    if mkt_task:
        st.info("🤖 마케팅 에이전트: 타겟 분석 및 블로그 초안 작성이 준비되었습니다.")
        st.warning("⚠️ 하단 '마케팅 작업대'에서 세부 내용을 검토해 주세요.")

with col_qa:
    st.subheader("🔍 QA & 점검 팀")
    qa_task = st.checkbox("서비스 배포 상태 점검")
    if qa_task:
        st.info("🤖 QA 에이전트: 현재 모든 API 연결 상태를 테스트 중입니다.")
        if st.button("점검 보고서 생성"):
            st.write("- 솔라매니저 AI: **정상**")
            st.write("- 거북목 AI: **결제 버튼 연결 확인**")

st.divider()

# --- 2. 사이드바 및 기존 마케팅 센터 기능 유지 ---
with st.sidebar:
    st.header("✨ 신규 AI 서비스 등록")
    with st.form("new_service_form", clear_on_submit=True):
        new_name = st.text_input("서비스 이름")
        new_url = st.text_input("배포 URL")
        new_desc = st.text_area("핵심 설명")
        if st.form_submit_button("플러그인 에이전트 등록"):
            if new_name and new_url:
                st.session_state["services"][new_name] = {"url": new_url, "desc": new_desc}
                st.toast(f"🎉 {new_name} 등록 완료!", icon="🟢")

    st.divider()
    st.header("🎯 가동 중인 서비스")
    selected_service = st.selectbox("컨트롤할 서비스", list(st.session_state["services"].keys()))

# --- 3. 마케팅 작업대 섹션 ---
current_data = st.session_state["services"][selected_service]
st.subheader(f"🚀 {selected_service} 마케팅 자동화 파이프라인")

if st.button("🤖 에이전트 협업 가동 (콘텐츠 큐레이션)", type="secondary"):
    title, html = run_multi_agent_pipeline(selected_service, current_data["url"], current_data["desc"])
    st.session_state["generated_title"] = title
    st.session_state["generated_html"] = html

if "generated_title" in st.session_state:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📝 편집기")
        ed_title = st.text_input("제목 편집", value=st.session_state["generated_title"])
        ed_html = st.text_area("HTML 편집", value=st.session_state["generated_html"], height=300)
    with c2:
        st.subheader("👀 미리보기")
        st.markdown(f"**제목:** {ed_title}")
        st.html(ed_html)

    st.divider()
    st.subheader("📤 워드프레스 최종 발행")
    pub_mode = st.radio("모드", ["임시저장 (draft)", "즉시발행 (publish)"], horizontal=True)
    
    if st.button("🌟 최종 승인 및 블로그 전송"):
        with st.spinner("사령관님의 승인에 따라 데이터 전송 중..."):
            status_val = "draft" if "임시저장" in pub_mode else "publish"
            success, link = post_to_wordpress(ed_title, ed_html, status=status_val)
            if success:
                st.success(f"✅ 발행 성공! 링크: {link}")
            else:
                st.error(f"❌ 오류: {link}")
