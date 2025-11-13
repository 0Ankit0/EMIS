"""Library_service"""
from utils.api_client import api_client

class library_service:
    @staticmethod
    def get_data():
        return api_client.get("/api/library")

library_service_instance = library_service()
