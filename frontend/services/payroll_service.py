"""
Payroll Service
"""
from utils.api_client import api_client


class PayrollService:
    @staticmethod
    def get_data():
        return api_client.get("/api/payroll")

payroll_service = PayrollService()
