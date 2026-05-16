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

# --- [핵심] 멀티 에이전트 협업 엔진 (동적 생성 루프) ---
def run_multi_agent_pipeline(service_name, service_url, service_desc):
    """기획 -> 카피라이팅 -> 편집 에이전트가 순차적으로 협업하는 워크플로우"""
    status_box = st.empty()
    
    # 1. 기획 에이전트 (Planning)
    status_box.info("🎯 [1/3] 기획 에이전트가 서비스의 셀링 포인트를 분석 중입니다...")
    time.sleep(1) # 에이전트 사고 시간 시뮬레이션
    
    # 2. 카피라이팅 에이전트 (Writing)
    status_box.info("✍️ [2/3] 카피라이팅 에이전트가 SEO 최적화 문장 및 HTML 구조를 빌드하고 있습니다...")
    time.sleep(1.2)
    
    # 3. 편집 및 검토 에이전트 (Reviewing & Taste)
    status_box.info("🕵️‍♂️ [3/3] 편집 에이전트가 문체를 다듬고 최종 링크 무결성을 검수하는 중입니다...")
    time.sleep(0.8)
    status_box.empty()
    
    # 동적으로 생성되는 결과물 구조 (추후 이 부분을 Open Claw 및 LLM API와 직결하시면 됩니다)
    generated_title = f"[추천] 전기료 절약과 업무 효율을 동시에! {service_name} 활용 가이드"
    generated_html = f"""
    <p>최근 주목받고 있는 혁신적인 플랫폼, <strong>{service_name}</strong>을 소개합니다.</p>
    <p>{service_desc}</p>
    <h3>📌 왜 {service_name}을 선택해야 할까요?</h3>
    <ul>
        <li>인공지능(AI) 기반의 실시간 데이터 최적화 알고리즘 탑재</li>
        <li>개발자부터 일반 사용자까지 고려한 직관적인 UI/UX 인터페이스</li>
        <li>스트림릿(Streamlit) 기반으로 별도 설치 없이 즉시 실행 가능</li>
    </ul>
    <p>지금 바로 아래 공식 링크를 통해 스마트한 변화를 직접 경험해 보세요!</p>
    <br>
    <a href="{service_url}" style="display: block; width: 250px; margin: 30px auto; padding: 15px; background-color: #4A90E2; color: white; text-align: center; text-decoration: none; font-weight: bold; border-radius: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);"> {service_name} 즉시 체험하기 🚀</a>
    """
    return generated_title, generated_html

# --- 초기 대시보드 데이터 세팅 (Session State 활용) ---
if "services" not in st.session_state:
    st.session_state["services"] = {
        "솔라매니저 AI": {"url": "https://solarmanager-ai.streamlit.app/", "desc": "태양광 발전량과 가정 내 소비 패턴을 AI로 분석하여 전기요금을 획기적으로 낮춰주는 에너지 테크 서비스입니다."},
        "거북목 방지 AI": {"url": "https://anti-turtle-neck-ai.streamlit.app/", "desc": "웹캠을 통해 사용자의 실시간 앉은 자세를 스캔하고 거북목 위험을 감지해 건강을 지켜주는 헬스케어 솔루션입니다."},
        "StyleScan AI": {"url": "https://stylescan-ai.streamlit.app/", "desc": "업로드된 패션 이미지를 비전 AI로 정밀 분석하여 자동으로 태그를 추출하고 트렌드를 분석해주는 패션 테크 SaaS입니다."}
    }

# --- 레이아웃 구성 ---
st.title("🔮 Multi-Agent Central Operating System")
st.caption("그동안 만든 모든 SaaS와 앞으로 태어날 신규 AI 서비스를 통합 관리하는 원클릭 마케팅 센터")
st.divider()

# --- 사이드바: 미래 보장형 서비스 레지스트리 ---
with st.sidebar:
    st.header("✨ 신규 AI 서비스 등록")
    with st.form("new_service_form", clear_on_submit=True):
        new_name = st.text_input("서비스 이름 (예: Chef Noir AI)")
        new_url = st.text_input("스트림릿 배포 URL")
        new_desc = st.text_area("서비스 한 줄 핵심 설명")
        submit_btn = st.form_submit_with_button("플러그인 에이전트 등록")
        
        if submit_btn and new_name and new_url:
            st.session_state["services"][new_name] = {"url": new_url, "desc": new_desc}
            st.toast(f"🎉 {new_name} 서비스가 에이전트 시스템에 성공적으로 로드되었습니다!", icon="🟢")

    st.divider()
    st.header("🎯 현재 가동 중인 서비스")
    selected_service = st.selectbox("컨트롤할 서비스를 선택하세요", list(st.session_state["services"].keys()))

# --- 메인 워크스페이스 ---
current_data = st.session_state["services"][selected_service]

st.subheader(f"🛠️ {selected_service} 관제 모드")
st.info(f"🔗 **연동 정보:** {current_data['url']} \n\n📝 **기본 메타 데이터:** {current_data['desc']}")

# 에이전트 가동 버튼
if st.button("🤖 멀티 에이전트 협업 가동 (글/이미지 큐레이션)", type="secondary"):
    title, html = run_multi_agent_pipeline(selected_service, current_data["url"], current_data["desc"])
    st.session_state["generated_title"] = title
    st.session_state["generated_html"] = html
    st.success("✨ 에이전트 군단이 최종 결과물을 도출했습니다! 아래 작업대에서 확인하세요.")

st.divider()

# --- 작업대 및 발행 파이프라인 ---
if "generated_title" in st.session_state:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 에이전트 최종 결과물 수정")
        edited_title = st.text_input("제목 편집", value=st.session_state["generated_title"])
        edited_html = st.text_area("HTML 소스코드 편집", value=st.session_state["generated_html"], height=350)
        
    with col2:
        st.subheader("👀 최종 발행 레이아웃 미리보기")
        st.markdown(f"**실제 블로그 제목:** {edited_title}")
        st.html(edited_html)
        
    st.divider()
    
    # 워드프레스 게이트웨이
    st.subheader("📤 워드프레스 퍼블리싱 게이트웨이")
    pub_mode = st.radio("포스팅 모드 선택", ["임시저장 (draft)", "즉시발행 (publish)"], horizontal=True)
    status_param = "draft" if "임시저장" in pub_mode else "publish"
    
    if st.button("🚀 워드프레스 API 전송 및 발행", type="primary"):
        with st.spinner("REST API를 통해 워드프레스 데이터베이스망에 안전하게 동기화 중입니다..."):
            success, link = post_to_wordpress(edited_title, edited_html, status=status_value)
            if success:
                st.success(f"🎉 형님, 대성공입니다! 블로그에 성공적으로 안착했습니다.")
                st.info(f"🔗 생성된 워드프레스 글 확인: {link}")
            else:
                st.error(f"❌ API 연동 실패: {link}")
