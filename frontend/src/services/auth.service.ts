import { apiClient } from '@/lib/api-client';

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface RegisterData {
    username: string;
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
}

export interface AuthResponse {
    user: User;
    access: string;
    refresh: string;
    access_expires_in: number;
    refresh_expires_in: number;
}

export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
    is_active: boolean;
}

class AuthService {
    async login(credentials: LoginCredentials): Promise<AuthResponse> {
        const response = await apiClient.post<AuthResponse>('/auth/login/', credentials);

        // Store tokens
        if (typeof window !== 'undefined') {
            localStorage.setItem('access_token', response.access);
            localStorage.setItem('refresh_token', response.refresh);
            localStorage.setItem('user', JSON.stringify(response.user));
        }

        return response;
    }

    async register(data: RegisterData): Promise<User> {
        const response = await apiClient.post<User>('/auth/register/', data);
        return response;
    }

    async logout(): Promise<void> {
        try {
            await apiClient.post('/auth/logout/');
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            if (typeof window !== 'undefined') {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
            }
        }
    }

    async getCurrentUser(): Promise<User> {
        return apiClient.get<User>('/auth/me/');
    }

    isAuthenticated(): boolean {
        if (typeof window === 'undefined') return false;
        return !!localStorage.getItem('access_token');
    }

    getAccessToken(): string | null {
        if (typeof window === 'undefined') return null;
        return localStorage.getItem('access_token');
    }

    getStoredUser(): User | null {
        if (typeof window === 'undefined') return null;
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }
}

export const authService = new AuthService();
export default authService;
