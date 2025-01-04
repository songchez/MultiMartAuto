import requests
from api.api_endpoints import NAVER_API_BASE_URL, API_ENDPOINTS

class APIHandler:
    def __init__(self, access_token):
        """
        Initialize APIHandler.
        :param access_token: OAuth 2.0 access token.
        """
        self.access_token = access_token

    def send_request(self, method, endpoint_key, data=None, query_params=None):
            """
            Send an HTTP request to the API.
            :param method: HTTP method (e.g., 'GET', 'POST').
            :param endpoint_key: Key to lookup endpoint in API_ENDPOINTS.
            :param data: Request payload.
            :param query_params: Query parameters for the request.
            :return: Response JSON or error message.
            """
            if endpoint_key not in API_ENDPOINTS:
                return {"error": f"Invalid endpoint key: {endpoint_key}"}

            endpoint = API_ENDPOINTS[endpoint_key]
            url = f"{NAVER_API_BASE_URL}{endpoint}"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }

            try:
                response = requests.request(method, url, headers=headers, json=data, params=query_params)

                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Error: {response.status_code} - {response.reason}")
                    print(f"Details: {response.text}")
                    return {"error": response.reason}
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                return {"error": str(e)}
    def list_categories(self):
        """
        Fetch categories from the API.
        :return: List of categories.
        """
        return self.send_request("GET", "categories")
