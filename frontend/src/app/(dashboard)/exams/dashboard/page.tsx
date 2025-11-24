"use client";

import Link from "next/link";
import { FileText, Plus, Calendar, Award, BarChart3, Edit } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ExamsDashboardPage() {
    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <FileText className="h-8 w-8 text-primary" />
                    Exams Dashboard
                </h2>
                <p className="text-muted-foreground">Manage examinations and results</p>
            </div>

            {/* Statistics Card */}
            <Card className="border-l-4 border-blue-500">
                <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-muted-foreground font-semibold uppercase">Total Items</p>
                            <h3 className="text-3xl font-bold mt-2">0</h3>
                        </div>
                        <div className="bg-blue-100 rounded-full p-4">
                            <FileText className="h-6 w-6 text-blue-600" />
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
                <CardHeader>
                    <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                        <Link href="/exams/list">
                            <FileText className="mr-2 h-5 w-5" />
                            Exam List
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                        <Link href="/exams/create">
                            <Plus className="mr-2 h-5 w-5" />
                            Create Exam
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                        <Link href="/exams/schedule">
                            <Calendar className="mr-2 h-5 w-5" />
                            Schedule
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-yellow-600 hover:bg-yellow-700" asChild>
                        <Link href="/exams/grade-entry">
                            <Edit className="mr-2 h-5 w-5" />
                            Grade Entry
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-indigo-600 hover:bg-indigo-700" asChild>
                        <Link href="/exams/results">
                            <Award className="mr-2 h-5 w-5" />
                            Results
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-red-600 hover:bg-red-700" asChild>
                        <Link href="/exams/analysis">
                            <BarChart3 className="mr-2 h-5 w-5" />
                            Analysis
                        </Link>
                    </Button>
                </CardContent>
            </Card>

            {/* Content Area */}
            <Card>
                <CardHeader>
                    <CardTitle>Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-muted-foreground">No recent activity to display.</p>
                </CardContent>
            </Card>
        </div>
    );
}
