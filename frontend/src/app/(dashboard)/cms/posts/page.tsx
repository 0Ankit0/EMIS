"use client";

import { FileText, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const postsData = [
    { id: 1, title: "Welcome to New Academic Year", category: "News", date: "2025-01-15", status: "published" },
    { id: 2, title: "Upcoming Cultural Fest", category: "Events", date: "2025-01-18", status: "draft" },
];

export default function CMSPostsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <FileText className="h-8 w-8 text-primary" />
                        Posts
                    </h2>
                    <p className="text-muted-foreground">Blog posts and articles</p>
                </div>
                <Link href="/cms/posts/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Create Post
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Posts</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Title</TableHead>
                                <TableHead>Category</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {postsData.map((post) => (
                                <TableRow key={post.id}>
                                    <TableCell className="font-semibold">{post.title}</TableCell>
                                    <TableCell>{post.category}</TableCell>
                                    <TableCell>{post.date}</TableCell>
                                    <TableCell>
                                        <Badge className={post.status === "published" ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"}>
                                            {post.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Link href={`/cms/posts/${post.id}`}>
                                            <Button variant="outline" size="sm">View</Button>
                                        </Link>
                                        <Link href={`/cms/posts/${post.id}/edit`}>
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
