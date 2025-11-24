"use client";

import Link from "next/link";
import {
    FileText,
    Send,
    Clock,
    CheckCircle,
    XCircle,
    PlusCircle,
    List,
    Trophy,
    History,
    Eye,
    ArrowRight,
    Inbox
} from "lucide-react";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

export default function AdmissionsDashboard() {
    // Mock data - replace with API call
    const stats = {
        total: 1250,
        submitted: 850,
        pending: 120,
        approved: 680,
        rejected: 45,
    };

    const recentApplications = [
        { id: 1, name: "John Doe", appNumber: "APP-2024-001", status: "approved" },
        { id: 2, name: "Jane Smith", appNumber: "APP-2024-002", status: "under_review" },
        { id: 3, name: "Robert Johnson", appNumber: "APP-2024-003", status: "rejected" },
        { id: 4, name: "Emily Davis", appNumber: "APP-2024-004", status: "submitted" },
    ];

    const meritLists = [
        { id: 1, name: "First Merit List", program: "BS Computer Science", year: "2024" },
        { id: 2, name: "Second Merit List", program: "BBA", year: "2024" },
    ];

    const getStatusBadge = (status: string) => {
        switch (status) {
            case "approved":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">Approved</Badge>;
            case "rejected":
                return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Rejected</Badge>;
            case "under_review":
                return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">Under Review</Badge>;
            default:
                return <Badge variant="secondary">Submitted</Badge>;
        }
    };

    return (
        <div className="space-y-8">
            {/* Header */}
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <FileText className="h-8 w-8 text-primary" />
                    Admissions Dashboard
                </h2>
                <p className="text-muted-foreground">Manage admission applications and processes</p>
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                <StatsCard title="Total Applications" value={stats.total} icon={FileText} color="blue" />
                <StatsCard title="Submitted" value={stats.submitted} icon={Send} color="purple" />
                <StatsCard title="Pending" value={stats.pending} icon={Clock} color="yellow" />
                <StatsCard title="Approved" value={stats.approved} icon={CheckCircle} color="green" />
                <StatsCard title="Rejected" value={stats.rejected} icon={XCircle} color="red" />
            </div>

            {/* Quick Actions */}
            <Card className="shadow-md">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Trophy className="h-5 w-5 text-primary" />
                        Quick Actions
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <Button className="h-auto py-4 flex flex-col items-center gap-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700" asChild>
                            <Link href="/admissions/applications/new">
                                <PlusCircle className="h-6 w-6" />
                                <span className="font-semibold">New Application</span>
                            </Link>
                        </Button>
                        <Button className="h-auto py-4 flex flex-col items-center gap-2 bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-600 hover:to-yellow-700" asChild>
                            <Link href="/admissions/applications?status=under_review">
                                <Clock className="h-6 w-6" />
                                <span className="font-semibold">Review Pending</span>
                            </Link>
                        </Button>
                        <Button className="h-auto py-4 flex flex-col items-center gap-2 bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700" asChild>
                            <Link href="/admissions/applications">
                                <List className="h-6 w-6" />
                                <span className="font-semibold">All Applications</span>
                            </Link>
                        </Button>
                        <Button className="h-auto py-4 flex flex-col items-center gap-2 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700" asChild>
                            <Link href="/admissions/merit-lists">
                                <Trophy className="h-6 w-6" />
                                <span className="font-semibold">Merit Lists</span>
                            </Link>
                        </Button>
                    </div>
                </CardContent>
            </Card>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Recent Applications */}
                <Card className="shadow-md">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <History className="h-5 w-5 text-primary" />
                            Recent Applications
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Applicant</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {recentApplications.length > 0 ? (
                                    recentApplications.map((app) => (
                                        <TableRow key={app.id}>
                                            <TableCell>
                                                <div className="font-medium">{app.name}</div>
                                                <div className="text-xs text-muted-foreground">{app.appNumber}</div>
                                            </TableCell>
                                            <TableCell>{getStatusBadge(app.status)}</TableCell>
                                            <TableCell>
                                                <Button variant="ghost" size="sm" asChild>
                                                    <Link href={`/admissions/applications/${app.id}`}>
                                                        <Eye className="h-4 w-4 text-blue-600" />
                                                    </Link>
                                                </Button>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                ) : (
                                    <TableRow>
                                        <TableCell colSpan={3} className="text-center py-8 text-muted-foreground">
                                            <Inbox className="h-8 w-8 mx-auto mb-2" />
                                            No recent applications
                                        </TableCell>
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </CardContent>
                </Card>

                {/* Merit Lists */}
                <Card className="shadow-md">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Trophy className="h-5 w-5 text-primary" />
                            Published Merit Lists
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-3">
                            {meritLists.length > 0 ? (
                                meritLists.map((list) => (
                                    <div key={list.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors flex items-center justify-between">
                                        <div>
                                            <h4 className="font-semibold">{list.name}</h4>
                                            <p className="text-sm text-muted-foreground">{list.program} - {list.year}</p>
                                        </div>
                                        <Button variant="ghost" size="sm" asChild>
                                            <Link href={`/admissions/merit-lists/${list.id}`}>
                                                <ArrowRight className="h-4 w-4 text-blue-600" />
                                            </Link>
                                        </Button>
                                    </div>
                                ))
                            ) : (
                                <div className="text-center py-8 text-muted-foreground">
                                    <Inbox className="h-8 w-8 mx-auto mb-2" />
                                    No published merit lists
                                </div>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
