"use client";

import { useState } from "react";
import { Edit } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";

const gradesData = [
    { id: 1, studentId: "STU001", name: "John Doe", marks: "" },
    { id: 2, studentId: "STU002", name: "Jane Smith", marks: "" },
    { id: 3, studentId: "STU003", name: "Mike Johnson", marks: "" },
];

export default function GradeEntryPage({ params }: { params: { id: string } }) {
    const [grades, setGrades] = useState(gradesData);

    const handleSave = () => {
        console.log("Saving grades:", grades);
        alert("Grades saved successfully!");
    };

    const updateGrade = (studentId: string, value: string) => {
        setGrades(grades.map(g =>
            g.studentId === studentId ? { ...g, marks: value } : g
        ));
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <Edit className="h-8 w-8 text-primary" />
                        Grade Entry
                    </h2>
                    <p className="text-muted-foreground">Enter exam scores for students</p>
                </div>
                <Button onClick={handleSave}>
                    Save Grades
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Student Grades</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Student ID</TableHead>
                                <TableHead>Student Name</TableHead>
                                <TableHead className="text-right">Marks (out of 100)</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {grades.map((student) => (
                                <TableRow key={student.id}>
                                    <TableCell className="font-mono text-sm">{student.studentId}</TableCell>
                                    <TableCell className="font-semibold">{student.name}</TableCell>
                                    <TableCell className="text-right">
                                        <Input
                                            type="number"
                                            placeholder="Enter marks"
                                            className="w-32 ml-auto"
                                            value={student.marks || ""}
                                            onChange={(e) => updateGrade(student.studentId, e.target.value)}
                                            min="0"
                                            max="100"
                                        />
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
