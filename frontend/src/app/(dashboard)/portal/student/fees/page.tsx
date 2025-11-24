"use client";

import { DollarSign } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const feesData = [
    { id: 1, type: "Tuition Fee", amount: 5000, dueDate: "2025-02-01", status: "pending" },
    { id: 2, type: "Lab Fee", amount: 1500, dueDate: "2025-02-01", status: "paid" },
];

export default function StudentFeesPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <DollarSign className="h-8 w-8 text-primary" />
                My Fees
            </h2>

            <div className="grid grid-cols-2 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Pending</p>
                        <h3 className="text-3xl font-bold text-red-600 mt-2">$5,000</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Paid</p>
                        <h3 className="text-3xl font-bold text-green-600 mt-2">$1,500</h3>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Fee Details</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Fee Type</TableHead>
                                <TableHead className="text-right">Amount</TableHead>
                                <TableHead>Due Date</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {feesData.map((fee) => (
                                <TableRow key={fee.id}>
                                    <TableCell className="font-semibold">{fee.type}</TableCell>
                                    <TableCell className="text-right font-bold">${fee.amount.toLocaleString()}</TableCell>
                                    <TableCell>{fee.dueDate}</TableCell>
                                    <TableCell>
                                        <Badge className={fee.status === "paid" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}>
                                            {fee.status.toUpperCase()}
                                        </Badge>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
