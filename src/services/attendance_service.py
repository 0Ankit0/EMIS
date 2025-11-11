"""Attendance Service for EMIS"""
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from uuid import UUID

from src.models.attendance import (
    Attendance, AttendanceSession, LeaveRequest,
    AttendanceStatus, LeaveRequestStatus
)
from src.lib.logging import get_logger

logger = get_logger(__name__)


class AttendanceService:
    """Service for managing student attendance and leave requests"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # Core attendance marking
    async def mark_attendance(
        self,
        student_id: UUID,
        course_id: UUID,
        attendance_date: date,
        status: AttendanceStatus,
        marked_by: UUID,
        **kwargs
    ) -> Attendance:
        """Mark attendance for a student"""
        
        # Check if attendance already exists for this date
        result = await self.db.execute(
            select(Attendance).where(
                and_(
                    Attendance.student_id == student_id,
                    Attendance.course_id == course_id,
                    Attendance.date == attendance_date
                )
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing attendance
            existing.status = status
            existing.marked_by = marked_by
            existing.marked_at = datetime.utcnow()
            for key, value in kwargs.items():
                setattr(existing, key, value)
            
            await self.db.commit()
            await self.db.refresh(existing)
            
            logger.info(f"Updated attendance for student {student_id} on {attendance_date}: {status}")
            return existing
        
        # Create new attendance record
        attendance = Attendance(
            student_id=student_id,
            course_id=course_id,
            date=attendance_date,
            status=status,
            marked_by=marked_by,
            marked_at=datetime.utcnow(),
            **kwargs
        )
        
        self.db.add(attendance)
        await self.db.commit()
        await self.db.refresh(attendance)
        
        logger.info(f"Marked attendance for student {student_id} on {attendance_date}: {status}")
        
        return attendance
    
    # T064: Leave request workflow
    async def create_leave_request(
        self,
        student_id: UUID,
        course_id: UUID,
        subject_teacher_id: UUID,
        leave_date: date,
        leave_type: str,
        reason: str,
        supporting_document_url: Optional[str] = None
    ) -> LeaveRequest:
        """Student creates a leave request"""
        
        # Check if leave already requested for this date and course
        result = await self.db.execute(
            select(LeaveRequest).where(
                and_(
                    LeaveRequest.student_id == student_id,
                    LeaveRequest.course_id == course_id,
                    LeaveRequest.leave_date == leave_date,
                    LeaveRequest.status != LeaveRequestStatus.REJECTED,
                    LeaveRequest.status != LeaveRequestStatus.CANCELLED
                )
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            raise ValueError(f"Leave already requested for {leave_date}")
        
        leave_request = LeaveRequest(
            student_id=student_id,
            course_id=course_id,
            subject_teacher_id=subject_teacher_id,
            leave_date=leave_date,
            leave_type=leave_type,
            reason=reason,
            supporting_document_url=supporting_document_url,
            status=LeaveRequestStatus.PENDING
        )
        
        self.db.add(leave_request)
        await self.db.commit()
        await self.db.refresh(leave_request)
        
        logger.info(f"Leave request created for student {student_id} on {leave_date}")
        
        return leave_request
    
    async def get_pending_leave_requests(
        self,
        teacher_id: UUID,
        course_id: Optional[UUID] = None
    ) -> List[LeaveRequest]:
        """Get pending leave requests for a teacher"""
        
        query = select(LeaveRequest).where(
            and_(
                LeaveRequest.subject_teacher_id == teacher_id,
                LeaveRequest.status == LeaveRequestStatus.PENDING
            )
        )
        
        if course_id:
            query = query.where(LeaveRequest.course_id == course_id)
        
        query = query.order_by(LeaveRequest.requested_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def approve_leave_request(
        self,
        leave_request_id: UUID,
        approved_by: UUID
    ) -> LeaveRequest:
        """Teacher approves leave request"""
        
        result = await self.db.execute(
            select(LeaveRequest).where(LeaveRequest.id == leave_request_id)
        )
        leave_request = result.scalar_one_or_none()
        
        if not leave_request:
            raise ValueError(f"Leave request {leave_request_id} not found")
        
        if leave_request.status != LeaveRequestStatus.PENDING:
            raise ValueError(f"Leave request is not pending (current status: {leave_request.status})")
        
        # Update leave request status
        leave_request.status = LeaveRequestStatus.APPROVED
        leave_request.approved_by = approved_by
        leave_request.approved_at = datetime.utcnow()
        
        await self.db.commit()
        
        # T065: Automatically mark attendance as LEAVE
        await self.mark_attendance_as_leave(leave_request)
        
        await self.db.refresh(leave_request)
        
        logger.info(f"Leave request {leave_request_id} approved by {approved_by}")
        
        return leave_request
    
    async def reject_leave_request(
        self,
        leave_request_id: UUID,
        rejected_by: UUID,
        rejection_reason: str
    ) -> LeaveRequest:
        """Teacher rejects leave request"""
        
        result = await self.db.execute(
            select(LeaveRequest).where(LeaveRequest.id == leave_request_id)
        )
        leave_request = result.scalar_one_or_none()
        
        if not leave_request:
            raise ValueError(f"Leave request {leave_request_id} not found")
        
        if leave_request.status != LeaveRequestStatus.PENDING:
            raise ValueError(f"Leave request is not pending")
        
        leave_request.status = LeaveRequestStatus.REJECTED
        leave_request.approved_by = rejected_by
        leave_request.approved_at = datetime.utcnow()
        leave_request.rejection_reason = rejection_reason
        
        await self.db.commit()
        await self.db.refresh(leave_request)
        
        logger.info(f"Leave request {leave_request_id} rejected by {rejected_by}")
        
        return leave_request
    
    # T065: Automatic leave marking on approval
    async def mark_attendance_as_leave(
        self,
        leave_request: LeaveRequest
    ) -> Attendance:
        """Automatically mark attendance as LEAVE when request is approved"""
        
        attendance = await self.mark_attendance(
            student_id=leave_request.student_id,
            course_id=leave_request.course_id,
            attendance_date=leave_request.leave_date,
            status=AttendanceStatus.LEAVE,
            marked_by=leave_request.approved_by,
            reason=f"Leave approved: {leave_request.reason}",
            is_excused=True
        )
        
        logger.info(f"Automatically marked attendance as LEAVE for student {leave_request.student_id} on {leave_request.leave_date}")
        
        return attendance
    
    # Attendance percentage calculation
    async def calculate_attendance_percentage(
        self,
        student_id: UUID,
        course_id: Optional[UUID] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        """Calculate attendance percentage for a student"""
        
        query = select(Attendance).where(Attendance.student_id == student_id)
        
        if course_id:
            query = query.where(Attendance.course_id == course_id)
        
        if start_date:
            query = query.where(Attendance.date >= start_date)
        
        if end_date:
            query = query.where(Attendance.date <= end_date)
        
        result = await self.db.execute(query)
        attendance_records = result.scalars().all()
        
        total_classes = len(attendance_records)
        
        if total_classes == 0:
            return {
                'total_classes': 0,
                'present': 0,
                'absent': 0,
                'late': 0,
                'leave': 0,
                'percentage': 0.0
            }
        
        present_count = len([a for a in attendance_records if a.status == AttendanceStatus.PRESENT])
        absent_count = len([a for a in attendance_records if a.status == AttendanceStatus.ABSENT])
        late_count = len([a for a in attendance_records if a.status == AttendanceStatus.LATE])
        leave_count = len([a for a in attendance_records if a.status == AttendanceStatus.LEAVE])
        
        # Calculate percentage (present + late + leave counted as attended)
        attended = present_count + late_count + leave_count
        percentage = (attended / total_classes) * 100 if total_classes > 0 else 0.0
        
        return {
            'total_classes': total_classes,
            'present': present_count,
            'absent': absent_count,
            'late': late_count,
            'leave': leave_count,
            'attended': attended,
            'percentage': round(percentage, 2)
        }
    
    # Low attendance alerts
    async def get_low_attendance_students(
        self,
        course_id: UUID,
        threshold_percentage: float = 75.0
    ) -> List[dict]:
        """Get students with attendance below threshold"""
        
        # Get all students for the course
        result = await self.db.execute(
            select(Attendance.student_id).where(
                Attendance.course_id == course_id
            ).distinct()
        )
        student_ids = [row[0] for row in result.all()]
        
        low_attendance_students = []
        
        for student_id in student_ids:
            stats = await self.calculate_attendance_percentage(
                student_id=student_id,
                course_id=course_id
            )
            
            if stats['percentage'] < threshold_percentage:
                low_attendance_students.append({
                    'student_id': student_id,
                    **stats
                })
        
        logger.info(f"Found {len(low_attendance_students)} students with <{threshold_percentage}% attendance in course {course_id}")
        
        return low_attendance_students
    
    # Bulk attendance marking
    async def create_attendance_session(
        self,
        course_id: UUID,
        instructor_id: UUID,
        session_date: date,
        academic_year: str,
        semester: str,
        **kwargs
    ) -> AttendanceSession:
        """Create attendance session for bulk marking"""
        
        session = AttendanceSession(
            course_id=course_id,
            instructor_id=instructor_id,
            session_date=session_date,
            academic_year=academic_year,
            semester=semester,
            **kwargs
        )
        
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        
        logger.info(f"Created attendance session for course {course_id} on {session_date}")
        
        return session
    
    async def bulk_mark_attendance(
        self,
        session_id: UUID,
        attendance_data: List[dict],
        marked_by: UUID
    ) -> AttendanceSession:
        """Bulk mark attendance for a session"""
        
        result = await self.db.execute(
            select(AttendanceSession).where(AttendanceSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise ValueError(f"Attendance session {session_id} not found")
        
        # Mark attendance for each student
        for data in attendance_data:
            await self.mark_attendance(
                student_id=data['student_id'],
                course_id=session.course_id,
                attendance_date=session.session_date,
                status=AttendanceStatus(data['status']),
                marked_by=marked_by,
                academic_year=session.academic_year,
                semester=session.semester,
                period=session.period,
                room=session.room,
                instructor_id=session.instructor_id
            )
        
        # Update session stats
        session.total_students = len(attendance_data)
        session.present_count = len([d for d in attendance_data if d['status'] == 'present'])
        session.absent_count = len([d for d in attendance_data if d['status'] == 'absent'])
        session.late_count = len([d for d in attendance_data if d['status'] == 'late'])
        session.leave_count = len([d for d in attendance_data if d['status'] == 'leave'])
        session.is_completed = True
        
        await self.db.commit()
        await self.db.refresh(session)
        
        logger.info(f"Bulk marked attendance for {len(attendance_data)} students in session {session_id}")
        
        return session
