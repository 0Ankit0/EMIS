"use client";

import { UserCheck, Calendar } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const attendanceData = [
    { id: 1, empId: "EMP001", name: "Dr. Smith", date: "2025-01-23", checkIn: "09:00 AM", checkOut: "05:00 PM", status: "present" },
    { id: 2, empId: "EMP002", name: "Prof. Johnson", date: "2025-01-23", checkIn: "09:15 AM", checkOut: "05:10 PM", status: "present" },
];

export default function HRAttendancePage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <UserCheck className="h-8 w-8 text-primary" />
                    HR Attendance
                </h2>
                <p className="text-muted-foreground">Employee attendance tracking</p>
            </div>

            <div className="grid grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Present Today</p>
                        <h3 className="text-4xl font-bold text-green-600 mt-2">45</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Absent</p>
                        <h3 className="text-4xl font-bold text-red-600 mt-2">3</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">On Leave</p>
                        <h3 className="text-4xl font-bold text-yellow-600 mt-2">2</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>Today's Attendance</CardTitle>
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <Calendar className="h-4 w-4" />
                            <span>January 23, 2025</span>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Employee ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Check In</TableHead>
                                <TableHead>Check Out</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {attendanceData.map((record) => (
                                <TableRow key={record.id}>
                                    <TableCell className="font-mono text-sm">{record.empId}</TableCell>
                                    <TableCell className="font-semibold">{record.name}</TableCell>
                                    <TableCell>{record.checkIn}</TableCell>
                                    <TableCell>{record.checkOut}</TableCell>
                                    <TableCell>
                                        <Badge className="bg-green-100 text-green-800">
                                            {record.status.toUpperCase()}
                                        </Badge>
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
