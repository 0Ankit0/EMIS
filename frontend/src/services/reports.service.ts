import { apiClient } from '@/lib/api-client';

class ReportService {
    private baseUrl = '/reports';

    async generateReport(type: string, params: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/generate/`, { type, ...params });
    }

    async getAcademicReports(params: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/academic/`, params);
    }

    async getFinancialReports(params: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/financial/`, params);
    }

    async getAttendanceReports(params: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/attendance/`, params);
    }

    async exportReport(id: number, format: 'pdf' | 'csv' | 'excel'): Promise<Blob> {
        return apiClient.get<Blob>(`${this.baseUrl}/${id}/export/`, { format });
    }
}

export const reportService = new ReportService();
