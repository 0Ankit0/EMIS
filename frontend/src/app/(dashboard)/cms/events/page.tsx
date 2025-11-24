"use client";

import { useState } from "react";
import Link from "next/link";
import { Calendar, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const eventsData = [
    { id: 1, title: "Annual Sports Day", date: "2025-02-15", location: "Main Ground", attendees: 500, status: "upcoming" },
    { id: 2, title: "Science Fair", date: "2025-02-20", location: "Science Block", attendees: 300, status: "upcoming" },
    { id: 3, title: "Cultural Fest", date: "2025-01-10", location: "Auditorium", attendees: 450, status: "completed" },
];

export default function EventsListPage() {
    const [events] = useState(eventsData);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <Calendar className="h-8 w-8 text-primary" />
                        Events
                    </h2>
                    <p className="text-muted-foreground">Manage school events and activities</p>
                </div>
                <Link href="/cms/events/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Create Event
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Events</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Event Title</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Location</TableHead>
                                <TableHead className="text-right">Attendees</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {events.map((event) => (
                                <TableRow key={event.id}>
                                    <TableCell className="font-semibold">{event.title}</TableCell>
                                    <TableCell>{event.date}</TableCell>
                                    <TableCell>{event.location}</TableCell>
                                    <TableCell className="text-right">{event.attendees}</TableCell>
                                    <TableCell>
                                        <Badge className={event.status === "upcoming" ? "bg-blue-100 text-blue-800" : "bg-gray-100 text-gray-800"}>
                                            {event.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Link href={`/cms/events/${event.id}`}>
                                            <Button variant="outline" size="sm">View</Button>
                                        </Link>
                                        <Link href={`/cms/events/${event.id}/edit`}>
                                            <Button size="sm">Edit</Button>
                                        </Link>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
