"use client";

import { useParams } from "next/navigation";
import { FileText, Edit, Trash2, Eye } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const pageData = {
    id: 1,
    title: "About Us",
    slug: "about-us",
    content: "Welcome to our institution. We are dedicated to providing quality education...",
    metaDescription: "Learn about our educational institution and our commitment to excellence.",
    status: "published",
    author: "Admin",
    createdAt: "2025-01-10",
    lastModified: "2025-01-20",
    views: 1245,
};

export default function PageDetailPage() {
    const params = useParams();

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-start">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <FileText className="h-8 w-8 text-primary" />
                        {pageData.title}
                    </h2>
                    <p className="text-muted-foreground">/{pageData.slug}/</p>
                </div>
                <div className="flex gap-2">
                    <Link href={`/cms/pages/${params.id}/edit`}>
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

            {/* Metadata */}
            <Card>
                <CardHeader>
                    <CardTitle>Page Information</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div>
                            <p className="text-sm text-muted-foreground">Status</p>
                            <Badge className="mt-1 bg-green-100 text-green-800">
                                {pageData.status.toUpperCase()}
                            </Badge>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Author</p>
                            <p className="font-semibold mt-1">{pageData.author}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Created</p>
                            <p className="font-semibold mt-1">{pageData.createdAt}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Views</p>
                            <p className="font-semibold mt-1 flex items-center gap-1">
                                <Eye className="h-4 w-4" />
                                {pageData.views.toLocaleString()}
                            </p>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Content */}
            <Card>
                <CardHeader>
                    <CardTitle>Content</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="prose max-w-none">
                        <p>{pageData.content}</p>
                    </div>
                </CardContent>
            </Card>

            {/* SEO */}
            <Card>
                <CardHeader>
                    <CardTitle>SEO</CardTitle>
                </CardHeader>
                <CardContent>
                    <div>
                        <p className="text-sm text-muted-foreground mb-1">Meta Description</p>
                        <p>{pageData.metaDescription}</p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
