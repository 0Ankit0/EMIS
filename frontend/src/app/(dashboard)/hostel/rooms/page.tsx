"use client";

import { Bed, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const roomsData = [
    { id: 1, number: "101", type: "Single", capacity: 1, occupied: 1, status: "Occupied", floor: "1st" },
    { id: 2, number: "102", type: "Double", capacity: 2, occupied: 1, status: "Available", floor: "1st" },
    { id: 3, number: "201", type: "Dormitory", capacity: 4, occupied: 0, status: "Vacant", floor: "2nd" },
];

export default function HostelRoomsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Bed className="h-8 w-8 text-primary" />
                    Room Management
                </h2>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Room
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Rooms</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Room No</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Floor</TableHead>
                                <TableHead className="text-right">Capacity</TableHead>
                                <TableHead className="text-right">Occupied</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {roomsData.map((room) => (
                                <TableRow key={room.id}>
                                    <TableCell className="font-bold">{room.number}</TableCell>
                                    <TableCell>{room.type}</TableCell>
                                    <TableCell>{room.floor}</TableCell>
                                    <TableCell className="text-right">{room.capacity}</TableCell>
                                    <TableCell className="text-right">{room.occupied}</TableCell>
                                    <TableCell>
                                        <Badge variant={room.status === "Occupied" ? "secondary" : "default"}>
                                            {room.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm">Edit</Button>
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
