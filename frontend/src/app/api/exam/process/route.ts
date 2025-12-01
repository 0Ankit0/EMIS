import { NextRequest, NextResponse } from 'next/server';

export const maxDuration = 300; // 5 minutes (Vercel limit, adjust as needed)
export const dynamic = 'force-dynamic';

export async function POST(request: NextRequest) {
    try {
        const token = request.headers.get('authorization');
        
        if (!token) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        // Get the form data from the request
        const formData = await request.formData();

        // Forward the request to Django backend with extended timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10 * 60 * 1000); // 10 minutes

        try {
            const response = await fetch('http://localhost:8000/api/exam/process/', {
                method: 'POST',
                headers: {
                    'Authorization': token,
                },
                body: formData,
                signal: controller.signal,
            });

            clearTimeout(timeoutId);

            // Handle non-ok responses
            if (!response.ok) {
                const errorText = await response.text();
                let errorData;
                try {
                    errorData = JSON.parse(errorText);
                } catch {
                    errorData = { error: errorText || 'Failed to process exam results' };
                }
                return NextResponse.json(errorData, { status: response.status });
            }

            // Check if response is a blob (file download)
            const contentType = response.headers.get('content-type');
            if (contentType?.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') ||
                contentType?.includes('application/octet-stream')) {
                const blob = await response.blob();
                const headers = new Headers();
                headers.set('Content-Type', contentType);
                const contentDisposition = response.headers.get('content-disposition');
                if (contentDisposition) {
                    headers.set('Content-Disposition', contentDisposition);
                }
                return new NextResponse(blob, { headers });
            }

            // Otherwise return JSON
            const data = await response.json();
            return NextResponse.json(data);

        } catch (fetchError: any) {
            clearTimeout(timeoutId);
            if (fetchError.name === 'AbortError') {
                return NextResponse.json(
                    { error: 'Request timeout - processing took too long' },
                    { status: 504 }
                );
            }
            throw fetchError;
        }

    } catch (error: any) {
        console.error('Proxy error:', error);
        return NextResponse.json(
            { error: error.message || 'Internal server error' },
            { status: 500 }
        );
    }
}
