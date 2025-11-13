"""Hr_service"""
from utils.api_client import api_client

class hr_service:
    @staticmethod
    def get_data():
        return api_client.get("/api/hr")

hr_service_instance = hr_service()
