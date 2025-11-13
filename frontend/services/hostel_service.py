"""Hostel_service"""
from utils.api_client import api_client

class hostel_service:
    @staticmethod
    def get_data():
        return api_client.get("/api/hostel")

hostel_service_instance = hostel_service()
