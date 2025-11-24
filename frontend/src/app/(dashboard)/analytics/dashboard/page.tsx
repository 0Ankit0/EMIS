"use client";

import { BarChart3, TrendingUp, Users, DollarSign } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function AnalyticsDashboardPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <BarChart3 className="h-8 w-8 text-primary" />
                Analytics Dashboard
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                            <Users className="h-4 w-4" />
                            <span className="text-sm">Total Students</span>
                        </div>
                        <h3 className="text-3xl font-bold">1,245</h3>
                        <p className="text-sm text-green-600 mt-1 flex items-center">
                            <TrendingUp className="h-3 w-3 mr-1" />
                            +5.2% this month
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                            <DollarSign className="h-4 w-4" />
                            <span className="text-sm">Revenue</span>
                        </div>
                        <h3 className="text-3xl font-bold">$45.2k</h3>
                        <p className="text-sm text-green-600 mt-1 flex items-center">
                            <TrendingUp className="h-3 w-3 mr-1" />
                            +12% vs last year
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                            <Users className="h-4 w-4" />
                            <span className="text-sm">Attendance</span>
                        </div>
                        <h3 className="text-3xl font-bold">94.5%</h3>
                        <p className="text-sm text-red-600 mt-1 flex items-center">
                            <TrendingUp className="h-3 w-3 mr-1" />
                            -0.5% this week
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                            <BarChart3 className="h-4 w-4" />
                            <span className="text-sm">Avg Grade</span>
                        </div>
                        <h3 className="text-3xl font-bold">B+</h3>
                        <p className="text-sm text-green-600 mt-1 flex items-center">
                            <TrendingUp className="h-3 w-3 mr-1" />
                            Improved
                        </p>
                    </CardContent>
                </Card>
            </div>

            <Tabs defaultValue="academic" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="academic">Academic Performance</TabsTrigger>
                    <TabsTrigger value="financial">Financial Overview</TabsTrigger>
                    <TabsTrigger value="attendance">Attendance Trends</TabsTrigger>
                </TabsList>
                <TabsContent value="academic" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Grade Distribution</CardTitle>
                        </CardHeader>
                        <CardContent className="h-96 flex items-center justify-center bg-muted/10">
                            <p className="text-muted-foreground">Chart: Grade distribution across all classes</p>
                        </CardContent>
                    </Card>
                </TabsContent>
                <TabsContent value="financial" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Revenue vs Expenses</CardTitle>
                        </CardHeader>
                        <CardContent className="h-96 flex items-center justify-center bg-muted/10">
                            <p className="text-muted-foreground">Chart: Monthly revenue and expense comparison</p>
                        </CardContent>
                    </Card>
                </TabsContent>
                <TabsContent value="attendance" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Daily Attendance Rate</CardTitle>
                        </CardHeader>
                        <CardContent className="h-96 flex items-center justify-center bg-muted/10">
                            <p className="text-muted-foreground">Chart: Daily attendance percentage over last 30 days</p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}
