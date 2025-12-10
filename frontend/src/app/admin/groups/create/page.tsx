"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import { createGroup, GroupCreate } from "@/services/groupService";
import { getPermissions, Permission } from "@/services/permissionService";
import { ArrowLeft, Loader2 } from "lucide-react";

export default function CreateGroupPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [permissions, setPermissions] = useState<Permission[]>([]);
    const [formData, setFormData] = useState<GroupCreate>({
        name: "",
        permissions: [],
    });

    useEffect(() => {
        fetchPermissions();
    }, []);

    const fetchPermissions = async () => {
        try {
            const data = await getPermissions();
            setPermissions(data);
        } catch (error) {
            console.error(error);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!formData.name) {
            toast.error("Please enter a group name");
            return;
        }

        try {
            setLoading(true);
            await createGroup(formData);
            toast.success("Group created successfully");
            router.push("/admin/groups");
        } catch (error: any) {
            toast.error(error.message || "Failed to create group");
        } finally {
            setLoading(false);
        }
    };

    const handlePermissionToggle = (permissionId: number) => {
        setFormData(prev => ({
            ...prev,
            permissions: prev.permissions?.includes(permissionId)
                ? prev.permissions.filter(id => id !== permissionId)
                : [...(prev.permissions || []), permissionId]
        }));
    };

    const groupedPermissions = permissions.reduce((acc, permission) => {
        const key = permission.content_type_name;
        if (!acc[key]) {
            acc[key] = [];
        }
        acc[key].push(permission);
        return acc;
    }, {} as Record<string, Permission[]>);

    return (
        <div className="container mx-auto py-6 space-y-6 max-w-2xl">
            <div className="flex items-center gap-4">
                <Button variant="ghost" size="icon" onClick={() => router.back()}>
                    <ArrowLeft className="h-4 w-4" />
                </Button>
                <div>
                    <h1 className="text-3xl font-bold">Create Group</h1>
                    <p className="text-muted-foreground">Add a new group to the system</p>
                </div>
            </div>

            <form onSubmit={handleSubmit}>
                <Card>
                    <CardHeader>
                        <CardTitle>Group Details</CardTitle>
                        <CardDescription>Enter the group information</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="name">Group Name *</Label>
                            <Input
                                id="name"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                required
                            />
                        </div>

                        <div className="space-y-2 pt-4">
                            <Label>Permissions</Label>
                            <div className="space-y-4 border rounded-lg p-4 max-h-96 overflow-y-auto">
                                {Object.entries(groupedPermissions).map(([contentType, perms]) => (
                                    <div key={contentType} className="space-y-2">
                                        <h4 className="font-semibold text-sm">{contentType}</h4>
                                        <div className="space-y-2 ml-4">
                                            {perms.map((permission) => (
                                                <div key={permission.id} className="flex items-center space-x-2">
                                                    <Checkbox
                                                        id={`permission-${permission.id}`}
                                                        checked={formData.permissions?.includes(permission.id)}
                                                        onCheckedChange={() => handlePermissionToggle(permission.id)}
                                                    />
                                                    <Label htmlFor={`permission-${permission.id}`} className="cursor-pointer text-sm">
                                                        {permission.name} ({permission.codename})
                                                    </Label>
                                                </div>
                                            ))}
                                        </div>
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
                        Create Group
                    </Button>
                </div>
            </form>
        </div>
    );
}
