"use client";

import Link from "next/link";
import { Plus, Search, Filter, Eye, Edit, List } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

// Mock data
const applications = [
    {
        id: 1,
        appNumber: "APP-2025-001",
        name: "Alice Johnson",
        email: "alice@example.com",
        program: "BS Computer Science",
        status: "submitted",
        submittedAt: "Oct 15, 2025",
    },
    {
        id: 2,
        appNumber: "APP-2025-002",
        name: "Bob Smith",
        email: "bob@example.com",
        program: "BBA",
        status: "under_review",
        submittedAt: "Oct 16, 2025",
    },
    {
        id: 3,
        appNumber: "APP-2025-003",
        name: "Charlie Brown",
        email: "charlie@example.com",
        program: "BS Software Engineering",
        status: "approved",
        submittedAt: "Oct 14, 2025",
    },
    {
        id: 4,
        appNumber: "APP-2025-004",
        name: "Diana Prince",
        email: "diana@example.com",
        program: "BS Computer Science",
        status: "rejected",
        submittedAt: "Oct 12, 2025",
    },
];

export default function ApplicationListPage() {
    const getStatusBadge = (status: string) => {
        switch (status) {
            case "approved":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Approved</Badge>;
            case "rejected":
                return <Badge className="bg-red-100 text-red-800 hover:bg-red-200 border-red-200">Rejected</Badge>;
            case "under_review":
                return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-yellow-200">Under Review</Badge>;
            case "submitted":
                return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-200 border-blue-200">Submitted</Badge>;
            default:
                return <Badge variant="secondary">Draft</Badge>;
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <List className="h-8 w-8 text-primary" />
                        Applications
                    </h2>
                    <p className="text-muted-foreground">View and manage admission applications</p>
                </div>
                <Button asChild className="bg-blue-600 hover:bg-blue-700">
                    <Link href="/admissions/applications/new">
                        <Plus className="mr-2 h-4 w-4" /> New Application
                    </Link>
                </Button>
            </div>

            {/* Filters */}
            <Card>
                <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="relative">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search applications..." className="pl-10" />
                        </div>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="All Status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Status</SelectItem>
                                <SelectItem value="draft">Draft</SelectItem>
                                <SelectItem value="submitted">Submitted</SelectItem>
                                <SelectItem value="under_review">Under Review</SelectItem>
                                <SelectItem value="approved">Approved</SelectItem>
                                <SelectItem value="rejected">Rejected</SelectItem>
                            </SelectContent>
                        </Select>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="Sort By" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="newest">Newest First</SelectItem>
                                <SelectItem value="oldest">Oldest First</SelectItem>
                                <SelectItem value="name">Name A-Z</SelectItem>
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
                            <TableHead>Application #</TableHead>
                            <TableHead>Applicant</TableHead>
                            <TableHead>Email</TableHead>
                            <TableHead>Program</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Submitted</TableHead>
                            <TableHead>Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {applications.map((app) => (
                            <TableRow key={app.id}>
                                <TableCell className="font-medium">{app.appNumber}</TableCell>
                                <TableCell>{app.name}</TableCell>
                                <TableCell>{app.email}</TableCell>
                                <TableCell>{app.program}</TableCell>
                                <TableCell>{getStatusBadge(app.status)}</TableCell>
                                <TableCell>{app.submittedAt}</TableCell>
                                <TableCell>
                                    <div className="flex space-x-2">
                                        <Button variant="ghost" size="icon" className="text-blue-600 hover:text-blue-800 hover:bg-blue-50">
                                            <Eye className="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="icon" className="text-green-600 hover:text-green-800 hover:bg-green-50">
                                            <Edit className="h-4 w-4" />
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
