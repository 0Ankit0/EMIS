"use client";

import { useState } from "react";
import { DollarSign, Download, Filter, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const paymentsData = [
    { id: 1, transactionId: "TXN-2025-001", student: "John Doe", studentId: "STU001", amount: 5000, date: "2025-01-20", method: "Credit Card", status: "completed", feeType: "Tuition" },
    { id: 2, transactionId: "TXN-2025-002", student: "Jane Smith", studentId: "STU002", amount: 1500, date: "2025-01-20", method: "Bank Transfer", status: "pending", feeType: "Library" },
    { id: 3, transactionId: "TXN-2025-003", student: "Mike Johnson", studentId: "STU003", amount: 3000, date: "2025-01-19", method: "Cash", status: "completed", feeType: "Lab Fee" },
    { id: 4, transactionId: "TXN-2025-004", student: "Sarah Williams", studentId: "STU004", amount: 2500, date: "2025-01-19", method: "Online", status: "failed", feeType: "Hostel" },
];

export default function PaymentsListPage() {
    const [payments] = useState(paymentsData);
    const [searchTerm, setSearchTerm] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");

    const filteredPayments = payments.filter(payment => {
        const matchesSearch = payment.student.toLowerCase().includes(searchTerm.toLowerCase()) ||
            payment.transactionId.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesStatus = statusFilter === "all" || payment.status === statusFilter;
        return matchesSearch && matchesStatus;
    });

    const getStatusBadge = (status: string) => {
        const variants = {
            completed: "bg-green-100 text-green-800",
            pending: "bg-yellow-100 text-yellow-800",
            failed: "bg-red-100 text-red-800",
            refunded: "bg-blue-100 text-blue-800",
        };
        return <Badge className={variants[status as keyof typeof variants]}>{status.toUpperCase()}</Badge>;
    };

    const totalAmount = filteredPayments.reduce((sum, p) => sum + p.amount, 0);
    const completedAmount = filteredPayments.filter(p => p.status === "completed").reduce((sum, p) => sum + p.amount, 0);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <DollarSign className="h-8 w-8 text-green-600" />
                        Payment Records
                    </h2>
                    <p className="text-muted-foreground">Track and manage financial transactions</p>
                </div>
                <Button>
                    <Download className="mr-2 h-4 w-4" />
                    Export
                </Button>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Transactions</p>
                        <h3 className="text-3xl font-bold mt-2">{filteredPayments.length}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Total Amount</p>
                        <h3 className="text-3xl font-bold text-blue-600 mt-2">${totalAmount.toLocaleString()}</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground">Completed</p>
                        <h3 className="text-3xl font-bold text-green-600 mt-2">${completedAmount.toLocaleString()}</h3>
                    </CardContent>
                </Card>
            </div>

            {/* Filters */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Filter className="h-5 w-5" />
                        Filters
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label className="text-sm font-medium mb-2 block">Search</label>
                            <div className="relative">
                                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <Input
                                    placeholder="Student or Transaction ID..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="pl-10"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="text-sm font-medium mb-2 block">Status</label>
                            <Select value={statusFilter} onValueChange={setStatusFilter}>
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="all">All Status</SelectItem>
                                    <SelectItem value="completed">Completed</SelectItem>
                                    <SelectItem value="pending">Pending</SelectItem>
                                    <SelectItem value="failed">Failed</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label className="text-sm font-medium mb-2 block">Date Range</label>
                            <input
                                type="date"
                                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                            />
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Payments Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Transactions ({filteredPayments.length})</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Transaction ID</TableHead>
                                <TableHead>Student</TableHead>
                                <TableHead>Fee Type</TableHead>
                                <TableHead className="text-right">Amount</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Method</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredPayments.map((payment) => (
                                <TableRow key={payment.id}>
                                    <TableCell className="font-mono text-sm">{payment.transactionId}</TableCell>
                                    <TableCell>
                                        <div>
                                            <p className="font-semibold">{payment.student}</p>
                                            <p className="text-sm text-muted-foreground">{payment.studentId}</p>
                                        </div>
                                    </TableCell>
                                    <TableCell>{payment.feeType}</TableCell>
                                    <TableCell className="text-right font-bold text-green-600">
                                        ${payment.amount.toLocaleString()}
                                    </TableCell>
                                    <TableCell>{payment.date}</TableCell>
                                    <TableCell>{payment.method}</TableCell>
                                    <TableCell>{getStatusBadge(payment.status)}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
