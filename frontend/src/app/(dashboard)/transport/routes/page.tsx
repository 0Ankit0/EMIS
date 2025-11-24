"use client";

import { Route, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const routesData = [
    { id: 1, name: "Route A - North", stops: 8, students: 45, vehicle: "BUS-001" },
    { id: 2, name: "Route B - South", stops: 6, students: 32, vehicle: "BUS-002" },
];

export default function TransportRoutesPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Route className="h-8 w-8 text-primary" />
                        Transport Routes
                    </h2>
                </div>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Route
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Routes</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Route Name</TableHead>
                                <TableHead className="text-right">Stops</TableHead>
                                <TableHead className="text-right">Students</TableHead>
                                <TableHead>Vehicle</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {routesData.map((route) => (
                                <TableRow key={route.id}>
                                    <TableCell className="font-semibold">{route.name}</TableCell>
                                    <TableCell className="text-right">{route.stops}</TableCell>
                                    <TableCell className="text-right">{route.students}</TableCell>
                                    <TableCell className="font-mono">{route.vehicle}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
