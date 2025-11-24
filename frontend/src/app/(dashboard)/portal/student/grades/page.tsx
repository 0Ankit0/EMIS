"use client";

import { BookOpen } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const gradesData = [
    { course: "CS101", midterm: 85, final: 90, assignment: 92, total: 89, grade: "A" },
    { course: "MATH201", midterm: 78, final: 82, assignment: 88, total: 83, grade: "B+" },
    { course: "ENG102", midterm: 92, final: 88, assignment: 90, total: 90, grade: "A-" },
];

export default function StudentGradesPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <BookOpen className="h-8 w-8 text-primary" />
                My Grades
            </h2>

            <Card>
                <CardContent className="p-6">
                    <p className="text-sm text-muted-foreground">Overall GPA</p>
                    <h3 className="text-5xl font-bold text-green-600 mt-2">3.67</h3>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Course Grades</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Course</TableHead>
                                <TableHead className="text-right">Midterm</TableHead>
                                <TableHead className="text-right">Final</TableHead>
                                <TableHead className="text-right">Assignment</TableHead>
                                <TableHead className="text-right">Total</TableHead>
                                <TableHead>Grade</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {gradesData.map((grade, i) => (
                                <TableRow key={i}>
                                    <TableCell className="font-semibold">{grade.course}</TableCell>
                                    <TableCell className="text-right">{grade.midterm}</TableCell>
                                    <TableCell className="text-right">{grade.final}</TableCell>
                                    <TableCell className="text-right">{grade.assignment}</TableCell>
                                    <TableCell className="text-right font-bold">{grade.total}</TableCell>
                                    <TableCell className="text-xl font-bold text-green-600">{grade.grade}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
