import streamlit as st

def home():
    # Streamlit 페이지 구성
    st.set_page_config(
        page_title="MultiMart Auto",
        page_icon="🛒",
        layout="wide"
    )

    # 메인 페이지
    st.title("MultiMart Auto")
    st.write("왼쪽 사이드바에서 원하는 기능을 선택하세요.")

pg = st.navigation([
    st.Page(home, title="홈",icon="🏠"),
    st.Page("product_listing.py", title="상품목록",icon="📂"),
    st.Page("product_registration.py", title="상품등록",icon="🔥")
])
pg.run()
