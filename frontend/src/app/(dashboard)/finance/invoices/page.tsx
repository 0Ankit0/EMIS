"use client";

import Link from "next/link";
import { Plus, Search, Filter, Eye, Download, CreditCard, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

// Mock data based on Invoice model
const invoices = [
    {
        id: 1,
        invoiceNumber: "INV-2025-001234",
        student: "John Doe",
        studentId: "STU-2025-001",
        amountDue: "$5,000.00",
        amountPaid: "$2,500.00",
        balance: "$2,500.00",
        dueDate: "Oct 30, 2025",
        status: "partial",
        date: "Oct 01, 2025",
    },
    {
        id: 2,
        invoiceNumber: "INV-2025-001235",
        student: "Jane Smith",
        studentId: "STU-2025-002",
        amountDue: "$4,800.00",
        amountPaid: "$4,800.00",
        balance: "$0.00",
        dueDate: "Oct 30, 2025",
        status: "paid",
        date: "Oct 01, 2025",
    },
    {
        id: 3,
        invoiceNumber: "INV-2025-001236",
        student: "Michael Brown",
        studentId: "STU-2022-045",
        amountDue: "$1,200.00",
        amountPaid: "$0.00",
        balance: "$1,200.00",
        dueDate: "Sep 30, 2025",
        status: "overdue",
        date: "Sep 01, 2025",
    },
    {
        id: 4,
        invoiceNumber: "INV-2025-001237",
        student: "Sarah Wilson",
        studentId: "STU-2024-112",
        amountDue: "$5,500.00",
        amountPaid: "$0.00",
        balance: "$5,500.00",
        dueDate: "Nov 15, 2025",
        status: "pending",
        date: "Oct 15, 2025",
    },
];

export default function InvoicesPage() {
    const getStatusBadge = (status: string) => {
        switch (status) {
            case "paid":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Paid</Badge>;
            case "partial":
                return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-yellow-200">Partial</Badge>;
            case "overdue":
                return <Badge className="bg-red-100 text-red-800 hover:bg-red-200 border-red-200">Overdue</Badge>;
            case "pending":
                return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-200 border-blue-200">Pending</Badge>;
            case "cancelled":
                return <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-200 border-gray-200">Cancelled</Badge>;
            default:
                return <Badge variant="secondary">{status}</Badge>;
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <FileText className="h-8 w-8 text-primary" />
                        Invoices
                    </h2>
                    <p className="text-muted-foreground">Manage student fee invoices</p>
                </div>
                <Button asChild className="bg-blue-600 hover:bg-blue-700">
                    <Link href="/finance/invoices/new">
                        <Plus className="mr-2 h-4 w-4" /> Generate Invoice
                    </Link>
                </Button>
            </div>

            {/* Filters */}
            <Card>
                <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="relative md:col-span-2">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search invoices by number or student..." className="pl-10" />
                        </div>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="Status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Status</SelectItem>
                                <SelectItem value="paid">Paid</SelectItem>
                                <SelectItem value="pending">Pending</SelectItem>
                                <SelectItem value="overdue">Overdue</SelectItem>
                                <SelectItem value="partial">Partially Paid</SelectItem>
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
                            <TableHead>Invoice #</TableHead>
                            <TableHead>Student</TableHead>
                            <TableHead>Date</TableHead>
                            <TableHead>Due Date</TableHead>
                            <TableHead className="text-right">Amount</TableHead>
                            <TableHead className="text-right">Balance</TableHead>
                            <TableHead className="text-center">Status</TableHead>
                            <TableHead className="text-center">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {invoices.map((invoice) => (
                            <TableRow key={invoice.id}>
                                <TableCell className="font-mono font-medium">{invoice.invoiceNumber}</TableCell>
                                <TableCell>
                                    <div className="font-medium">{invoice.student}</div>
                                    <div className="text-xs text-muted-foreground">{invoice.studentId}</div>
                                </TableCell>
                                <TableCell>{invoice.date}</TableCell>
                                <TableCell>{invoice.dueDate}</TableCell>
                                <TableCell className="text-right font-medium">{invoice.amountDue}</TableCell>
                                <TableCell className="text-right font-bold text-gray-700">{invoice.balance}</TableCell>
                                <TableCell className="text-center">{getStatusBadge(invoice.status)}</TableCell>
                                <TableCell className="text-center">
                                    <div className="flex justify-center space-x-2">
                                        <Button variant="ghost" size="icon" className="text-blue-600 hover:text-blue-800 hover:bg-blue-50" title="View Details">
                                            <Eye className="h-4 w-4" />
                                        </Button>
                                        {invoice.status !== 'paid' && (
                                            <Button variant="ghost" size="icon" className="text-green-600 hover:text-green-800 hover:bg-green-50" title="Record Payment">
                                                <CreditCard className="h-4 w-4" />
                                            </Button>
                                        )}
                                        <Button variant="ghost" size="icon" className="text-gray-600 hover:text-gray-800 hover:bg-gray-50" title="Download PDF">
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
