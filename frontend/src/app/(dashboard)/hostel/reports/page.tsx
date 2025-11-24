"use client";

import { BarChart, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const hostelReports = [
    { id: 1, name: "Monthly Occupancy Report", date: "2025-01-01", type: "Occupancy", status: "Generated" },
    { id: 2, name: "Mess Expenditure Summary", date: "2025-01-05", type: "Financial", status: "Generated" },
    { id: 3, name: "Maintenance Request Log", date: "2025-01-10", type: "Maintenance", status: "Pending" },
];

export default function HostelReportsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <BarChart className="h-8 w-8 text-primary" />
                    Hostel Reports
                </h2>
                <Button variant="outline">
                    <Download className="mr-2 h-4 w-4" />
                    Export All
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Occupancy Rate</p>
                        <h3 className="text-3xl font-bold text-blue-600 mt-2">85%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Mess Budget Used</p>
                        <h3 className="text-3xl font-bold text-green-600 mt-2">72%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Open Complaints</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">5</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Generated Reports</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Report Name</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {hostelReports.map((report) => (
                                <TableRow key={report.id}>
                                    <TableCell className="font-semibold">{report.name}</TableCell>
                                    <TableCell>{report.type}</TableCell>
                                    <TableCell>{report.date}</TableCell>
                                    <TableCell>{report.status}</TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm">Download</Button>
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
