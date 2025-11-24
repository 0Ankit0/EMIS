import { apiClient } from '@/lib/api-client';

class AnalyticsService {
    private baseUrl = '/analytics';

    async getDashboardStats(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/dashboard/`);
    }

    async getStudentAnalytics(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/students/`, params);
    }

    async getFinancialAnalytics(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/financial/`, params);
    }

    async getAcademicAnalytics(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/academic/`, params);
    }

    async getAttendanceAnalytics(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/attendance/`, params);
    }

    async exportAnalytics(type: string, params: any): Promise<Blob> {
        return apiClient.get<Blob>(`${this.baseUrl}/${type}/export/`, params);
    }
}

export const analyticsService = new AnalyticsService();
