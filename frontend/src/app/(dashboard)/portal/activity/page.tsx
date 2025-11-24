"use client";

import { Activity, Calendar } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const activityData = [
    { id: 1, action: "Logged in", timestamp: "2025-01-23 09:00 AM", icon: "🔐" },
    { id: 2, action: "Viewed grades", timestamp: "2025-01-23 09:15 AM", icon: "📊" },
    { id: 3, action: "Submitted assignment", timestamp: "2025-01-22 03:30 PM", icon: "📝" },
    { id: 4, action: "Downloaded certificate", timestamp: "2025-01-20 11:00 AM", icon: "📜" },
];

export default function ActivityLogPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Activity className="h-8 w-8 text-primary" />
                Activity Log
            </h2>

            <div className="space-y-3">
                {activityData.map((activity) => (
                    <Card key={activity.id}>
                        <CardContent className="p-4">
                            <div className="flex items-center gap-4">
                                <div className="text-3xl">{activity.icon}</div>
                                <div className="flex-1">
                                    <p className="font-semibold">{activity.action}</p>
                                    <div className="flex items-center gap-2 text-sm text-muted-foreground mt-1">
                                        <Calendar className="h-3 w-3" />
                                        <span>{activity.timestamp}</span>
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
