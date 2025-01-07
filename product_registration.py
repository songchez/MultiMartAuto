import streamlit as st
from auth.auth_manager import AuthManager
from api.api_handler import APIHandler
from secrets.auth_env import auth_info
from datetime import datetime
from data.summary_info_options import summary_info_options

# 페이지 설정
st.set_page_config(page_title="상품 등록", page_icon="🔥", layout="wide")

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

# APIHandler 초기화
api_handler = APIHandler(access_token)

# 상품 등록 폼
with st.form("product_form"):
    
    product_name = st.text_input("상품 이름 (필수)", help="등록할 상품의 이름을 입력하세요.")
    # product_category = st.text_input("리프 카테고리 ID (필수)", help="등록할 상품의 리프 카테고리 ID를 입력하세요.")
    product_price = st.number_input("판매 가격 (필수)", min_value=1, step=1, help="상품의 판매 가격을 입력하세요.")
    product_stock = st.number_input("재고 수량 (필수)", min_value=1, step=1, help="상품의 재고 수량을 입력하세요.")
    product_detail = st.text_area("상품 상세 정보 (필수)", help="상품의 상세 설명을 입력하세요.")
    # 옵션정보정보정보
    with st.form("option_form"):
        # 단독형 옵션
        simple_options = []
        option_count = st.selectbox("단독형 옵션 개수 (1-3)", options=[1, 2, 3], index=0, help="사용할 단독형 옵션의 개수를 선택하세요.")
        for i in range(option_count):  # 사용자가 선택한 개수만큼 단독형 옵션
            col1, col2 = st.columns(2)
            with col1:
                group_name = st.text_input(f"단독형 옵션 그룹명 {i+1}", help="옵션 그룹명을 입력하세요.")
            with col2:
                option_name = st.text_input(f"단독형 옵션값 {i+1}", help="옵션 값을 입력하세요.")
            if group_name and option_name:
                simple_options.append({
                    "groupName": group_name,
                    "name": option_name,
                })

    # 폼 제출 버튼
    submit_options = st.form_submit_button("옵션 등록")
    # sale_type = st.selectbox("판매 유형 (필수)", ["NEW", "OLD"], help="상품이 새 상품인지 중고 상품인지 선택하세요.")
    sale_start_date = st.date_input("판매 시작일 (필수)", help="판매 시작 날짜를 선택하세요.")
    sale_end_date = st.date_input("판매 종료일 (필수)", help="판매 종료 날짜를 선택하세요.")
    representative_image = st.file_uploader("대표 이미지 (필수)", type=["jpg", "png", "jpeg"], help="대표 이미지를 업로드하세요.")
    additional_images = st.file_uploader("추가 이미지 (선택, 최대 9개)", type=["jpg", "png", "jpeg"], accept_multiple_files=True, help="추가 이미지를 업로드하세요.")
    # delivery_type = st.selectbox("배송 방식 (필수)", ["DELIVERY", "DIRECT"], help="배송 방식을 선택하세요.")
    # delivery_attribute_type = st.selectbox("배송 속성 (필수)", ["NORMAL", "TODAY", "HOPE", "SELLER_GUARANTEE"], help="배송 속성을 선택하세요.")
    # delivery_fee_type = st.selectbox("배송비 유형", ["FREE", "PAID"], help="배송비 유형을 선택하세요.")
    base_fee = st.number_input("기본 배송비", min_value=0, step=1, help="기본 배송비를 입력하세요.")
    # delivery_company = st.text_input("택배사 (선택)", help="배송에 사용할 택배사를 입력하세요.")

    # 상품요약정보필드(옵션)
    # snake_case를 camelCase로 변환하는 함수
def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])

# 상품요약정보필드(옵션)
selected_option = st.selectbox(
    "카테고리를 선택하세요:",
    options=list(summary_info_options.keys()),
    format_func=lambda x: summary_info_options[x]['label']
)

product_info_summary_payload = {}

