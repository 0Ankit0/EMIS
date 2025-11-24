"use client";

import { useState } from "react";
import { BarChart3, Download, TrendingUp, DollarSign } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const reportsData = {
    summary: {
        totalRevenue: 450000,
        totalCollected: 420000,
        totalPending: 30000,
        collectionRate: 93.3,
    },
    monthly: [
        { month: "September", revenue: 85000, collected: 82000, pending: 3000 },
        { month: "October", revenue: 90000, collected: 88000, pending: 2000 },
        { month: "November", revenue: 95000, collected: 90000, pending: 5000 },
        { month: "December", revenue: 88000, collected: 80000, pending: 8000 },
        { month: "January", revenue: 92000, collected: 80000, pending: 12000 },
    ],
    byCategory: [
        { category: "Tuition Fees", amount: 350000, percentage: 77.8 },
        { category: "Lab Fees", amount: 45000, percentage: 10 },
        { category: "Library Fees", amount: 25000, percentage: 5.6 },
        { category: "Hostel Fees", amount: 30000, percentage: 6.7 },
    ],
};

export default function FinanceReportsPage() {
    const [period, setPeriod] = useState("semester");
    const [data] = useState(reportsData);

    const handleExport = (type: string) => {
        console.log("Exporting report:", type);
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <BarChart3 className="h-8 w-8 text-primary" />
                        Financial Reports
                    </h2>
                    <p className="text-muted-foreground">Comprehensive financial analytics and insights</p>
                </div>
                <div className="flex gap-3">
                    <Select value={period} onValueChange={setPeriod}>
                        <SelectTrigger className="w-40">
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="month">This Month</SelectItem>
                            <SelectItem value="quarter">This Quarter</SelectItem>
                            <SelectItem value="semester">This Semester</SelectItem>
                            <SelectItem value="year">This Year</SelectItem>
                        </SelectContent>
                    </Select>
                    <Button onClick={() => handleExport("full")}>
                        <Download className="mr-2 h-4 w-4" />
                        Export Full Report
                    </Button>
                </div>
            </div>

            {/* Summary Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card className="border-l-4 border-blue-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Total Revenue</p>
                                <h3 className="text-3xl font-bold text-blue-600 mt-2">
                                    ${data.summary.totalRevenue.toLocaleString()}
                                </h3>
                            </div>
                            <DollarSign className="h-8 w-8 text-blue-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-green-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Collected</p>
                                <h3 className="text-3xl font-bold text-green-600 mt-2">
                                    ${data.summary.totalCollected.toLocaleString()}
                                </h3>
                            </div>
                            <TrendingUp className="h-8 w-8 text-green-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-red-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Pending</p>
                                <h3 className="text-3xl font-bold text-red-600 mt-2">
                                    ${data.summary.totalPending.toLocaleString()}
                                </h3>
                            </div>
                            <DollarSign className="h-8 w-8 text-red-600" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-purple-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Collection Rate</p>
                                <h3 className="text-3xl font-bold text-purple-600 mt-2">
                                    {data.summary.collectionRate}%
                                </h3>
                            </div>
                            <BarChart3 className="h-8 w-8 text-purple-600" />
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Monthly Trend */}
                <Card>
                    <CardHeader>
                        <div className="flex justify-between items-center">
                            <CardTitle>Monthly Revenue Trend</CardTitle>
                            <Button variant="ghost" size="sm" onClick={() => handleExport("monthly")}>
                                <Download className="h-4 w-4" />
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {data.monthly.map((month, index) => (
                                <div key={index} className="space-y-2">
                                    <div className="flex justify-between">
                                        <span className="font-semibold">{month.month}</span>
                                        <span className="font-bold text-green-600">${month.collected.toLocaleString()}</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                                        <div
                                            className="bg-green-600 h-2.5 rounded-full"
                                            style={{ width: `${(month.collected / month.revenue) * 100}%` }}
                                        />
                                    </div>
                                    <div className="flex justify-between text-xs text-muted-foreground">
                                        <span>Revenue: ${month.revenue.toLocaleString()}</span>
                                        <span className="text-red-600">Pending: ${month.pending.toLocaleString()}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                {/* Revenue by Category */}
                <Card>
                    <CardHeader>
                        <div className="flex justify-between items-center">
                            <CardTitle>Revenue by Category</CardTitle>
                            <Button variant="ghost" size="sm" onClick={() => handleExport("category")}>
                                <Download className="h-4 w-4" />
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {data.byCategory.map((category, index) => (
                                <div key={index} className="space-y-2">
                                    <div className="flex justify-between">
                                        <span className="font-semibold">{category.category}</span>
                                        <span className="font-bold text-blue-600">${category.amount.toLocaleString()}</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                                        <div
                                            className="bg-blue-600 h-2.5 rounded-full"
                                            style={{ width: `${category.percentage}%` }}
                                        />
                                    </div>
                                    <div className="text-xs text-muted-foreground text-right">
                                        {category.percentage}% of total
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Quick Reports */}
            <Card>
                <CardHeader>
                    <CardTitle>Quick Report Actions</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <Button variant="outline" className="h-auto py-4 flex-col gap-2">
                        <Download className="h-6 w-6" />
                        <span className="font-semibold text-sm">Fee Collection Summary</span>
                    </Button>
                    <Button variant="outline" className="h-auto py-4 flex-col gap-2">
                        <Download className="h-6 w-6" />
                        <span className="font-semibold text-sm">Outstanding Report</span>
                    </Button>
                    <Button variant="outline" className="h-auto py-4 flex-col gap-2">
                        <Download className="h-6 w-6" />
                        <span className="font-semibold text-sm">Payment History</span>
                    </Button>
                    <Button variant="outline" className="h-auto py-4 flex-col gap-2">
                        <Download className="h-6 w-6" />
                        <span className="font-semibold text-sm">Refund Report</span>
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
