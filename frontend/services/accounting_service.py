"""
Accounting Service
"""
from utils.api_client import api_client


class AccountingService:
    @staticmethod
    def get_data():
        return api_client.get("/api/accounting")

accounting_service = AccountingService()
