"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, Award, Users, TrendingUp, Download, Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const meritListData = {
    id: 1,
    name: "Fall 2025 - Computer Science",
    program: "Computer Science",
    academicYear: "2024-2025",
    semester: "Fall",
    totalApplications: 150,
    cutoffRank: 50,
    cutoffScore: 85.5,
    publishedDate: "2025-01-20",
    isPublished: true,
    selectedStudents: [
        { rank: 1, name: "Alice Johnson", score: 98.5, applicationNo: "APP-2025-001", status: "selected" },
        { rank: 2, name: "Bob Smith", score: 97.2, applicationNo: "APP-2025-002", status: "selected" },
        { rank: 3, name: "Carol Williams", score: 96.8, applicationNo: "APP-2025-003", status: "selected" },
        { rank: 4, name: "David Brown", score: 95.5, applicationNo: "APP-2025-004", status: "selected" },
        { rank: 5, name: "Eve Davis", score: 94.2, applicationNo: "APP-2025-005", status: "selected" },
    ],
};

export default function MeritListDetailPage({ params }: { params: { id: string } }) {
    const [meritList] = useState(meritListData);

    const handlePublish = () => {
        // TODO: API call to publish
        alert("Merit list published!");
    };

    const handleExport = () => {
        // TODO: Generate PDF/Excel export
        console.log("Exporting merit list...");
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link href="/admissions/merit-lists">
                        <Button variant="ghost" size="icon">
                            <ArrowLeft className="h-5 w-5" />
                        </Button>
                    </Link>
                    <div>
                        <h2 className="text-3xl font-bold text-gray-800">{meritList.name}</h2>
                        <p className="text-muted-foreground">{meritList.program} - {meritList.semester} {meritList.academicYear}</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    {meritList.isPublished ? (
                        <Badge className="bg-green-100 text-green-800">Published</Badge>
                    ) : (
                        <Badge variant="secondary">Draft</Badge>
                    )}
                    <Button variant="outline" onClick={handleExport}>
                        <Download className="mr-2 h-4 w-4" />
                        Export
                    </Button>
                    {!meritList.isPublished && (
                        <Button onClick={handlePublish}>
                            <Award className="mr-2 h-4 w-4" />
                            Publish List
                        </Button>
                    )}
                </div>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Total Applications</p>
                                <h3 className="text-3xl font-bold mt-2">{meritList.totalApplications}</h3>
                            </div>
                            <Users className="h-8 w-8 text-blue-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Selected</p>
                                <h3 className="text-3xl font-bold mt-2">{meritList.selectedStudents.length}</h3>
                            </div>
                            <Award className="h-8 w-8 text-green-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Cutoff Rank</p>
                                <h3 className="text-3xl font-bold mt-2">#{meritList.cutoffRank}</h3>
                            </div>
                            <TrendingUp className="h-8 w-8 text-purple-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Cutoff Score</p>
                                <h3 className="text-3xl font-bold mt-2">{meritList.cutoffScore}</h3>
                            </div>
                            <TrendingUp className="h-8 w-8 text-yellow-600" />
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Merit List Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Selected Candidates</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead className="w-20">Rank</TableHead>
                                <TableHead>Candidate Name</TableHead>
                                <TableHead>Application No.</TableHead>
                                <TableHead className="text-right">Merit Score</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {meritList.selectedStudents.map((student) => (
                                <TableRow key={student.rank}>
                                    <TableCell className="font-bold">#{student.rank}</TableCell>
                                    <TableCell className="font-semibold">{student.name}</TableCell>
                                    <TableCell className="font-mono text-sm">{student.applicationNo}</TableCell>
                                    <TableCell className="text-right font-bold text-green-600">{student.score}</TableCell>
                                    <TableCell>
                                        <Badge className="bg-green-100 text-green-800 capitalize">
                                            {student.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Link href={`/admissions/applications/${student.applicationNo}`}>
                                            <Button variant="ghost" size="sm">
                                                <Eye className="h-4 w-4" />
                                            </Button>
                                        </Link>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

            {/* Publication Info */}
            {meritList.isPublished && (
                <Card className="bg-green-50 border-green-200">
                    <CardContent className="p-4">
                        <p className="text-sm text-green-800">
                            <strong>Published on:</strong> {meritList.publishedDate}
                        </p>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
