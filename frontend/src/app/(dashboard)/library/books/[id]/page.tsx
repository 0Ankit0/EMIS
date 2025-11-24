"use client";

import { BookOpen, Edit, Trash2 } from "lucide-react";
import { useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";

const bookData = {
    isbn: "978-0-123-45678-9",
    title: "Introduction to Programming",
    author: "John Doe",
    publisher: "Tech Books Publishing",
    published_year: 2023,
    category: "Computer Science",
    total_copies: 10,
    available_copies: 7,
    description: "A comprehensive guide to programming fundamentals",
};

export default function BookDetailPage() {
    const params = useParams();

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-start">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <BookOpen className="h-8 w-8 text-primary" />
                        {bookData.title}
                    </h2>
                    <p className="text-lg text-muted-foreground mt-1">by {bookData.author}</p>
                </div>
                <div className="flex gap-2">
                    <Link href={`/library/books/${params.id}/edit`}>
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

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Copies</p>
                        <h3 className="text-4xl font-bold text-blue-600 mt-2">{bookData.total_copies}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Available</p>
                        <h3 className="text-4xl font-bold text-green-600 mt-2">{bookData.available_copies}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Issued</p>
                        <h3 className="text-4xl font-bold text-orange-600 mt-2">{bookData.total_copies - bookData.available_copies}</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Book Information</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <p className="text-sm text-muted-foreground">ISBN</p>
                            <p className="font-mono font-semibold">{bookData.isbn}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Category</p>
                            <p className="font-semibold">{bookData.category}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Publisher</p>
                            <p className="font-semibold">{bookData.publisher}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Published Year</p>
                            <p className="font-semibold">{bookData.published_year}</p>
                        </div>
                    </div>
                    <div className="mt-4">
                        <p className="text-sm text-muted-foreground">Description</p>
                        <p className="mt-2">{bookData.description}</p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
