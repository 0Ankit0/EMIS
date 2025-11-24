"use client";

import { Bell, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const notificationsData = [
    { id: 1, title: "Exam Schedule Updated", message: "Mid term exams rescheduled to Feb 20", date: "2025-01-23", type: "announcement", read: false },
    { id: 2, title: "Fee Payment Due", message: "Your tuition fee is due on Feb 1", date: "2025-01-22", type: "reminder", read: true },
];

export default function NotificationsListPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Bell className="h-8 w-8 text-primary" />
                    Notifications
                </h2>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Send Notification
                </Button>
            </div>

            <div className="grid grid-cols-1 gap-4">
                {notificationsData.map((notif) => (
                    <Card key={notif.id} className={!notif.read ? "border-l-4 border-blue-500 bg-blue-50" : ""}>
                        <CardContent className="p-6">
                            <div className="flex justify-between items-start">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <h3 className="font-bold text-lg">{notif.title}</h3>
                                        {!notif.read && <Badge className="bg-blue-600">NEW</Badge>}
                                    </div>
                                    <p className="text-muted-foreground mb-2">{notif.message}</p>
                                    <p className="text-sm text-muted-foreground">{notif.date}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
