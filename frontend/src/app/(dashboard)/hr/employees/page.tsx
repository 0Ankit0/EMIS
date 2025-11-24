"use client";

import { Users, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import Link from "next/link";

const employeesData = [
    { id: 1, empId: "EMP001", name: "Dr. Smith", department: "Computer Science", position: "Professor", email: "smith@school.edu" },
    { id: 2, empId: "EMP002", name: "Prof. Johnson", department: "Mathematics", position: "Associate Professor", email: "johnson@school.edu" },
];

export default function HREmployeesPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Users className="h-8 w-8 text-primary" />
                        Employees
                    </h2>
                    <p className="text-muted-foreground">Manage staff members</p>
                </div>
                <Link href="/hr/employees/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Employee
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Employees</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Employee ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Department</TableHead>
                                <TableHead>Position</TableHead>
                                <TableHead>Email</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {employeesData.map((emp) => (
                                <TableRow key={emp.id}>
                                    <TableCell className="font-mono text-sm">{emp.empId}</TableCell>
                                    <TableCell className="font-semibold">{emp.name}</TableCell>
                                    <TableCell>{emp.department}</TableCell>
                                    <TableCell>{emp.position}</TableCell>
                                    <TableCell>{emp.email}</TableCell>
                                    <TableCell className="text-right">
                                        <Link href={`/hr/employees/${emp.id}`}>
                                            <Button variant="outline" size="sm">View</Button>
                                        </Link>
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
