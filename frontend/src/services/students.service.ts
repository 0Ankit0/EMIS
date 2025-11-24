import { apiClient } from '@/lib/api-client';
import {
    Student,
    CreateStudentInput,
    PaginatedResponse,
    APIResponse,
} from '@/types/api.types';

class StudentService {
    private baseUrl = '/students';

    // Get all students with pagination
    async getStudents(params?: {
        page?: number;
        search?: string;
        grade?: string;
        section?: string;
        status?: string;
    }): Promise<PaginatedResponse<Student>> {
        return apiClient.get<PaginatedResponse<Student>>(this.baseUrl + '/', params);
    }

    // Get single student
    async getStudent(id: number): Promise<Student> {
        return apiClient.get<Student>(`${this.baseUrl}/${id}/`);
    }

    // Create student
    async createStudent(data: CreateStudentInput): Promise<Student> {
        return apiClient.post<Student>(this.baseUrl + '/', data);
    }

    // Update student
    async updateStudent(id: number, data: Partial<CreateStudentInput>): Promise<Student> {
        return apiClient.patch<Student>(`${this.baseUrl}/${id}/`, data);
    }

    // Delete student
    async deleteStudent(id: number): Promise<void> {
        return apiClient.delete<void>(`${this.baseUrl}/${id}/`);
    }

    // Get student statistics
    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }
}

export const studentService = new StudentService();
