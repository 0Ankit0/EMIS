"use client";

import { Fuel, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const fuelData = [
    { id: 1, vehicle: "BUS-001", date: "2025-01-20", liters: 45, cost: 4500, driver: "John Driver" },
    { id: 2, vehicle: "VAN-002", date: "2025-01-21", liters: 30, cost: 3000, driver: "Jane Driver" },
];

export default function TransportFuelPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Fuel className="h-8 w-8 text-primary" />
                    Fuel Logs
                </h2>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Log
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Fuel Logs</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Vehicle</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead className="text-right">Liters</TableHead>
                                <TableHead className="text-right">Cost</TableHead>
                                <TableHead>Driver</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {fuelData.map((log) => (
                                <TableRow key={log.id}>
                                    <TableCell className="font-mono">{log.vehicle}</TableCell>
                                    <TableCell>{log.date}</TableCell>
                                    <TableCell className="text-right">{log.liters} L</TableCell>
                                    <TableCell className="text-right">${log.cost}</TableCell>
                                    <TableCell>{log.driver}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
