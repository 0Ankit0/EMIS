"use client";

import { Award } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const certificatesData = [
    { id: 1, course: "CS101", title: "Programming Certificate", issueDate: "2025-01-15", grade: "A" },
    { id: 2, course: "WEB201", title: "Web Development Certificate", issueDate: "2024-12-20", grade: "A-" },
];

export default function LMSCertificatesPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Award className="h-8 w-8 text-primary" />
                My Certificates
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {certificatesData.map((cert) => (
                    <Card key={cert.id} className="border-2 border-blue-200">
                        <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
                            <CardTitle className="flex items-center gap-2">
                                <Award className="h-6 w-6" />
                                Certificate of Completion
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-6">
                            <h3 className="text-xl font-bold mb-2">{cert.title}</h3>
                            <p className="text-sm text-muted-foreground mb-1">Course: {cert.course}</p>
                            <p className="text-sm text-muted-foreground mb-1">Issue Date: {cert.issueDate}</p>
                            <p className="text-sm mb-4">Grade: <span className="text-2xl font-bold text-green-600">{cert.grade}</span></p>
                            <button className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">
                                Download Certificate
                            </button>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
