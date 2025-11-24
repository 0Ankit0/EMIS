"use client";

import { FileText, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const reportTypes = [
    { id: 1, name: "Academic Performance Report", description: "Student grades and performance metrics" },
    { id: 2, name: "Attendance Report", description: "Class and student attendance statistics" },
    { id: 3, name: "Financial Report", description: "Fee collection and expenditure summary" },
    { id: 4, name: "Student Enrollment Report", description: "Student demographics and enrollment trends" },
];

export default function ReportsListPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <FileText className="h-8 w-8 text-primary" />
                    Reports
                </h2>
                <p className="text-muted-foreground">Generate and export system reports</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reportTypes.map((report) => (
                    <Card key={report.id} className="hover:shadow-lg transition cursor-pointer">
                        <CardHeader>
                            <CardTitle>{report.name}</CardTitle>
                            <p className="text-sm text-muted-foreground">{report.description}</p>
                        </CardHeader>
                        <CardContent>
                            <Button className="w-full">
                                <Download className="mr-2 h-4 w-4" />
                                Generate Report
                            </Button>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
