"use client";

import { Truck, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const suppliersData = [
    { id: 1, name: "Tech Supplies Co.", contact: "John Doe", phone: "+1234567890", email: "john@techsupplies.com" },
    { id: 2, name: "Office Mart", contact: "Jane Smith", phone: "+1234567891", email: "jane@officemart.com" },
];

export default function InventorySuppliersPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Truck className="h-8 w-8 text-primary" />
                        Suppliers
                    </h2>
                </div>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Supplier
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Suppliers</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Company Name</TableHead>
                                <TableHead>Contact Person</TableHead>
                                <TableHead>Phone</TableHead>
                                <TableHead>Email</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {suppliersData.map((supplier) => (
                                <TableRow key={supplier.id}>
                                    <TableCell className="font-semibold">{supplier.name}</TableCell>
                                    <TableCell>{supplier.contact}</TableCell>
                                    <TableCell>{supplier.phone}</TableCell>
                                    <TableCell>{supplier.email}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
