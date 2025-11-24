"use client";

import Link from "next/link";
import { GraduationCap, User, Lock, LogIn } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";

export default function LoginPage() {
    return (
        <Card className="border-none shadow-2xl">
            <CardHeader className="space-y-1 text-center bg-gradient-to-br from-primary to-secondary text-white rounded-t-xl p-8">
                <div className="flex justify-center mb-4">
                    <GraduationCap className="h-12 w-12" />
                </div>
                <CardTitle className="text-2xl font-bold">EMIS Login</CardTitle>
                <CardDescription className="text-blue-100">
                    Education Management Information System
                </CardDescription>
            </CardHeader>
            <CardContent className="p-8">
                <form className="space-y-6">
                    <div className="space-y-2">
                        <Label htmlFor="username">Username or Email</Label>
                        <div className="relative">
                            <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input
                                id="username"
                                placeholder="Enter your username or email"
                                className="pl-10"
                                required
                            />
                        </div>
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="password">Password</Label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input
                                id="password"
                                type="password"
                                placeholder="Enter your password"
                                className="pl-10"
                                required
                            />
                        </div>
                    </div>
                    <div className="flex items-center space-x-2">
                        <Checkbox id="remember" />
                        <Label htmlFor="remember" className="text-sm font-normal">Remember me</Label>
                    </div>
                    <Button type="submit" className="w-full bg-gradient-to-r from-primary to-secondary hover:opacity-90 transition-opacity">
                        <LogIn className="mr-2 h-4 w-4" /> Login
                    </Button>
                </form>
            </CardContent>
            <CardFooter className="flex flex-col space-y-4 bg-gray-50 p-6 rounded-b-xl text-sm text-center text-muted-foreground">
                <div className="flex justify-center space-x-4">
                    <Link href="/password-reset" className="hover:text-primary hover:underline">
                        Forgot Password?
                    </Link>
                    <span>|</span>
                    <Link href="/admin" className="hover:text-primary hover:underline">
                        Admin Panel
                    </Link>
                </div>
                <div>
                    &copy; {new Date().getFullYear()} EMIS. All rights reserved.
                </div>
            </CardFooter>
        </Card>
    );
}
