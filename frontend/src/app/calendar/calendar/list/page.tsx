"use client";

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
import { useCalendars, useDeleteCalendar } from "@/hooks/use-calendar-queries";
import type { Calendar } from "@/types/calendar";



export default function CalendarListPage() {
    const { data: calendars = [], isLoading } = useCalendars();
    const deleteCalendar = useDeleteCalendar();

    const handleDelete = (id: string) => {
        if (!confirm("Are you sure you want to delete this calendar?")) return;
        deleteCalendar.mutate(id);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold tracking-tight">Calendars</h1>
                <Button asChild>
                    <Link href="/calendar/calendar/add">
                        <Plus className="mr-2 h-4 w-4" /> Add Calendar
                    </Link>
                </Button>
            </div>

            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Title</TableHead>
                            <TableHead>Start Date</TableHead>
                            <TableHead>End Date</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-4">Loading...</TableCell>
                            </TableRow>
                        ) : calendars.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-4">No calendars found</TableCell>
                            </TableRow>
                        ) : (
                            calendars.map((calendar: Calendar) => (
                                <TableRow key={calendar.ukid}>
                                    <TableCell className="font-medium">{calendar.title}</TableCell>
                                    <TableCell>{calendar.start_date}</TableCell>
                                    <TableCell>{calendar.end_date}</TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button variant="ghost" size="icon" title="View" asChild>
                                                <Link href={`/calendar/calendar/add?id=${calendar.ukid}`}>
                                                    <Eye className="h-4 w-4" />
                                                </Link>
                                            </Button>
                                            <Button variant="ghost" size="icon" title="Edit" asChild>
                                                <Link href={`/calendar/calendar/add?id=${calendar.ukid}`}>
                                                    <Edit className="h-4 w-4" />
                                                </Link>
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                title="Delete"
                                                className="text-destructive hover:text-destructive"
                                                onClick={() => handleDelete(calendar.ukid)}
                                                disabled={deleteCalendar.isPending}
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
