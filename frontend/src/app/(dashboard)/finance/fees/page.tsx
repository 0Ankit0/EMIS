"use client";

import Link from "next/link";
import { Plus, Search, Filter, Eye, Edit, Trash, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

// Mock data based on FeeStructure model
const feeStructures = [
    {
        id: 1,
        code: "FEE-BSCS-2025",
        name: "BS Computer Science - Fall 2025",
        program: "BS Computer Science",
        academicYear: "2025-2026",
        semester: "Fall",
        totalAmount: "$5,500",
        isActive: true,
        components: { tuition: 5000, lab: 400, library: 100 },
    },
    {
        id: 2,
        code: "FEE-BBA-2025",
        name: "BBA - Fall 2025",
        program: "BBA",
        academicYear: "2025-2026",
        semester: "Fall",
        totalAmount: "$4,800",
        isActive: true,
        components: { tuition: 4500, library: 300 },
    },
    {
        id: 3,
        code: "FEE-BSCS-2024",
        name: "BS Computer Science - Spring 2025",
        program: "BS Computer Science",
        academicYear: "2024-2025",
        semester: "Spring",
        totalAmount: "$5,200",
        isActive: false,
        components: { tuition: 4800, lab: 300, library: 100 },
    },
];

export default function FeeManagementPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <FileText className="h-8 w-8 text-primary" />
                        Fee Structures
                    </h2>
                    <p className="text-muted-foreground">Manage fee templates for programs</p>
                </div>
                <Button asChild className="bg-blue-600 hover:bg-blue-700">
                    <Link href="/finance/fees/new">
                        <Plus className="mr-2 h-4 w-4" /> Create Fee Structure
                    </Link>
                </Button>
            </div>

            {/* Filters */}
            <Card>
                <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="relative md:col-span-2">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search fee structures..." className="pl-10" />
                        </div>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="All Programs" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Programs</SelectItem>
                                <SelectItem value="bscs">BS Computer Science</SelectItem>
                                <SelectItem value="bba">BBA</SelectItem>
                            </SelectContent>
                        </Select>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="Status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Status</SelectItem>
                                <SelectItem value="active">Active</SelectItem>
                                <SelectItem value="inactive">Inactive</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>

            {/* Table */}
            <Card className="overflow-hidden">
                <Table>
                    <TableHeader className="bg-gray-50">
                        <TableRow>
                            <TableHead>Code</TableHead>
                            <TableHead>Name</TableHead>
                            <TableHead>Program</TableHead>
                            <TableHead>Semester</TableHead>
                            <TableHead className="text-right">Total Amount</TableHead>
                            <TableHead className="text-center">Status</TableHead>
                            <TableHead className="text-center">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {feeStructures.map((fee) => (
                            <TableRow key={fee.id}>
                                <TableCell className="font-mono font-semibold">{fee.code}</TableCell>
                                <TableCell>
                                    <div className="font-medium">{fee.name}</div>
                                    <div className="text-xs text-muted-foreground">{fee.academicYear}</div>
                                </TableCell>
                                <TableCell>{fee.program}</TableCell>
                                <TableCell>{fee.semester}</TableCell>
                                <TableCell className="text-right font-bold">{fee.totalAmount}</TableCell>
                                <TableCell className="text-center">
                                    {fee.isActive ? (
                                        <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Active</Badge>
                                    ) : (
                                        <Badge variant="secondary">Inactive</Badge>
                                    )}
                                </TableCell>
                                <TableCell className="text-center">
                                    <div className="flex justify-center space-x-2">
                                        <Button variant="ghost" size="icon" className="text-blue-600 hover:text-blue-800 hover:bg-blue-50">
                                            <Eye className="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="icon" className="text-yellow-600 hover:text-yellow-800 hover:bg-yellow-50">
                                            <Edit className="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="icon" className="text-red-600 hover:text-red-800 hover:bg-red-50">
                                            <Trash className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Card>
        </div>
    );
}
