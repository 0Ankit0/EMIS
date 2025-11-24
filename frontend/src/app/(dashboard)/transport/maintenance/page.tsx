"use client";

import { Wrench, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const maintenanceData = [
    { id: 1, vehicle: "BUS-001", type: "Service", date: "2025-01-10", cost: 1500, status: "Completed" },
    { id: 2, vehicle: "VAN-002", type: "Repair", date: "2025-01-25", cost: 0, status: "Scheduled" },
];

export default function TransportMaintenancePage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Wrench className="h-8 w-8 text-primary" />
                    Vehicle Maintenance
                </h2>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Schedule Maintenance
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Maintenance Records</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Vehicle</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead className="text-right">Cost</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {maintenanceData.map((record) => (
                                <TableRow key={record.id}>
                                    <TableCell className="font-mono">{record.vehicle}</TableCell>
                                    <TableCell>{record.type}</TableCell>
                                    <TableCell>{record.date}</TableCell>
                                    <TableCell className="text-right">{record.cost > 0 ? `$${record.cost}` : "-"}</TableCell>
                                    <TableCell>
                                        <Badge variant={record.status === "Completed" ? "default" : "outline"}>
                                            {record.status}
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
