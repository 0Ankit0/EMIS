export const API_BASE_URL = '/api';

export const AUTH_ENDPOINTS = {
    LOGIN: `${API_BASE_URL}/auth/login/`,
    LOGOUT: `${API_BASE_URL}/auth/logout/`,
    PASSWORD_CHANGE: `${API_BASE_URL}/auth/password/change/`,
    PASSWORD_RESET: `${API_BASE_URL}/auth/password/reset/`,
    PASSWORD_RESET_CONFIRM: `${API_BASE_URL}/auth/password/reset/confirm/`,
    USER: `${API_BASE_URL}/auth/user/`,
};

export const CALENDAR_ENDPOINTS = {
    CALENDARS: `${API_BASE_URL}/calendar/calendars/`,
    EVENTS: `${API_BASE_URL}/calendar/events/`,
    CATEGORIES: `${API_BASE_URL}/calendar/categories/`,
    LAYOUTS: `${API_BASE_URL}/calendar/layouts/`,
};
