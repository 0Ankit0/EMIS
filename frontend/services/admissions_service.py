"""Admissions_service"""
from utils.api_client import api_client

class admissions_service:
    @staticmethod
    def get_data():
        return api_client.get("/api/admissions")

admissions_service_instance = admissions_service()