# 상품요약정보필드(필드표시)
if selected_option:
    st.subheader(f"선택한 유형: {summary_info_options[selected_option]['label']}")
    fields = summary_info_options[selected_option]["fields"]
    
    # camelCase로 변환된 필드 키
    camel_case_option = snake_to_camel(selected_option)
    product_info_summary = {}

    for field_key, field_description in fields.items():
        # Check if the field has options (for radio button)
        if isinstance(field_description, dict) and "options" in field_description:
            options = field_description["options"]
            selected_value = st.radio(
                field_description["label"],
                options=list(options.keys()),
                format_func=lambda x: options[x]
            )
            product_info_summary[field_key] = selected_value
        else:
            # Use text input for simple fields
            input_value = st.text_input(field_description, key=field_key)
            if input_value:
                product_info_summary[field_key] = input_value

    # productInfoProvidedNoticeType 추가
    product_info_summary_payload["productInfoProvidedNoticeType"] = summary_info_options[selected_option]["label"]
    # 카테고리를 camelCase 키로 추가
    product_info_summary_payload[camel_case_option] = product_info_summary
    
    outbound_location_id = st.text_input("판매자 창고 ID (선택)", help="상품을 출고할 창고 ID를 입력하세요.")
    after_service_phone_number = st.text_input("A/S(고객센터) 전화번호 (필수)", help="고객센터 전화번호")
    after_service_guide_content = st.text_input("A/S 가이드 (필수)", help="예) 문의시 기재된 번호로 연락주세요")
    brand_name = st.text_input("브랜드이름 (선택)", help="브랜드 명을 적어주세요")
    submit_button = st.form_submit_button("상품 등록")

    if submit_button:
        # 필수 입력값 검증
        if not (product_name and product_price and product_stock and product_detail and representative_image and after_service_phone_number and after_service_guide_content):
            st.error("모든 필수 필드를 입력해야 합니다.")
            st.stop()

        # 이미지 업로드 함수
        def upload_image(file):
            temp_file_path = f"temp_{file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(file.getbuffer())
            return api_handler.upload_image(temp_file_path)

        # 대표 이미지 업로드
        rep_image_url = upload_image(representative_image)
        if "error" in rep_image_url:
            st.error(f"대표 이미지 업로드 실패: {rep_image_url['error']}")
            st.stop()

        # 추가 이미지 업로드
        additional_image_urls = []
        for image in additional_images:
            img_url = upload_image(image)
            if "error" in img_url:
                st.error(f"추가 이미지 업로드 실패: {img_url['error']}")
                st.stop()
            additional_image_urls.append(img_url)

        # 날짜 형식 변환
        sale_start_datetime = datetime.combine(sale_start_date, datetime.min.time()).isoformat()
        sale_end_datetime = datetime.combine(sale_end_date, datetime.min.time()).isoformat()

        # Payload 생성
        payload = {
            "name": product_name,
            # "leafCategoryId": product_category,
            "statusType":"SALE",
            "salePrice": product_price,
            "stockQuantity": product_stock,
            "detailContent": product_detail,
            "images": {
                "representativeImage": rep_image_url,
                "optionalImages": additional_image_urls
            },
            # "saleType": sale_type,
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
            "claimDeliveryInfo" :{
                "returnDeliveryFee": 3000,
                "exchangeDeliveryFee":3000
            },
            "detailAttribute":{
                "naverShoppingSearchInfo":{
                    "manufacturerName":brand_name,
                    "brandName":brand_name
                },
            },
            "afterServiceInfo":{
                "afterServiceTelephoneNumber": after_service_phone_number,
                "afterServiceGuideContent": after_service_guide_content
            },
            "originAreaInfo" : {
                "originAreaCode": "02",
                "importer": brand_name,
            },
            "optionInfo":{
                "optionSimple": simple_options,
            },
            "minorPurchasable": True,
            "productInfoProvidedNotice":{
                "productInfoProvidedNoticeType": ""
            }

        }

        # API 호출
        try:
            response = api_handler.send_request("POST", "products", data=payload)
            if "error" in response:
                st.error(f"상품 등록 실패: {response['error']}")
            else:
                st.success("상품 등록 성공!")
                st.write("API 응답:", response)
        except Exception as e:
            st.error(f"상품 등록 처리 중 오류 발생: {e}")
