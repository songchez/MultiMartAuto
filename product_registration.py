import streamlit as st
from auth.auth_manager import AuthManager
from api.api_handler import APIHandler
from data.auth_env import auth_info

# 페이지 설정
st.set_page_config(page_title="상품 등록", page_icon="🔥")

st.title("상품 등록")

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

# 상품 등록 폼
with st.form("product_form"):
    product_name = st.text_input("상품 이름")
    product_price = st.number_input("가격", min_value=0, step=1)
    product_stock = st.number_input("재고 수량", min_value=0, step=1)
    product_category = st.text_input("카테고리")
    product_image = st.file_uploader("상품 이미지 업로드", type=["jpg", "png", "jpeg"])
    submit_button = st.form_submit_button("상품 등록")

# 등록 처리
if submit_button:
    if not product_name or not product_price or not product_stock or not product_category or not product_image:
        st.error("모든 필드를 입력해야 합니다.")
    else:
        try:
            # 이미지 업로드
            with open(f"temp_{product_image.name}", "wb") as f:
                f.write(product_image.getbuffer())
            image_response = api_handler.upload_image(f"temp_{product_image.name}")

            if "error" in image_response:
                st.error(f"이미지 업로드 실패: {image_response['error']}")
            else:
                image_url = image_response.get("url")
                product_data = {
                    "name": product_name,
                    "price": product_price,
                    "stock": product_stock,
                    "category": product_category,
                    "image_url": image_url,
                }
                response = api_handler.send_request("POST", "list_products", data=product_data)

                if "error" in response:
                    st.error(f"상품 등록 실패: {response['error']}")
                else:
                    st.success(f"상품 등록 성공! 상품 ID: {response.get('id')}")
        except Exception as e:
            st.error(f"상품 등록 중 오류 발생: {e}")
