"use client";

import { useParams } from "next/navigation";
import { BookOpen, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const modulesData = [
    { id: 1, title: "Introduction to Programming", order: 1, duration: "2 weeks", lessons: 8 },
    { id: 2, title: "Data Structures", order: 2, duration: "3 weeks", lessons: 12 },
    { id: 3, title: "Algorithms", order: 3, duration: "4 weeks", lessons: 15 },
];

export default function CourseModulesPage() {
    const params = useParams();

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <BookOpen className="h-8 w-8 text-primary" />
                    Course Modules
                </h2>
                <Link href={`/courses/${params.id}/modules/new`}>
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Module
                    </Button>
                </Link>
            </div>

            <div className="space-y-4">
                {modulesData.map((module) => (
                    <Card key={module.id}>
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <div>
                                    <CardTitle>Module {module.order}: {module.title}</CardTitle>
                                    <p className="text-sm text-muted-foreground mt-1">
                                        {module.duration} • {module.lessons} lessons
                                    </p>
                                </div>
                                <Button variant="outline" size="sm">View Details</Button>
                            </div>
                        </CardHeader>
                    </Card>
                ))}
            </div>
        </div>
    );
}
