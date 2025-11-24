"use client";

import { Calendar, FileText } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const schedulesData = [
    { id: 1, exam: "Mid-term Math", date: "2025-02-15", time: "09:00 AM", duration: "3 hours", room: "Hall A" },
    { id: 2, exam: "Final English", date: "2025-03-20", time: "10:00 AM", duration: "2 hours", room: "Room 101" },
];

export default function ExamSchedulesPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Calendar className="h-8 w-8 text-primary" />
                Exam Schedules
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Upcoming Exams</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Exam Name</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Time</TableHead>
                                <TableHead>Duration</TableHead>
                                <TableHead>Room</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {schedulesData.map((schedule) => (
                                <TableRow key={schedule.id}>
                                    <TableCell className="font-semibold">{schedule.exam}</TableCell>
                                    <TableCell>{schedule.date}</TableCell>
                                    <TableCell>{schedule.time}</TableCell>
                                    <TableCell>{schedule.duration}</TableCell>
                                    <TableCell>{schedule.room}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
