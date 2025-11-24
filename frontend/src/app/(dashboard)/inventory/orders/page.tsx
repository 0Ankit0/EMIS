"use client";

import { ShoppingCart, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const ordersData = [
    { id: 1, number: "PO-001", supplier: "Office Supplies Co", items: 5, total: 1500, status: "Pending", date: "2025-01-23" },
    { id: 2, number: "PO-002", supplier: "Tech Vendors Inc", items: 2, total: 4500, status: "Approved", date: "2025-01-20" },
];

export default function PurchaseOrdersPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <ShoppingCart className="h-8 w-8 text-primary" />
                    Purchase Orders
                </h2>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Create Order
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Orders</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>PO Number</TableHead>
                                <TableHead>Supplier</TableHead>
                                <TableHead className="text-right">Items</TableHead>
                                <TableHead className="text-right">Total</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {ordersData.map((order) => (
                                <TableRow key={order.id}>
                                    <TableCell className="font-mono font-bold">{order.number}</TableCell>
                                    <TableCell>{order.supplier}</TableCell>
                                    <TableCell className="text-right">{order.items}</TableCell>
                                    <TableCell className="text-right">${order.total}</TableCell>
                                    <TableCell>{order.date}</TableCell>
                                    <TableCell>
                                        <Badge variant={order.status === "Approved" ? "default" : "secondary"}>
                                            {order.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm">View</Button>
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
