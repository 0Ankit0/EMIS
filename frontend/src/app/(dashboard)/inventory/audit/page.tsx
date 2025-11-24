"use client";

import { ClipboardList } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const auditData = [
    { id: 1, date: "2025-01-15", auditor: "John Admin", itemsChecked: 150, discrepancies: 2, status: "Completed" },
    { id: 2, date: "2024-12-15", auditor: "Jane Staff", itemsChecked: 145, discrepancies: 0, status: "Completed" },
];

export default function InventoryAuditPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <ClipboardList className="h-8 w-8 text-primary" />
                    Inventory Audit
                </h2>
                <Button>Start New Audit</Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Audit History</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Date</TableHead>
                                <TableHead>Auditor</TableHead>
                                <TableHead className="text-right">Items Checked</TableHead>
                                <TableHead className="text-right">Discrepancies</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {auditData.map((audit) => (
                                <TableRow key={audit.id}>
                                    <TableCell>{audit.date}</TableCell>
                                    <TableCell>{audit.auditor}</TableCell>
                                    <TableCell className="text-right">{audit.itemsChecked}</TableCell>
                                    <TableCell className="text-right">{audit.discrepancies}</TableCell>
                                    <TableCell>{audit.status}</TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="outline" size="sm">View Report</Button>
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
