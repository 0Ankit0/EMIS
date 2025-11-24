"use client";

import { BookOpen } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const coursesData = [
    { id: 1, title: "Introduction to Programming", instructor: "Dr. Smith", progress: 75, enrolled: 45 },
    { id: 2, title: "Web Development Basics", instructor: "Prof. Johnson", progress: 60, enrolled: 38 },
    { id: 3, title: "Data Structures", instructor: "Dr. Williams", progress: 40, enrolled: 32 },
];

export default function LMSCoursesPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <BookOpen className="h-8 w-8 text-primary" />
                    LMS Courses
                </h2>
                <p className="text-muted-foreground">Available online courses</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {coursesData.map((course) => (
                    <Card key={course.id}>
                        <CardHeader>
                            <CardTitle>{course.title}</CardTitle>
                            <p className="text-sm text-muted-foreground">by {course.instructor}</p>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-3">
                                <div>
                                    <div className="flex justify-between text-sm mb-1">
                                        <span>Progress</span>
                                        <span className="font-semibold">{course.progress}%</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className="bg-blue-600 h-2 rounded-full"
                                            style={{ width: `${course.progress}%` }}
                                        />
                                    </div>
                                </div>
                                <p className="text-sm text-muted-foreground">{course.enrolled} students enrolled</p>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
