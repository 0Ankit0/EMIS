"use client";

import { Package, Plus, AlertTriangle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const itemsData = [
    { id: 1, code: "ITM001", name: "Laptop Dell XPS", category: "Electronics", quantity: 15, minStock: 10, status: "good" },
    { id: 2, code: "ITM002", name: "Whiteboard Markers", category: "Stationery", quantity: 5, minStock: 20, status: "low" },
    { id: 3, code: "ITM003", name: "Projector", category: "Electronics", quantity: 8, minStock: 5, status: "good" },
];

export default function InventoryItemsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Package className="h-8 w-8 text-primary" />
                        Inventory Items
                    </h2>
                    <p className="text-muted-foreground">Manage stock and assets</p>
                </div>
                <Link href="/inventory/items/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Item
                    </Button>
                </Link>
            </div>

            {itemsData.filter(i => i.status === "low").length > 0 && (
                <Card className="bg-yellow-50 border-yellow-200">
                    <CardContent className="p-4 flex items-center gap-3">
                        <AlertTriangle className="h-6 w-6 text-yellow-600" />
                        <div>
                            <p className="font-semibold text-yellow-900">Low Stock Alert</p>
                            <p className="text-sm text-yellow-800">
                                {itemsData.filter(i => i.status === "low").length} items are below minimum stock level
                            </p>
                        </div>
                    </CardContent>
                </Card>
            )}

            <Card>
                <CardHeader>
                    <CardTitle>All Items</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Item Code</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Category</TableHead>
                                <TableHead className="text-right">Quantity</TableHead>
                                <TableHead className="text-right">Min Stock</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {itemsData.map((item) => (
                                <TableRow key={item.id}>
                                    <TableCell className="font-mono text-sm">{item.code}</TableCell>
                                    <TableCell className="font-semibold">{item.name}</TableCell>
                                    <TableCell>{item.category}</TableCell>
                                    <TableCell className="text-right font-bold">{item.quantity}</TableCell>
                                    <TableCell className="text-right">{item.minStock}</TableCell>
                                    <TableCell>
                                        <Badge className={item.status === "low" ? "bg-yellow-100 text-yellow-800" : "bg-green-100 text-green-800"}>
                                            {item.status === "low" ? "LOW STOCK" : "IN STOCK"}
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
