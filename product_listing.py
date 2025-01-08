import streamlit as st
from auth.auth_manager import AuthManager
from api.api_handler import APIHandler
from secret_env.auth_env import auth_info
from datetime import datetime
import requests
from PIL import Image

# 페이지 설정
st.set_page_config(page_title="상품목록", page_icon="📂", layout="wide")
st.header("상품 목록")
st.divider()

# 인증 정보 가져오기
client_id = auth_info["naver"]["seller_id"]
client_secret = auth_info["naver"]["secret"]

# AuthManager 초기화 및 액세스 토큰 가져오기
auth_manager = AuthManager(client_id, client_secret)
access_token = auth_manager.get_access_token()

if not access_token:
    st.sidebar.error("액세스 토큰을 가져오지 못했습니다.")
    st.stop()
else:
    # st.sidebar.success("인증 성공!")
    api_handler = APIHandler(access_token)

# 상품 목록 조회 함수
def fetch_products(page):
    payload = {
        "productStatusTypes": ["SALE"],
        "page": page,
        "size": 10,
        "orderType": "REG_DATE",
        "periodType": "PROD_REG_DAY",
        "fromDate": "2020-01-01",
        "toDate": datetime.today().strftime('%Y-%m-%d')
    }
    try:
        response = api_handler.send_request("POST", "products_search", data=payload)
        if "error" in response:
            st.error(f"상품 목록 조회 실패: {response['error']}")
            return [], 1
        else:
            total_pages = response.get("totalPages", 1)
            return response.get("contents", []), total_pages
    except Exception as e:
        st.error(f"상품 목록 조회 중 오류 발생: {e}")
        return [],1

# 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = 1
if "products" not in st.session_state:
    st.session_state.products = {}
if "total_pages" not in st.session_state:
    products, total_pages = fetch_products(1)
    st.session_state.totalPages = total_pages

# 상품 정보 표시 함수
def display_product(product):
    product = product.get("channelProducts", [{}])[0]
    name = product.get("name", "이름 없음")
    image_url = product.get("representativeImage", {}).get("url", None)

    col1, col2 = st.columns([1, 7], gap="small")
    with col1:
        if image_url:
            try:
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    product_image = Image.open(response.raw)
                    st.image(product_image, width=120)
                else:
                    st.warning("이미지를 로드할 수 없습니다.")
            except Exception:
                st.warning("이미지를 로드할 수 없습니다.")
        else:
            st.write("이미지 없음")
    with col2:
        st.markdown(f"#### {name}")
        with st.expander(f"**가격**: {product.get('salePrice', 0):,}원  :blue[더보기↓]"):
            st.write(f"**카테고리**: {product.get('wholeCategoryName', '없음')}")
            st.write(f"**판매 상태**: {product.get('statusType', '알 수 없음')}")
            st.write(f"**재고 수량**: {product.get('stockQuantity', 0):,}개")


# 상품 목록 표시 함수
def fetch_and_display_products(page):
    if page not in st.session_state.products:
        products, total_pages = fetch_products(page)
        st.session_state.products[page] = products
        st.session_state.totalPages = total_pages
    else:
        products = st.session_state.products[page]

    if not products:
        st.warning("조회된 상품이 없습니다.")
    else:
        for product in products:
            display_product(product)

# 숫자 페이지 네비게이션
total_pages = st.session_state.totalPages
option_map = {i: i + 1 for i in range(total_pages)}
selection = st.sidebar.segmented_control(
    "페이지",
    options=list(option_map.keys()),
    format_func=lambda option: f"{option_map[option]}",
    selection_mode="single",
)
if selection is None:
    st.session_state.page = option_map[0]
    fetch_and_display_products(st.session_state.page)
else:
    st.session_state.page = option_map[selection]
    fetch_and_display_products(st.session_state.page)
