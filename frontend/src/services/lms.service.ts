import { apiClient } from '@/lib/api-client';
import { Course, PaginatedResponse } from '@/types/api.types';

class LMSService {
    private baseUrl = '/lms';

    async getCourses(params?: any): Promise<PaginatedResponse<Course>> {
        return apiClient.get<PaginatedResponse<Course>>(`${this.baseUrl}/courses/`, params);
    }

    async getCourse(id: number): Promise<Course> {
        return apiClient.get<Course>(`${this.baseUrl}/courses/${id}/`);
    }

    async getAssignments(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/assignments/`, params);
    }

    async getAssignment(id: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/assignments/${id}/`);
    }

    async submitAssignment(id: number, data: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/assignments/${id}/submit/`, data);
    }

    async getQuizzes(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/quizzes/`, params);
    }

    async getQuiz(id: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/quizzes/${id}/`);
    }

    async submitQuiz(id: number, answers: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/quizzes/${id}/submit/`, { answers });
    }

    async getDiscussions(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/discussions/`, params);
    }

    async getCertificates(): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/certificates/`);
    }

    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }
}

export const lmsService = new LMSService();
