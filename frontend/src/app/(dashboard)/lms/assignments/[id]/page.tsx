"use client";

import { useParams } from "next/navigation";
import { ClipboardList, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

const assignmentData = {
    title: "Python Basics Assignment",
    course: "CS101",
    description: "Create a simple calculator program in Python",
    dueDate: "2025-02-01",
    maxScore: 100,
};

export default function LMSAssignmentDetailPage() {
    const params = useParams();

    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <ClipboardList className="h-8 w-8 text-primary" />
                    {assignmentData.title}
                </h2>
                <p className="text-muted-foreground mt-1">{assignmentData.course}</p>
            </div>

            <div className="grid grid-cols-2 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Due Date</p>
                        <p className="text-2xl font-bold mt-2">{assignmentData.dueDate}</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Max Score</p>
                        <p className="text-2xl font-bold mt-2">{assignmentData.maxScore}</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Instructions</CardTitle>
                </CardHeader>
                <CardContent>
                    <p>{assignmentData.description}</p>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Submit Assignment</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <Textarea placeholder="Paste your code or add comments..." className="min-h-[200px]" />
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                        <Upload className="h-8 w-8 mx-auto text-gray-400 mb-2" />
                        <p className="text-sm text-muted-foreground mb-3">Upload files (optional)</p>
                        <Button variant="outline">Choose Files</Button>
                    </div>
                    <Button className="w-full" size="lg">Submit Assignment</Button>
                </CardContent>
            </Card>
        </div>
    );
}
