import streamlit as st
from auth.auth_manager import AuthManager
from api.api_handler import APIHandler
from logs.logger import Logger

# Initialize logger
logger = Logger()

# App title
st.title("Product Management System")

# Sidebar for platform selection
st.sidebar.header("Platform Selection")
platform = st.sidebar.selectbox("Select Platform", ["Naver", "Coupang", "Cafe24"]).lower()

# Load authentication information
auth_manager = AuthManager()
auth_info = auth_manager.load_auth_info(platform)
if not auth_info:
    st.sidebar.error("No authentication information found for the selected platform.")
    st.stop()

# API Handler
api_handler = APIHandler(platform, auth_info)

# Tabs for different functionalities
tab = st.tabs(["Add Product", "View Products", "Update Product", "Delete Product"])

# Add Product Tab
with tab[0]:
    st.header("Add Product")
    with st.form("add_product_form"):
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        category = st.text_input("Category")
        stock = st.number_input("Stock Quantity", min_value=0, step=1)
        options = st.text_input("Options (comma-separated)")
        image_path = st.text_input("Image Path")
        submitted = st.form_submit_button("Add Product")

        if submitted:
            product_data = {
                "name": name,
                "price": price,
                "category": category,
                "stock": stock,
                "options": options.split(','),
                "image_path": image_path,
            }
            response = api_handler.create_product(product_data)
            if "error" in response:
                st.error(f"Error: {response['error']}")
                logger.log_error(f"Product creation failed: {response['error']}")
            else:
                st.success(f"Product added successfully: {response}")
                logger.log_success(f"Product created: {response}")

# View Products Tab
with tab[1]:
    st.header("View Products")
    st.write("This feature requires integration with a product database or API.")

# Update Product Tab
with tab[2]:
    st.header("Update Product")
    product_id = st.text_input("Enter Product ID to Update")
    with st.form("update_product_form"):
        name = st.text_input("New Product Name")
        price = st.number_input("New Price", min_value=0.0, step=0.01)
        category = st.text_input("New Category")
        stock = st.number_input("New Stock Quantity", min_value=0, step=1)
        options = st.text_input("New Options (comma-separated)")
        image_path = st.text_input("New Image Path")
        submitted = st.form_submit_button("Update Product")

        if submitted and product_id:
            updated_data = {
                "name": name,
                "price": price,
                "category": category,
                "stock": stock,
                "options": options.split(','),
                "image_path": image_path,
            }
            response = api_handler.update_product(product_id, updated_data)
            if "error" in response:
                st.error(f"Error: {response['error']}")
                logger.log_error(f"Product update failed: {response['error']}")
            else:
                st.success(f"Product updated successfully: {response}")
                logger.log_success(f"Product updated: {response}")

# Delete Product Tab
with tab[3]:
    st.header("Delete Product")
    product_id = st.text_input("Enter Product ID to Delete")
    if st.button("Delete Product"):
        if product_id:
            response = api_handler.delete_product(product_id)
            if "error" in response:
                st.error(f"Error: {response['error']}")
                logger.log_error(f"Product deletion failed: {response['error']}")
            else:
                st.success(f"Product deleted successfully: {response}")
                logger.log_success(f"Product deleted: {response}")
