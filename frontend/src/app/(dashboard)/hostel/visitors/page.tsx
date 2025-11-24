"use client";

import { ClipboardList, UserCheck } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const visitorsData = [
    { id: 1, name: "Parent Name", student: "John Doe", relation: "Father", checkIn: "10:00 AM", checkOut: "11:30 AM", date: "2025-01-23" },
];

export default function VisitorLogPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <ClipboardList className="h-8 w-8 text-primary" />
                    Visitor Log
                </h2>
                <Button>
                    <UserCheck className="mr-2 h-4 w-4" />
                    Log Visitor
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Visitors</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Visitor Name</TableHead>
                                <TableHead>Student</TableHead>
                                <TableHead>Relation</TableHead>
                                <TableHead>Check In</TableHead>
                                <TableHead>Check Out</TableHead>
                                <TableHead>Date</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {visitorsData.map((visitor) => (
                                <TableRow key={visitor.id}>
                                    <TableCell className="font-semibold">{visitor.name}</TableCell>
                                    <TableCell>{visitor.student}</TableCell>
                                    <TableCell>{visitor.relation}</TableCell>
                                    <TableCell>{visitor.checkIn}</TableCell>
                                    <TableCell>{visitor.checkOut || "-"}</TableCell>
                                    <TableCell>{visitor.date}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
