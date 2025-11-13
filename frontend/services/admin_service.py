"""Admin_service"""
from utils.api_client import api_client

class admin_service:
    @staticmethod
    def get_data():
        return api_client.get("/api/admin")

admin_service_instance = admin_service()
