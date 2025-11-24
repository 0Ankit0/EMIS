"use client";

import Link from "next/link";
import { DollarSign, CreditCard, FileText, TrendingUp, Users, AlertCircle, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// Mock data
const stats = [
    { label: "Total Revenue", value: "$1,250,000", change: "+12.5%", trend: "up", icon: DollarSign, color: "text-green-600", bg: "bg-green-100" },
    { label: "Pending Fees", value: "$45,000", change: "-2.3%", trend: "down", icon: AlertCircle, color: "text-red-600", bg: "bg-red-100" },
    { label: "Active Invoices", value: "150", change: "+5.1%", trend: "up", icon: FileText, color: "text-blue-600", bg: "bg-blue-100" },
    { label: "Recent Payments", value: "25", change: "+8.2%", trend: "up", icon: CreditCard, color: "text-purple-600", bg: "bg-purple-100" },
];

const recentTransactions = [
    { id: 1, student: "John Doe", amount: "$5,000", type: "Tuition Fee", date: "Oct 25, 2025", status: "completed" },
    { id: 2, student: "Jane Smith", amount: "$2,500", type: "Lab Fee", date: "Oct 24, 2025", status: "completed" },
    { id: 3, student: "Michael Brown", amount: "$1,000", type: "Library Fee", date: "Oct 24, 2025", status: "pending" },
    { id: 4, student: "Sarah Wilson", amount: "$5,000", type: "Tuition Fee", date: "Oct 23, 2025", status: "completed" },
    { id: 5, student: "David Lee", amount: "$500", type: "Late Fee", date: "Oct 23, 2025", status: "failed" },
];

export default function FinanceDashboardPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <DollarSign className="h-8 w-8 text-primary" />
                        Finance Dashboard
                    </h2>
                    <p className="text-muted-foreground">Financial management and fee collection overview</p>
                </div>
                <div className="flex gap-2">
                    <Button asChild variant="outline">
                        <Link href="/finance/invoices/new">
                            <FileText className="mr-2 h-4 w-4" /> Create Invoice
                        </Link>
                    </Button>
                    <Button asChild className="bg-green-600 hover:bg-green-700">
                        <Link href="/finance/payments/new">
                            <CreditCard className="mr-2 h-4 w-4" /> Record Payment
                        </Link>
                    </Button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, index) => (
                    <Card key={index} className="border-none shadow-sm">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className={`w-12 h-12 rounded-full ${stat.bg} flex items-center justify-center`}>
                                    <stat.icon className={`h-6 w-6 ${stat.color}`} />
                                </div>
                                <div className={`flex items-center text-sm font-medium ${stat.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                                    {stat.trend === 'up' ? <ArrowUpRight className="h-4 w-4 mr-1" /> : <ArrowDownRight className="h-4 w-4 mr-1" />}
                                    {stat.change}
                                </div>
                            </div>
                            <div>
                                <p className="text-sm font-medium text-muted-foreground mb-1">{stat.label}</p>
                                <h3 className="text-2xl font-bold">{stat.value}</h3>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Recent Transactions */}
                <Card className="lg:col-span-2">
                    <CardHeader>
                        <CardTitle>Recent Transactions</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {recentTransactions.map((tx) => (
                                <div key={tx.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                                    <div className="flex items-center gap-4">
                                        <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center border shadow-sm">
                                            <DollarSign className="h-5 w-5 text-green-600" />
                                        </div>
                                        <div>
                                            <p className="font-semibold text-gray-800">{tx.student}</p>
                                            <p className="text-sm text-gray-500">{tx.type} • {tx.date}</p>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <p className="font-bold text-gray-800">{tx.amount}</p>
                                        <Badge variant={tx.status === 'completed' ? 'default' : tx.status === 'pending' ? 'secondary' : 'destructive'} className="mt-1">
                                            {tx.status}
                                        </Badge>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="mt-4 text-center">
                            <Button variant="ghost" asChild>
                                <Link href="/finance/payments">View All Transactions</Link>
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                {/* Quick Actions */}
                <Card>
                    <CardHeader>
                        <CardTitle>Quick Actions</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                        <Button variant="outline" className="w-full justify-start h-auto py-3" asChild>
                            <Link href="/finance/fees">
                                <div className="flex items-center text-left">
                                    <div className="bg-blue-100 p-2 rounded-md mr-3">
                                        <FileText className="h-5 w-5 text-blue-600" />
                                    </div>
                                    <div>
                                        <div className="font-semibold">Fee Structures</div>
                                        <div className="text-xs text-muted-foreground">Manage fee templates</div>
                                    </div>
                                </div>
                            </Link>
                        </Button>
                        <Button variant="outline" className="w-full justify-start h-auto py-3" asChild>
                            <Link href="/finance/invoices">
                                <div className="flex items-center text-left">
                                    <div className="bg-purple-100 p-2 rounded-md mr-3">
                                        <FileText className="h-5 w-5 text-purple-600" />
                                    </div>
                                    <div>
                                        <div className="font-semibold">Invoices</div>
                                        <div className="text-xs text-muted-foreground">View and manage invoices</div>
                                    </div>
                                </div>
                            </Link>
                        </Button>
                        <Button variant="outline" className="w-full justify-start h-auto py-3" asChild>
                            <Link href="/finance/reports">
                                <div className="flex items-center text-left">
                                    <div className="bg-orange-100 p-2 rounded-md mr-3">
                                        <TrendingUp className="h-5 w-5 text-orange-600" />
                                    </div>
                                    <div>
                                        <div className="font-semibold">Financial Reports</div>
                                        <div className="text-xs text-muted-foreground">View revenue analytics</div>
                                    </div>
                                </div>
                            </Link>
                        </Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
