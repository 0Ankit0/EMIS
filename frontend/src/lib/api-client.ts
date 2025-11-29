import { getAuthToken } from './auth-utils';
import { CALENDAR_ENDPOINTS } from './api-constants';

interface ApiRequestOptions {
    method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
    body?: any;
    params?: Record<string, string>;
}

async function apiRequest<T>(endpoint: string, options: ApiRequestOptions = {}): Promise<T> {
    const { method = 'GET', body, params } = options;
    const token = getAuthToken();

    let url = endpoint;
    if (params) {
        const searchParams = new URLSearchParams(params);
        url += `?${searchParams.toString()}`;
    }

    const headers: HeadersInit = {
        'Authorization': `Token ${token}`,
    };

    if (body) {
        headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
}

// Calendar API
export const calendarApi = {
    getAll: () => apiRequest<any[]>(CALENDAR_ENDPOINTS.CALENDARS),
    getById: (id: number) => apiRequest<any>(`${CALENDAR_ENDPOINTS.CALENDARS}${id}/`),
    create: (data: any) => apiRequest<any>(CALENDAR_ENDPOINTS.CALENDARS, { method: 'POST', body: data }),
    update: (id: number, data: any) => apiRequest<any>(`${CALENDAR_ENDPOINTS.CALENDARS}${id}/`, { method: 'PATCH', body: data }),
    delete: (id: number) => apiRequest<void>(`${CALENDAR_ENDPOINTS.CALENDARS}${id}/`, { method: 'DELETE' }),
};

// Event API
export const eventApi = {
    getAll: (params?: Record<string, string>) => apiRequest<any[]>(CALENDAR_ENDPOINTS.EVENTS, { params }),
    getById: (id: number) => apiRequest<any>(`${CALENDAR_ENDPOINTS.EVENTS}${id}/`),
    create: (data: any) => apiRequest<any>(CALENDAR_ENDPOINTS.EVENTS, { method: 'POST', body: data }),
    update: (id: number, data: any) => apiRequest<any>(`${CALENDAR_ENDPOINTS.EVENTS}${id}/`, { method: 'PATCH', body: data }),
    delete: (id: number) => apiRequest<void>(`${CALENDAR_ENDPOINTS.EVENTS}${id}/`, { method: 'DELETE' }),
};

// Category API
export const categoryApi = {
    getAll: () => apiRequest<any[]>(CALENDAR_ENDPOINTS.CATEGORIES),
    getById: (id: number) => apiRequest<any>(`${CALENDAR_ENDPOINTS.CATEGORIES}${id}/`),
    create: (data: any) => apiRequest<any>(CALENDAR_ENDPOINTS.CATEGORIES, { method: 'POST', body: data }),
    update: (id: number, data: any) => apiRequest<any>(`${CALENDAR_ENDPOINTS.CATEGORIES}${id}/`, { method: 'PATCH', body: data }),
    delete: (id: number) => apiRequest<void>(`${CALENDAR_ENDPOINTS.CATEGORIES}${id}/`, { method: 'DELETE' }),
};
