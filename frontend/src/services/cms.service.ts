import { apiClient } from '@/lib/api-client';

class CMSService {
    private baseUrl = '/cms';

    async getPages(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/pages/`, params);
    }

    async getPage(id: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/pages/${id}/`);
    }

    async createPage(data: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/pages/`, data);
    }

    async updatePage(id: number, data: any): Promise<any> {
        return apiClient.patch<any>(`${this.baseUrl}/pages/${id}/`, data);
    }

    async getAnnouncements(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/announcements/`, params);
    }

    async getAnnouncement(id: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/announcements/${id}/`);
    }

    async createAnnouncement(data: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/announcements/`, data);
    }

    async getEvents(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/events/`, params);
    }

    async getEvent(id: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/events/${id}/`);
    }

    async createEvent(data: any): Promise<any> {
        return apiClient.post<any>(`${this.baseUrl}/events/`, data);
    }

    async getGalleries(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/galleries/`, params);
    }

    async getGallery(id: number): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/galleries/${id}/`);
    }

    async getMenus(): Promise<any[]> {
        return apiClient.get<any[]>(`${this.baseUrl}/menus/`);
    }

    async getMediaLibrary(params?: any): Promise<any> {
        return apiClient.get<any>(`${this.baseUrl}/media/`, params);
    }

    async uploadMedia(file: File): Promise<any> {
        return apiClient.upload<any>(`${this.baseUrl}/media/upload/`, file);
    }
}

export const cmsService = new CMSService();
