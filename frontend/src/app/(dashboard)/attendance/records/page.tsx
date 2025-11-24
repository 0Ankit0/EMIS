"use client";

import { useState } from "react";
import { Calendar, Download, Filter, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const mockRecords = [
    { id: 1, student: "John Doe", studentId: "STU001", course: "CS101", date: "2025-01-20", status: "present", session: "Morning" },
    { id: 2, student: "Jane Smith", studentId: "STU002", course: "CS101", date: "2025-01-20", status: "absent", session: "Morning" },
    { id: 3, student: "Mike Johnson", studentId: "STU003", course: "MATH201", date: "2025-01-20", status: "late", session: "Afternoon" },
    { id: 4, student: "Sarah Williams", studentId: "STU004", course: "CS101", date: "2025-01-19", status: "present", session: "Morning" },
    { id: 5, student: "Tom Brown", studentId: "STU005", course: "MATH201", date: "2025-01-19", status: "present", session: "Afternoon" },
];

export default function ViewAttendanceRecordsPage() {
    const [records] = useState(mockRecords);
    const [searchTerm, setSearchTerm] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");
    const [courseFilter, setCourseFilter] = useState("all");

    const filteredRecords = records.filter(record => {
        const matchesSearch = record.student.toLowerCase().includes(searchTerm.toLowerCase()) ||
            record.studentId.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesStatus = statusFilter === "all" || record.status === statusFilter;
        const matchesCourse = courseFilter === "all" || record.course === courseFilter;
        return matchesSearch && matchesStatus && matchesCourse;
    });

    const getStatusBadge = (status: string) => {
        const variants = {
            present: "bg-green-100 text-green-800",
            absent: "bg-red-100 text-red-800",
            late: "bg-yellow-100 text-yellow-800",
            excused: "bg-blue-100 text-blue-800",
        };
        return <Badge className={variants[status as keyof typeof variants]}>{status.toUpperCase()}</Badge>;
    };

    const handleExport = () => {
        // TODO: Generate CSV/Excel export
        console.log("Exporting attendance records...");
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <Calendar className="h-8 w-8 text-primary" />
                        Attendance Records
                    </h2>
                    <p className="text-muted-foreground">View and filter attendance records</p>
                </div>
                <Button onClick={handleExport}>
                    <Download className="mr-2 h-4 w-4" />
                    Export
                </Button>
            </div>

            {/* Filters */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Filter className="h-5 w-5" />
                        Filters
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div>
                            <label className="text-sm font-medium mb-2 block">Search</label>
                            <div className="relative">
                                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <Input
                                    placeholder="Student name or ID..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="pl-10"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="text-sm font-medium mb-2 block">Course</label>
                            <Select value={courseFilter} onValueChange={setCourseFilter}>
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="all">All Courses</SelectItem>
                                    <SelectItem value="CS101">CS101</SelectItem>
                                    <SelectItem value="MATH201">MATH201</SelectItem>
                                    <SelectItem value="ENG102">ENG102</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label className="text-sm font-medium mb-2 block">Status</label>
                            <Select value={statusFilter} onValueChange={setStatusFilter}>
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="all">All Status</SelectItem>
                                    <SelectItem value="present">Present</SelectItem>
                                    <SelectItem value="absent">Absent</SelectItem>
                                    <SelectItem value="late">Late</SelectItem>
                                    <SelectItem value="excused">Excused</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label className="text-sm font-medium mb-2 block">Date Range</label>
                            <input
                                type="date"
                                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                            />
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Records Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Records ({filteredRecords.length})</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Student ID</TableHead>
                                <TableHead>Student Name</TableHead>
                                <TableHead>Course</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Session</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredRecords.length > 0 ? (
                                filteredRecords.map((record) => (
                                    <TableRow key={record.id}>
                                        <TableCell className="font-mono text-sm">{record.studentId}</TableCell>
                                        <TableCell className="font-semibold">{record.student}</TableCell>
                                        <TableCell>{record.course}</TableCell>
                                        <TableCell>{record.date}</TableCell>
                                        <TableCell>{record.session}</TableCell>
                                        <TableCell>{getStatusBadge(record.status)}</TableCell>
                                    </TableRow>
                                ))
                            ) : (
                                <TableRow>
                                    <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                                        No records found
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
