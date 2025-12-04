import { getAuthToken } from "@/lib/auth-utils";
import type {
    AcademicRecord,
    AcademicRecordCreateInput,
    AcademicRecordUpdateInput,
    AcademicRecordFilters
} from "@/types/student";

const API_BASE = "/api/academic-records";

export const getAcademicRecords = async (filters?: AcademicRecordFilters): Promise<AcademicRecord[]> => {
    const token = getAuthToken();

    const params = new URLSearchParams();
    if (filters?.student) params.append("student", String(filters.student));
    if (filters?.semester) params.append("semester", filters.semester);

    const queryString = params.toString();
    const url = queryString ? `${API_BASE}/?${queryString}` : `${API_BASE}/`;

    const response = await fetch(url, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch academic records" }));
        throw new Error(errorData.error || "Failed to fetch academic records");
    }

    return response.json();
};

export const getAcademicRecord = async (id: number): Promise<AcademicRecord> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch academic record" }));
        throw new Error(errorData.error || "Failed to fetch academic record");
    }

    return response.json();
};

export const createAcademicRecord = async (data: AcademicRecordCreateInput): Promise<AcademicRecord> => {
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
        const errorData = await response.json().catch(() => ({ error: "Failed to create academic record" }));
        throw new Error(errorData.error || "Failed to create academic record");
    }

    return response.json();
};

export const updateAcademicRecord = async (id: number, data: AcademicRecordUpdateInput): Promise<AcademicRecord> => {
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
        const errorData = await response.json().catch(() => ({ error: "Failed to update academic record" }));
        throw new Error(errorData.error || "Failed to update academic record");
    }

    return response.json();
};

export const deleteAcademicRecord = async (id: number): Promise<void> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        method: "DELETE",
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to delete academic record" }));
        throw new Error(errorData.error || "Failed to delete academic record");
    }
};
