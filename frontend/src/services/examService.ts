import { getAuthToken } from "@/lib/auth-utils";

export const processExamResults = async (formData: FormData) => {
    const token = getAuthToken();
    
    // Set a very long timeout for the fetch request (30 minutes)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30 * 60 * 1000);
    
    try {
        const response = await fetch(`/api/exam/process/`, {
            method: "POST",
            headers: {
                Authorization: `Token ${token}`,
            },
            body: formData,
            signal: controller.signal,
            // Disable keep-alive timeout
            keepalive: false,
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to process exam results");
        }

        return response;
    } catch (error: any) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timeout - process took too long');
        }
        throw error;
    }
};
