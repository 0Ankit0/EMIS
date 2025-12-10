"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";

export default function AdminLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const router = useRouter();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAdminAccess = async () => {
            try {
                const token = document.cookie
                    .split('; ')
                    .find(row => row.startsWith('auth_token='))
                    ?.split('=')[1];

                if (!token) {
                    router.push('/login');
                    return;
                }

                // Check if user is admin by trying to access the admin API
                const response = await fetch('/api/admin/users/', {
                    headers: {
                        'Authorization': `Token ${token}`,
                    },
                });

                if (response.status === 403 || response.status === 401) {
                    router.push('/');
                    return;
                }

                setLoading(false);
            } catch (error) {
                router.push('/');
            }
        };

        checkAdminAccess();
    }, [router]);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <Loader2 className="h-8 w-8 animate-spin" />
            </div>
        );
    }

    return <>{children}</>;
}
