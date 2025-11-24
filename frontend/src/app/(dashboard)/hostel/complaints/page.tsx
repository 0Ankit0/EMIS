"use client";

import { MessageSquare, AlertCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const complaintsData = [
    { id: 1, title: "Leaking Tap", room: "101", student: "John Doe", status: "Pending", date: "2025-01-23" },
    { id: 2, title: "Broken Chair", room: "102", student: "Jane Smith", status: "Resolved", date: "2025-01-20" },
];

export default function HostelComplaintsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <MessageSquare className="h-8 w-8 text-primary" />
                    Complaints & Requests
                </h2>
                <Button variant="destructive">
                    <AlertCircle className="mr-2 h-4 w-4" />
                    Report Issue
                </Button>
            </div>

            <div className="space-y-4">
                {complaintsData.map((complaint) => (
                    <Card key={complaint.id}>
                        <CardContent className="p-6 flex items-center justify-between">
                            <div>
                                <h3 className="font-bold text-lg">{complaint.title}</h3>
                                <p className="text-sm text-muted-foreground">
                                    Room {complaint.room} • Reported by {complaint.student} • {complaint.date}
                                </p>
                            </div>
                            <Badge variant={complaint.status === "Resolved" ? "default" : "destructive"}>
                                {complaint.status}
                            </Badge>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
