import { getAuthToken } from "@/lib/auth-utils";
import type {
    Guardian,
    GuardianCreateInput,
    GuardianUpdateInput
} from "@/types/student";

const API_BASE = "/api/guardians";

export const getGuardians = async (studentId?: number): Promise<Guardian[]> => {
    const token = getAuthToken();

    const params = new URLSearchParams();
    if (studentId) params.append("student", String(studentId));

    const queryString = params.toString();
    const url = queryString ? `${API_BASE}/?${queryString}` : `${API_BASE}/`;

    const response = await fetch(url, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch guardians" }));
        throw new Error(errorData.error || "Failed to fetch guardians");
    }

    return response.json();
};

export const getGuardian = async (id: number): Promise<Guardian> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch guardian" }));
        throw new Error(errorData.error || "Failed to fetch guardian");
    }

    return response.json();
};

export const createGuardian = async (data: GuardianCreateInput): Promise<Guardian> => {
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
        const errorData = await response.json().catch(() => ({ error: "Failed to create guardian" }));
        throw new Error(errorData.error || "Failed to create guardian");
    }

    return response.json();
};

export const updateGuardian = async (id: number, data: GuardianUpdateInput): Promise<Guardian> => {
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
        const errorData = await response.json().catch(() => ({ error: "Failed to update guardian" }));
        throw new Error(errorData.error || "Failed to update guardian");
    }

    return response.json();
};

export const deleteGuardian = async (id: number): Promise<void> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        method: "DELETE",
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to delete guardian" }));
        throw new Error(errorData.error || "Failed to delete guardian");
    }
};

export const linkStudent = async (guardianId: number, studentId: number): Promise<Guardian> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${guardianId}/link-student/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
        },
        body: JSON.stringify({ student_id: studentId }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to link student" }));
        throw new Error(errorData.error || "Failed to link student");
    }

    return response.json();
};

export const unlinkStudent = async (guardianId: number, studentId: number): Promise<Guardian> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${guardianId}/unlink-student/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
        },
        body: JSON.stringify({ student_id: studentId }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to unlink student" }));
        throw new Error(errorData.error || "Failed to unlink student");
    }

    return response.json();
};
