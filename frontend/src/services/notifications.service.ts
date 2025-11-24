import { apiClient } from '@/lib/api-client';

class NotificationService {
    private baseUrl = '/notifications';

    async getNotifications(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/`, params);
    }

    async sendNotification(data: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/send/`, data);
    }

    async getTemplates(): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/templates/`);
    }

    async markAsRead(id: number): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/${id}/read/`, {});
    }

    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }
}

export const notificationService = new NotificationService();
