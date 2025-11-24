"use client";

import Link from "next/link";
import { Menu, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const menusData = [
    { id: 1, name: "Main Menu", location: "Primary", items: 5 },
    { id: 2, name: "Footer Menu", location: "Footer", items: 3 },
    { id: 3, name: "Sidebar Menu", location: "Sidebar", items: 7 },
];

export default function MenusPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Menu className="h-8 w-8 text-primary" />
                        Menus
                    </h2>
                    <p className="text-muted-foreground">Manage navigation menus</p>
                </div>
                <Link href="/cms/menus/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Create Menu
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Menus</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Menu Name</TableHead>
                                <TableHead>Location</TableHead>
                                <TableHead className="text-right">Items</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {menusData.map((menu) => (
                                <TableRow key={menu.id}>
                                    <TableCell className="font-semibold">{menu.name}</TableCell>
                                    <TableCell>{menu.location}</TableCell>
                                    <TableCell className="text-right">{menu.items}</TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Link href={`/cms/menus/${menu.id}`}>
                                            <Button variant="outline" size="sm">Edit</Button>
                                        </Link>
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
