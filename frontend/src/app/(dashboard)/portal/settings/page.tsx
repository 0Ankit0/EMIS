"use client";

import { Settings } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";

export default function PortalSettingsPage() {
    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Settings className="h-8 w-8 text-primary" />
                Portal Settings
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Profile Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Display Name</Label>
                        <Input defaultValue="John Doe" className="mt-2" />
                    </div>
                    <div>
                        <Label>Email</Label>
                        <Input type="email" defaultValue="john@example.com" className="mt-2" />
                    </div>
                    <div>
                        <Label>Phone</Label>
                        <Input defaultValue="+1234567890" className="mt-2" />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Notification Preferences</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <Label>Email Notifications</Label>
                        <Switch defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                        <Label>SMS Notifications</Label>
                        <Switch />
                    </div>
                    <div className="flex items-center justify-between">
                        <Label>Push Notifications</Label>
                        <Switch defaultChecked />
                    </div>
                </CardContent>
            </Card>

            <Button className="w-full" size="lg">Save Settings</Button>
        </div>
    );
}
