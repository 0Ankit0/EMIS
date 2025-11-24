"use client";

import { MessageSquare, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const discussionsData = [
    { id: 1, title: "Python vs JavaScript", course: "CS101", replies: 15, lastActivity: "2 hours ago" },
    { id: 2, title: "Best IDE for Web Development", course: "WEB201", replies: 8, lastActivity: "1 day ago" },
];

export default function LMSDiscussionsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <MessageSquare className="h-8 w-8 text-primary" />
                    Discussions
                </h2>
                <Link href="/lms/discussions/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        New Discussion
                    </Button>
                </Link>
            </div>

            <div className="grid grid-cols-1 gap-4">
                {discussionsData.map((discussion) => (
                    <Card key={discussion.id} className="cursor-pointer hover:shadow-lg transition">
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <div>
                                    <CardTitle>{discussion.title}</CardTitle>
                                    <p className="text-sm text-muted-foreground mt-1">{discussion.course}</p>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="flex justify-between items-center">
                                <div className="flex gap-6 text-sm text-muted-foreground">
                                    <span>{discussion.replies} replies</span>
                                    <span>Last activity: {discussion.lastActivity}</span>
                                </div>
                                <Link href={`/lms/discussions/${discussion.id}`}>
                                    <Button variant="outline" size="sm">View</Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
