import requests


class APIHandler:
    def __init__(self, platform, auth_info):
        """
        Initialize APIHandler for a specific platform.
        :param platform: Platform name (e.g., 'naver', 'coupang', 'cafe24').
        :param auth_info: Authentication information for the platform.
        """
        self.platform = platform.lower()
        self.auth_info = auth_info
        self.base_url = self.get_base_url()

    def get_base_url(self):
        """
        Retrieve the base URL for the platform's API.
        """
        if self.platform == 'naver':
            return "https://api.naver.com"
        elif self.platform == 'coupang':
            return "https://api-gateway.coupang.com"
        elif self.platform == 'cafe24':
            return "https://api.cafe24.com"
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")

    def update_product(self, product_id, product_data):
        """
        Update a product on the platform.
        :param product_id: ID of the product to update.
        :param product_data: Dictionary containing updated product details.
        :return: API response as JSON.
        """
        if self.platform == 'naver':
            return self._update_product_naver(product_id, product_data)
        elif self.platform == 'coupang':
            return self._update_product_coupang(product_id, product_data)
        elif self.platform == 'cafe24':
            return self._update_product_cafe24(product_id, product_data)

    def delete_product(self, product_id):
        """
        Delete a product on the platform.
        :param product_id: ID of the product to delete.
        :return: API response as JSON.
        """
        if self.platform == 'naver':
            return self._delete_product_naver(product_id)
        elif self.platform == 'coupang':
            return self._delete_product_coupang(product_id)
        elif self.platform == 'cafe24':
            return self._delete_product_cafe24(product_id)

    # Private methods for Naver
    def _update_product_naver(self, product_id, product_data):
        url = f"{self.base_url}/product/{product_id}"
        headers = {"Authorization": f"Bearer {self.auth_info['token']}"}
        response = requests.put(url, headers=headers, json=product_data)
        return response.json()

    def _delete_product_naver(self, product_id):
        url = f"{self.base_url}/product/{product_id}"
        headers = {"Authorization": f"Bearer {self.auth_info['token']}"}
        response = requests.delete(url, headers=headers)
        return response.json()

    # Private methods for Coupang
    def _update_product_coupang(self, product_id, product_data):
        url = f"{self.base_url}/v2/providers/seller_api/apis/api/v1/marketplace/seller-products/{product_id}"
        headers = {"Authorization": f"Bearer {self.auth_info['token']}"}
        response = requests.put(url, headers=headers, json=product_data)
        return response.json()

    def _delete_product_coupang(self, product_id):
        url = f"{self.base_url}/v2/providers/seller_api/apis/api/v1/marketplace/seller-products/{product_id}"
        headers = {"Authorization": f"Bearer {self.auth_info['token']}"}
        response = requests.delete(url, headers=headers)
        return response.json()

    # Private methods for Cafe24
    def _update_product_cafe24(self, product_id, product_data):
        url = f"{self.base_url}/api/v2/admin/products/{product_id}"
        headers = {"Authorization": f"Bearer {self.auth_info['access_token']}"}
        response = requests.put(url, headers=headers, json=product_data)
        return response.json()

    def _delete_product_cafe24(self, product_id):
        url = f"{self.base_url}/api/v2/admin/products/{product_id}"
        headers = {"Authorization": f"Bearer {self.auth_info['access_token']}"}
        response = requests.delete(url, headers=headers)
        return response.json()
