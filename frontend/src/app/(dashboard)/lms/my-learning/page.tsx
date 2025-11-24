"use client";

import { BookOpen, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const coursesData = [
    { id: 1, code: "CS101", name: "Intro to Programming", lessons: 12, students: 45, completion: 75 },
    { id: 2, code: "WEB201", name: "Web Development", lessons: 10, students: 38, completion: 60 },
];

export default function LMSMyLearningPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <BookOpen className="h-8 w-8 text-primary" />
                    My Learning
                </h2>
                <p className="text-muted-foreground">Your enrolled courses and progress</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {coursesData.map((course) => (
                    <Card key={course.id}>
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <div>
                                    <p className="text-sm font-mono text-muted-foreground">{course.code}</p>
                                    <CardTitle className="mt-1">{course.name}</CardTitle>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                <div>
                                    <div className="flex justify-between text-sm mb-2">
                                        <span>Overall Progress</span>
                                        <span className="font-semibold">{course.completion}%</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-3">
                                        <div className="bg-blue-600 h-3 rounded-full" style={{ width: `${course.completion}%` }} />
                                    </div>
                                </div>
                                <div className="grid grid-cols-2 gap-4 text-sm">
                                    <div>
                                        <p className="text-muted-foreground">Lessons</p>
                                        <p className="font-semibold">{course.lessons}</p>
                                    </div>
                                    <div>
                                        <p className="text-muted-foreground">Students</p>
                                        <p className="font-semibold">{course.students}</p>
                                    </div>
                                </div>
                                <Button className="w-full">Continue Learning</Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
