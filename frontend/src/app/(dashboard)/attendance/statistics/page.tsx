"use client";

import { useState } from "react";
import { BarChart3, TrendingUp, TrendingDown, Calendar, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const statisticsData = {
    overall: {
        averageAttendance: 92.5,
        totalSessions: 156,
        totalPresent: 14430,
        totalAbsent: 1170,
        totalLate: 400,
        trend: "+2.3%",
    },
    byMonth: [
        { month: "September", rate: 91.2, present: 2850, absent: 250, late: 100 },
        { month: "October", rate: 92.8, present: 2920, absent: 200, late: 80 },
        { month: "November", rate: 93.5, present: 2940, absent: 150, late: 110 },
        { month: "December", rate: 91.8, present: 2880, absent: 220, late: 100 },
        { month: "January", rate: 92.5, present: 2840, absent: 220, late: 140 },
    ],
    byCourse: [
        { course: "CS101", rate: 94.5, sessions: 45, avgPresent: 47 },
        { course: "MATH201", rate: 91.2, sessions: 42, avgPresent: 40 },
        { course: "ENG102", rate: 93.8, sessions: 40, avgPresent: 44 },
        { course: "PHY201", rate: 89.5, sessions: 38, avgPresent: 36 },
    ],
    topAbsentees: [
        { studentId: "STU045", name: "Sarah Williams", absences: 12, rate: 73 },
        { studentId: "STU032", name: "Mike Johnson", absences: 10, rate: 78 },
        { studentId: "STU015", name: "Jane Smith", absences: 8, rate: 82 },
    ],
};

export default function AttendanceStatisticsPage() {
    const [period, setPeriod] = useState("semester");
    const [data] = useState(statisticsData);

    const handleExport = () => {
        console.log("Exporting statistics...");
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <BarChart3 className="h-8 w-8 text-primary" />
                        Attendance Statistics
                    </h2>
                    <p className="text-muted-foreground">Detailed attendance analytics and trends</p>
                </div>
                <div className="flex gap-3">
                    <Select value={period} onValueChange={setPeriod}>
                        <SelectTrigger className="w-40">
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="week">This Week</SelectItem>
                            <SelectItem value="month">This Month</SelectItem>
                            <SelectItem value="semester">This Semester</SelectItem>
                            <SelectItem value="year">This Year</SelectItem>
                        </SelectContent>
                    </Select>
                    <Button onClick={handleExport}>
                        <Download className="mr-2 h-4 w-4" />
                        Export Report
                    </Button>
                </div>
            </div>

            {/* Overall Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card className="border-l-4 border-blue-500">
                    <CardContent className="p-6">
                        <div>
                            <p className="text-sm text-muted-foreground">Average Attendance</p>
                            <div className="flex items-end gap-2 mt-2">
                                <h3 className="text-3xl font-bold text-blue-600">{data.overall.averageAttendance}%</h3>
                                <span className="text-sm text-green-600 font-semibold flex items-center mb-1">
                                    <TrendingUp className="h-4 w-4 mr-1" />
                                    {data.overall.trend}
                                </span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Sessions</p>
                        <h3 className="text-3xl font-bold mt-2">{data.overall.totalSessions}</h3>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Present</p>
                        <h3 className="text-3xl font-bold text-green-600 mt-2">{data.overall.totalPresent.toLocaleString()}</h3>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Absent</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">{data.overall.totalAbsent.toLocaleString()}</h3>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Monthly Trend */}
                <Card>
                    <CardHeader>
                        <CardTitle>Monthly Trend</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {data.byMonth.map((month, index) => (
                                <div key={index} className="flex items-center justify-between">
                                    <div className="flex-1">
                                        <div className="flex justify-between mb-1">
                                            <span className="text-sm font-medium">{month.month}</span>
                                            <span className="text-sm font-bold text-blue-600">{month.rate}%</span>
                                        </div>
                                        <div className="w-full bg-gray-200 rounded-full h-2">
                                            <div
                                                className="bg-blue-600 h-2 rounded-full"
                                                style={{ width: `${month.rate}%` }}
                                            />
                                        </div>
                                    </div>
                                    <div className="ml-4 text-right">
                                        <p className="text-xs text-muted-foreground">Present</p>
                                        <p className="text-sm font-semibold text-green-600">{month.present}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                {/* Course-wise Statistics */}
                <Card>
                    <CardHeader>
                        <CardTitle>Course-wise Statistics</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {data.byCourse.map((course, index) => (
                                <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                                    <div className="flex justify-between items-center mb-2">
                                        <h4 className="font-semibold">{course.course}</h4>
                                        <span className="text-lg font-bold text-blue-600">{course.rate}%</span>
                                    </div>
                                    <div className="grid grid-cols-2 gap-4 text-sm">
                                        <div>
                                            <p className="text-muted-foreground">Sessions</p>
                                            <p className="font-semibold">{course.sessions}</p>
                                        </div>
                                        <div>
                                            <p className="text-muted-foreground">Avg. Present</p>
                                            <p className="font-semibold">{course.avgPresent}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Top Absentees */}
            <Card className="bg-red-50">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-red-900">
                        <TrendingDown className="h-5 w-5" />
                        Students Requiring Attention
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-3">
                        {data.topAbsentees.map((student, index) => (
                            <div key={index} className="bg-white rounded-lg p-4 flex justify-between items-center">
                                <div>
                                    <p className="font-semibold text-gray-900">{student.name}</p>
                                    <p className="text-sm text-gray-600">ID: {student.studentId}</p>
                                </div>
                                <div className="text-right">
                                    <p className="text-2xl font-bold text-red-600">{student.absences}</p>
                                    <p className="text-sm text-gray-600">absences ({student.rate}% attendance)</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
