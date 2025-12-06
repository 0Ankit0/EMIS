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
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { format } from "date-fns";
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
                                            <Dialog>
                                                <DialogTrigger asChild>
                                                    <Button variant="ghost" size="icon" title="View">
                                                        <Eye className="h-4 w-4" />
                                                    </Button>
                                                </DialogTrigger>
                                                <DialogContent>
                                                    <DialogHeader>
                                                        <DialogTitle>{event.title}</DialogTitle>
                                                        <DialogDescription>
                                                            {event.type === 'single'
                                                                ? format(new Date(event.start_date), 'EEEE, MMMM d, yyyy')
                                                                : `${format(new Date(event.start_date), 'MMM d')} - ${format(new Date(event.end_date), 'MMM d, yyyy')}`
                                                            }
                                                        </DialogDescription>
                                                    </DialogHeader>
                                                    <div className="space-y-4 pt-4">
                                                        <div className="flex items-center gap-2">
                                                            <Badge variant="outline" style={{
                                                                borderColor: event.category_color,
                                                                color: event.category_color
                                                            }}>
                                                                {event.category?.name}
                                                            </Badge>
                                                            <span className="text-sm text-muted-foreground">
                                                                {event.start_time.substring(0, 5)} - {event.end_time.substring(0, 5)}
                                                            </span>
                                                        </div>
                                                        {event.description && (
                                                            <div className="space-y-1">
                                                                <h4 className="text-sm font-medium">Description</h4>
                                                                <p className="text-sm text-muted-foreground">{event.description}</p>
                                                            </div>
                                                        )}
                                                        {event.location && (
                                                            <div className="space-y-1">
                                                                <h4 className="text-sm font-medium">Location</h4>
                                                                <p className="text-sm text-muted-foreground">📍 {event.location}</p>
                                                            </div>
                                                        )}
                                                        <div className="grid grid-cols-2 gap-4 text-sm">
                                                            <div>
                                                                <span className="font-medium">Status: </span>
                                                                <span className="capitalize">{event.status}</span>
                                                            </div>
                                                            <div>
                                                                <span className="font-medium">Calendar: </span>
                                                                <span>{event.calendar?.title || "Unlinked"}</span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </DialogContent>
                                            </Dialog>
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
