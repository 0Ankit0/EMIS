"use client";

import { useParams } from "next/navigation";
import { Calendar, Edit, MapPin, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const eventData = {
    title: "Annual Sports Day",
    description: "Join us for our annual sports day featuring various competitions and activities for all students.",
    date: "2025-02-15",
    time: "09:00 AM",
    location: "Main Ground",
    capacity: 500,
    registered: 342,
    status: "upcoming",
};

export default function EventDetailPage() {
    const params = useParams();

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-start">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Calendar className="h-8 w-8 text-primary" />
                        {eventData.title}
                    </h2>
                    <Badge className="mt-2 bg-blue-100 text-blue-800">
                        {eventData.status.toUpperCase()}
                    </Badge>
                </div>
                <Link href={`/cms/events/${params.id}/edit`}>
                    <Button>
                        <Edit className="mr-2 h-4 w-4" />
                        Edit
                    </Button>
                </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                            <Calendar className="h-4 w-4" />
                            <span className="text-sm">Date & Time</span>
                        </div>
                        <p className="font-bold text-lg">{eventData.date}</p>
                        <p className="text-muted-foreground">{eventData.time}</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                            <MapPin className="h-4 w-4" />
                            <span className="text-sm">Location</span>
                        </div>
                        <p className="font-bold text-lg">{eventData.location}</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                            <Users className="h-4 w-4" />
                            <span className="text-sm">Attendance</span>
                        </div>
                        <p className="font-bold text-lg">{eventData.registered}/{eventData.capacity}</p>
                        <p className="text-sm text-muted-foreground">Registered</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Description</CardTitle>
                </CardHeader>
                <CardContent>
                    <p>{eventData.description}</p>
                </CardContent>
            </Card>
        </div>
    );
}
