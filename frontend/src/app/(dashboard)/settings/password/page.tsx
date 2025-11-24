"use client";

import { Lock, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function PasswordChangePage() {
    return (
        <div className="max-w-md mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Lock className="h-8 w-8 text-primary" />
                Change Password
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Update Password</CardTitle>
                    <CardDescription>
                        Ensure your account is using a long, random password to stay secure.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="current">Current Password</Label>
                        <Input id="current" type="password" />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="new">New Password</Label>
                        <Input id="new" type="password" />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="confirm">Confirm New Password</Label>
                        <Input id="confirm" type="password" />
                    </div>
                    <Button className="w-full">
                        <Save className="mr-2 h-4 w-4" />
                        Update Password
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
