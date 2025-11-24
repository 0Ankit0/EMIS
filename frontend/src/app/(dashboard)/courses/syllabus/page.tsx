"use client";

import { FileText } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const syllabusData = {
    course: "Computer Science 101",
    semester: "Fall 2025",
    units: [
        { number: 1, title: "Introduction to Programming", topics: ["Variables", "Data Types", "Control Flow"] },
        { number: 2, title: "Object-Oriented Programming", topics: ["Classes", "Objects", "Inheritance"] },
        { number: 3, title: "Data Structures", topics: ["Arrays", "Lists", "Trees"] },
    ],
};

export default function SyllabusPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <FileText className="h-8 w-8 text-primary" />
                    Course Syllabus
                </h2>
                <p className="text-lg text-muted-foreground mt-1">
                    {syllabusData.course} - {syllabusData.semester}
                </p>
            </div>

            <div className="space-y-4">
                {syllabusData.units.map((unit) => (
                    <Card key={unit.number}>
                        <CardHeader>
                            <CardTitle>Unit {unit.number}: {unit.title}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <ul className="list-disc list-inside space-y-1">
                                {unit.topics.map((topic, idx) => (
                                    <li key={idx} className="text-muted-foreground">{topic}</li>
                                ))}
                            </ul>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
