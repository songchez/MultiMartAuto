import requests
from api.api_endpoints import NAVER_API_BASE_URL, API_ENDPOINTS

class APIHandler:
    def __init__(self, access_token):
        """
        Initialize APIHandler with the access token.
        """
        self.access_token = access_token
        self.base_url = NAVER_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def send_request(self, method, endpoint_key, data=None, params=None):
        """
        Send an HTTP request to the API based on the endpoint key.
        """
        if endpoint_key not in API_ENDPOINTS:
            return {"error": f"Invalid endpoint key: {endpoint_key}"}

        url = f"{self.base_url}{API_ENDPOINTS[endpoint_key]}"
        try:
            if method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data, params=params)
            elif method.upper() == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()  # Raise HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def upload_image(self, image_path):
        """
        Upload a product image and return the uploaded URL.
        """
        if "upload_product_images" not in API_ENDPOINTS:
            return {"error": "Upload endpoint not defined"}

        url = f"{self.base_url}{API_ENDPOINTS['upload_product_images']}"
        try:
            with open(image_path, "rb") as image_file:
                files = {"file": image_file}
                response = requests.post(url, headers={"Authorization": self.headers["Authorization"]}, files=files)
                response.raise_for_status()
                return response.json().get("url")  # Return the uploaded image URL
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
