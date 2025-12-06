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
import { useEvents, useDeleteEvent, useUpdateEvent } from "@/hooks/use-event-queries";
import type { Event } from "@/types/calendar";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";



export default function EventListPage() {
    const [showUnlinkedOnly, setShowUnlinkedOnly] = useState(false);

    const { data: allEvents = [], isLoading } = useEvents();
    const deleteEvent = useDeleteEvent();
    const updateEvent = useUpdateEvent();

    const handleStatusChange = (id: string, status: string) => {
        updateEvent.mutate({ id, data: { status } });
    };

    // Filter events based on checkbox
    const events = showUnlinkedOnly
        ? allEvents.filter((e: Event) => e.calendar === null)
        : allEvents;

    const handleDelete = (id: string) => {
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
                            <TableHead>Status</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={9} className="text-center py-4">Loading...</TableCell>
                            </TableRow>
                        ) : events.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={9} className="text-center py-4">No events found</TableCell>
                            </TableRow>
                        ) : (
                            events.map((event: Event) => (
                                <TableRow key={event.ukid}>
                                    <TableCell className="font-medium">{event.title}</TableCell>
                                    <TableCell>{event.type === "single" ? "Single Day" : "Multi Day"}</TableCell>
                                    <TableCell>{event.start_date}</TableCell>
                                    <TableCell>{event.end_date}</TableCell>
                                    <TableCell>{event.start_time} - {event.end_time}</TableCell>
                                    <TableCell>{event.category?.name || "N/A"}</TableCell>
                                    <TableCell>{event.calendar?.title || "Unlinked"}</TableCell>
                                    <TableCell>
                                        <Select
                                            defaultValue={event.status}
                                            onValueChange={(value) => handleStatusChange(event.ukid, value)}
                                            disabled={updateEvent.isPending}
                                        >
                                            <SelectTrigger className="w-[110px] h-8">
                                                <SelectValue />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="draft">Draft</SelectItem>
                                                <SelectItem value="published">Published</SelectItem>
                                                <SelectItem value="postponed">Postponed</SelectItem>
                                                <SelectItem value="cancelled">Cancelled</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button variant="ghost" size="icon" title="View" asChild>
                                                <Link href={`/calendar/event/add?id=${event.ukid}`}>
                                                    <Eye className="h-4 w-4" />
                                                </Link>
                                            </Button>
                                            <Button variant="ghost" size="icon" title="Edit" asChild>
                                                <Link href={`/calendar/event/add?id=${event.ukid}`}>
                                                    <Edit className="h-4 w-4" />
                                                </Link>
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                title="Delete"
                                                className="text-destructive hover:text-destructive"
                                                onClick={() => handleDelete(event.ukid)}
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
