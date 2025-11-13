"""
Student Service
Handles all student-related API calls
"""
from utils.api_client import api_client
from typing import Dict, List, Optional


class StudentService:
    """Student service for API operations"""
    
    @staticmethod
    def get_profile(student_id: int) -> Dict:
        """Get student profile"""
        return api_client.get(f"/api/students/{student_id}")
    
    @staticmethod
    def update_profile(student_id: int, data: Dict) -> Dict:
        """Update student profile"""
        return api_client.put(f"/api/students/{student_id}", data)
    
    @staticmethod
    def get_dashboard(student_id: int) -> Dict:
        """Get student dashboard data"""
        return api_client.get(f"/api/students/{student_id}/dashboard")
    
    @staticmethod
    def get_courses(student_id: int) -> List[Dict]:
        """Get enrolled courses"""
        response = api_client.get(f"/api/students/{student_id}/courses")
        return response.get("items", [])
    
    @staticmethod
    def get_assignments(student_id: int, status: Optional[str] = None) -> List[Dict]:
        """Get assignments"""
        params = {"status": status} if status else {}
        response = api_client.get(f"/api/students/{student_id}/assignments", params=params)
        return response.get("items", [])
    
    @staticmethod
    def submit_assignment(assignment_id: int, file) -> Dict:
        """Submit assignment"""
        files = {'file': file}
        return api_client.post(f"/api/assignments/{assignment_id}/submit", files=files)
    
    @staticmethod
    def get_attendance(student_id: int) -> Dict:
        """Get attendance summary"""
        return api_client.get(f"/api/students/{student_id}/attendance/summary")
    
    @staticmethod
    def apply_leave(student_id: int, data: Dict) -> Dict:
        """Apply for leave"""
        return api_client.post("/api/students/leave", data)
    
    @staticmethod
    def get_exams(student_id: int) -> List[Dict]:
        """Get exam schedule"""
        response = api_client.get(f"/api/students/{student_id}/exams/upcoming")
        return response.get("items", [])
    
    @staticmethod
    def get_results(student_id: int) -> List[Dict]:
        """Get exam results"""
        response = api_client.get(f"/api/students/{student_id}/results")
        return response.get("items", [])
    
    @staticmethod
    def get_fees(student_id: int) -> Dict:
        """Get fee information"""
        return api_client.get(f"/api/students/{student_id}/fees/pending")
    
    @staticmethod
    def make_payment(student_id: int, amount: float, method: str) -> Dict:
        """Make fee payment"""
        data = {
            "student_id": student_id,
            "amount": amount,
            "payment_method": method
        }
        return api_client.post("/api/students/payments", data)
    
    @staticmethod
    def get_library_books(student_id: int) -> List[Dict]:
        """Get issued library books"""
        response = api_client.get(f"/api/students/{student_id}/library/issued")
        return response.get("items", [])
    
    @staticmethod
    def search_books(query: str, category: Optional[str] = None) -> List[Dict]:
        """Search library books"""
        params = {"query": query}
        if category:
            params["category"] = category
        response = api_client.get("/api/library/books/search", params=params)
        return response.get("items", [])


# Singleton instance
student_service = StudentService()
