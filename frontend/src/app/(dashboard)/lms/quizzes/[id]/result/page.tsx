"use client";

import { CheckCircle, XCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const resultData = {
    quiz: "Python Basics Quiz",
    score: 80,
    total: 100,
    passed: true,
    correctAnswers: 8,
    totalQuestions: 10,
    timeTaken: "12 mins",
};

export default function QuizResultPage() {
    return (
        <div className="max-w-2xl mx-auto space-y-6 text-center">
            <div className="py-8">
                {resultData.passed ? (
                    <CheckCircle className="h-24 w-24 text-green-500 mx-auto mb-4" />
                ) : (
                    <XCircle className="h-24 w-24 text-red-500 mx-auto mb-4" />
                )}
                <h2 className="text-4xl font-bold mb-2">
                    {resultData.passed ? "Congratulations!" : "Keep Trying!"}
                </h2>
                <p className="text-xl text-muted-foreground">
                    You scored {resultData.score}% in {resultData.quiz}
                </p>
            </div>

            <div className="grid grid-cols-3 gap-4">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Correct</p>
                        <p className="text-2xl font-bold text-green-600">{resultData.correctAnswers}</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total</p>
                        <p className="text-2xl font-bold">{resultData.totalQuestions}</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Time</p>
                        <p className="text-2xl font-bold">{resultData.timeTaken}</p>
                    </CardContent>
                </Card>
            </div>

            <div className="flex justify-center gap-4 mt-8">
                <Link href="/lms/quizzes">
                    <Button variant="outline">Back to Quizzes</Button>
                </Link>
                <Link href="/lms/courses">
                    <Button>Continue Learning</Button>
                </Link>
            </div>
        </div>
    );
}
