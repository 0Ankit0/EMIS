import { getAuthToken } from "@/lib/auth-utils";
import type {
    Enrollment,
    EnrollmentCreateInput,
    EnrollmentUpdateInput,
    EnrollmentFilters
} from "@/types/student";

const API_BASE = "/api/enrollments";

export const getEnrollments = async (filters?: EnrollmentFilters): Promise<Enrollment[]> => {
    const token = getAuthToken();

    const params = new URLSearchParams();
    if (filters?.student) params.append("student", String(filters.student));
    if (filters?.program) params.append("program", filters.program);
    if (filters?.semester) params.append("semester", filters.semester);
    if (filters?.status) params.append("status", filters.status);

    const queryString = params.toString();
    const url = queryString ? `${API_BASE}/?${queryString}` : `${API_BASE}/`;

    const response = await fetch(url, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch enrollments" }));
        throw new Error(errorData.error || "Failed to fetch enrollments");
    }

    return response.json();
};

export const getEnrollment = async (id: number): Promise<Enrollment> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch enrollment" }));
        throw new Error(errorData.error || "Failed to fetch enrollment");
    }

    return response.json();
};

export const createEnrollment = async (data: EnrollmentCreateInput): Promise<Enrollment> => {
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
        const errorData = await response.json().catch(() => ({ error: "Failed to create enrollment" }));
        throw new Error(errorData.error || "Failed to create enrollment");
    }

    return response.json();
};

export const updateEnrollment = async (id: number, data: EnrollmentUpdateInput): Promise<Enrollment> => {
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
        const errorData = await response.json().catch(() => ({ error: "Failed to update enrollment" }));
        throw new Error(errorData.error || "Failed to update enrollment");
    }

    return response.json();
};

export const deleteEnrollment = async (id: number): Promise<void> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        method: "DELETE",
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to delete enrollment" }));
        throw new Error(errorData.error || "Failed to delete enrollment");
    }
};
