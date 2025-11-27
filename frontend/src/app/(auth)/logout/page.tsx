"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { removeAuthToken, getAuthToken } from "@/lib/auth-utils";
import { AUTH_ENDPOINTS } from "@/lib/api-constants";
import { Loader2 } from "lucide-react";

export default function LogoutPage() {
    const router = useRouter();

    useEffect(() => {
        const logout = async () => {
            try {
                const token = getAuthToken();
                if (token) {
                    // Attempt to notify backend, but don't block if it fails
                    await fetch(AUTH_ENDPOINTS.LOGOUT, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            // Add Authorization header if needed, usually 'Token <token>' or 'Bearer <token>'
                            // dj-rest-auth usually expects 'Authorization: Token <key>'
                            "Authorization": `Token ${token}`
                        },
                    }).catch(err => console.error("Logout API failed", err));
                }
            } finally {
                removeAuthToken();
                router.push("/login");
            }
        };

        logout();
    }, [router]);

    return (
        <div className="flex min-h-screen items-center justify-center">
            <div className="flex flex-col items-center gap-4">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <p className="text-muted-foreground">Logging out...</p>
            </div>
        </div>
    );
}
