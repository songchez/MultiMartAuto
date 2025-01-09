import streamlit as st
from streamlit_local_storage import LocalStorage
from secret_env.auth_env import auth_info
from auth.auth_manager import AuthManager
from api.api_handler import APIHandler
from product_registration.product_info_provided_notice import get_product_info_provided_notice

# Helper functions

def validate_required_fields(fields):
    for key, value in fields.items():
        if not value:
            st.error(f"{key}은(는) 필수 입력값입니다.")
            return False
    return True

def upload_image(api_handler, file):
    temp_file_path = f"temp_{file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(file.getbuffer())
    return api_handler.upload_image(temp_file_path)

# Streamlit setup
st.set_page_config(page_title="상품 등록", page_icon="🔥", layout="wide")
st.title("상품 등록")

# -------------------------
# (0) 로컬 스토리지 설정
# -------------------------
local_storage = LocalStorage()

# -------------------------
# (1) 인증 및 초기화
# -------------------------
client_id = auth_info["naver"]["seller_id"]
client_secret = auth_info["naver"]["secret"]

auth_manager = AuthManager(client_id, client_secret)
access_token = auth_manager.get_access_token()

if not access_token:
    st.sidebar.error("액세스 토큰을 가져오지 못했습니다.")
    st.stop()

api_handler = APIHandler(access_token)

# -------------------------
# (2) 카테고리 조회 및 선택
# -------------------------
st.header("카테고리 선택")
categories_response = api_handler.send_request("GET", "categories")

if "error" in categories_response:
    st.error(f"카테고리 조회 실패: {categories_response['error']}")
    st.stop()

if not isinstance(categories_response, list) or len(categories_response) == 0:
    st.error("조회된 카테고리가 없거나 형식이 올바르지 않습니다.")
    st.stop()

leaf_categories = [cat for cat in categories_response if cat.get("last") is True]

if not leaf_categories:
    st.error("리프 카테고리가 없습니다. (마지막 하위 카테고리만 등록 가능하다고 가정)")
    st.stop()

selected_whole_cat = st.selectbox(
    "리프 카테고리를 선택하세요",
    [cat["wholeCategoryName"] for cat in leaf_categories]
)
selected_cat = next((cat for cat in leaf_categories if cat["wholeCategoryName"] == selected_whole_cat), None)
selected_cat_id = selected_cat["id"] if selected_cat else None

st.write(f"선택된 카테고리 ID: {selected_cat_id}")

# -------------------------
# (3) 상품 등록 기본 정보 입력
# -------------------------
st.header("기본 정보 입력")
product_name = st.text_input(
    "상품 이름 (필수)",
    value=local_storage.getItem("product_name") or "",
    help="등록할 상품의 이름을 입력하세요."
)
product_price = st.number_input(
    "판매 가격 원(필수)",
    value=int(local_storage.getItem("product_price") or 1),
    min_value=1,
    step=1,
    help="상품의 판매 가격을 입력하세요."
)
product_stock = st.number_input(
    "재고 수량 (필수)",
    value=int(local_storage.getItem("product_stock") or 1),
    min_value=1,
    step=1,
    help="상품의 재고 수량을 입력하세요."
)
product_detail = st.text_area(
    "상품 상세 정보 (필수)",
    value=local_storage.getItem("product_detail") or "",
    help="상품의 상세 설명을 입력하세요."
)

