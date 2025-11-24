"use client";

import { useParams } from "next/navigation";
import { Megaphone, Edit, Trash2, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const announcementData = {
    title: "Mid-term Exam Schedule",
    content: "The mid-term examinations will be held from February 20-25, 2025. Students are advised to prepare accordingly.",
    priority: "high",
    publishDate: "2025-01-20",
    expiryDate: "2025-02-25",
    author: "Admin",
    published: true,
};

export default function AnnouncementDetailPage() {
    const params = useParams();

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-start">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Megaphone className="h-8 w-8 text-primary" />
                        {announcementData.title}
                    </h2>
                </div>
                <div className="flex gap-2">
                    <Link href={`/cms/announcements/${params.id}/edit`}>
                        <Button>
                            <Edit className="mr-2 h-4 w-4" />
                            Edit
                        </Button>
                    </Link>
                    <Button variant="destructive">
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                    </Button>
                </div>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Details</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div>
                            <p className="text-sm text-muted-foreground">Priority</p>
                            <Badge className="mt-1 bg-red-100 text-red-800">
                                {announcementData.priority.toUpperCase()}
                            </Badge>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Author</p>
                            <p className="font-semibold mt-1">{announcementData.author}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Published</p>
                            <p className="font-semibold mt-1 flex items-center gap-1">
                                <Calendar className="h-4 w-4" />
                                {announcementData.publishDate}
                            </p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Expires</p>
                            <p className="font-semibold mt-1">{announcementData.expiryDate}</p>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Content</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="prose max-w-none">
                        <p>{announcementData.content}</p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
