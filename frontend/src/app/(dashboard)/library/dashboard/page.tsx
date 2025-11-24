"use client";

import Link from "next/link";
import { Book, Plus, CheckCircle, AlertTriangle, Users, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Mock data
const stats = {
    totalBooks: 5432,
    availableBooks: 3890,
    issuedBooks: 1542,
    overdueBooks: 87,
    totalMembers: 2150,
};

const recentIssues = [
    { id: 1, bookTitle: "Introduction to Algorithms", borrowerName: "John Doe", issueDate: "Oct 20, 2025" },
    { id: 2, bookTitle: "Clean Code", borrowerName: "Jane Smith", issueDate: "Oct 19, 2025" },
    { id: 3, bookTitle: "The Pragmatic Programmer", borrowerName: "Mike Brown", issueDate: "Oct 18, 2025" },
];

const popularBooks = [
    { id: 1, title: "Design Patterns", author: "Gang of Four", issueCount: 45 },
    { id: 2, title: "Refactoring", author: "Martin Fowler", issueCount: 38 },
    { id: 3, title: "Code Complete", author: "Steve McConnell", issueCount: 32 },
];

export default function LibraryDashboardPage() {
    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Book className="h-8 w-8 text-primary" />
                    Library Dashboard
                </h2>
                <p className="text-muted-foreground">Library management system</p>
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
                <Card className="border-l-4 border-blue-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Total Books</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.totalBooks.toLocaleString()}</h3>
                            </div>
                            <div className="bg-blue-100 rounded-full p-4">
                                <Book className="h-6 w-6 text-blue-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-green-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Available</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.availableBooks.toLocaleString()}</h3>
                            </div>
                            <div className="bg-green-100 rounded-full p-4">
                                <CheckCircle className="h-6 w-6 text-green-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-yellow-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Issued</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.issuedBooks.toLocaleString()}</h3>
                            </div>
                            <div className="bg-yellow-100 rounded-full p-4">
                                <TrendingUp className="h-6 w-6 text-yellow-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-red-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Overdue</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.overdueBooks}</h3>
                            </div>
                            <div className="bg-red-100 rounded-full p-4">
                                <AlertTriangle className="h-6 w-6 text-red-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-purple-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Members</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.totalMembers.toLocaleString()}</h3>
                            </div>
                            <div className="bg-purple-100 rounded-full p-4">
                                <Users className="h-6 w-6 text-purple-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Quick Actions */}
            <Card>
                <CardHeader>
                    <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                        <Link href="/library/books">
                            <Book className="mr-2 h-5 w-5" />
                            Books Catalog
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                        <Link href="/library/books/new">
                            <Plus className="mr-2 h-5 w-5" />
                            Add Book
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-yellow-600 hover:bg-yellow-700" asChild>
                        <Link href="/library/issue">
                            <TrendingUp className="mr-2 h-5 w-5" />
                            Issue Book
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                        <Link href="/library/return">
                            <CheckCircle className="mr-2 h-5 w-5" />
                            Return Book
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-indigo-600 hover:bg-indigo-700" asChild>
                        <Link href="/library/issued">
                            <Book className="mr-2 h-5 w-5" />
                            Issued Books
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-red-600 hover:bg-red-700" asChild>
                        <Link href="/library/overdue">
                            <AlertTriangle className="mr-2 h-5 w-5" />
                            Overdue Books
                        </Link>
                    </Button>
                </CardContent>
            </Card>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Recent Issues */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <TrendingUp className="h-5 w-5 text-primary" />
                            Recent Issues
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {recentIssues.length > 0 ? (
                            <div className="space-y-3">
                                {recentIssues.map((issue) => (
                                    <div key={issue.id} className="border-l-4 border-blue-500 pl-4 py-2 rounded hover:bg-gray-50 transition-colors">
                                        <p className="font-semibold text-gray-800">{issue.bookTitle}</p>
                                        <p className="text-sm text-gray-600">Issued to: {issue.borrowerName}</p>
                                        <p className="text-xs text-gray-500">{issue.issueDate}</p>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-center text-muted-foreground py-4">No recent issues.</p>
                        )}
                    </CardContent>
                </Card>

                {/* Popular Books */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Book className="h-5 w-5 text-primary" />
                            Popular Books
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {popularBooks.length > 0 ? (
                            <div className="space-y-3">
                                {popularBooks.map((book) => (
                                    <div key={book.id} className="border-l-4 border-green-500 pl-4 py-2 rounded hover:bg-gray-50 transition-colors">
                                        <p className="font-semibold text-gray-800">{book.title}</p>
                                        <p className="text-sm text-gray-600">by {book.author}</p>
                                        <p className="text-xs text-gray-500">Issues: {book.issueCount}</p>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-center text-muted-foreground py-4">No data available.</p>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
