"use client";

import { useState } from "react";
import Link from "next/link";
import { Book, Plus, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const booksData = [
    { id: 1, isbn: "978-0-123-45678-9", title: "Introduction to Programming", author: "John Smith", category: "Computer Science", copies: 10, available: 7 },
    { id: 2, isbn: "978-0-987-65432-1", title: "Advanced Mathematics", author: "Jane Doe", category: "Mathematics", copies: 8, available: 3 },
    { id: 3, isbn: "978-0-555-77777-3", title: "World History", author: "Mike Johnson", category: "History", copies: 12, available: 12 },
];

export default function BooksPage() {
    const [books] = useState(booksData);
    const [searchTerm, setSearchTerm] = useState("");

    const filteredBooks = books.filter(book =>
        book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        book.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
        book.isbn.includes(searchTerm)
    );

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <Book className="h-8 w-8 text-primary" />
                        Book Catalog
                    </h2>
                    <p className="text-muted-foreground">Browse and manage library books</p>
                </div>
                <Link href="/library/books/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Book
                    </Button>
                </Link>
            </div>

            {/* Search */}
            <Card>
                <CardContent className="p-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search by title, author, or ISBN..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="pl-10"
                        />
                    </div>
                </CardContent>
            </Card>

            {/* Books Table */}
            <Card>
                <CardHeader>
                    <CardTitle>All Books ({filteredBooks.length})</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>ISBN</TableHead>
                                <TableHead>Title</TableHead>
                                <TableHead>Author</TableHead>
                                <TableHead>Category</TableHead>
                                <TableHead className="text-right">Total Copies</TableHead>
                                <TableHead className="text-right">Available</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredBooks.map((book) => (
                                <TableRow key={book.id}>
                                    <TableCell className="font-mono text-sm">{book.isbn}</TableCell>
                                    <TableCell className="font-semibold">{book.title}</TableCell>
                                    <TableCell>{book.author}</TableCell>
                                    <TableCell>{book.category}</TableCell>
                                    <TableCell className="text-right">{book.copies}</TableCell>
                                    <TableCell className="text-right font-bold">{book.available}</TableCell>
                                    <TableCell>
                                        <Badge className={book.available > 0 ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}>
                                            {book.available > 0 ? "Available" : "Out of Stock"}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Link href={`/library/books/${book.id}`}>
                                            <Button variant="outline" size="sm">View</Button>
                                        </Link>
                                        <Link href={`/library/issue?bookId=${book.id}`}>
                                            <Button size="sm" disabled={book.available === 0}>Issue</Button>
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
