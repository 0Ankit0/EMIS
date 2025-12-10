import { getAuthToken } from '@/lib/auth-utils';

const API_BASE_URL = '/api/admin';

export interface Permission {
    id: number;
    name: string;
    codename: string;
    content_type: number;
    content_type_name: string;
}

export interface ContentType {
    id: number;
    app_label: string;
    model: string;
}

const getAuthHeaders = () => ({
    'Authorization': `Token ${getAuthToken()}`,
    'Content-Type': 'application/json',
});

export const getPermissions = async (filters?: {
    content_type?: number;
    search?: string;
}): Promise<Permission[]> => {
    const params = new URLSearchParams();
    if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                params.append(key, value.toString());
            }
        });
    }
    
    const url = `${API_BASE_URL}/permissions/${params.toString() ? `?${params.toString()}` : ''}`;
    const response = await fetch(url, {
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch permissions');
    }
    
    return response.json();
};

export const getPermission = async (id: number): Promise<Permission> => {
    const response = await fetch(`${API_BASE_URL}/permissions/${id}/`, {
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch permission');
    }
    
    return response.json();
};

export const getContentTypes = async (): Promise<ContentType[]> => {
    const response = await fetch(`${API_BASE_URL}/content-types/`, {
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch content types');
    }
    
    return response.json();
};
