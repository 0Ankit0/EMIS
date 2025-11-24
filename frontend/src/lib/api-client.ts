import axios, { AxiosInstance, AxiosError } from 'axios';
import { APIError, AuthenticationError, ValidationError, NotFoundError, AuthorizationError } from '@/types/api.types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class APIClient {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: API_URL,
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 30000, // 30 seconds
        });

        // Request interceptor
        this.client.interceptors.request.use(
            (config) => {
                // Add auth token
                const token = this.getToken();
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }

                // Log request in development
                if (process.env.NODE_ENV === 'development') {
                    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data);
                }

                return config;
            },
            (error) => Promise.reject(error)
        );

        // Response interceptor
        this.client.interceptors.response.use(
            (response) => {
                // Log response in development
                if (process.env.NODE_ENV === 'development') {
                    console.log(`[API Response] ${response.config.url}`, response.data);
                }
                return response;
            },
            async (error: AxiosError) => {
                // Log error in development
                if (process.env.NODE_ENV === 'development') {
                    console.error(`[API Error] ${error.config?.url}`, error.response?.data);
                }

                // Handle 401 - Token expired
                if (error.response?.status === 401) {
                    const originalRequest: any = error.config;

                    if (!originalRequest._retry) {
                        originalRequest._retry = true;

                        try {
                            const refreshToken = this.getRefreshToken();
                            if (refreshToken) {
                                const { data } = await axios.post(`${API_URL}/auth/refresh/`, {
                                    refresh: refreshToken,
                                });

                                this.setToken(data.access);
                                originalRequest.headers.Authorization = `Bearer ${data.access}`;

                                return this.client(originalRequest);
                            }
                        } catch (refreshError) {
                            this.logout();
                            if (typeof window !== 'undefined') {
                                window.location.href = '/auth/login';
                            }
                            throw new AuthenticationError();
                        }
                    }
                }

                // Transform error
                throw this.handleError(error);
            }
        );
    }

    private getToken(): string | null {
        if (typeof window === 'undefined') return null;
        return localStorage.getItem('access_token');
    }

    private getRefreshToken(): string | null {
        if (typeof window === 'undefined') return null;
        return localStorage.getItem('refresh_token');
    }

    private setToken(token: string): void {
        if (typeof window !== 'undefined') {
            localStorage.setItem('access_token', token);
        }
    }

    private logout(): void {
        if (typeof window !== 'undefined') {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        }
    }

    private handleError(error: AxiosError): APIError {
        const response: any = error.response?.data;

        switch (error.response?.status) {
            case 400:
                if (response && typeof response === 'object') {
                    return new ValidationError(
                        response.message || 'Validation failed',
                        response.errors || response
                    );
                }
                return new APIError(response?.message || 'Bad request', 400);

            case 401:
                return new AuthenticationError(response?.message);

            case 403:
                return new AuthorizationError(response?.message);

            case 404:
                return new NotFoundError(response?.message);

            case 500:
                return new APIError('Server error. Please try again later.', 500);

            default:
                return new APIError(
                    response?.message || error.message || 'An unexpected error occurred',
                    error.response?.status
                );
        }
    }

    // Public methods
    async get<T>(url: string, params?: any): Promise<T> {
        const response = await this.client.get<T>(url, { params });
        return response.data;
    }

    async post<T>(url: string, data?: any): Promise<T> {
        const response = await this.client.post<T>(url, data);
        return response.data;
    }

    async put<T>(url: string, data?: any): Promise<T> {
        const response = await this.client.put<T>(url, data);
        return response.data;
    }

    async patch<T>(url: string, data?: any): Promise<T> {
        const response = await this.client.patch<T>(url, data);
        return response.data;
    }

    async delete<T>(url: string): Promise<T> {
        const response = await this.client.delete<T>(url);
        return response.data;
    }

    // File upload
    async upload<T>(url: string, file: File, onProgress?: (progress: number) => void): Promise<T> {
        const formData = new FormData();
        formData.append('file', file);

        const response = await this.client.post<T>(url, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            onUploadProgress: (progressEvent) => {
                if (onProgress && progressEvent.total) {
                    const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    onProgress(progress);
                }
            },
        });

        return response.data;
    }
}

// Export singleton instance
export const apiClient = new APIClient();
