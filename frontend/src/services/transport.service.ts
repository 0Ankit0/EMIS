import { apiClient } from '@/lib/api-client';

class TransportService {
    private baseUrl = '/transport';

    async getVehicles(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/vehicles/`, params);
    }

    async getVehicle(id: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/vehicles/${id}/`);
    }

    async createVehicle(data: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/vehicles/`, data);
    }

    async getRoutes(): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/routes/`);
    }

    async getRoute(id: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/routes/${id}/`);
    }

    async getDrivers(): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/drivers/`);
    }

    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }
}

export const transportService = new TransportService();
