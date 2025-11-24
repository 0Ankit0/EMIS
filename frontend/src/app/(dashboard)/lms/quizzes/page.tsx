"use client";

import { FileQuestion } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const quizzesData = [
    { id: 1, title: "Python Basics Quiz", course: "CS101", questions: 20, duration: "30 mins", status: "available" },
    { id: 2, title: "Web Design Quiz", course: "WEB201", questions: 15, duration: "20 mins", status: "completed" },
];

export default function LMSQuizzesPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <FileQuestion className="h-8 w-8 text-primary" />
                Quizzes
            </h2>

            <div className="grid grid-cols-1 gap-4">
                {quizzesData.map((quiz) => (
                    <Card key={quiz.id}>
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <div>
                                    <CardTitle>{quiz.title}</CardTitle>
                                    <p className="text-sm text-muted-foreground mt-1">{quiz.course}</p>
                                </div>
                                <Badge className={quiz.status === "completed" ? "bg-green-100 text-green-800" : "bg-blue-100 text-blue-800"}>
                                    {quiz.status.toUpperCase()}
                                </Badge>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="flex justify-between items-center">
                                <div className="flex gap-6">
                                    <div>
                                        <p className="text-sm text-muted-foreground">Questions</p>
                                        <p className="font-semibold">{quiz.questions}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm text-muted-foreground">Duration</p>
                                        <p className="font-semibold">{quiz.duration}</p>
                                    </div>
                                </div>
                                <Link href={`/lms/quizzes/${quiz.id}`}>
                                    <Button variant={quiz.status === "available" ? "default" : "outline"}>
                                        {quiz.status === "available" ? "Take Quiz" : "View Results"}
                                    </Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
