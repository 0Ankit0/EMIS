import { getAuthToken } from "@/lib/auth-utils";

export const processExamResults = async (formData: FormData) => {
    const token = getAuthToken();
    const response = await fetch(`/api/exam/process/`, {
        method: "POST",
        headers: {
            Authorization: `Token ${token}`,
        },
        body: formData,
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to process exam results");
    }

    return response;
};
