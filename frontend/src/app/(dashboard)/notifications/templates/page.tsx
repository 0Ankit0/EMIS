"use client";

import { Bell, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const templatesData = [
    { id: 1, name: "Welcome Email", type: "Email", usage: 450 },
    { id: 2, name: "Fee Reminder", type: "SMS", usage: 320 },
    { id: 3, name: "Event Notification", type: "Push", usage: 180 },
];

export default function NotificationTemplatesPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <Bell className="h-8 w-8 text-primary" />
                        Notification Templates
                    </h2>
                </div>
                <Button>Create Template</Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Templates</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Template Name</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead className="text-right">Usage Count</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {templatesData.map((template) => (
                                <TableRow key={template.id}>
                                    <TableCell className="font-semibold">{template.name}</TableCell>
                                    <TableCell>{template.type}</TableCell>
                                    <TableCell className="text-right">{template.usage}</TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="outline" size="sm">Edit</Button>
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
