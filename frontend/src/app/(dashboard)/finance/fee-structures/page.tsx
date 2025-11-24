"use client";

import { CreditCard, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const feeStructures = [
    { id: 1, name: "Grade 10 - Annual", amount: 5000, frequency: "Yearly", type: "Tuition" },
    { id: 2, name: "Transport - Zone A", amount: 500, frequency: "Monthly", type: "Transport" },
    { id: 3, name: "Lab Fee - Science", amount: 200, frequency: "Termly", type: "Laboratory" },
];

export default function FeeStructuresPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <CreditCard className="h-8 w-8 text-primary" />
                    Fee Structures
                </h2>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Structure
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Active Fee Structures</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Frequency</TableHead>
                                <TableHead className="text-right">Amount</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {feeStructures.map((fee) => (
                                <TableRow key={fee.id}>
                                    <TableCell className="font-semibold">{fee.name}</TableCell>
                                    <TableCell>{fee.type}</TableCell>
                                    <TableCell>{fee.frequency}</TableCell>
                                    <TableCell className="text-right font-mono">${fee.amount}</TableCell>
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
