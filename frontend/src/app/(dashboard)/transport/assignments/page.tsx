"use client";

import { Bus, UserPlus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const assignmentsData = [
    { id: 1, student: "Alice Johnson", grade: "10-A", route: "Route A", stop: "Main St", status: "Active" },
    { id: 2, student: "Bob Smith", grade: "11-B", route: "Route B", stop: "Park Ave", status: "Active" },
];

export default function TransportAssignmentsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Bus className="h-8 w-8 text-primary" />
                    Student Assignments
                </h2>
                <Button>
                    <UserPlus className="mr-2 h-4 w-4" />
                    Assign Student
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Current Assignments</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Student</TableHead>
                                <TableHead>Grade</TableHead>
                                <TableHead>Route</TableHead>
                                <TableHead>Pickup/Dropoff</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {assignmentsData.map((assignment) => (
                                <TableRow key={assignment.id}>
                                    <TableCell className="font-semibold">{assignment.student}</TableCell>
                                    <TableCell>{assignment.grade}</TableCell>
                                    <TableCell>{assignment.route}</TableCell>
                                    <TableCell>{assignment.stop}</TableCell>
                                    <TableCell>
                                        <Badge className="bg-green-100 text-green-800">{assignment.status}</Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm">Edit</Button>
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
