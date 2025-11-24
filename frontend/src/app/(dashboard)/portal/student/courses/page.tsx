"use client";

import { BookOpen } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const coursesData = [
    { id: 1, code: "CS101", name: "Introduction to Programming", instructor: "Dr. Smith", credits: 3, grade: "A", status: "active" },
    { id: 2, code: "MATH201", name: "Calculus II", instructor: "Prof. Johnson", credits: 4, grade: "B+", status: "active" },
    { id: 3, code: "ENG102", name: "English Literature", instructor: "Dr. Williams", credits: 3, grade: "A-", status: "completed" },
];

export default function StudentCoursesPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <BookOpen className="h-8 w-8 text-primary" />
                    My Courses
                </h2>
                <p className="text-muted-foreground">Your enrolled courses</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {coursesData.map((course) => (
                    <Card key={course.id}>
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <div>
                                    <p className="text-sm font-mono text-muted-foreground">{course.code}</p>
                                    <CardTitle className="mt-1">{course.name}</CardTitle>
                                </div>
                                <Badge className={course.status === "active" ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"}>
                                    {course.status}
                                </Badge>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-2">
                                <div className="flex justify-between">
                                    <span className="text-sm text-muted-foreground">Instructor:</span>
                                    <span className="text-sm font-semibold">{course.instructor}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-sm text-muted-foreground">Credits:</span>
                                    <span className="text-sm font-semibold">{course.credits}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-sm text-muted-foreground">Grade:</span>
                                    <span className="text-lg font-bold text-green-600">{course.grade}</span>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