# 이미지 업로드
st.subheader("이미지 업로드")
representative_image = st.file_uploader("대표 이미지 (필수)", type=["jpg", "png", "jpeg"])
additional_images = st.file_uploader("추가 이미지 (선택, 최대 9개)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# 배송 정보
st.subheader("배송 정보 입력")
base_fee = st.number_input("기본 배송비", min_value=0, step=1)
outbound_location_id = st.text_input("판매자 창고 ID (선택)")
after_service_phone_number = st.text_input("A/S(고객센터) 전화번호 (필수)")
after_service_guide_content = st.text_input("A/S 가이드 (필수)")
brand_name = st.text_input("브랜드 이름 (선택)")

# 옵션 생성
st.subheader("단독형 옵션 입력")
simple_options = []
option_count = st.selectbox("단독형 옵션 개수 (1-3)", options=[1, 2, 3], index=0)

if option_count > 0:
    for i in range(option_count):
        col1, col2 = st.columns(2)
        with col1:
            group_name = st.text_input(
                f"단독형 옵션 그룹명 {i+1}",
                placeholder="예시: 컬러",
                key=f"group_name_{i+1}"
            )
        with col2:
            option_name = st.text_input(
                f"단독형 옵션값 {i+1}",
                placeholder="예시: 블랙, 화이트",
                key=f"option_name_{i+1}"
            )
        if group_name and option_name:
            simple_options.append({"groupName": group_name, "name": option_name})
            
# 상품정보제공공시
product_info_summary_payload = get_product_info_provided_notice()


col1, col2 = st.columns(2,gap="small")

with col1:
    # 중간 저장 버튼
    save_to_local_storage = st.button("중간 저장하기")

if save_to_local_storage:
    # 로컬 스토리지에 데이터 저장
    local_storage.setItem("product_name", product_name, key="product_name")
    local_storage.setItem("product_price", product_price,key="product_price")
    local_storage.setItem("product_stock", product_stock,key="product_stock")
    local_storage.setItem("product_detail", product_detail,key="product_detail")
    local_storage.setItem("base_fee", base_fee, key="base_fee")
    local_storage.setItem("outbound_location_id", outbound_location_id, key="outbound_location_id")
    local_storage.setItem("after_service_phone_number", after_service_phone_number, key="after_service_phone_number")
    local_storage.setItem("after_service_guide_content", after_service_guide_content, key="after_service_guide_content")
    local_storage.setItem("brand_name", brand_name, key="brand_name")
    local_storage.setItem("simple_options", simple_options, key="simple_options")
    
    st.success("입력된 정보를 중간 저장했습니다!")

# 중간 저장된 데이터 불러오기
if local_storage.getItem("product_name"):
    product_name = local_storage.getItem("product_name")
if local_storage.getItem("product_price"):
    product_price = int(local_storage.getItem("product_price"))
if local_storage.getItem("product_stock"):
    product_stock = int(local_storage.getItem("product_stock"))
if local_storage.getItem("product_detail"):
    product_detail = local_storage.getItem("product_detail")
if local_storage.getItem("base_fee"):
    base_fee = int(local_storage.getItem("base_fee"))
if local_storage.getItem("outbound_location_id"):
    outbound_location_id = local_storage.getItem("outbound_location_id")
if local_storage.getItem("after_service_phone_number"):
    after_service_phone_number = local_storage.getItem("after_service_phone_number")
if local_storage.getItem("after_service_guide_content"):
    after_service_guide_content = local_storage.getItem("after_service_guide_content")
if local_storage.getItem("brand_name"):
    brand_name = local_storage.getItem("brand_name")
if local_storage.getItem("simple_options"):
    simple_options = local_storage.getItem("simple_options")




with col2:
    # 상품 등록 버튼
    submit_product = st.button("상품 등록하기")

# -------------------------
# (4) 상품 등록
# -------------------------
if submit_product:
    if not product_name or not product_price or not product_stock or not product_detail:
        st.error("모든 필수 입력 항목을 채워주세요.")
        st.stop()

    if not selected_cat_id:
        st.error("유효한 리프 카테고리를 선택하세요.")
        st.stop()

    # 이미지 업로드 처리
    rep_image_url = upload_image(api_handler, representative_image) if representative_image else None
    additional_image_urls = [upload_image(api_handler, img) for img in additional_images] if additional_images else []
    



    # Payload 생성
    payload = {
        "originProduct":{
            "statusType": "SALE",
            "name": product_name,
            "leafCategoryId": selected_cat_id,
            "salePrice": product_price,
            "stockQuantity": product_stock,
            "detailContent": product_detail,
            "images": {
                "representativeImage": rep_image_url,
                "optionalImages": additional_image_urls
            },
            "deliveryInfo": {
                "deliveryType": "DELIVERY",
                "deliveryAttributeType": "NORMAL",
                "deliveryFee": {
                    "type": "PAID",
                    "baseFee": base_fee
                },
                "deliveryCompany": "HYUNDAI",
                "outboundLocationId": outbound_location_id,
            },
            "claimDeliveryInfo": {
                "returnDeliveryFee": 3000,
                "exchangeDeliveryFee": 3000
            },
            "detailAttribute": {
                "naverShoppingSearchInfo": {
                    "manufacturerName": brand_name,
                    "brandName": brand_name
                },
                "afterServiceInfo": {
                    "afterServiceTelephoneNumber": after_service_phone_number,
                    "afterServiceGuideContent": after_service_guide_content
                },
                "originAreaInfo": {
                    "originAreaCode": "02",
                    "importer": brand_name,
                },
                "optionInfo": {
                    "optionSimple": simple_options,
                },
                "minorPurchasable": True,
                "productInfoProvidedNotice": {
                    "productInfoProvidedNoticeType": product_info_summary_payload  # 기본값으로 설정
                }
            }
        },
        "smartstoreChannelProduct": {
            "naverShoppingRegistration": True,
            "channelProductDisplayStatusType": "ON"
        },
    }
    print(payload)

    # 등록 요청
    try:
        response = api_handler.send_request("POST", "create_product", data=payload)
        if "error" in response:
            st.error(f"상품 등록 실패: {response['error']}")
        else:
            st.success("상품 등록이 완료되었습니다.")
            st.json(response)
    except Exception as e:
        st.error(f"상품 등록 실패: {e}")