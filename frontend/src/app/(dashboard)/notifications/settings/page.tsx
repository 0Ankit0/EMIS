"use client";

import { Bell, Settings } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";

export default function NotificationSettingsPage() {
    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Settings className="h-8 w-8 text-primary" />
                Notification Settings
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Email Notifications</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <Label>New Assignments</Label>
                            <p className="text-sm text-muted-foreground">Receive emails when new assignments are posted</p>
                        </div>
                        <Switch defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <Label>Exam Schedules</Label>
                            <p className="text-sm text-muted-foreground">Receive emails about upcoming exams</p>
                        </div>
                        <Switch defaultChecked />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Push Notifications</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <Label>Grade Updates</Label>
                            <p className="text-sm text-muted-foreground">Get notified when grades are published</p>
                        </div>
                        <Switch defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <Label>Announcements</Label>
                            <p className="text-sm text-muted-foreground">Get notified about school announcements</p>
                        </div>
                        <Switch defaultChecked />
                    </div>
                </CardContent>
            </Card>

            <Button className="w-full">Save Preferences</Button>
        </div>
    );
}
