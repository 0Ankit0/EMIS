"use client";

import { Users, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const studentData = [
    { id: 1, grade: "Grade 10", total: 45, boys: 20, girls: 25, attendance: "95%" },
    { id: 2, grade: "Grade 11", total: 42, boys: 22, girls: 20, attendance: "92%" },
    { id: 3, grade: "Grade 12", total: 40, boys: 18, girls: 22, attendance: "94%" },
];

export default function StudentReportsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Users className="h-8 w-8 text-primary" />
                    Student Reports
                </h2>
                <Button variant="outline">
                    <Download className="mr-2 h-4 w-4" />
                    Export CSV
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Enrollment by Grade</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Grade</TableHead>
                                <TableHead className="text-right">Total Students</TableHead>
                                <TableHead className="text-right">Boys</TableHead>
                                <TableHead className="text-right">Girls</TableHead>
                                <TableHead className="text-right">Avg Attendance</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {studentData.map((item) => (
                                <TableRow key={item.id}>
                                    <TableCell className="font-semibold">{item.grade}</TableCell>
                                    <TableCell className="text-right">{item.total}</TableCell>
                                    <TableCell className="text-right">{item.boys}</TableCell>
                                    <TableCell className="text-right">{item.girls}</TableCell>
                                    <TableCell className="text-right">{item.attendance}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
