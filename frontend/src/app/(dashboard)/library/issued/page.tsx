"use client";

import { useState } from "react";
import { BookCheck, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const issuedBooksData = [
    { id: 1, book: "Introduction to Programming", student: "John Doe", studentId: "STU001", issueDate: "2025-01-10", dueDate: "2025-01-24", status: "active" },
    { id: 2, book: "Advanced Mathematics", student: "Jane Smith", studentId: "STU002", issueDate: "2025-01-12", dueDate: "2025-01-26", status: "active" },
    { id: 3, book: "World History", student: "Mike Johnson", studentId: "STU003", issueDate: "2024-12-20", dueDate: "2025-01-03", status: "overdue" },
];

export default function IssuedBooksPage() {
    const [issued] = useState(issuedBooksData);

    const handleReturn = (id: number) => {
        console.log("Returning book:", id);
        alert("Book returned successfully!");
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <BookCheck className="h-8 w-8 text-primary" />
                    Issued Books
                </h2>
                <p className="text-muted-foreground">Currently issued books</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Issued Books ({issued.length})</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Book Title</TableHead>
                                <TableHead>Student</TableHead>
                                <TableHead>Issue Date</TableHead>
                                <TableHead>Due Date</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {issued.map((item) => (
                                <TableRow key={item.id}>
                                    <TableCell className="font-semibold">{item.book}</TableCell>
                                    <TableCell>
                                        <div>
                                            <p className="font-semibold">{item.student}</p>
                                            <p className="text-sm text-muted-foreground">{item.studentId}</p>
                                        </div>
                                    </TableCell>
                                    <TableCell>{item.issueDate}</TableCell>
                                    <TableCell>{item.dueDate}</TableCell>
                                    <TableCell>
                                        <Badge className={item.status === "overdue" ? "bg-red-100 text-red-800" : "bg-green-100 text-green-800"}>
                                            {item.status.toUpperCase()}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Button size="sm" onClick={() => handleReturn(item.id)}>
                                            <CheckCircle className="mr-2 h-4 w-4" />
                                            Return
                                        </Button>
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
