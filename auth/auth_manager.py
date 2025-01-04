import requests
import time
import bcrypt
import pybase64

class AuthManager:
    def __init__(self, client_id, client_secret):
        """
        Initialize the AuthManager with client credentials.
        :param client_id: Application client ID.
        :param client_secret: Application client secret.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://api.commerce.naver.com/external/v1/oauth2/token"
        self.access_token = None

    def generate_signature(self, timestamp):
        """
        Generate the client_secret_sign using HMAC-SHA256.
        :param timestamp: Unix timestamp in milliseconds.
        :return: Base64 encoded signature.
        """
        password = self.client_id + "_" +str(timestamp)

        # utf-8로 인코딩한 후 해시화
        hashed = bcrypt.hashpw(password.encode('utf-8'), self.client_secret.encode('utf-8'))

        # base64 인코딩
        return pybase64.standard_b64encode(hashed).decode('utf-8')


    def get_access_token(self, token_type="SELF", account_id=None):
        """
        Request and retrieve an access token from the OAuth server.
        :param token_type: Type of the token (e.g., 'SELF', 'SELLER').
        :param account_id: Account ID or UID (required if type is 'SELLER').
        :return: Access token as a string.
        """
        try:
            timestamp = int(time.time() * 1000)  # Current Unix timestamp in milliseconds
            signature = self.generate_signature(timestamp)

            payload = {
                "client_id": self.client_id,
                "timestamp": timestamp,
                "grant_type": "client_credentials",
                "client_secret_sign": signature,
                "type": token_type
            }

            if token_type == "SELLER" and account_id:
                payload["account_id"] = account_id

            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(self.token_url, data=payload, headers=headers, timeout=30)
            print(response.json())
            
            # Handle HTTP response codes
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                return self.access_token
            elif response.status_code == 400:
                print("Bad Request: Check your payload or parameters.")
            elif response.status_code == 401:
                print("Unauthorized: Check your client_id and client_secret.")
            elif response.status_code == 403:
                print("Forbidden: You do not have permission to access this resource.")
            elif response.status_code == 429:
                print("Too Many Requests: You have exceeded your request quota.")
            elif response.status_code == 500:
                print("Internal Server Error: The server encountered an unexpected condition.")
            else:
                print(f"Unexpected error: {response.status_code} - {response.reason}")

            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching access token: {e}")
            return None
