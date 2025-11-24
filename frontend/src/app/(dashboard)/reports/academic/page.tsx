"use client";

import { FileText, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const reportTypes = [
    { name: "Student Performance", icon: "📊" },
    { name: "Attendance Summary", icon: "📅" },
    { name: "Financial Overview", icon: "💰" },
    { name: "Enrollment Trends", icon: "📈" },
];

export default function ReportsAcademicPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <FileText className="h-8 w-8 text-primary" />
                    Academic Reports
                </h2>
                <Button>
                    <Download className="mr-2 h-4 w-4" />
                    Export All
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reportTypes.map((report, idx) => (
                    <Card key={idx} className="cursor-pointer hover:shadow-lg transition">
                        <CardContent className="p-8">
                            <div className="text-5xl mb-4">{report.icon}</div>
                            <h3 className="text-xl font-bold mb-2">{report.name}</h3>
                            <Button className="w-full mt-4">
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
