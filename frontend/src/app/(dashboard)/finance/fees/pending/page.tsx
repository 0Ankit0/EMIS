"use client";

import { useState } from "react";
import { AlertTriangle, Send, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const pendingFeesData = [
    { id: 1, studentId: "STU001", name: "John Doe", class: "Grade 10-A", feeType: "Tuition", amount: 5000, dueDate: "2025-01-15", daysOverdue: 8 },
    { id: 2, studentId: "STU015", name: "Jane Smith", class: "Grade 11-B", feeType: "Library", amount: 1500, dueDate: "2025-01-10", daysOverdue: 13 },
    { id: 3, studentId: "STU032", name: "Mike Johnson", class: "Grade 12-A", feeType: "Lab Fee", amount: 3000, dueDate: "2025-01-20", daysOverdue: 3 },
    { id: 4, studentId: "STU045", name: "Sarah Williams", class: "Grade 10-B", feeType: "Hostel", amount: 8000, dueDate: "2025-01-05", daysOverdue: 18 },
];

export default function PendingFeesPage() {
    const [fees] = useState(pendingFeesData);

    const totalPending = fees.reduce((sum, fee) => sum + fee.amount, 0);
    const criticalCount = fees.filter(f => f.daysOverdue > 15).length;

    const handleSendReminder = (studentId: string) => {
        console.log("Sending reminder to:", studentId);
        alert("Reminder sent successfully!");
    };

    const handleBulkReminder = () => {
        console.log("Sending bulk reminders");
        alert(`Reminders sent to ${fees.length} students!`);
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <AlertTriangle className="h-8 w-8 text-red-600" />
                        Pending Fees
                    </h2>
                    <p className="text-muted-foreground">Outstanding fee payments requiring attention</p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" onClick={handleBulkReminder}>
                        <Send className="mr-2 h-4 w-4" />
                        Send All Reminders
                    </Button>
                    <Button>
                        <Download className="mr-2 h-4 w-4" />
                        Export
                    </Button>
                </div>
            </div>

            {/* Alert */}
            {criticalCount > 0 && (
                <Card className="bg-red-50 border-red-200">
                    <CardContent className="p-4 flex items-center gap-3">
                        <AlertTriangle className="h-6 w-6 text-red-600" />
                        <div>
                            <p className="font-semibold text-red-900">Critical Overdue Alert</p>
                            <p className="text-sm text-red-800">
                                {criticalCount} {criticalCount === 1 ? 'student has' : 'students have'} fees overdue by more than 15 days
                            </p>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Pending</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">${totalPending.toLocaleString()}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Students</p>
                        <h3 className="text-3xl font-bold mt-2">{fees.length}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Critical Cases</p>
                        <h3 className="text-3xl font-bold text-orange-600 mt-2">{criticalCount}</h3>
                    </CardContent>
                </Card>
            </div>

            {/* Pending Fees Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Outstanding Payments</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Student ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Class</TableHead>
                                <TableHead>Fee Type</TableHead>
                                <TableHead className="text-right">Amount</TableHead>
                                <TableHead>Due Date</TableHead>
                                <TableHead>Days Overdue</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {fees.map((fee) => (
                                <TableRow key={fee.id}>
                                    <TableCell className="font-mono text-sm">{fee.studentId}</TableCell>
                                    <TableCell className="font-semibold">{fee.name}</TableCell>
                                    <TableCell>{fee.class}</TableCell>
                                    <TableCell>{fee.feeType}</TableCell>
                                    <TableCell className="text-right font-bold text-red-600">
                                        ${fee.amount.toLocaleString()}
                                    </TableCell>
                                    <TableCell>{fee.dueDate}</TableCell>
                                    <TableCell>
                                        <Badge className={
                                            fee.daysOverdue > 15 ? "bg-red-100 text-red-800" :
                                                fee.daysOverdue > 7 ? "bg-orange-100 text-orange-800" :
                                                    "bg-yellow-100 text-yellow-800"
                                        }>
                                            {fee.daysOverdue} days
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => handleSendReminder(fee.studentId)}
                                        >
                                            <Send className="mr-1 h-3 w-3" />
                                            Remind
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
