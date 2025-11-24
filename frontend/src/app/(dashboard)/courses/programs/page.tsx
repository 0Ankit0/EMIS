"use client";

import { BookOpen } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const programsData = [
    { id: 1, name: "Computer Science", degree: "Bachelor of Science", duration: "4 years", courses: 45 },
    { id: 2, name: "Business Administration", degree: "Bachelor of Business", duration: "4 years", courses: 40 },
];

export default function ProgramsPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <BookOpen className="h-8 w-8 text-primary" />
                Academic Programs
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {programsData.map((program) => (
                    <Card key={program.id}>
                        <CardHeader>
                            <CardTitle>{program.name}</CardTitle>
                            <p className="text-sm text-muted-foreground">{program.degree}</p>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <p className="text-sm text-muted-foreground">Duration</p>
                                    <p className="font-semibold">{program.duration}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-muted-foreground">Total Courses</p>
                                    <p className="font-semibold">{program.courses}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
