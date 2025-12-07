import { getAuthToken } from "@/lib/auth-utils";
import type {
    Student,
    StudentCreateInput,
    StudentUpdateInput,
    StudentFilters
} from "@/types/student";

const API_BASE = "/api/student/students";

export const getStudents = async (filters?: StudentFilters): Promise<Student[]> => {
    const token = getAuthToken();

    const params = new URLSearchParams();
    if (filters?.search) params.append("search", filters.search);
    if (filters?.is_active !== undefined) params.append("is_active", String(filters.is_active));
    if (filters?.enrollment_date_from) params.append("enrollment_date_from", filters.enrollment_date_from);
    if (filters?.enrollment_date_to) params.append("enrollment_date_to", filters.enrollment_date_to);
    if (filters?.city) params.append("city", filters.city);
    if (filters?.state) params.append("state", filters.state);

    const queryString = params.toString();
    const url = queryString ? `${API_BASE}/?${queryString}` : `${API_BASE}/`;

    const response = await fetch(url, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch students" }));
        throw new Error(errorData.error || "Failed to fetch students");
    }

    return response.json();
};

export const getStudent = async (id: string): Promise<Student> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch student" }));
        throw new Error(errorData.error || "Failed to fetch student");
    }

    return response.json();
};

export const createStudent = async (data: StudentCreateInput): Promise<Student> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to create student" }));
        throw new Error(errorData.error || "Failed to create student");
    }

    return response.json();
};

export const updateStudent = async (id: string, data: StudentUpdateInput): Promise<Student> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to update student" }));
        throw new Error(errorData.error || "Failed to update student");
    }

    return response.json();
};

export const deleteStudent = async (id: string): Promise<void> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        method: "DELETE",
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to delete student" }));
        throw new Error(errorData.error || "Failed to delete student");
    }
};

export const activateStudent = async (id: string): Promise<Student> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/activate/`, {
        method: "POST",
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to activate student" }));
        throw new Error(errorData.error || "Failed to activate student");
    }

    return response.json();
};
