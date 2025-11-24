"use client";

import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { FileQuestion, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const quizData = {
    title: "Python Basics Quiz",
    course: "CS101",
    duration: "30 mins",
    questions: [
        {
            id: 1,
            question: "What is the output of print(2 + 3)?",
            options: ["5", "23", "Error", "None"],
            correct: 0,
        },
        {
            id: 2,
            question: "Which keyword is used to define a function in Python?",
            options: ["function", "def", "func", "define"],
            correct: 1,
        },
    ],
};

export default function LMSQuizTakePage() {
    const params = useParams();
    const router = useRouter();
    const [currentQ, setCurrentQ] = useState(0);
    const [answers, setAnswers] = useState<Record<number, number>>({});

    const handleSubmit = () => {
        console.log("Submitted answers:", answers);
        alert("Quiz submitted!");
        router.push(`/lms/quizzes/${params.id}/result`);
    };

    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <FileQuestion className="h-8 w-8 text-primary" />
                    {quizData.title}
                </h2>
                <p className="text-muted-foreground mt-1">{quizData.course} • {quizData.duration}</p>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex justify-between items-center">
                        <CardTitle>Question {currentQ + 1} of {quizData.questions.length}</CardTitle>
                        <span className="text-sm text-muted-foreground">Time Remaining: 25:30</span>
                    </div>
                </CardHeader>
                <CardContent className="space-y-6">
                    <p className="text-lg font-semibold">{quizData.questions[currentQ].question}</p>

                    <div className="space-y-3">
                        {quizData.questions[currentQ].options.map((option, idx) => (
                            <div
                                key={idx}
                                onClick={() => setAnswers({ ...answers, [currentQ]: idx })}
                                className={`flex items-center space-x-3 p-4 border-2 rounded-lg cursor-pointer hover:bg-gray-50 transition ${answers[currentQ] === idx ? "border-blue-600 bg-blue-50" : "border-gray-200"
                                    }`}
                            >
                                <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${answers[currentQ] === idx ? "border-blue-600" : "border-gray-300"
                                    }`}>
                                    {answers[currentQ] === idx && (
                                        <div className="w-3 h-3 rounded-full bg-blue-600" />
                                    )}
                                </div>
                                <span className="flex-1">{option}</span>
                            </div>
                        ))}
                    </div>

                    <div className="flex justify-between">
                        <Button
                            variant="outline"
                            disabled={currentQ === 0}
                            onClick={() => setCurrentQ(currentQ - 1)}
                        >
                            Previous
                        </Button>
                        {currentQ < quizData.questions.length - 1 ? (
                            <Button onClick={() => setCurrentQ(currentQ + 1)}>
                                Next <ChevronRight className="ml-2 h-4 w-4" />
                            </Button>
                        ) : (
                            <Button onClick={handleSubmit}>Submit Quiz</Button>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
