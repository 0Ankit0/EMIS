"use client";

import { useState } from "react";
import { Calendar, Download, TrendingUp, Users, UserCheck, UserX } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const mockData = {
    date: "2025-01-23",
    totalSessions: 12,
    totalStudents: 350,
    presentCount: 322,
    absentCount: 28,
    lateCount: 15,
    attendanceRate: 92,
    sessions: [
        { course: "CS101", time: "09:00-10:30", present: 45, absent: 3, late: 2, total: 50 },
        { course: "MATH201", time: "11:00-12:30", present: 38, absent: 5, late: 1, total: 44 },
        { course: "ENG102", time: "14:00-15:30", present: 42, absent: 2, late: 3, total: 47 },
    ],
    absentees: [
        { studentId: "STU001", name: "John Doe", course: "CS101", reason: "Sick" },
        { studentId: "STU015", name: "Jane Smith", course: "MATH201", reason: "Family emergency" },
        { studentId: "STU032", name: "Mike Johnson", course: "ENG102", reason: "Not specified" },
    ],
};

export default function DailyAttendanceReportPage() {
    const [selectedDate, setSelectedDate] = useState(mockData.date);
    const [data] = useState(mockData);

    const handleExport = () => {
        console.log("Exporting daily report for:", selectedDate);
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <Calendar className="h-8 w-8 text-primary" />
                        Daily Attendance Report
                    </h2>
                    <p className="text-muted-foreground">Comprehensive attendance summary for {selectedDate}</p>
                </div>
                <div className="flex gap-3">
                    <input
                        type="date"
                        value={selectedDate}
                        onChange={(e) => setSelectedDate(e.target.value)}
                        className="flex h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
                    />
                    <Button onClick={handleExport}>
                        <Download className="mr-2 h-4 w-4" />
                        Export PDF
                    </Button>
                </div>
            </div>

            {/* Summary Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Sessions</p>
                                <h3 className="text-3xl font-bold mt-2">{data.totalSessions}</h3>
                            </div>
                            <Calendar className="h-8 w-8 text-blue-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Total Students</p>
                                <h3 className="text-3xl font-bold mt-2">{data.totalStudents}</h3>
                            </div>
                            <Users className="h-8 w-8 text-purple-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Present</p>
                                <h3 className="text-3xl font-bold text-green-600 mt-2">{data.presentCount}</h3>
                            </div>
                            <UserCheck className="h-8 w-8 text-green-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Absent</p>
                                <h3 className="text-3xl font-bold text-red-600 mt-2">{data.absentCount}</h3>
                            </div>
                            <UserX className="h-8 w-8 text-red-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Attendance Rate</p>
                                <h3 className="text-3xl font-bold text-blue-600 mt-2">{data.attendanceRate}%</h3>
                            </div>
                            <TrendingUp className="h-8 w-8 text-blue-600" />
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Session-wise Breakdown */}
            <Card>
                <CardHeader>
                    <CardTitle>Session-wise Breakdown</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Course</TableHead>
                                <TableHead>Time</TableHead>
                                <TableHead className="text-right">Total</TableHead>
                                <TableHead className="text-right">Present</TableHead>
                                <TableHead className="text-right">Late</TableHead>
                                <TableHead className="text-right">Absent</TableHead>
                                <TableHead className="text-right">Rate</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {data.sessions.map((session, index) => (
                                <TableRow key={index}>
                                    <TableCell className="font-semibold">{session.course}</TableCell>
                                    <TableCell>{session.time}</TableCell>
                                    <TableCell className="text-right font-bold">{session.total}</TableCell>
                                    <TableCell className="text-right text-green-600 font-semibold">{session.present}</TableCell>
                                    <TableCell className="text-right text-yellow-600 font-semibold">{session.late}</TableCell>
                                    <TableCell className="text-right text-red-600 font-semibold">{session.absent}</TableCell>
                                    <TableCell className="text-right font-bold">
                                        {Math.round((session.present / session.total) * 100)}%
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

            {/* Absentees List */}
            <Card>
                <CardHeader>
                    <CardTitle>Today's Absentees ({data.absentees.length})</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Student ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Course</TableHead>
                                <TableHead>Reason</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {data.absentees.map((student, index) => (
                                <TableRow key={index}>
                                    <TableCell className="font-mono text-sm">{student.studentId}</TableCell>
                                    <TableCell className="font-semibold">{student.name}</TableCell>
                                    <TableCell>{student.course}</TableCell>
                                    <TableCell className="text-muted-foreground">{student.reason}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
