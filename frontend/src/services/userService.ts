import { getAuthToken } from '@/lib/auth-utils';

const API_BASE_URL = '/api/admin';

export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    is_active: boolean;
    is_staff: boolean;
    is_superuser: boolean;
    groups: number[] | string[];
    date_joined: string;
    last_login: string | null;
}

export interface UserCreate {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    password: string;
    is_active?: boolean;
    is_staff?: boolean;
    is_superuser?: boolean;
    groups?: number[];
}

export interface UserUpdate {
    username?: string;
    email?: string;
    first_name?: string;
    last_name?: string;
    password?: string;
    is_active?: boolean;
    is_staff?: boolean;
    is_superuser?: boolean;
    groups?: number[];
}

const getAuthHeaders = () => ({
    'Authorization': `Token ${getAuthToken()}`,
    'Content-Type': 'application/json',
});

export const getUsers = async (filters?: {
    is_active?: boolean;
    is_staff?: boolean;
    is_superuser?: boolean;
    group?: number;
    search?: string;
}): Promise<User[]> => {
    const params = new URLSearchParams();
    if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                params.append(key, value.toString());
            }
        });
    }
    
    const url = `${API_BASE_URL}/users/${params.toString() ? `?${params.toString()}` : ''}`;
    const response = await fetch(url, {
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch users');
    }
    
    return response.json();
};

export const getUser = async (id: number): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/`, {
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch user');
    }
    
    return response.json();
};

export const createUser = async (data: UserCreate): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/users/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create user');
    }
    
    return response.json();
};

export const updateUser = async (id: number, data: UserUpdate): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update user');
    }
    
    return response.json();
};

export const deleteUser = async (id: number): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to delete user');
    }
};

export const activateUser = async (id: number): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/activate/`, {
        method: 'POST',
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to activate user');
    }
    
    return response.json();
};

export const deactivateUser = async (id: number): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/deactivate/`, {
        method: 'POST',
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to deactivate user');
    }
    
    return response.json();
};

export const resetUserPassword = async (id: number, password: string): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/users/${id}/reset_password/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ password }),
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to reset password');
    }
};
