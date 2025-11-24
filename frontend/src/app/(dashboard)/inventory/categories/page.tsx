"use client";

import { Package, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import Link from "next/link";

const categoriesData = [
    { id: 1, name: "Electronics", items: 25, value: 125000 },
    { id: 2, name: "Furniture", items: 40, value: 80000 },
    { id: 3, name: "Stationery", items: 150, value: 15000 },
];

export default function InventoryCategoriesPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Package className="h-8 w-8 text-primary" />
                        Inventory Categories
                    </h2>
                </div>
                <Link href="/inventory/categories/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Category
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Categories</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Category Name</TableHead>
                                <TableHead className="text-right">Items</TableHead>
                                <TableHead className="text-right">Total Value</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {categoriesData.map((cat) => (
                                <TableRow key={cat.id}>
                                    <TableCell className="font-semibold">{cat.name}</TableCell>
                                    <TableCell className="text-right">{cat.items}</TableCell>
                                    <TableCell className="text-right font-bold">${cat.value.toLocaleString()}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
