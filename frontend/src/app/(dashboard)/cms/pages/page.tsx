"use client";

import { useState } from "react";
import Link from "next/link";
import { FileText, Plus, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const pagesData = [
    { id: 1, title: "About Us", slug: "about-us", status: "published", author: "Admin", lastModified: "2025-01-20", views: 1245 },
    { id: 2, title: "Contact", slug: "contact", status: "published", author: "Admin", lastModified: "2025-01-18", views: 892 },
    { id: 3, title: "Admissions Policy", slug: "admissions-policy", status: "draft", author: "John Doe", lastModified: "2025-01-22", views: 0 },
    { id: 4, title: "Faculty Directory", slug: "faculty", status: "published", author: "Jane Smith", lastModified: "2025-01-15", views: 2341 },
];

export default function CMSPagesListPage() {
    const [pages] = useState(pagesData);
    const [searchTerm, setSearchTerm] = useState("");

    const filteredPages = pages.filter(page =>
        page.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <FileText className="h-8 w-8 text-primary" />
                        Pages
                    </h2>
                    <p className="text-muted-foreground">Manage website pages and content</p>
                </div>
                <Link href="/cms/pages/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Create Page
                    </Button>
                </Link>
            </div>

            {/* Search & Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card className="md:col-span-2">
                    <CardContent className="p-4">
                        <div className="relative">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search pages..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="pl-10"
                            />
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Pages</p>
                        <h3 className="text-3xl font-bold mt-2">{pages.length}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Published</p>
                        <h3 className="text-3xl font-bold text-green-600 mt-2">
                            {pages.filter(p => p.status === "published").length}
                        </h3>
                    </CardContent>
                </Card>
            </div>

            {/* Pages Table */}
            <Card>
                <CardHeader>
                    <CardTitle>All Pages</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Title</TableHead>
                                <TableHead>Slug</TableHead>
                                <TableHead>Author</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>Last Modified</TableHead>
                                <TableHead className="text-right">Views</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredPages.map((page) => (
                                <TableRow key={page.id}>
                                    <TableCell className="font-semibold">{page.title}</TableCell>
                                    <TableCell className="font-mono text-sm text-muted-foreground">{page.slug}</TableCell>
                                    <TableCell>{page.author}</TableCell>
                                    <TableCell>
                                        <Badge className={page.status === "published" ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"}>
                                            {page.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>{page.lastModified}</TableCell>
                                    <TableCell className="text-right">{page.views.toLocaleString()}</TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Link href={`/cms/pages/${page.id}`}>
                                            <Button variant="outline" size="sm">View</Button>
                                        </Link>
                                        <Link href={`/cms/pages/${page.id}/edit`}>
                                            <Button variant="default" size="sm">Edit</Button>
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
