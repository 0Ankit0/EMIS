"use client";

import { Umbrella, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const leaveData = [
    { id: 1, empId: "EMP001", name: "Dr. Smith", type: "Sick Leave", from: "2025-01-25", to: "2025-01-27", days: 3, status: "approved" },
    { id: 2, empId: "EMP002", name: "Prof. Johnson", type: "Casual Leave", from: "2025-02-01", to: "2025-02-02", days: 2, status: "pending" },
];

export default function HRLeavePage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Umbrella className="h-8 w-8 text-primary" />
                        Leave Management
                    </h2>
                    <p className="text-muted-foreground">Employee leave requests</p>
                </div>
                <Link href="/hr/leave/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        New Leave Request
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Leave Requests</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Emp ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>From</TableHead>
                                <TableHead>To</TableHead>
                                <TableHead className="text-right">Days</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {leaveData.map((leave) => (
                                <TableRow key={leave.id}>
                                    <TableCell className="font-mono text-sm">{leave.empId}</TableCell>
                                    <TableCell className="font-semibold">{leave.name}</TableCell>
                                    <TableCell>{leave.type}</TableCell>
                                    <TableCell>{leave.from}</TableCell>
                                    <TableCell>{leave.to}</TableCell>
                                    <TableCell className="text-right font-bold">{leave.days}</TableCell>
                                    <TableCell>
                                        <Badge className={leave.status === "approved" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}>
                                            {leave.status.toUpperCase()}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right space-x-2">
                                        {leave.status === "pending" && (
                                            <>
                                                <Button size="sm" variant="outline">Approve</Button>
                                                <Button size="sm" variant="destructive">Reject</Button>
                                            </>
                                        )}
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
