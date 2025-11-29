"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Edit, Eye, Trash2, Plus } from "lucide-react";
import Link from "next/link";
import { useEvents, useDeleteEvent } from "@/hooks/use-event-queries";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

interface Event {
    id: number;
    title: string;
    type: string;
    start_date: string;
    end_date: string;
    start_time: string;
    end_time: string;
    category: number;
    calendar: number | null;
}

export default function EventListPage() {
    const [showUnlinkedOnly, setShowUnlinkedOnly] = useState(false);

    const { data: allEvents = [], isLoading } = useEvents();
    const deleteEvent = useDeleteEvent();

    // Filter events based on checkbox
    const events = showUnlinkedOnly
        ? allEvents.filter((e: Event) => e.calendar === null)
        : allEvents;

    const handleDelete = (id: number) => {
        if (!confirm("Are you sure you want to delete this event?")) return;
        deleteEvent.mutate(id);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold tracking-tight">Events</h1>
                <Button asChild>
                    <Link href="/calendar/event/add">
                        <Plus className="mr-2 h-4 w-4" /> Add Event
                    </Link>
                </Button>
            </div>

            <div className="flex items-center space-x-2">
                <Checkbox
                    id="unlinked"
                    checked={showUnlinkedOnly}
                    onCheckedChange={(checked) => setShowUnlinkedOnly(checked === true)}
                />
                <Label htmlFor="unlinked">Show only unlinked events</Label>
            </div>

            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Title</TableHead>
                            <TableHead>Type</TableHead>
                            <TableHead>Start Date</TableHead>
                            <TableHead>End Date</TableHead>
                            <TableHead>Time</TableHead>
                            <TableHead>Category</TableHead>
                            <TableHead>Calendar</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={8} className="text-center py-4">Loading...</TableCell>
                            </TableRow>
                        ) : events.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={8} className="text-center py-4">No events found</TableCell>
                            </TableRow>
                        ) : (
                            events.map((event: Event) => (
                                <TableRow key={event.id}>
                                    <TableCell className="font-medium">{event.title}</TableCell>
                                    <TableCell>{event.type === "single" ? "Single Day" : "Multi Day"}</TableCell>
                                    <TableCell>{event.start_date}</TableCell>
                                    <TableCell>{event.end_date}</TableCell>
                                    <TableCell>{event.start_time} - {event.end_time}</TableCell>
                                    <TableCell>{event.category || "N/A"}</TableCell>
                                    <TableCell>{event.calendar || "Unlinked"}</TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button variant="ghost" size="icon" title="View">
                                                <Eye className="h-4 w-4" />
                                            </Button>
                                            <Button variant="ghost" size="icon" title="Edit">
                                                <Edit className="h-4 w-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                title="Delete"
                                                className="text-destructive hover:text-destructive"
                                                onClick={() => handleDelete(event.id)}
                                                disabled={deleteEvent.isPending}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </div>
        </div>
    );
}
