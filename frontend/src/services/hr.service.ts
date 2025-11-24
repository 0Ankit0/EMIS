import { apiClient } from '@/lib/api-client';
import { Employee, PaginatedResponse } from '@/types/api.types';

class HRService {
    private baseUrl = '/hr';

    async getEmployees(params?: any): Promise<PaginatedResponse<Employee>> {
        return apiClient.get<PaginatedResponse<Employee>>(`${this.baseUrl}/employees/`, params);
    }

    async getEmployee(id: number): Promise<Employee> {
        return apiClient.get<Employee>(`${this.baseUrl}/employees/${id}/`);
    }

    async createEmployee(data: any): Promise<Employee> {
        return apiClient.post<Employee>(`${this.baseUrl}/employees/`, data);
    }

    async updateEmployee(id: number, data: any): Promise<Employee> {
        return apiClient.patch<Employee>(`${this.baseUrl}/employees/${id}/`, data);
    }

    async getPayroll(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/payroll/`, params);
    }

    async getAttendance(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/attendance/`, params);
    }

    async getLeaveRequests(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/leave/`, params);
    }

    async submitLeaveRequest(data: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/leave/`, data);
    }

    async approveLeave(id: number): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/leave/${id}/approve/`, {});
    }

    async rejectLeave(id: number, reason: string): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/leave/${id}/reject/`, { reason });
    }

    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }
}

export const hrService = new HRService();
