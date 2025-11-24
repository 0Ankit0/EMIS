"use client";

import { AlertTriangle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const lowStockData = [
    { id: 1, name: "Printer Paper A4", sku: "OFF-001", current: 5, min: 20, category: "Stationery" },
    { id: 2, name: "Whiteboard Markers", sku: "OFF-005", current: 2, min: 10, category: "Stationery" },
];

export default function InventoryLowStockPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2 text-red-600">
                <AlertTriangle className="h-8 w-8" />
                Low Stock Alerts
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Items Below Minimum Level</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Item Name</TableHead>
                                <TableHead>SKU</TableHead>
                                <TableHead>Category</TableHead>
                                <TableHead className="text-right">Current Stock</TableHead>
                                <TableHead className="text-right">Min Level</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {lowStockData.map((item) => (
                                <TableRow key={item.id}>
                                    <TableCell className="font-semibold">{item.name}</TableCell>
                                    <TableCell className="font-mono text-sm">{item.sku}</TableCell>
                                    <TableCell>{item.category}</TableCell>
                                    <TableCell className="text-right font-bold text-red-600">{item.current}</TableCell>
                                    <TableCell className="text-right">{item.min}</TableCell>
                                    <TableCell>
                                        <Badge variant="destructive">Low Stock</Badge>
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
