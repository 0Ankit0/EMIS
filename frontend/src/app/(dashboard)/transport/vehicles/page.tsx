"use client";

import { Bus, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const vehiclesData = [
    { id: 1, vehicleNo: "BUS-001", type: "School Bus", capacity: 50, driver: "John Driver", status: "active" },
    { id: 2, vehicleNo: "VAN-002", type: "Van", capacity: 15, driver: "Jane Driver", status: "maintenance" },
];

export default function TransportVehiclesPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Bus className="h-8 w-8 text-primary" />
                        Vehicles
                    </h2>
                    <p className="text-muted-foreground">Manage transport fleet</p>
                </div>
                <Link href="/transport/vehicles/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Vehicle
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Vehicles</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Vehicle No</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead className="text-right">Capacity</TableHead>
                                <TableHead>Driver</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {vehiclesData.map((vehicle) => (
                                <TableRow key={vehicle.id}>
                                    <TableCell className="font-mono font-bold">{vehicle.vehicleNo}</TableCell>
                                    <TableCell>{vehicle.type}</TableCell>
                                    <TableCell className="text-right">{vehicle.capacity}</TableCell>
                                    <TableCell>{vehicle.driver}</TableCell>
                                    <TableCell>
                                        <Badge className={vehicle.status === "active" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}>
                                            {vehicle.status.toUpperCase()}
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
