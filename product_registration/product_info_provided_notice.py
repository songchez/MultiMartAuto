import streamlit as st
from data.summary_info_options import summary_info_options  # 상품정보제공공시 옵션 데이터 가져오기

def get_product_info_provided_notice():
    """
    상품정보제공공시 데이터를 입력받아 payload에 사용할 데이터를 반환하는 함수.
    :return: dict
    """
    st.header("상품정보제공공시 입력")

    # 상품정보제공공시 유형 선택
    selected_notice_type = st.selectbox(
        "상품정보제공공시 유형을 선택하세요:",
        list(summary_info_options.keys()),
        format_func=lambda x: summary_info_options[x]['label']
    )

    # 반환할 데이터 구조 초기화
    product_info_summary_payload = {
        "productInfoProvidedNoticeType": selected_notice_type,
        snake_to_camel(selected_notice_type): {}
    }

    if selected_notice_type:
        st.write(f"#### {summary_info_options[selected_notice_type]['label']}에 대한 정보 입력")
        fields = summary_info_options[selected_notice_type]["fields"]
        camel_case_option = snake_to_camel(selected_notice_type)

        for field_key, field_description in fields.items():
            if isinstance(field_description, dict) and "options" in field_description:
                # 선택형 옵션 처리 (라디오 버튼)
                options = field_description["options"]
                selected_value = st.radio(
                    field_description["label"],
                    options=list(options.keys()),
                    format_func=lambda x, opt=options: opt[x],
                    key=f"{selected_notice_type}_{field_key}"
                )
                product_info_summary_payload[camel_case_option][field_key] = selected_value
            else:
                # 일반 텍스트 입력
                input_value = st.text_input(
                    field_description if isinstance(field_description, str) else field_description["label"],
                    key=f"{selected_notice_type}_{field_key}"
                )
                if input_value:
                    product_info_summary_payload[camel_case_option][field_key] = input_value

    return product_info_summary_payload


def snake_to_camel(snake_str):
    """
    snake_case 문자열을 camelCase로 변환하는 유틸리티 함수
    :param snake_str: str
    :return: str
    """
    components = snake_str.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])
