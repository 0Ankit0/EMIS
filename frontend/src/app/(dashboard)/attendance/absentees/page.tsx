"use client";

import Link from "next/link";
import { UserX, Mail, Phone, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const absenteesData = [
    { id: 1, studentId: "STU001", name: "John Doe", course: "CS101", date: "2025-01-23", consecutiveDays: 1, email: "john@example.com", phone: "+1234567890" },
    { id: 2, studentId: "STU015", name: "Jane Smith", course: "MATH201", date: "2025-01-23", consecutiveDays: 3, email: "jane@example.com", phone: "+1234567891" },
    { id: 3, studentId: "STU032", name: "Mike Johnson", course: "ENG102", date: "2025-01-23", consecutiveDays: 2, email: "mike@example.com", phone: "+1234567892" },
    { id: 4, studentId: "STU045", name: "Sarah Williams", course: "CS101", date: "2025-01-23", consecutiveDays: 5, email: "sarah@example.com", phone: "+1234567893" },
];

export default function AbsenteesPage() {
    const handleNotify = (studentId: string) => {
        console.log("Notifying student:", studentId);
        alert("Notification sent!");
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <UserX className="h-8 w-8 text-red-600" />
                    Absentees
                </h2>
                <p className="text-muted-foreground">Students absent today and requiring attention</p>
            </div>

            {/* Alert for chronic absentees */}
            <Card className="bg-red-50 border-red-200">
                <CardContent className="p-4 flex items-center gap-3">
                    <AlertTriangle className="h-6 w-6 text-red-600" />
                    <div>
                        <p className="font-semibold text-red-900">Chronic Absenteeism Alert</p>
                        <p className="text-sm text-red-800">
                            {absenteesData.filter(a => a.consecutiveDays >= 3).length} students have been absent for 3+ consecutive days
                        </p>
                    </div>
                </CardContent>
            </Card>

            {/* Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Absentees Today</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">{absenteesData.length}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Chronic (3+ days)</p>
                        <h3 className="text-3xl font-bold text-orange-600 mt-2">
                            {absenteesData.filter(a => a.consecutiveDays >= 3).length}
                        </h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Critical (5+ days)</p>
                        <h3 className="text-3xl font-bold text-red-700 mt-2">
                            {absenteesData.filter(a => a.consecutiveDays >= 5).length}
                        </h3>
                    </CardContent>
                </Card>
            </div>

            {/* Absentees Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Student List</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Student ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Course</TableHead>
                                <TableHead>Consecutive Days</TableHead>
                                <TableHead>Contact</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {absenteesData.map((student) => (
                                <TableRow key={student.id}>
                                    <TableCell className="font-mono text-sm">{student.studentId}</TableCell>
                                    <TableCell className="font-semibold">{student.name}</TableCell>
                                    <TableCell>{student.course}</TableCell>
                                    <TableCell>
                                        <Badge className={
                                            student.consecutiveDays >= 5 ? "bg-red-100 text-red-800" :
                                                student.consecutiveDays >= 3 ? "bg-orange-100 text-orange-800" :
                                                    "bg-yellow-100 text-yellow-800"
                                        }>
                                            {student.consecutiveDays} {student.consecutiveDays === 1 ? 'day' : 'days'}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex flex-col gap-1">
                                            <span className="text-sm flex items-center gap-1">
                                                <Mail className="h-3 w-3" />
                                                {student.email}
                                            </span>
                                            <span className="text-sm flex items-center gap-1">
                                                <Phone className="h-3 w-3" />
                                                {student.phone}
                                            </span>
                                        </div>
                                    </TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Link href={`/students/${student.studentId}`}>
                                            <Button variant="outline" size="sm">View</Button>
                                        </Link>
                                        <Button
                                            variant="default"
                                            size="sm"
                                            onClick={() => handleNotify(student.studentId)}
                                        >
                                            Notify
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
