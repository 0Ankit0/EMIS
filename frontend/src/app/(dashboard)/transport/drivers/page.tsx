"use client";

import { Users, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const driversData = [
    { id: 1, name: "John Driver", license: "DL123456", phone: "+1234567890", vehicle: "BUS-001" },
    { id: 2, name: "Jane Driver", license: "DL789012", phone: "+1234567891", vehicle: "VAN-002" },
];

export default function TransportDriversPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Users className="h-8 w-8 text-primary" />
                        Drivers
                    </h2>
                </div>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Driver
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Drivers</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>License</TableHead>
                                <TableHead>Phone</TableHead>
                                <TableHead>Assigned Vehicle</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {driversData.map((driver) => (
                                <TableRow key={driver.id}>
                                    <TableCell className="font-semibold">{driver.name}</TableCell>
                                    <TableCell className="font-mono text-sm">{driver.license}</TableCell>
                                    <TableCell>{driver.phone}</TableCell>
                                    <TableCell className="font-mono">{driver.vehicle}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
