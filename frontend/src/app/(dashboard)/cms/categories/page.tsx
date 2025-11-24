"use client";

import { Folder, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import Link from "next/link";

const categoriesData = [
    { id: 1, name: "Announcements", slug: "announcements", count: 15 },
    { id: 2, name: "Events", slug: "events", count: 8 },
    { id: 3, name: "News", slug: "news", count: 23 },
];

export default function CMSCategoriesPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Folder className="h-8 w-8 text-primary" />
                        Categories
                    </h2>
                    <p className="text-muted-foreground">Organize content by categories</p>
                </div>
                <Link href="/cms/categories/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        New Category
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Categories</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Slug</TableHead>
                                <TableHead className="text-right">Posts</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {categoriesData.map((category) => (
                                <TableRow key={category.id}>
                                    <TableCell className="font-semibold">{category.name}</TableCell>
                                    <TableCell className="font-mono text-sm text-muted-foreground">{category.slug}</TableCell>
                                    <TableCell className="text-right">{category.count}</TableCell>
                                    <TableCell className="text-right">
                                        <Link href={`/cms/categories/${category.id}`}>
                                            <Button variant="outline" size="sm">Edit</Button>
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
