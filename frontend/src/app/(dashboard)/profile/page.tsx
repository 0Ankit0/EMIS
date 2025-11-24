"use client";

import Link from "next/link";
import { User, ArrowLeft, Edit, Key, Shield, Mail, Phone, Calendar, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

export default function ProfilePage() {
    // Mock user data
    const user = {
        username: "admin_user",
        email: "admin@emis.edu",
        firstName: "Admin",
        lastName: "User",
        phone: "+1 234 567 890",
        memberSince: "January 15, 2023",
        lastLogin: "November 23, 2025 10:30 AM",
        role: "Administrator",
        isSuperuser: true,
        profilePhoto: "/avatars/01.png",
        twoFactorEnabled: false,
    };

    const getRoleBadge = () => {
        if (user.isSuperuser) return <Badge variant="destructive">Administrator</Badge>;
        return <Badge>User</Badge>;
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <User className="h-8 w-8" />
                    My Profile
                </h2>
                <Button variant="outline" asChild>
                    <Link href="/dashboard">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back to Dashboard
                    </Link>
                </Button>
            </div>
            <Separator />

            <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
                {/* Profile Card */}
                <div className="md:col-span-4">
                    <Card className="shadow-sm">
                        <CardContent className="pt-6 text-center">
                            <div className="mb-4 flex justify-center">
                                <Avatar className="h-32 w-32">
                                    <AvatarImage src={user.profilePhoto} alt="Profile" />
                                    <AvatarFallback className="text-4xl bg-primary/10 text-primary">
                                        <User className="h-16 w-16" />
                                    </AvatarFallback>
                                </Avatar>
                            </div>
                            <h4 className="text-xl font-bold">{user.firstName} {user.lastName}</h4>
                            <p className="text-muted-foreground mb-4">{user.email}</p>

                            <div className="mb-4">
                                {getRoleBadge()}
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Details Card */}
                <div className="md:col-span-8 space-y-6">
                    <Card className="shadow-sm">
                        <CardHeader>
                            <CardTitle>Profile Information</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="text-muted-foreground font-medium">Username:</div>
                                <div className="md:col-span-2 font-semibold">{user.username}</div>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="text-muted-foreground font-medium flex items-center gap-2">
                                    <Mail className="h-4 w-4" /> Email:
                                </div>
                                <div className="md:col-span-2">{user.email}</div>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="text-muted-foreground font-medium">First Name:</div>
                                <div className="md:col-span-2">{user.firstName}</div>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="text-muted-foreground font-medium">Last Name:</div>
                                <div className="md:col-span-2">{user.lastName}</div>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="text-muted-foreground font-medium flex items-center gap-2">
                                    <Phone className="h-4 w-4" /> Phone:
                                </div>
                                <div className="md:col-span-2">{user.phone}</div>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="text-muted-foreground font-medium flex items-center gap-2">
                                    <Calendar className="h-4 w-4" /> Member Since:
                                </div>
                                <div className="md:col-span-2">{user.memberSince}</div>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="text-muted-foreground font-medium flex items-center gap-2">
                                    <Clock className="h-4 w-4" /> Last Login:
                                </div>
                                <div className="md:col-span-2">{user.lastLogin}</div>
                            </div>

                            <Separator className="my-4" />

                            <div className="flex flex-wrap gap-2">
                                <Button disabled>
                                    <Edit className="mr-2 h-4 w-4" />
                                    Edit Profile
                                </Button>
                                <Button variant="outline" asChild>
                                    <Link href="/password-change">
                                        <Key className="mr-2 h-4 w-4" />
                                        Change Password
                                    </Link>
                                </Button>
                                {!user.twoFactorEnabled && (
                                    <Button variant="outline" className="text-blue-600 border-blue-200 hover:bg-blue-50">
                                        <Shield className="mr-2 h-4 w-4" />
                                        Enable 2FA
                                    </Button>
                                )}
                            </div>
                        </CardContent>
                    </Card>

                    {user.isSuperuser && (
                        <Card className="shadow-sm border-l-4 border-l-blue-500">
                            <CardHeader>
                                <CardTitle className="text-lg">Permissions & Roles</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="bg-blue-50 text-blue-800 p-4 rounded-md flex items-center gap-2">
                                    <Shield className="h-5 w-5" />
                                    You have administrative access to the system.
                                </div>
                            </CardContent>
                        </Card>
                    )}
                </div>
            </div>
        </div>
    );
}
