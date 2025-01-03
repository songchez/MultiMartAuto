import os
import json
from cryptography.fernet import Fernet

class AuthManager:
    def __init__(self, file_path='../data/auth_info.json'):
        """
        Initialize the AuthManager.
        :param file_path: Path to the file where authentication information will be stored.
        """
        self.file_path = file_path
        self.key = os.getenv('AUTH_KEY') or Fernet.generate_key()
        self.cipher = Fernet(self.key)

        # Prompt the user to securely save the key if not already set
        if not os.getenv('AUTH_KEY'):
            print("Save this key securely:", self.key.decode())

    def save_auth_info(self, platform, client_id, client_secret):
        """
        Save authentication information for a platform.
        :param platform: Platform name (e.g., 'Naver', 'Coupang', 'Cafe24').
        :param client_id: Client ID for the platform.
        :param client_secret: Client Secret for the platform.
        """
        auth_data = {platform: {"client_id": client_id, "client_secret": client_secret}}
        encrypted_data = self.cipher.encrypt(json.dumps(auth_data).encode())

        # Save encrypted data to file
        with open(self.file_path, 'wb') as file:
            file.write(encrypted_data)

        print(f"Authentication information for {platform} saved successfully.")

    def load_auth_info(self, platform):
        """
        Load authentication information for a platform.
        :param platform: Platform name to retrieve authentication information for.
        :return: Authentication details or None if not found.
        """
        try:
            with open(self.file_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = self.cipher.decrypt(encrypted_data).decode()
            auth_data = json.loads(decrypted_data)
            return auth_data.get(platform)
        except Exception as e:
            print(f"Error loading authentication info for {platform}: {e}")
            return None