"use client";

import { DollarSign, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const financialData = [
    { id: 1, category: "Tuition Fees", amount: 150000, type: "Income", date: "2025-01-01" },
    { id: 2, category: "Staff Salaries", amount: 80000, type: "Expense", date: "2025-01-05" },
    { id: 3, category: "Maintenance", amount: 5000, type: "Expense", date: "2025-01-10" },
];

export default function FinancialReportsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <DollarSign className="h-8 w-8 text-primary" />
                    Financial Reports
                </h2>
                <Button variant="outline">
                    <Download className="mr-2 h-4 w-4" />
                    Export PDF
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Income</p>
                        <h3 className="text-3xl font-bold text-green-600 mt-2">$150,000</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Expenses</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">$85,000</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Net Profit</p>
                        <h3 className="text-3xl font-bold text-blue-600 mt-2">$65,000</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Transactions</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Date</TableHead>
                                <TableHead>Category</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead className="text-right">Amount</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {financialData.map((item) => (
                                <TableRow key={item.id}>
                                    <TableCell>{item.date}</TableCell>
                                    <TableCell>{item.category}</TableCell>
                                    <TableCell className={item.type === "Income" ? "text-green-600" : "text-red-600"}>
                                        {item.type}
                                    </TableCell>
                                    <TableCell className="text-right font-mono">${item.amount.toLocaleString()}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
