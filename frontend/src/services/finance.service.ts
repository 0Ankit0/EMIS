import { apiClient } from '@/lib/api-client';
import {
    Fee,
    CreateFeeInput,
    PaginatedResponse,
} from '@/types/api.types';

class FinanceService {
    private baseUrl = '/finance';

    // Get fees
    async getFees(params?: {
        student_id?: number;
        status?: string;
        fee_type?: string;
    }): Promise<PaginatedResponse<Fee>> {
        return apiClient.get<PaginatedResponse<Fee>>(`${this.baseUrl}/fees/`, params);
    }

    // Create fee
    async createFee(data: CreateFeeInput): Promise<Fee> {
        return apiClient.post<Fee>(`${this.baseUrl}/fees/`, data);
    }

    // Get invoices
    async getInvoices(params?: any): Promise<PaginatedResponse<any>> {
        return apiClient.get<PaginatedResponse<any>>(`${this.baseUrl}/invoices/`, params);
    }

    // Record payment
    async recordPayment(feeId: number, data: { amount: number; payment_method: string }): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/fees/${feeId}/pay/`, data);
    }

    // Get pending fees
    async getPendingFees(): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/fees/pending/`);
    }

    // Get financial reports
    async getReports(params: { start_date: string; end_date: string }): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/reports/`, params);
    }

    // Get dashboard statistics
    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }
}

export const financeService = new FinanceService();
