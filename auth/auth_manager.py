import json
import logging
from pathlib import Path

class AuthManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.auth_file = Path("data/auth_info.json")
        
    def load_auth_info(self):
        try:
            with open(self.auth_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"인증 정보 로드 실패: {str(e)}")
            return None
            
    def save_auth_info(self, auth_data):
        try:
            with open(self.auth_file, 'w') as f:
                json.dump(auth_data, f)
        except Exception as e:
            self.logger.error(f"인증 정보 저장 실패: {str(e)}") 