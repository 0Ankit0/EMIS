"use client";

import { useState } from "react";
import { AlertCircle, Mail } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const overdueData = [
    { id: 1, book: "World History", student: "Mike Johnson", studentId: "STU003", issueDate: "2024-12-20", dueDate: "2025-01-03", daysOverdue: 20 },
    { id: 2, book: "Chemistry Basics", student: "Sarah Williams", studentId: "STU004", issueDate: "2024-12-25", dueDate: "2025-01-08", daysOverdue: 15 },
];

export default function OverdueBooksPage() {
    const [overdue] = useState(overdueData);

    const handleSendReminder = (studentId: string) => {
        console.log("Sending reminder to:", studentId);
        alert("Reminder sent!");
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <AlertCircle className="h-8 w-8 text-red-600" />
                    Overdue Books
                </h2>
                <p className="text-muted-foreground">Books past their due date</p>
            </div>

            <Card className="bg-red-50 border-red-200">
                <CardContent className="p-4 flex items-center gap-3">
                    <AlertCircle className="h-6 w-6 text-red-600" />
                    <div>
                        <p className="font-semibold text-red-900">Overdue Books Alert</p>
                        <p className="text-sm text-red-800">{overdue.length} books are currently overdue</p>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Overdue Books ({overdue.length})</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Book Title</TableHead>
                                <TableHead>Student</TableHead>
                                <TableHead>Issue Date</TableHead>
                                <TableHead>Due Date</TableHead>
                                <TableHead>Days Overdue</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {overdue.map((item) => (
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
                                        <Badge className="bg-red-100 text-red-800">
                                            {item.daysOverdue} days
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Button size="sm" variant="outline" onClick={() => handleSendReminder(item.studentId)}>
                                            <Mail className="mr-2 h-4 w-4" />
                                            Send Reminder
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
