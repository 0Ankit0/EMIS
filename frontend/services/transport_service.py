"""Transport_service"""
from utils.api_client import api_client

class transport_service:
    @staticmethod
    def get_data():
        return api_client.get("/api/transport")

transport_service_instance = transport_service()
