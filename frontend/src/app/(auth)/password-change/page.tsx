"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
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
import { getAuthToken } from "@/lib/auth-utils";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";

export default function PasswordChangePage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        old_password: "",
        new_password: "",
        confirm_password: "",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.id]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (formData.new_password !== formData.confirm_password) {
            toast.error("New passwords do not match");
            return;
        }

        setLoading(true);

        try {
            const token = getAuthToken();
            if (!token) {
                throw new Error("Not authenticated");
            }

            const res = await fetch(AUTH_ENDPOINTS.PASSWORD_CHANGE, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Token ${token}`,
                },
                body: JSON.stringify({
                    old_password: formData.old_password,
                    new_password1: formData.new_password,
                    new_password2: formData.confirm_password,
                }),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || JSON.stringify(data));
            }

            toast.success("Password changed successfully");
            router.push("/settings/profile");
        } catch (error: any) {
            toast.error(error.message || "Failed to change password");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-muted/50 px-4 py-12 sm:px-6 lg:px-8">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle>Change Password</CardTitle>
                    <CardDescription>
                        Enter your current password and a new password.
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="old_password">Current Password</Label>
                            <Input
                                id="old_password"
                                type="password"
                                required
                                value={formData.old_password}
                                onChange={handleChange}
                                disabled={loading}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="new_password">New Password</Label>
                            <Input
                                id="new_password"
                                type="password"
                                required
                                value={formData.new_password}
                                onChange={handleChange}
                                disabled={loading}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="confirm_password">Confirm New Password</Label>
                            <Input
                                id="confirm_password"
                                type="password"
                                required
                                value={formData.confirm_password}
                                onChange={handleChange}
                                disabled={loading}
                            />
                        </div>
                    </CardContent>
                    <CardFooter>
                        <Button className="w-full" type="submit" disabled={loading}>
                            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            Change Password
                        </Button>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
}
