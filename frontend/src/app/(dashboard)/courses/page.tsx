"use client";

import Link from "next/link";
import { BookOpen, Plus, Search, Filter, Eye, Edit, List, Trash } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

// Mock data
const courses = [
    {
        id: 1,
        code: "CS101",
        title: "Introduction to Computer Science",
        department: "Computer Science",
        credits: 4,
        status: "active",
        description: "Fundamental concepts of computing...",
    },
    {
        id: 2,
        code: "PHY201",
        title: "Advanced Physics",
        department: "Physics",
        credits: 3,
        status: "active",
        description: "Study of matter and energy...",
    },
    {
        id: 3,
        code: "HIS105",
        title: "World History",
        department: "History",
        credits: 3,
        status: "draft",
        description: "Overview of major historical events...",
    },
    {
        id: 4,
        code: "MATH301",
        title: "Calculus III",
        department: "Mathematics",
        credits: 4,
        status: "archived",
        description: "Multivariable calculus...",
    },
];

export default function CourseListPage() {
    const getStatusBadge = (status: string) => {
        switch (status) {
            case "active":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Active</Badge>;
            case "draft":
                return <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-200 border-gray-200">Draft</Badge>;
            case "archived":
                return <Badge className="bg-red-100 text-red-800 hover:bg-red-200 border-red-200">Archived</Badge>;
            default:
                return <Badge variant="secondary">{status}</Badge>;
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <BookOpen className="h-8 w-8 text-primary" />
                        All Courses
                    </h2>
                    <p className="text-muted-foreground">Manage and view all courses in the system</p>
                </div>
                <Button asChild className="bg-blue-600 hover:bg-blue-700">
                    <Link href="/courses/new">
                        <Plus className="mr-2 h-4 w-4" /> Add New Course
                    </Link>
                </Button>
            </div>

            {/* Filters */}
            <Card>
                <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="relative md:col-span-2">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input placeholder="Search courses..." className="pl-10" />
                        </div>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="All Status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Status</SelectItem>
                                <SelectItem value="active">Active</SelectItem>
                                <SelectItem value="draft">Draft</SelectItem>
                                <SelectItem value="archived">Archived</SelectItem>
                            </SelectContent>
                        </Select>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="All Departments" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Departments</SelectItem>
                                <SelectItem value="cs">Computer Science</SelectItem>
                                <SelectItem value="physics">Physics</SelectItem>
                                <SelectItem value="history">History</SelectItem>
                                <SelectItem value="math">Mathematics</SelectItem>
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
                            <TableHead>Title</TableHead>
                            <TableHead>Department</TableHead>
                            <TableHead className="text-center">Credits</TableHead>
                            <TableHead className="text-center">Status</TableHead>
                            <TableHead className="text-center">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {courses.map((course) => (
                            <TableRow key={course.id}>
                                <TableCell className="font-mono font-semibold">{course.code}</TableCell>
                                <TableCell>
                                    <div className="font-semibold">{course.title}</div>
                                    <div className="text-xs text-muted-foreground truncate max-w-[200px]">{course.description}</div>
                                </TableCell>
                                <TableCell>{course.department}</TableCell>
                                <TableCell className="text-center">
                                    <span className="inline-flex items-center justify-center w-8 h-8 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                                        {course.credits}
                                    </span>
                                </TableCell>
                                <TableCell className="text-center">{getStatusBadge(course.status)}</TableCell>
                                <TableCell className="text-center">
                                    <div className="flex justify-center space-x-2">
                                        <Button asChild variant="ghost" size="icon" className="text-blue-600 hover:text-blue-800 hover:bg-blue-50">
                                            <Link href={`/courses/${course.id}`}>
                                                <Eye className="h-4 w-4" />
                                            </Link>
                                        </Button>
                                        <Button asChild variant="ghost" size="icon" className="text-yellow-600 hover:text-yellow-800 hover:bg-yellow-50">
                                            <Link href={`/courses/${course.id}/edit`}>
                                                <Edit className="h-4 w-4" />
                                            </Link>
                                        </Button>
                                        <Button asChild variant="ghost" size="icon" className="text-gray-600 hover:text-gray-800 hover:bg-gray-50">
                                            <Link href={`/courses/${course.id}/modules`}>
                                                <List className="h-4 w-4" />
                                            </Link>
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
