"use client";

import { useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Users, Shield, UserCog, ChevronRight } from "lucide-react";

export default function AdminDashboard() {
    const router = useRouter();

    const adminSections = [
        {
            title: "User Management",
            description: "Manage system users, create new users, and control access",
            icon: Users,
            href: "/admin/users",
            color: "text-blue-500",
        },
        {
            title: "Group Management",
            description: "Manage user groups and assign permissions to groups",
            icon: UserCog,
            href: "/admin/groups",
            color: "text-green-500",
        },
        {
            title: "Permission Management",
            description: "View and manage system permissions",
            icon: Shield,
            href: "/admin/permissions",
            color: "text-purple-500",
        },
    ];

    return (
        <div className="container mx-auto py-6 space-y-6">
            <div>
                <h1 className="text-3xl font-bold">Admin Dashboard</h1>
                <p className="text-muted-foreground">
                    Manage users, groups, and permissions
                </p>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {adminSections.map((section) => {
                    const Icon = section.icon;
                    return (
                        <Card
                            key={section.href}
                            className="cursor-pointer hover:shadow-lg transition-shadow"
                            onClick={() => router.push(section.href)}
                        >
                            <CardHeader>
                                <div className="flex items-center justify-between">
                                    <Icon className={`h-10 w-10 ${section.color}`} />
                                    <ChevronRight className="h-5 w-5 text-muted-foreground" />
                                </div>
                                <CardTitle className="mt-4">{section.title}</CardTitle>
                                <CardDescription>{section.description}</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <Button variant="ghost" className="w-full">
                                    Go to {section.title}
                                </Button>
                            </CardContent>
                        </Card>
                    );
                })}
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Quick Actions</CardTitle>
                    <CardDescription>Common administrative tasks</CardDescription>
                </CardHeader>
                <CardContent className="space-y-2">
                    <Button
                        variant="outline"
                        className="w-full justify-start"
                        onClick={() => router.push("/admin/users/create")}
                    >
                        <Users className="mr-2 h-4 w-4" />
                        Create New User
                    </Button>
                    <Button
                        variant="outline"
                        className="w-full justify-start"
                        onClick={() => router.push("/admin/groups/create")}
                    >
                        <UserCog className="mr-2 h-4 w-4" />
                        Create New Group
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
