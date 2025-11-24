import { apiClient } from '@/lib/api-client';
import {
    Attendance,
    MarkAttendanceInput,
    PaginatedResponse,
} from '@/types/api.types';

class AttendanceService {
    private baseUrl = '/attendance';

    // Get attendance records
    async getAttendance(params?: {
        date?: string;
        student_id?: number;
        grade?: string;
        section?: string;
    }): Promise<PaginatedResponse<Attendance>> {
        return apiClient.get<PaginatedResponse<Attendance>>(this.baseUrl + '/', params);
    }

    // Mark attendance
    async markAttendance(data: MarkAttendanceInput[]): Promise<Attendance[]> {
        return apiClient.post<Attendance[]>(`${this.baseUrl}/mark/`, { attendance: data });
    }

    // Get daily report
    async getDailyReport(date: string): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/daily-report/`, { date });
    }

    // Get statistics
    async getStatistics(params?: { start_date?: string; end_date?: string }): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`, params);
    }

    // Get absentees
    async getAbsentees(date: string): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/absentees/`, { date });
    }

    // Export attendance
    async exportAttendance(params: { start_date: string; end_date: string; format: 'csv' | 'pdf' }): Promise<Blob> {
        return apiClient.get<Blob>(`${this.baseUrl}/export/`, params);
    }
}

export const attendanceService = new AttendanceService();
