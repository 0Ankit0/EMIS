import { apiClient } from '@/lib/api-client';
import {
    Book,
    BookIssue,
    IssueBookInput,
    PaginatedResponse,
} from '@/types/api.types';

class LibraryService {
    private baseUrl = '/library';

    // Get books
    async getBooks(params?: {
        search?: string;
        category?: string;
        author?: string;
        status?: string;
    }): Promise<PaginatedResponse<Book>> {
        return apiClient.get<PaginatedResponse<Book>>(`${this.baseUrl}/books/`, params);
    }

    // Get single book
    async getBook(id: number): Promise<Book> {
        return apiClient.get<Book>(`${this.baseUrl}/books/${id}/`);
    }

    // Add book
    async addBook(data: any): Promise<Book> {
        return apiClient.post<Book>(`${this.baseUrl}/books/`, data);
    }

    // Issue book
    async issueBook(data: IssueBookInput): Promise<BookIssue> {
        return apiClient.post<BookIssue>(`${this.baseUrl}/issues/`, data);
    }

    // Get issued books
    async getIssuedBooks(params?: { student_id?: number; status?: string }): Promise<PaginatedResponse<BookIssue>> {
        return apiClient.get<PaginatedResponse<BookIssue>>(`${this.baseUrl}/issues/`, params);
    }

    // Return book
    async returnBook(issueId: number): Promise<BookIssue> {
        return apiClient.post<BookIssue>(`${this.baseUrl}/issues/${issueId}/return/`, {});
    }

    // Get overdue books
    async getOverdueBooks(): Promise<BookIssue[]> {
        return apiClient.get<BookIssue[]>(`${this.baseUrl}/issues/overdue/`);
    }

    //Get library statistics
    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }

    // Get reports
    async getReports(params: { start_date: string; end_date: string }): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/reports/`, params);
    }
}

export const libraryService = new LibraryService();
