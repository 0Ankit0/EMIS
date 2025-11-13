"""
Faculty Service
Handles all faculty-related API calls
"""
from utils.api_client import api_client
from typing import Dict, List, Optional


class FacultyService:
    """Faculty service for API operations"""
    
    @staticmethod
    def get_profile(faculty_id: int) -> Dict:
        """Get faculty profile"""
        return api_client.get(f"/api/faculty/{faculty_id}")
    
    @staticmethod
    def update_profile(faculty_id: int, data: Dict) -> Dict:
        """Update faculty profile"""
        return api_client.put(f"/api/faculty/{faculty_id}", data)
    
    @staticmethod
    def get_dashboard(faculty_id: int) -> Dict:
        """Get faculty dashboard data"""
        return api_client.get(f"/api/faculty/{faculty_id}/dashboard")
    
    @staticmethod
    def get_courses(faculty_id: int) -> List[Dict]:
        """Get teaching courses"""
        response = api_client.get(f"/api/faculty/{faculty_id}/courses")
        return response.get("items", [])
    
    @staticmethod
    def get_course_students(course_id: int) -> List[Dict]:
        """Get students in a course"""
        response = api_client.get(f"/api/courses/{course_id}/students")
        return response.get("items", [])
    
    @staticmethod
    def mark_attendance(course_id: int, date: str, attendance_data: List[Dict]) -> Dict:
        """Mark attendance for a class"""
        data = {
            "course_id": course_id,
            "date": date,
            "attendance": attendance_data
        }
        return api_client.post("/api/attendance/mark", data)
    
    @staticmethod
    def get_attendance_report(course_id: int, from_date: str, to_date: str) -> Dict:
        """Get attendance report"""
        params = {"from_date": from_date, "to_date": to_date}
        return api_client.get(f"/api/courses/{course_id}/attendance/report", params=params)
    
    @staticmethod
    def create_assignment(data: Dict) -> Dict:
        """Create new assignment"""
        return api_client.post("/api/assignments", data)
    
    @staticmethod
    def get_assignments(course_id: int) -> List[Dict]:
        """Get course assignments"""
        response = api_client.get(f"/api/courses/{course_id}/assignments")
        return response.get("items", [])
    
    @staticmethod
    def get_submissions(assignment_id: int) -> List[Dict]:
        """Get assignment submissions"""
        response = api_client.get(f"/api/assignments/{assignment_id}/submissions")
        return response.get("items", [])
    
    @staticmethod
    def grade_submission(submission_id: int, marks: float, feedback: str) -> Dict:
        """Grade an assignment submission"""
        data = {
            "marks": marks,
            "feedback": feedback
        }
        return api_client.put(f"/api/submissions/{submission_id}/grade", data)
    
    @staticmethod
    def upload_course_material(course_id: int, title: str, description: str, file) -> Dict:
        """Upload course material"""
        data = {
            "course_id": course_id,
            "title": title,
            "description": description
        }
        files = {'file': file}
        return api_client.post("/api/courses/materials", data=data, files=files)
    
    @staticmethod
    def enter_marks(exam_id: int, marks_data: List[Dict]) -> Dict:
        """Enter exam marks"""
        data = {
            "exam_id": exam_id,
            "marks": marks_data
        }
        return api_client.post("/api/exams/marks", data)
    
    @staticmethod
    def get_gradebook(course_id: int) -> Dict:
        """Get course gradebook"""
        return api_client.get(f"/api/courses/{course_id}/gradebook")
    
    @staticmethod
    def apply_leave(faculty_id: int, from_date: str, to_date: str, reason: str) -> Dict:
        """Apply for leave"""
        data = {
            "faculty_id": faculty_id,
            "from_date": from_date,
            "to_date": to_date,
            "reason": reason
        }
        return api_client.post("/api/faculty/leave", data)


# Singleton instance
faculty_service = FacultyService()
