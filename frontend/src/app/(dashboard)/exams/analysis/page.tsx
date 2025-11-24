"use client";

import { BarChart3, TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ExamAnalysisPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <BarChart3 className="h-8 w-8 text-primary" />
                Exam Analysis
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                            <TrendingUp className="h-4 w-4" />
                            <span className="text-sm">Average Score</span>
                        </div>
                        <h3 className="text-4xl font-bold text-blue-600">78.5%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Pass Rate</p>
                        <h3 className="text-4xl font-bold text-green-600 mt-2">85%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Top Performer</p>
                        <h3 className="text-2xl font-bold text-purple-600 mt-2">98.5%</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Performance Trends</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="h-64 flex items-center justify-center text-muted-foreground">
                        Chart visualization would go here
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
