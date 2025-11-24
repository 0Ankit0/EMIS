"use client";

import { ClipboardList } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const assignmentsData = [
    { id: 1, title: "Python Basics Assignment", course: "CS101", dueDate: "2025-02-01", status: "pending" },
    { id: 2, title: "Web Design Project", course: "WEB201", dueDate: "2025-01-25", status: "submitted" },
];

export default function LMSAssignmentsPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <ClipboardList className="h-8 w-8 text-primary" />
                    Assignments
                </h2>
                <p className="text-muted-foreground">Course assignments and submissions</p>
            </div>

            <div className="grid grid-cols-1 gap-4">
                {assignmentsData.map((assignment) => (
                    <Card key={assignment.id}>
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <div>
                                    <CardTitle>{assignment.title}</CardTitle>
                                    <p className="text-sm text-muted-foreground mt-1">{assignment.course}</p>
                                </div>
                                <Badge className={assignment.status === "submitted" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}>
                                    {assignment.status.toUpperCase()}
                                </Badge>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="flex justify-between items-center">
                                <div>
                                    <p className="text-sm text-muted-foreground">Due Date</p>
                                    <p className="font-semibold">{assignment.dueDate}</p>
                                </div>
                                <Link href={`/lms/assignments/${assignment.id}`}>
                                    <Button variant={assignment.status === "pending" ? "default" : "outline"}>
                                        {assignment.status === "pending" ? "Submit" : "View"}
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
