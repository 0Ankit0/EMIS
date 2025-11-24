"use client";

import { useParams } from "next/navigation";
import { BookOpen, Play, CheckCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const courseData = {
    title: "Introduction to Programming",
    instructor: "Dr. Smith",
    description: "Learn the fundamentals of programming with Python",
    progress: 75,
    lessons: [
        { id: 1, title: "Variables and Data Types", duration: "30 mins", completed: true },
        { id: 2, title: "Control Flow", duration: "45 mins", completed: true },
        { id: 3, title: "Functions", duration: "60 mins", completed: false },
    ],
};

export default function LMSCourseDetailPage() {
    const params = useParams();

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <BookOpen className="h-8 w-8 text-primary" />
                    {courseData.title}
                </h2>
                <p className="text-lg text-muted-foreground mt-1">by {courseData.instructor}</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Course Progress</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-2">
                        <div className="flex justify-between text-sm mb-2">
                            <span>Overall Completion</span>
                            <span className="font-semibold">{courseData.progress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                            <div className="bg-blue-600 h-3 rounded-full transition-all" style={{ width: `${courseData.progress}%` }} />
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Course Content</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-3">
                        {courseData.lessons.map((lesson, idx) => (
                            <div key={lesson.id} className="flex items-center justify-between p-4 border rounded-lg">
                                <div className="flex items-center gap-4">
                                    {lesson.completed ? (
                                        <CheckCircle className="h-6 w-6 text-green-600" />
                                    ) : (
                                        <Play className="h-6 w-6 text-blue-600" />
                                    )}
                                    <div>
                                        <p className="font-semibold">{idx + 1}. {lesson.title}</p>
                                        <p className="text-sm text-muted-foreground">{lesson.duration}</p>
                                    </div>
                                </div>
                                <Button variant={lesson.completed ? "outline" : "default"} size="sm">
                                    {lesson.completed ? "Review" : "Start"}
                                </Button>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
