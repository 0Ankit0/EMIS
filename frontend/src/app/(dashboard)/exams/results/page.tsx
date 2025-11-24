"use client";

import { BarChart3, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const resultsData = {
    examName: "Mid-term Examination",
    course: "CS101",
    averageScore: 78.5,
    highestScore: 98,
    lowestScore: 45,
    passRate: 85,
    students: [
        { id: 1, name: "John Doe", studentId: "STU001", marks: 92, grade: "A" },
        { id: 2, name: "Jane Smith", studentId: "STU002", marks: 78, grade: "B+" },
        { id: 3, name: "Mike Johnson", studentId: "STU003", marks: 65, grade: "C+" },
    ],
};

export default function ExamResultsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <BarChart3 className="h-8 w-8 text-primary" />
                        Exam Results
                    </h2>
                    <p className="text-lg text-muted-foreground mt-1">{resultsData.examName} - {resultsData.course}</p>
                </div>
                <Button>
                    <Download className="mr-2 h-4 w-4" />
                    Export Results
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Average Score</p>
                        <h3 className="text-3xl font-bold text-blue-600 mt-2">{resultsData.averageScore}%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Highest</p>
                        <h3 className="text-3xl font-bold text-green-600 mt-2">{resultsData.highestScore}%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Lowest</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">{resultsData.lowestScore}%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Pass Rate</p>
                        <h3 className="text-3xl font-bold text-purple-600 mt-2">{resultsData.passRate}%</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Student Results</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Student ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead className="text-right">Marks</TableHead>
                                <TableHead>Grade</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {resultsData.students.map((student) => (
                                <TableRow key={student.id}>
                                    <TableCell className="font-mono text-sm">{student.studentId}</TableCell>
                                    <TableCell className="font-semibold">{student.name}</TableCell>
                                    <TableCell className="text-right font-bold">{student.marks}/100</TableCell>
                                    <TableCell className="text-2xl font-bold text-green-600">{student.grade}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
