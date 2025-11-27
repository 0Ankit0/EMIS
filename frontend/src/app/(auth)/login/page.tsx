"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { AUTH_ENDPOINTS } from "@/lib/api-constants";
import { setAuthToken } from "@/lib/auth-utils";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";

export default function LoginPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.id]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            // Support both username and email login if backend supports it, 
            // usually dj-rest-auth uses 'username' or 'email' field depending on config.
            // We'll send both or just the one filled. 
            // Assuming standard dj-rest-auth which often expects 'username' or 'email'.
            // Let's try to send 'username' as the primary field, but if it looks like an email, maybe backend handles it.
            // Or we can just send the payload as is.

            const payload: any = {
                password: formData.password,
            };

            if (formData.username) {
                payload.username = formData.username;
            }
            if (formData.email) {
                payload.email = formData.email;
            }

            // If user only filled one input (e.g. a single "Username or Email" field), we might need to adapt.
            // For now, let's assume the UI has separate fields or we use one as username.
            // Let's simplify to just "username" for now as per standard Django User model, 
            // but often people want email. I'll add a toggle or just use "username" field for both if backend allows.
            // Let's stick to a single "username" field in the UI for simplicity unless requested otherwise.

            const res = await fetch(AUTH_ENDPOINTS.LOGIN, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.non_field_errors?.[0] || "Login failed");
            }

            if (data.key) {
                setAuthToken(data.key);
                toast.success("Logged in successfully");
                router.push("/");
            } else {
                throw new Error("No token received");
            }
        } catch (error: any) {
            toast.error(error.message || "Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-muted/50 px-4 py-12 sm:px-6 lg:px-8">
            <Card className="w-full max-w-md">
                <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl font-bold tracking-tight">
                        Sign in to your account
                    </CardTitle>
                    <CardDescription>
                        Enter your username and password below to login
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="username">Username</Label>
                            <Input
                                id="username"
                                placeholder="johndoe"
                                required
                                value={formData.username}
                                onChange={handleChange}
                                disabled={loading}
                            />
                        </div>
                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <Label htmlFor="password">Password</Label>
                                <Link
                                    href="/password-reset"
                                    className="text-sm font-medium text-primary hover:underline"
                                >
                                    Forgot password?
                                </Link>
                            </div>
                            <Input
                                id="password"
                                type="password"
                                required
                                value={formData.password}
                                onChange={handleChange}
                                disabled={loading}
                            />
                        </div>
                    </CardContent>
                    <CardFooter>
                        <Button className="w-full" type="submit" disabled={loading}>
                            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            Sign In
                        </Button>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
}
