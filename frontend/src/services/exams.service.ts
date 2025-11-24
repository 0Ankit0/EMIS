import { apiClient } from '@/lib/api-client';
import { Exam, Grade, PaginatedResponse } from '@/types/api.types';

class ExamService {
    private baseUrl = '/exams';

    async getExams(params?: any): Promise<PaginatedResponse<Exam>> {
        return apiClient.get<PaginatedResponse<Exam>>(this.baseUrl + '/', params);
    }

    async getExam(id: number): Promise<Exam> {
        return apiClient.get<Exam>(`${this.baseUrl}/${id}/`);
    }

    async createExam(data: any): Promise<Exam> {
        return apiClient.post<Exam>(this.baseUrl + '/', data);
    }

    async updateExam(id: number, data: any): Promise<Exam> {
        return apiClient.patch<Exam>(`${this.baseUrl}/${id}/`, data);
    }

    async getGrades(examId: number): Promise<Grade[]> {
        return apiClient.get<Grade[]>(`${this.baseUrl}/${examId}/grades/`);
    }

    async submitGrades(examId: number, grades: any[]): Promise<Grade[]> {
        return apiClient.post<Grade[]>(`${this.baseUrl}/${examId}/grades/`, { grades });
    }

    async getResults(examId: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/${examId}/results/`);
    }

    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }
}

export const examService = new ExamService();
