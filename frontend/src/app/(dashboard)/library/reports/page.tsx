"use client";

import { BookCheck, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const reportsData = {
    totalBooks: 150,
    issuedBooks: 45,
    overdueBooks: 5,
    topBooks: [
        { title: "Introduction to Programming", issues: 25 },
        { title: "Advanced Mathematics", issues: 18 },
    ],
};

export default function LibraryReportsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <BookCheck className="h-8 w-8 text-primary" />
                        Library Reports
                    </h2>
                    <p className="text-muted-foreground">Usage statistics and analytics</p>
                </div>
                <Button>
                    <Download className="mr-2 h-4 w-4" />
                    Export Report
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Books</p>
                        <h3 className="text-4xl font-bold text-blue-600 mt-2">{reportsData.totalBooks}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Currently Issued</p>
                        <h3 className="text-4xl font-bold text-green-600 mt-2">{reportsData.issuedBooks}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Overdue</p>
                        <h3 className="text-4xl font-bold text-red-600 mt-2">{reportsData.overdueBooks}</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Most Issued Books</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Book Title</TableHead>
                                <TableHead className="text-right">Total Issues</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {reportsData.topBooks.map((book, idx) => (
                                <TableRow key={idx}>
                                    <TableCell className="font-semibold">{book.title}</TableCell>
                                    <TableCell className="text-right font-bold">{book.issues}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
