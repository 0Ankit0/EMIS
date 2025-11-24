"use client";

import Link from "next/link";
import { Users, UserPlus, Search, Filter, Eye, Edit, Mail, Phone, Briefcase } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

// Mock data based on Faculty model
const facultyMembers = [
    {
        id: 1,
        employeeId: "FAC-001",
        name: "Dr. Robert Langdon",
        designation: "Professor",
        department: "History",
        email: "robert.langdon@emis.edu",
        phone: "+1 234 567 8901",
        status: "active",
        specialization: "Symbology",
    },
    {
        id: 2,
        employeeId: "FAC-002",
        name: "Dr. Katherine Solomon",
        designation: "Associate Professor",
        department: "Physics",
        email: "katherine.solomon@emis.edu",
        phone: "+1 234 567 8902",
        status: "on_leave",
        specialization: "Noetic Science",
    },
    {
        id: 3,
        employeeId: "FAC-003",
        name: "Prof. Albus Dumbledore",
        designation: "Professor",
        department: "Magic",
        email: "albus.dumbledore@emis.edu",
        phone: "+1 234 567 8903",
        status: "active",
        specialization: "Transfiguration",
    },
    {
        id: 4,
        employeeId: "FAC-004",
        name: "Dr. Sheldon Cooper",
        designation: "Assistant Professor",
        department: "Physics",
        email: "sheldon.cooper@emis.edu",
        phone: "+1 234 567 8904",
        status: "sabbatical",
        specialization: "Theoretical Physics",
    },
];

export default function FacultyListPage() {
    const getStatusBadge = (status: string) => {
        switch (status) {
            case "active":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Active</Badge>;
            case "on_leave":
                return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-yellow-200">On Leave</Badge>;
            case "sabbatical":
                return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-200 border-blue-200">Sabbatical</Badge>;
            case "retired":
                return <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-200 border-gray-200">Retired</Badge>;
            default:
                return <Badge variant="secondary">{status}</Badge>;
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <Briefcase className="h-8 w-8 text-primary" />
                        Faculty
                    </h2>
                    <p className="text-muted-foreground">Manage faculty members and staff</p>
                </div>
                <Button asChild className="bg-blue-600 hover:bg-blue-700">
                    <Link href="/faculty/new">
                        <UserPlus className="mr-2 h-4 w-4" /> Add Faculty
                    </Link>
                </Button>
            </div>

            {/* Filters */}
            <Card>
                <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="relative md:col-span-2">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search faculty by name, ID, or department..." className="pl-10" />
                        </div>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="Department" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Departments</SelectItem>
                                <SelectItem value="cs">Computer Science</SelectItem>
                                <SelectItem value="physics">Physics</SelectItem>
                                <SelectItem value="history">History</SelectItem>
                            </SelectContent>
                        </Select>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="Designation" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Designations</SelectItem>
                                <SelectItem value="professor">Professor</SelectItem>
                                <SelectItem value="associate">Associate Professor</SelectItem>
                                <SelectItem value="assistant">Assistant Professor</SelectItem>
                                <SelectItem value="lecturer">Lecturer</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>

            {/* Table */}
            <Card className="overflow-hidden">
                <Table>
                    <TableHeader className="bg-gray-50">
                        <TableRow>
                            <TableHead>ID</TableHead>
                            <TableHead>Name</TableHead>
                            <TableHead>Designation</TableHead>
                            <TableHead>Department</TableHead>
                            <TableHead>Contact</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {facultyMembers.map((faculty) => (
                            <TableRow key={faculty.id}>
                                <TableCell className="font-medium">{faculty.employeeId}</TableCell>
                                <TableCell>
                                    <div>
                                        <div className="font-medium">{faculty.name}</div>
                                        <div className="text-xs text-muted-foreground">{faculty.specialization}</div>
                                    </div>
                                </TableCell>
                                <TableCell>{faculty.designation}</TableCell>
                                <TableCell>{faculty.department}</TableCell>
                                <TableCell>
                                    <div className="flex flex-col text-sm">
                                        <span className="flex items-center gap-1">
                                            <Mail className="h-3 w-3 text-muted-foreground" /> {faculty.email}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Phone className="h-3 w-3 text-muted-foreground" /> {faculty.phone}
                                        </span>
                                    </div>
                                </TableCell>
                                <TableCell>{getStatusBadge(faculty.status)}</TableCell>
                                <TableCell>
                                    <div className="flex space-x-2">
                                        <Button asChild variant="ghost" size="icon" className="text-blue-600 hover:text-blue-800 hover:bg-blue-50">
                                            <Link href={`/faculty/${faculty.id}`}>
                                                <Eye className="h-4 w-4" />
                                            </Link>
                                        </Button>
                                        <Button asChild variant="ghost" size="icon" className="text-green-600 hover:text-green-800 hover:bg-green-50">
                                            <Link href={`/faculty/${faculty.id}/edit`}>
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
