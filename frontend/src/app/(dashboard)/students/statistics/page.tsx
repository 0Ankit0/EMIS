"use client";

import { BarChart3 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

export default function StudentsStatisticsPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <BarChart3 className="h-8 w-8 text-primary" />
                Student Statistics
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Students</p>
                        <h3 className="text-4xl font-bold text-blue-600 mt-2">1,250</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Active</p>
                        <h3 className="text-4xl font-bold text-green-600 mt-2">1,180</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">New This Month</p>
                        <h3 className="text-4xl font-bold text-purple-600 mt-2">45</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Avg Attendance</p>
                        <h3 className="text-4xl font-bold text-orange-600 mt-2">92%</h3>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
