"""
Finance Service
"""
from utils.api_client import api_client


class FinanceService:
    @staticmethod
    def get_data():
        return api_client.get("/api/finance")

finance_service = FinanceService()
