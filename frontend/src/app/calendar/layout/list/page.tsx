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
import { Edit, Trash2, Plus, Check, Eye } from "lucide-react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getAuthToken } from "@/lib/auth-utils";
import { CALENDAR_ENDPOINTS } from "@/lib/api-constants";
import { CalendarLayout } from "@/types/calendar";
import { toast } from "sonner";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { LayoutView } from "@/components/calendar/layout/layout-view";

async function getLayouts(): Promise<CalendarLayout[]> {
    const token = getAuthToken();
    const res = await fetch(CALENDAR_ENDPOINTS.LAYOUTS, {
        headers: { Authorization: `Token ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch layouts");
    return res.json();
}

async function deleteLayout(id: number) {
    const token = getAuthToken();
    const res = await fetch(`${CALENDAR_ENDPOINTS.LAYOUTS}${id}/`, {
        method: "DELETE",
        headers: { Authorization: `Token ${token}` },
    });
    if (!res.ok) throw new Error("Failed to delete layout");
}

async function setActiveLayout(id: number) {
    const token = getAuthToken();
    // We need to fetch the layout first to get its data, then update active=true
    // Or if the backend supports a specific endpoint, use that.
    // Standard DRF update:
    const res = await fetch(`${CALENDAR_ENDPOINTS.LAYOUTS}${id}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`
        },
        body: JSON.stringify({ active: true })
    });
    if (!res.ok) throw new Error("Failed to set active layout");
    return res.json();
}

export default function LayoutListPage() {
    const queryClient = useQueryClient();
    const { data: layouts = [], isLoading } = useQuery({
        queryKey: ["calendar-layouts"],
        queryFn: getLayouts,
    });

    const deleteMutation = useMutation({
        mutationFn: deleteLayout,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["calendar-layouts"] });
            toast.success("Layout deleted");
        },
        onError: () => toast.error("Failed to delete layout"),
    });

    const setActiveMutation = useMutation({
        mutationFn: setActiveLayout,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["calendar-layouts"] });
            toast.success("Active layout updated");
        },
        onError: () => toast.error("Failed to update active layout"),
    });

    const handleDelete = (id: number) => {
        if (!confirm("Are you sure you want to delete this layout?")) return;
        deleteMutation.mutate(id);
    };

    const handleSetActive = (id: number) => {
        setActiveMutation.mutate(id);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold tracking-tight">Calendar Layouts</h1>
                <Button asChild>
                    <Link href="/calendar/layout/add">
                        <Plus className="mr-2 h-4 w-4" /> Add Layout
                    </Link>
                </Button>
            </div>

            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Name</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={3} className="text-center py-4">Loading...</TableCell>
                            </TableRow>
                        ) : layouts.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={3} className="text-center py-4">No layouts found</TableCell>
                            </TableRow>
                        ) : (
                            layouts.map((layout: CalendarLayout) => (
                                <TableRow key={layout.id}>
                                    <TableCell className="font-medium">{layout.name}</TableCell>
                                    <TableCell>
                                        {layout.active ? (
                                            <Badge variant="default" className="bg-green-600">Active</Badge>
                                        ) : (
                                            <Badge variant="outline">Inactive</Badge>
                                        )}
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Dialog>
                                                <DialogTrigger asChild>
                                                    <Button variant="ghost" size="icon" title="View">
                                                        <Eye className="h-4 w-4" />
                                                    </Button>
                                                </DialogTrigger>
                                                <DialogContent maxWidth="max-w-[98vw]" height="h-[95vh]" className="flex flex-col p-0">
                                                    <DialogHeader className="px-6 py-4 border-b">
                                                        <DialogTitle>{layout.name}</DialogTitle>
                                                    </DialogHeader>
                                                    <div className="flex-1 overflow-hidden p-6">
                                                        <LayoutView layoutId={layout.id} mode="view" />
                                                    </div>
                                                </DialogContent>
                                            </Dialog>
                                            {!layout.active && (
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => handleSetActive(layout.id)}
                                                    title="Set as Active"
                                                >
                                                    <Check className="h-4 w-4 mr-1" /> Set Active
                                                </Button>
                                            )}
                                            <Button variant="ghost" size="icon" title="Edit" asChild>
                                                <Link href={`/calendar/layout/add?id=${layout.id}`}>
                                                    <Edit className="h-4 w-4" />
                                                </Link>
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                title="Delete"
                                                className="text-destructive hover:text-destructive"
                                                onClick={() => handleDelete(layout.id)}
                                                disabled={deleteMutation.isPending}
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
