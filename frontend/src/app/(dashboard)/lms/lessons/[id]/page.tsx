"use client";

import { Play, CheckCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const lessonData = {
    title: "Variables and Data Types",
    course: "Introduction to Python",
    content: "In this lesson, we will cover the basic data types in Python including integers, floats, strings, and booleans...",
    videoUrl: "https://example.com/video.mp4",
    duration: "15 mins",
    nextLesson: "Control Flow",
};

export default function LessonViewPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Play className="h-8 w-8 text-primary" />
                        {lessonData.title}
                    </h2>
                    <p className="text-lg text-muted-foreground mt-1">{lessonData.course}</p>
                </div>
                <Button>
                    <CheckCircle className="mr-2 h-4 w-4" />
                    Mark as Complete
                </Button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-6">
                    <Card>
                        <CardContent className="p-0 aspect-video bg-black flex items-center justify-center text-white">
                            <Play className="h-16 w-16 opacity-50" />
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader>
                            <CardTitle>Lesson Content</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="leading-relaxed">{lessonData.content}</p>
                        </CardContent>
                    </Card>
                </div>
                <div className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Up Next</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="p-4 border rounded-lg bg-muted/50">
                                <p className="font-semibold">{lessonData.nextLesson}</p>
                                <Button variant="link" className="px-0 mt-2">Start Next Lesson &rarr;</Button>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
