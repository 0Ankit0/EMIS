"use client";

import { useState } from "react";
import Link from "next/link";
import { FileText, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const examsData = [
    { id: 1, name: "Mid-term Examination", course: "CS101", date: "2025-02-15", duration: "3 hours", totalMarks: 100, status: "scheduled" },
    { id: 2, name: "Final Examination", course: "MATH201", date: "2025-03-20", duration: "3 hours", totalMarks: 100, status: "scheduled" },
    { id: 3, name: "Quiz 1", course: "ENG102", date: "2025-01-15", duration: "1 hour", totalMarks: 20, status: "completed" },
];

export default function ExamsListPage() {
    const [exams] = useState(examsData);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <FileText className="h-8 w-8 text-primary" />
                        Examinations
                    </h2>
                    <p className="text-muted-foreground">Manage exams and assessments</p>
                </div>
                <Link href="/exams/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Create Exam
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Exams</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Exam Name</TableHead>
                                <TableHead>Course</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Duration</TableHead>
                                <TableHead className="text-right">Total Marks</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {exams.map((exam) => (
                                <TableRow key={exam.id}>
                                    <TableCell className="font-semibold">{exam.name}</TableCell>
                                    <TableCell>{exam.course}</TableCell>
                                    <TableCell>{exam.date}</TableCell>
                                    <TableCell>{exam.duration}</TableCell>
                                    <TableCell className="text-right font-bold">{exam.totalMarks}</TableCell>
                                    <TableCell>
                                        <Badge className={exam.status === "completed" ? "bg-green-100 text-green-800" : "bg-blue-100 text-blue-800"}>
                                            {exam.status.toUpperCase()}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Link href={`/exams/${exam.id}/grades`}>
                                            <Button variant="outline" size="sm">Grades</Button>
                                        </Link>
                                        <Link href={`/exams/${exam.id}`}>
                                            <Button size="sm">View</Button>
                                        </Link>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
