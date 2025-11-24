"use client";

import Link from "next/link";
import { Users, UserPlus, Search, Filter, Eye, Edit, GraduationCap, UserCheck, UserX } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Mock data
const students = [
    {
        id: 1,
        studentId: "STU-2025-001",
        name: "John Doe",
        email: "john.doe@example.com",
        status: "active",
        admissionDate: "Sep 01, 2023",
        gpa: "3.8",
    },
    {
        id: 2,
        studentId: "STU-2025-002",
        name: "Jane Smith",
        email: "jane.smith@example.com",
        status: "applicant",
        admissionDate: "-",
        gpa: "-",
    },
    {
        id: 3,
        studentId: "STU-2022-045",
        name: "Michael Brown",
        email: "michael.b@example.com",
        status: "graduated",
        admissionDate: "Sep 01, 2019",
        gpa: "3.9",
    },
    {
        id: 4,
        studentId: "STU-2024-112",
        name: "Sarah Wilson",
        email: "sarah.w@example.com",
        status: "suspended",
        admissionDate: "Sep 01, 2024",
        gpa: "2.5",
    },
];

const stats = [
    { label: "Total Students", value: "1,250", icon: Users, color: "text-blue-600", bg: "bg-blue-100" },
    { label: "Active", value: "1,100", icon: UserCheck, color: "text-green-600", bg: "bg-green-100" },
    { label: "Applicants", value: "85", icon: UserPlus, color: "text-yellow-600", bg: "bg-yellow-100" },
    { label: "Graduated", value: "450", icon: GraduationCap, color: "text-purple-600", bg: "bg-purple-100" },
];

export default function StudentListPage() {
    const getStatusBadge = (status: string) => {
        switch (status) {
            case "active":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Active</Badge>;
            case "applicant":
                return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-yellow-200">Applicant</Badge>;
            case "graduated":
                return <Badge className="bg-purple-100 text-purple-800 hover:bg-purple-200 border-purple-200">Graduated</Badge>;
            case "suspended":
                return <Badge className="bg-red-100 text-red-800 hover:bg-red-200 border-red-200">Suspended</Badge>;
            default:
                return <Badge variant="secondary">{status}</Badge>;
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <Users className="h-8 w-8 text-primary" />
                        Students
                    </h2>
                    <p className="text-muted-foreground">Manage student records and admissions</p>
                </div>
                <Button asChild className="bg-green-600 hover:bg-green-700">
                    <Link href="/students/new">
                        <UserPlus className="mr-2 h-4 w-4" /> Add Student
                    </Link>
                </Button>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, index) => (
                    <Card key={index} className="border-none shadow-sm">
                        <CardContent className="p-6 flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-muted-foreground mb-1">{stat.label}</p>
                                <h3 className="text-2xl font-bold">{stat.value}</h3>
                            </div>
                            <div className={`w-12 h-12 rounded-full ${stat.bg} flex items-center justify-center`}>
                                <stat.icon className={`h-6 w-6 ${stat.color}`} />
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            {/* Filters */}
            <Card>
                <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="relative md:col-span-2">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search students by name, ID, or email..." className="pl-10" />
                        </div>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="All Statuses" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Statuses</SelectItem>
                                <SelectItem value="active">Active</SelectItem>
                                <SelectItem value="applicant">Applicant</SelectItem>
                                <SelectItem value="graduated">Graduated</SelectItem>
                                <SelectItem value="suspended">Suspended</SelectItem>
                            </SelectContent>
                        </Select>
                        <Button variant="secondary">
                            <Filter className="mr-2 h-4 w-4" /> Apply Filters
                        </Button>
                    </div>
                </CardContent>
            </Card>

            {/* Table */}
            <Card className="overflow-hidden">
                <Table>
                    <TableHeader className="bg-gray-50">
                        <TableRow>
                            <TableHead>Student Number</TableHead>
                            <TableHead>Name</TableHead>
                            <TableHead>Email</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Admission Date</TableHead>
                            <TableHead>GPA</TableHead>
                            <TableHead>Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {students.map((student) => (
                            <TableRow key={student.id}>
                                <TableCell className="font-medium">{student.studentId}</TableCell>
                                <TableCell>{student.name}</TableCell>
                                <TableCell>{student.email}</TableCell>
                                <TableCell>{getStatusBadge(student.status)}</TableCell>
                                <TableCell>{student.admissionDate}</TableCell>
                                <TableCell>{student.gpa}</TableCell>
                                <TableCell>
                                    <div className="flex space-x-2">
                                        <Button asChild variant="ghost" size="icon" className="text-blue-600 hover:text-blue-800 hover:bg-blue-50">
                                            <Link href={`/students/${student.id}`}>
                                                <Eye className="h-4 w-4" />
                                            </Link>
                                        </Button>
                                        <Button asChild variant="ghost" size="icon" className="text-yellow-600 hover:text-yellow-800 hover:bg-yellow-50">
                                            <Link href={`/students/${student.id}/edit`}>
                                                <Edit className="h-4 w-4" />
                                            </Link>
                                        </Button>
                                    </div>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Card>
        </div>
    );
}
