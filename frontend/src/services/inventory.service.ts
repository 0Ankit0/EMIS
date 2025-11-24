import { apiClient } from '@/lib/api-client';

class InventoryService {
    private baseUrl = '/inventory';

    async getItems(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/items/`, params);
    }

    async getItem(id: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/items/${id}/`);
    }

    async createItem(data: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/items/`, data);
    }

    async updateItem(id: number, data: any): Promise<any> {
        return apiClient.patch<any>(`${this.baseUrl}/items/${id}/`, data);
    }

    async getCategories(): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/categories/`);
    }

    async getSuppliers(): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/suppliers/`);
    }

    async getStatistics(): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/statistics/`);
    }

    async getLowStockItems(): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/items/low-stock/`);
    }
}

export const inventoryService = new InventoryService();
