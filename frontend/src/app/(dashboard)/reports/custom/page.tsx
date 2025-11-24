"use client";

import { FileText, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const customReports = [
    { id: 1, name: "Quarterly Performance Review", created: "2025-01-15", type: "Academic", author: "Admin" },
    { id: 2, name: "Staff Attendance Summary", created: "2025-01-10", type: "HR", author: "HR Manager" },
    { id: 3, name: "Library Inventory Audit", created: "2025-01-05", type: "Inventory", author: "Librarian" },
];

export default function CustomReportsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <FileText className="h-8 w-8 text-primary" />
                    Custom Reports
                </h2>
                <Button>Create New Report</Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Saved Reports</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Report Name</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Created Date</TableHead>
                                <TableHead>Author</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {customReports.map((report) => (
                                <TableRow key={report.id}>
                                    <TableCell className="font-semibold">{report.name}</TableCell>
                                    <TableCell>{report.type}</TableCell>
                                    <TableCell>{report.created}</TableCell>
                                    <TableCell>{report.author}</TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="outline" size="sm">
                                            <Download className="mr-2 h-4 w-4" />
                                            Download
                                        </Button>
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
