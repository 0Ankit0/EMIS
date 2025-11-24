import { apiClient } from '@/lib/api-client';

class TimetableService {
    private baseUrl = '/timetable';

    async getTimetable(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/`, params);
    }

    async createTimetable(data: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/`, data);
    }

    async getClassSchedule(classId: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/class/${classId}/`);
    }

    async getTeacherSchedule(teacherId: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/teacher/${teacherId}/`);
    }

    async getRoomSchedule(roomId: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/room/${roomId}/`);
    }

    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }
}

export const timetableService = new TimetableService();
