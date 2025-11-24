"use client";

import { Users, GraduationCap } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const enrollmentsData = [
    { id: 1, student: "John Doe", studentId: "STU001", course: "CS101", status: "active", enrolledDate: "2025-01-15" },
    { id: 2, student: "Jane Smith", studentId: "STU002", course: "MATH201", status: "active", enrolledDate: "2025-01-16" },
];

export default function EnrollmentsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <GraduationCap className="h-8 w-8 text-primary" />
                    Course Enrollments
                </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Enrollments</p>
                        <h3 className="text-4xl font-bold text-blue-600 mt-2">245</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Active</p>
                        <h3 className="text-4xl font-bold text-green-600 mt-2">230</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Pending</p>
                        <h3 className="text-4xl font-bold text-yellow-600 mt-2">15</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Enrollments</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Student ID</TableHead>
                                <TableHead>Student Name</TableHead>
                                <TableHead>Course</TableHead>
                                <TableHead>Enrolled Date</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {enrollmentsData.map((enrollment) => (
                                <TableRow key={enrollment.id}>
                                    <TableCell className="font-mono text-sm">{enrollment.studentId}</TableCell>
                                    <TableCell className="font-semibold">{enrollment.student}</TableCell>
                                    <TableCell>{enrollment.course}</TableCell>
                                    <TableCell>{enrollment.enrolledDate}</TableCell>
                                    <TableCell>
                                        <Badge className="bg-green-100 text-green-800">
                                            {enrollment.status.toUpperCase()}
                                        </Badge>
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
