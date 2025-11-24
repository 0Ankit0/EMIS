"use client";

import Link from "next/link";
import { GraduationCap, BookOpen, Calendar, Bell } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const studentData = {
    name: "John Doe",
    studentId: "STU001",
    class: "Grade 10-A",
    attendance: 95,
    upcomingClasses: [
        { id: 1, subject: "Mathematics", time: "09:00 AM", room: "Room 101" },
        { id: 2, subject: "Physics", time: "11:00 AM", room: "Lab 2" },
    ],
    recentGrades: [
        { id: 1, subject: "Chemistry", grade: "A", marks: "92/100" },
        { id: 2, subject: "English", grade: "B+", marks: "85/100" },
    ],
    announcements: [
        { id: 1, title: "Mid-term Exam Schedule", date: "2025-01-20" },
        { id: 2, title: "Sports Day Event", date: "2025-02-15" },
    ],
};

export default function StudentPortalPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <GraduationCap className="h-8 w-8 text-primary" />
                    Student Portal
                </h2>
                <p className="text-lg text-muted-foreground">Welcome back, {studentData.name}!</p>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Student ID</p>
                        <h3 className="text-2xl font-bold mt-2">{studentData.studentId}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Class</p>
                        <h3 className="text-2xl font-bold mt-2">{studentData.class}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Attendance</p>
                        <h3 className="text-2xl font-bold text-green-600 mt-2">{studentData.attendance}%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <Link href="/portal/student/courses">
                            <Button className="w-full">My Courses</Button>
                        </Link>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Upcoming Classes */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Calendar className="h-5 w-5" />
                            Today's Classes
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-3">
                            {studentData.upcomingClasses.map((cls) => (
                                <div key={cls.id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                                    <div>
                                        <p className="font-semibold">{cls.subject}</p>
                                        <p className="text-sm text-muted-foreground">{cls.room}</p>
                                    </div>
                                    <span className="text-sm font-bold text-blue-600">{cls.time}</span>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                {/* Recent Grades */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <BookOpen className="h-5 w-5" />
                            Recent Grades
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-3">
                            {studentData.recentGrades.map((grade) => (
                                <div key={grade.id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                                    <div>
                                        <p className="font-semibold">{grade.subject}</p>
                                        <p className="text-sm text-muted-foreground">{grade.marks}</p>
                                    </div>
                                    <span className="text-xl font-bold text-green-600">{grade.grade}</span>
                                </div>
                            ))}
                        </div>
                        <Link href="/portal/student/grades">
                            <Button variant="outline" className="w-full mt-4">View All Grades</Button>
                        </Link>
                    </CardContent>
                </Card>
            </div>

            {/* Announcements */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Bell className="h-5 w-5" />
                        Latest Announcements
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-3">
                        {studentData.announcements.map((announcement) => (
                            <div key={announcement.id} className="flex justify-between items-center p-3 border-l-4 border-blue-500 bg-blue-50">
                                <p className="font-semibold">{announcement.title}</p>
                                <span className="text-sm text-muted-foreground">{announcement.date}</span>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
