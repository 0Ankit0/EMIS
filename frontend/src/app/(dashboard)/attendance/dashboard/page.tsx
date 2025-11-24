"use client";

import Link from "next/link";
import { Calendar, Plus, List, UserCheck, UserX, TrendingUp, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

// Mock data
const stats = {
    sessionsToday: 12,
    attendanceRate: 92,
    presentCount: 1150,
    absentCount: 98,
};

const todaySessions = [
    { id: 1, title: "CS101 - Lecture", course: "Introduction to Computer Science", startTime: "09:00", endTime: "10:30", status: "completed" },
    { id: 2, title: "MATH201 - Tutorial", course: "Calculus II", startTime: "11:00", endTime: "12:00", status: "in_progress" },
    { id: 3, title: "ENG102 - Lab", course: "English Literature", startTime: "14:00", endTime: "15:30", status: "scheduled" },
];

const recentRecords = [
    { id: 1, student: "John Doe", course: "CS101", status: "present" },
    { id: 2, student: "Jane Smith", course: "MATH201", status: "present" },
    { id: 3, student: "Mike Brown", course: "ENG102", status: "absent" },
    { id: 4, student: "Sarah Wilson", course: "CS101", status: "late" },
];

export default function AttendanceDashboardPage() {
    const getSessionStatusBadge = (status: string) => {
        switch (status) {
            case "completed":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Completed</Badge>;
            case "in_progress":
                return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-yellow-200">In Progress</Badge>;
            case "scheduled":
                return <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-200 border-gray-200">Scheduled</Badge>;
            default:
                return <Badge variant="secondary">{status}</Badge>;
        }
    };

    const getRecordStatusBadge = (status: string) => {
        switch (status) {
            case "present":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Present</Badge>;
            case "absent":
                return <Badge className="bg-red-100 text-red-800 hover:bg-red-200 border-red-200">Absent</Badge>;
            case "late":
                return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-yellow-200">Late</Badge>;
            case "excused":
                return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-200 border-blue-200">Excused</Badge>;
            default:
                return <Badge variant="secondary">{status}</Badge>;
        }
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Calendar className="h-8 w-8 text-primary" />
                    Attendance Dashboard
                </h2>
                <p className="text-muted-foreground">Track and manage attendance records</p>
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card className="border-l-4 border-blue-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Sessions Today</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.sessionsToday}</h3>
                            </div>
                            <div className="bg-blue-100 rounded-full p-4">
                                <Calendar className="h-6 w-6 text-blue-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-green-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Attendance Rate</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.attendanceRate}%</h3>
                            </div>
                            <div className="bg-green-100 rounded-full p-4">
                                <TrendingUp className="h-6 w-6 text-green-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-yellow-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Present</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.presentCount.toLocaleString()}</h3>
                            </div>
                            <div className="bg-yellow-100 rounded-full p-4">
                                <UserCheck className="h-6 w-6 text-yellow-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-red-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Absent</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.absentCount}</h3>
                            </div>
                            <div className="bg-red-100 rounded-full p-4">
                                <UserX className="h-6 w-6 text-red-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Quick Actions */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        Quick Actions
                    </CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                        <Link href="/attendance/mark">
                            <Plus className="mr-2 h-5 w-5" />
                            Mark Attendance
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                        <Link href="/attendance/sessions/new">
                            <Calendar className="mr-2 h-5 w-5" />
                            New Session
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                        <Link href="/attendance/records">
                            <List className="mr-2 h-5 w-5" />
                            View Records
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-yellow-600 hover:bg-yellow-700" asChild>
                        <Link href="/attendance/sessions">
                            <Clock className="mr-2 h-5 w-5" />
                            View Sessions
                        </Link>
                    </Button>
                </CardContent>
            </Card>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Today's Sessions */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Calendar className="h-5 w-5 text-primary" />
                            Today's Sessions
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-3">
                            {todaySessions.length > 0 ? (
                                todaySessions.map((session) => (
                                    <div key={session.id} className="border-l-4 border-blue-500 pl-4 py-2 hover:bg-gray-50 transition-colors rounded">
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <Link href={`/attendance/sessions/${session.id}`} className="font-semibold text-gray-800 hover:text-blue-600">
                                                    {session.title}
                                                </Link>
                                                <p className="text-sm text-muted-foreground">{session.course} • {session.startTime} - {session.endTime}</p>
                                            </div>
                                            {getSessionStatusBadge(session.status)}
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <p className="text-center text-muted-foreground py-4">No sessions scheduled for today</p>
                            )}
                        </div>
                    </CardContent>
                </Card>

                {/* Recent Records */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Clock className="h-5 w-5 text-primary" />
                            Recent Records
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Student</TableHead>
                                    <TableHead>Course</TableHead>
                                    <TableHead>Status</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {recentRecords.length > 0 ? (
                                    recentRecords.map((record) => (
                                        <TableRow key={record.id}>
                                            <TableCell>{record.student}</TableCell>
                                            <TableCell className="text-sm">{record.course}</TableCell>
                                            <TableCell>{getRecordStatusBadge(record.status)}</TableCell>
                                        </TableRow>
                                    ))
                                ) : (
                                    <TableRow>
                                        <TableCell colSpan={3} className="text-center text-muted-foreground">No recent records</TableCell>
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
