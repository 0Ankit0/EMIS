"use client";

import { useState } from "react";
import Link from "next/link";
import { Megaphone, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const announcementsData = [
    { id: 1, title: "Mid-term Exam Schedule", date: "2025-01-20", author: "Admin", published: true, priority: "high" },
    { id: 2, title: "Holiday Notice", date: "2025-01-18", author: "Admin", published: true, priority: "normal" },
    { id: 3, title: "Sports Day Announcement", date: "2025-01-15", author: "John Doe", published: false, priority: "low" },
];

export default function AnnouncementsListPage() {
    const [announcements] = useState(announcementsData);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <Megaphone className="h-8 w-8 text-primary" />
                        Announcements
                    </h2>
                    <p className="text-muted-foreground">Manage school announcements and notices</p>
                </div>
                <Link href="/cms/announcements/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        New Announcement
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Announcements</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Title</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Author</TableHead>
                                <TableHead>Priority</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {announcements.map((announcement) => (
                                <TableRow key={announcement.id}>
                                    <TableCell className="font-semibold">{announcement.title}</TableCell>
                                    <TableCell>{announcement.date}</TableCell>
                                    <TableCell>{announcement.author}</TableCell>
                                    <TableCell>
                                        <Badge className={
                                            announcement.priority === "high" ? "bg-red-100 text-red-800" :
                                                announcement.priority === "normal" ? "bg-blue-100 text-blue-800" :
                                                    "bg-gray-100 text-gray-800"
                                        }>
                                            {announcement.priority.toUpperCase()}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <Badge className={announcement.published ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"}>
                                            {announcement.published ? "Published" : "Draft"}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Link href={`/cms/announcements/${announcement.id}`}>
                                            <Button variant="outline" size="sm">View</Button>
                                        </Link>
                                        <Link href={`/cms/announcements/${announcement.id}/edit`}>
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
