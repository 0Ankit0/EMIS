import { getAuthToken } from "@/lib/auth-utils";
import type {
    SubjectResult,
    SubjectResultCreateInput,
    SubjectResultUpdateInput,
    SubjectResultFilters
} from "@/types/student";

const API_BASE = "/api/subject-results";

export const getSubjectResults = async (filters?: SubjectResultFilters): Promise<SubjectResult[]> => {
    const token = getAuthToken();

    const params = new URLSearchParams();
    if (filters?.student) params.append("student", String(filters.student));
    if (filters?.semester) params.append("semester", filters.semester);
    if (filters?.subject_name) params.append("subject_name", filters.subject_name);
    if (filters?.attempt_type) params.append("attempt_type", filters.attempt_type);

    const queryString = params.toString();
    const url = queryString ? `${API_BASE}/?${queryString}` : `${API_BASE}/`;

    const response = await fetch(url, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch subject results" }));
        throw new Error(errorData.error || "Failed to fetch subject results");
    }

    return response.json();
};

export const getSubjectResult = async (id: number): Promise<SubjectResult> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch subject result" }));
        throw new Error(errorData.error || "Failed to fetch subject result");
    }

    return response.json();
};

export const createSubjectResult = async (data: SubjectResultCreateInput): Promise<SubjectResult> => {
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
        const errorData = await response.json().catch(() => ({ error: "Failed to create subject result" }));
        throw new Error(errorData.error || "Failed to create subject result");
    }

    return response.json();
};

export const updateSubjectResult = async (id: number, data: SubjectResultUpdateInput): Promise<SubjectResult> => {
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
        const errorData = await response.json().catch(() => ({ error: "Failed to update subject result" }));
        throw new Error(errorData.error || "Failed to update subject result");
    }

    return response.json();
};

export const deleteSubjectResult = async (id: number): Promise<void> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        method: "DELETE",
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to delete subject result" }));
        throw new Error(errorData.error || "Failed to delete subject result");
    }
};

export const bulkImportResults = async (file: File): Promise<{ message: string; imported: number }> => {
    const token = getAuthToken();

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE}/bulk-import/`, {
        method: "POST",
        headers: {
            Authorization: `Token ${token}`,
        },
        body: formData,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to import results" }));
        throw new Error(errorData.error || "Failed to import results");
    }

    return response.json();
};
