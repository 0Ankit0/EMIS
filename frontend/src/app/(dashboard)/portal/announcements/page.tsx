"use client";

import { Bell } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const announcementsData = [
    { id: 1, title: "Exam Schedule Released", date: "2025-01-23", category: "Academic", priority: "high" },
    { id: 2, title: "Sports Day Registration", date: "2025-01-22", category: "Events", priority: "normal" },
];

export default function PortalAnnouncementsPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Bell className="h-8 w-8 text-primary" />
                Portal Announcements
            </h2>

            <div className="grid grid-cols-1 gap-4">
                {announcementsData.map((announcement) => (
                    <Card key={announcement.id} className="cursor-pointer hover:shadow-lg transition">
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <div>
                                    <h3 className="text-xl font-bold">{announcement.title}</h3>
                                    <p className="text-sm text-muted-foreground mt-1">{announcement.date}</p>
                                </div>
                                <Badge className={announcement.priority === "high" ? "bg-red-100 text-red-800" : "bg-blue-100 text-blue-800"}>
                                    {announcement.priority.toUpperCase()}
                                </Badge>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <span className="text-sm text-muted-foreground">{announcement.category}</span>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
