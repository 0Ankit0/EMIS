"use client";

import { BarChart3, Download } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function AnalyticsReportsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <BarChart3 className="h-8 w-8 text-primary" />
                        Analytics Reports
                    </h2>
                    <p className="text-muted-foreground">Data insights and analytics</p>
                </div>
                <Button>
                    <Download className="mr-2 h-4 w-4" />
                    Export
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <h4 className="font-bold text-lg mb-2">Student Analytics</h4>
                        <p className="text-sm text-muted-foreground mb-4">Enrollment, performance, demographics</p>
                        <Button className="w-full">View Report</Button>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <h4 className="font-bold text-lg mb-2">Financial Analytics</h4>
                        <p className="text-sm text-muted-foreground mb-4">Revenue, expenses, collection rates</p>
                        <Button className="w-full">View Report</Button>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <h4 className="font-bold text-lg mb-2">Academic Analytics</h4>
                        <p className="text-sm text-muted-foreground mb-4">Grades, attendance, performance trends</p>
                        <Button className="w-full">View Report</Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
