"use client";

import { DollarSign, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const payrollData = [
    { id: 1, empId: "EMP001", name: "Dr. Smith", basicSalary: 8000, allowances: 2000, deductions: 500, netSalary: 9500 },
    { id: 2, empId: "EMP002", name: "Prof. Johnson", basicSalary: 7000, allowances: 1500, deductions: 400, netSalary: 8100 },
];

export default function HRPayrollPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <DollarSign className="h-8 w-8 text-primary" />
                        Payroll
                    </h2>
                    <p className="text-muted-foreground">Employee salary management</p>
                </div>
                <Button>
                    <Download className="mr-2 h-4 w-4" />
                    Export
                </Button>
            </div>

            <div className="grid grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Payroll</p>
                        <h3 className="text-3xl font-bold text-blue-600 mt-2">$17,600</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Allowances</p>
                        <h3 className="text-3xl font-bold text-green-600 mt-2">$3,500</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Deductions</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">$900</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Payroll Details</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Employee ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead className="text-right">Basic</TableHead>
                                <TableHead className="text-right">Allowances</TableHead>
                                <TableHead className="text-right">Deductions</TableHead>
                                <TableHead className="text-right">Net Salary</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {payrollData.map((emp) => (
                                <TableRow key={emp.id}>
                                    <TableCell className="font-mono text-sm">{emp.empId}</TableCell>
                                    <TableCell className="font-semibold">{emp.name}</TableCell>
                                    <TableCell className="text-right">${emp.basicSalary.toLocaleString()}</TableCell>
                                    <TableCell className="text-right text-green-600">${emp.allowances.toLocaleString()}</TableCell>
                                    <TableCell className="text-right text-red-600">${emp.deductions.toLocaleString()}</TableCell>
                                    <TableCell className="text-right font-bold">${emp.netSalary.toLocaleString()}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
