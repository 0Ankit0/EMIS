"use client";

import Link from "next/link";
import { Plus, Search, Filter, Eye, Download, CreditCard, DollarSign } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

// Mock data based on Payment model
const payments = [
    {
        id: 1,
        receiptNumber: "RCP-2025-005678",
        student: "John Doe",
        studentId: "STU-2025-001",
        amount: "$2,500.00",
        method: "online",
        date: "Oct 25, 2025",
        invoiceNumber: "INV-2025-001234",
        status: "completed",
    },
    {
        id: 2,
        receiptNumber: "RCP-2025-005679",
        student: "Jane Smith",
        studentId: "STU-2025-002",
        amount: "$4,800.00",
        method: "bank_transfer",
        date: "Oct 24, 2025",
        invoiceNumber: "INV-2025-001235",
        status: "completed",
    },
    {
        id: 3,
        receiptNumber: "RCP-2025-005680",
        student: "Michael Brown",
        studentId: "STU-2022-045",
        amount: "$500.00",
        method: "cash",
        date: "Oct 24, 2025",
        invoiceNumber: "INV-2025-001236",
        status: "pending",
    },
    {
        id: 4,
        receiptNumber: "RCP-2025-005681",
        student: "Sarah Wilson",
        studentId: "STU-2024-112",
        amount: "$1,500.00",
        method: "cheque",
        date: "Oct 23, 2025",
        invoiceNumber: "INV-2025-001237",
        status: "failed",
    },
];

export default function PaymentsPage() {
    const getMethodBadge = (method: string) => {
        switch (method) {
            case "online":
                return <Badge variant="outline" className="border-blue-200 text-blue-700 bg-blue-50">Online</Badge>;
            case "cash":
                return <Badge variant="outline" className="border-green-200 text-green-700 bg-green-50">Cash</Badge>;
            case "bank_transfer":
                return <Badge variant="outline" className="border-purple-200 text-purple-700 bg-purple-50">Bank Transfer</Badge>;
            default:
                return <Badge variant="outline">{method}</Badge>;
        }
    };

    const getStatusBadge = (status: string) => {
        switch (status) {
            case "completed":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Completed</Badge>;
            case "pending":
                return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-yellow-200">Pending</Badge>;
            case "failed":
                return <Badge className="bg-red-100 text-red-800 hover:bg-red-200 border-red-200">Failed</Badge>;
            default:
                return <Badge variant="secondary">{status}</Badge>;
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <CreditCard className="h-8 w-8 text-primary" />
                        Payments
                    </h2>
                    <p className="text-muted-foreground">View and record fee payments</p>
                </div>
                <Button asChild className="bg-green-600 hover:bg-green-700">
                    <Link href="/finance/payments/new">
                        <Plus className="mr-2 h-4 w-4" /> Record Payment
                    </Link>
                </Button>
            </div>

            {/* Filters */}
            <Card>
                <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="relative md:col-span-2">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search payments by receipt, student, or invoice..." className="pl-10" />
                        </div>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="Payment Method" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Methods</SelectItem>
                                <SelectItem value="online">Online</SelectItem>
                                <SelectItem value="cash">Cash</SelectItem>
                                <SelectItem value="bank_transfer">Bank Transfer</SelectItem>
                                <SelectItem value="cheque">Cheque</SelectItem>
                            </SelectContent>
                        </Select>
                        <Button variant="secondary">
                            <Filter className="mr-2 h-4 w-4" /> Apply Filters
                        </Button>
                    </div>
                </CardContent>
            </Card>

            {/* Table */}
            <Card className="overflow-hidden">
                <Table>
                    <TableHeader className="bg-gray-50">
                        <TableRow>
                            <TableHead>Receipt #</TableHead>
                            <TableHead>Student</TableHead>
                            <TableHead>Date</TableHead>
                            <TableHead>Method</TableHead>
                            <TableHead>Invoice #</TableHead>
                            <TableHead className="text-right">Amount</TableHead>
                            <TableHead className="text-center">Status</TableHead>
                            <TableHead className="text-center">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {payments.map((payment) => (
                            <TableRow key={payment.id}>
                                <TableCell className="font-mono font-medium">{payment.receiptNumber}</TableCell>
                                <TableCell>
                                    <div className="font-medium">{payment.student}</div>
                                    <div className="text-xs text-muted-foreground">{payment.studentId}</div>
                                </TableCell>
                                <TableCell>{payment.date}</TableCell>
                                <TableCell>{getMethodBadge(payment.method)}</TableCell>
                                <TableCell className="font-mono text-sm">{payment.invoiceNumber}</TableCell>
                                <TableCell className="text-right font-bold text-gray-700">{payment.amount}</TableCell>
                                <TableCell className="text-center">{getStatusBadge(payment.status)}</TableCell>
                                <TableCell className="text-center">
                                    <div className="flex justify-center space-x-2">
                                        <Button variant="ghost" size="icon" className="text-blue-600 hover:text-blue-800 hover:bg-blue-50" title="View Details">
                                            <Eye className="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="icon" className="text-gray-600 hover:text-gray-800 hover:bg-gray-50" title="Download Receipt">
                                            <Download className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Card>
        </div>
    );
}
