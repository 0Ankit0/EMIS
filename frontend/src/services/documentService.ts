import { getAuthToken } from "@/lib/auth-utils";
import type { Document, DocumentUploadInput } from "@/types/student";

const API_BASE = "/api/documents";

export const getDocuments = async (studentId: string): Promise<Document[]> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/?student=${studentId}`, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch documents" }));
        throw new Error(errorData.error || "Failed to fetch documents");
    }

    return response.json();
};

export const getDocument = async (id: string): Promise<Document> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to fetch document" }));
        throw new Error(errorData.error || "Failed to fetch document");
    }

    return response.json();
};

export const uploadDocument = async (data: DocumentUploadInput): Promise<Document> => {
    const token = getAuthToken();

    const formData = new FormData();
    formData.append("student", String(data.student));
    formData.append("document_type", data.document_type);
    formData.append("file", data.file);

    const response = await fetch(`${API_BASE}/`, {
        method: "POST",
        headers: {
            Authorization: `Token ${token}`,
        },
        body: formData,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to upload document" }));
        throw new Error(errorData.error || "Failed to upload document");
    }

    return response.json();
};

export const deleteDocument = async (id: string): Promise<void> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/`, {
        method: "DELETE",
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to delete document" }));
        throw new Error(errorData.error || "Failed to delete document");
    }
};

export const verifyDocument = async (id: string, verifiedBy: string): Promise<Document> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/verify/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
        },
        body: JSON.stringify({ verified_by: verifiedBy }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to verify document" }));
        throw new Error(errorData.error || "Failed to verify document");
    }

    return response.json();
};

export const downloadDocument = async (id: string): Promise<Blob> => {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE}/${id}/download/`, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });

    if (!response.ok) {
        throw new Error("Failed to download document");
    }

    return response.blob();
};
