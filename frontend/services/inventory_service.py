"""Inventory_service"""
from utils.api_client import api_client

class inventory_service:
    @staticmethod
    def get_data():
        return api_client.get("/api/inventory")

inventory_service_instance = inventory_service()
