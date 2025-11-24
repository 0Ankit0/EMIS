"use client";

import { Calendar, Users } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const attendanceReports = [
    { id: 1, class: "Grade 10-A", date: "2025-01-23", present: 28, absent: 2, late: 1, rate: "93%" },
    { id: 2, class: "Grade 10-B", date: "2025-01-23", present: 25, absent: 5, late: 0, rate: "83%" },
    { id: 3, class: "Grade 11-A", date: "2025-01-23", present: 30, absent: 0, late: 2, rate: "100%" },
];

export default function AttendanceReportsPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Calendar className="h-8 w-8 text-primary" />
                Attendance Reports
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Average Attendance</p>
                        <h3 className="text-3xl font-bold text-blue-600 mt-2">92%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Most Regular Class</p>
                        <h3 className="text-2xl font-bold text-green-600 mt-2">Grade 11-A</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Absentees Today</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">7</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Daily Class Summary</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Class</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead className="text-right">Present</TableHead>
                                <TableHead className="text-right">Absent</TableHead>
                                <TableHead className="text-right">Late</TableHead>
                                <TableHead className="text-right">Rate</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {attendanceReports.map((report) => (
                                <TableRow key={report.id}>
                                    <TableCell className="font-semibold">{report.class}</TableCell>
                                    <TableCell>{report.date}</TableCell>
                                    <TableCell className="text-right text-green-600">{report.present}</TableCell>
                                    <TableCell className="text-right text-red-600">{report.absent}</TableCell>
                                    <TableCell className="text-right text-orange-600">{report.late}</TableCell>
                                    <TableCell className="text-right font-bold">{report.rate}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
