"use client";

import { GraduationCap, BookOpen, Users, Calendar } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function FacultyDashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <GraduationCap className="h-8 w-8 text-primary" />
                    Faculty Dashboard
                </h2>
                <p className="text-lg text-muted-foreground">Welcome, Dr. Smith</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Courses</p>
                        <h3 className="text-3xl font-bold mt-2">5</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Students</p>
                        <h3 className="text-3xl font-bold mt-2">150</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Pending Grades</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">23</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Classes Today</p>
                        <h3 className="text-3xl font-bold mt-2">3</h3>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Link href="/exams/list">
                    <Card className="cursor-pointer hover:shadow-lg transition">
                        <CardContent className="p-6">
                            <BookOpen className="h-12 w-12 text-blue-600 mb-4" />
                            <h4 className="font-bold text-lg">Grade Entry</h4>
                            <p className="text-sm text-muted-foreground">Enter student grades</p>
                        </CardContent>
                    </Card>
                </Link>

                <Link href="/portal/student/courses">
                    <Card className="cursor-pointer hover:shadow-lg transition">
                        <CardContent className="p-6">
                            <Users className="h-12 w-12 text-green-600 mb-4" />
                            <h4 className="font-bold text-lg">My Students</h4>
                            <p className="text-sm text-muted-foreground">View student list</p>
                        </CardContent>
                    </Card>
                </Link>

                <Link href="/attendance/mark">
                    <Card className="cursor-pointer hover:shadow-lg transition">
                        <CardContent className="p-6">
                            <Calendar className="h-12 w-12 text-purple-600 mb-4" />
                            <h4 className="font-bold text-lg">Attendance</h4>
                            <p className="text-sm text-muted-foreground">Mark attendance</p>
                        </CardContent>
                    </Card>
                </Link>
            </div>
        </div>
    );
}
