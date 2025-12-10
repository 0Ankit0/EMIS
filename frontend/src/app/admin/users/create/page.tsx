"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import { createUser, UserCreate } from "@/services/userService";
import { getGroups, Group } from "@/services/groupService";
import { ArrowLeft, Loader2 } from "lucide-react";

export default function CreateUserPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [groups, setGroups] = useState<Group[]>([]);
    const [formData, setFormData] = useState<UserCreate>({
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        password: "",
        is_active: true,
        is_staff: false,
        is_superuser: false,
        groups: [],
    });

    useEffect(() => {
        fetchGroups();
    }, []);

    const fetchGroups = async () => {
        try {
            const data = await getGroups();
            setGroups(data);
        } catch (error) {
            console.error(error);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!formData.username || !formData.email || !formData.password) {
            toast.error("Please fill in all required fields");
            return;
        }

        try {
            setLoading(true);
            await createUser(formData);
            toast.success("User created successfully");
            router.push("/admin/users");
        } catch (error: any) {
            toast.error(error.message || "Failed to create user");
        } finally {
            setLoading(false);
        }
    };

    const handleGroupToggle = (groupId: number) => {
        setFormData(prev => ({
            ...prev,
            groups: prev.groups?.includes(groupId)
                ? prev.groups.filter(id => id !== groupId)
                : [...(prev.groups || []), groupId]
        }));
    };

    return (
        <div className="container mx-auto py-6 space-y-6 max-w-2xl">
            <div className="flex items-center gap-4">
                <Button variant="ghost" size="icon" onClick={() => router.back()}>
                    <ArrowLeft className="h-4 w-4" />
                </Button>
                <div>
                    <h1 className="text-3xl font-bold">Create User</h1>
                    <p className="text-muted-foreground">Add a new user to the system</p>
                </div>
            </div>

            <form onSubmit={handleSubmit}>
                <Card>
                    <CardHeader>
                        <CardTitle>User Details</CardTitle>
                        <CardDescription>Enter the user information</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="username">Username *</Label>
                            <Input
                                id="username"
                                value={formData.username}
                                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                required
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="email">Email *</Label>
                            <Input
                                id="email"
                                type="email"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                required
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="first_name">First Name</Label>
                                <Input
                                    id="first_name"
                                    value={formData.first_name}
                                    onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                                />
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="last_name">Last Name</Label>
                                <Input
                                    id="last_name"
                                    value={formData.last_name}
                                    onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="password">Password *</Label>
                            <Input
                                id="password"
                                type="password"
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                required
                            />
                        </div>

                        <div className="space-y-4 pt-4">
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="is_active"
                                    checked={formData.is_active}
                                    onCheckedChange={(checked) => setFormData({ ...formData, is_active: checked as boolean })}
                                />
                                <Label htmlFor="is_active" className="cursor-pointer">Active</Label>
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="is_staff"
                                    checked={formData.is_staff}
                                    onCheckedChange={(checked) => setFormData({ ...formData, is_staff: checked as boolean })}
                                />
                                <Label htmlFor="is_staff" className="cursor-pointer">Staff Status</Label>
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="is_superuser"
                                    checked={formData.is_superuser}
                                    onCheckedChange={(checked) => setFormData({ ...formData, is_superuser: checked as boolean })}
                                />
                                <Label htmlFor="is_superuser" className="cursor-pointer">Superuser Status</Label>
                            </div>
                        </div>

                        <div className="space-y-2 pt-4">
                            <Label>Groups</Label>
                            <div className="space-y-2 border rounded-lg p-4 max-h-48 overflow-y-auto">
                                {groups.map((group) => (
                                    <div key={group.id} className="flex items-center space-x-2">
                                        <Checkbox
                                            id={`group-${group.id}`}
                                            checked={formData.groups?.includes(group.id)}
                                            onCheckedChange={() => handleGroupToggle(group.id)}
                                        />
                                        <Label htmlFor={`group-${group.id}`} className="cursor-pointer">
                                            {group.name}
                                        </Label>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <div className="flex justify-end gap-4 mt-6">
                    <Button type="button" variant="outline" onClick={() => router.back()}>
                        Cancel
                    </Button>
                    <Button type="submit" disabled={loading}>
                        {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                        Create User
                    </Button>
                </div>
            </form>
        </div>
    );
}
