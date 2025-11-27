"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { AUTH_ENDPOINTS } from "@/lib/api-constants";
import { getAuthToken } from "@/lib/auth-utils";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";

export default function ProfilePage() {
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [user, setUser] = useState<any>({
        username: "",
        email: "",
        first_name: "",
        last_name: "",
    });

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const token = getAuthToken();
                if (!token) return;

                const res = await fetch(AUTH_ENDPOINTS.USER, {
                    headers: {
                        "Authorization": `Token ${token}`,
                    },
                });

                if (!res.ok) throw new Error("Failed to fetch user");

                const data = await res.json();
                setUser(data);
            } catch (error) {
                toast.error("Could not load profile");
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setUser({ ...user, [e.target.id]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);

        try {
            const token = getAuthToken();
            const res = await fetch(AUTH_ENDPOINTS.USER, {
                method: "PATCH", // Or PUT
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Token ${token}`,
                },
                body: JSON.stringify({
                    first_name: user.first_name,
                    last_name: user.last_name,
                    email: user.email,
                    // username usually read-only or requires special handling
                }),
            });

            if (!res.ok) throw new Error("Failed to update profile");

            toast.success("Profile updated");
        } catch (error) {
            toast.error("Failed to update profile");
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return <Loader2 className="h-8 w-8 animate-spin" />;
    }

    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-medium">Profile</h3>
                <p className="text-sm text-muted-foreground">
                    This is how others will see you on the site.
                </p>
            </div>
            <Separator />
            <form onSubmit={handleSubmit} className="space-y-8">
                <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="username" className="text-right">
                            Username
                        </Label>
                        <Input
                            id="username"
                            value={user.username}
                            disabled
                            className="col-span-3"
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="email" className="text-right">
                            Email
                        </Label>
                        <Input
                            id="email"
                            value={user.email}
                            onChange={handleChange}
                            className="col-span-3"
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="first_name" className="text-right">
                            First Name
                        </Label>
                        <Input
                            id="first_name"
                            value={user.first_name}
                            onChange={handleChange}
                            className="col-span-3"
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="last_name" className="text-right">
                            Last Name
                        </Label>
                        <Input
                            id="last_name"
                            value={user.last_name}
                            onChange={handleChange}
                            className="col-span-3"
                        />
                    </div>
                </div>
                <div className="flex justify-end">
                    <Button type="submit" disabled={saving}>
                        {saving && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                        Save changes
                    </Button>
                </div>
            </form>
        </div>
    );
}
