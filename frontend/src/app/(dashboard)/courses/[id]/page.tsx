"use client";

import Link from "next/link";
import { ArrowLeft, Edit, Trash, Info, FileText, List, Plus, Calendar, Star, BookOpen, CheckCircle, AlertCircle, File, Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

export default function CourseDetailPage({ params }: { params: { id: string } }) {
    // Mock data
    const course = {
        id: params.id,
        code: "CS101",
        title: "Introduction to Computer Science",
        credits: 4,
        department: "Computer Science",
        semester: "Fall 2025",
        academicYear: "2025-2026",
        status: "active",
        createdAt: "August 15, 2025",
        description: "This course provides a comprehensive introduction to the fundamental concepts of computer science. Topics include algorithms, data structures, software engineering, and the impact of computing on society.",
        syllabus: "Week 1: Introduction to Computing\nWeek 2: Algorithms and Flowcharts\nWeek 3: Programming Basics\nWeek 4: Data Structures\nWeek 5: Midterm Exam\nWeek 6: Software Engineering Principles\nWeek 7: Database Systems\nWeek 8: Web Development\nWeek 9: Artificial Intelligence Overview\nWeek 10: Final Project",
        modules: [
            { id: 1, title: "Module 1: Computing Basics", description: "History of computing and basic concepts." },
            { id: 2, title: "Module 2: Programming Fundamentals", description: "Variables, loops, and control structures." },
            { id: 3, title: "Module 3: Data Structures", description: "Arrays, lists, stacks, and queues." },
        ],
        assignments: [
            { id: 1, title: "Assignment 1: Hello World", dueDate: "Sep 15, 2025", maxScore: 10 },
            { id: 2, title: "Assignment 2: Calculator App", dueDate: "Oct 01, 2025", maxScore: 20 },
        ],
    };

    const getStatusBadge = (status: string) => {
        switch (status) {
            case "active":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Active</Badge>;
            case "draft":
                return <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-200 border-gray-200">Draft</Badge>;
            default:
                return <Badge variant="secondary">{status}</Badge>;
        }
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div className="flex items-center gap-4">
                    <Button variant="outline" size="icon" asChild>
                        <Link href="/courses">
                            <ArrowLeft className="h-4 w-4" />
                        </Link>
                    </Button>
                    <div>
                        <h2 className="text-3xl font-bold text-gray-800 mb-1">{course.title}</h2>
                        <div className="flex items-center gap-2 text-muted-foreground">
                            <span className="font-mono font-semibold">{course.code}</span>
                            <span>•</span>
                            <span>{course.credits} Credits</span>
                            <span>•</span>
                            <span>{course.department}</span>
                        </div>
                    </div>
                </div>
                <div className="flex gap-2">
                    <Button className="bg-blue-600 hover:bg-blue-700" asChild>
                        <Link href={`/courses/${course.id}/edit`}>
                            <Edit className="mr-2 h-4 w-4" /> Edit Course
                        </Link>
                    </Button>
                    <Button variant="destructive">
                        <Trash className="mr-2 h-4 w-4" /> Delete
                    </Button>
                </div>
            </div>

            {/* Status Banner */}
            <div className={`p-4 rounded-lg border-l-4 flex items-center gap-3 ${course.status === 'active' ? 'bg-green-50 border-green-500 text-green-700' : 'bg-gray-50 border-gray-500 text-gray-700'
                }`}>
                {course.status === 'active' ? <CheckCircle className="h-5 w-5" /> : <AlertCircle className="h-5 w-5" />}
                <p><span className="font-semibold">Status:</span> {course.status.charAt(0).toUpperCase() + course.status.slice(1)}</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Content */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Description */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Info className="h-5 w-5 text-primary" />
                                Description
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-gray-700 leading-relaxed">{course.description}</p>
                        </CardContent>
                    </Card>

                    {/* Syllabus */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <FileText className="h-5 w-5 text-primary" />
                                Syllabus
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="whitespace-pre-line text-gray-700 leading-relaxed">
                                {course.syllabus}
                            </div>
                        </CardContent>
                    </Card>

                    {/* Modules */}
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between">
                            <CardTitle className="flex items-center gap-2">
                                <List className="h-5 w-5 text-primary" />
                                Course Modules
                            </CardTitle>
                            <Button size="sm" asChild>
                                <Link href={`/courses/${course.id}/modules/new`}>
                                    <Plus className="mr-2 h-4 w-4" /> Add Module
                                </Link>
                            </Button>
                        </CardHeader>
                        <CardContent>
                            {course.modules.length > 0 ? (
                                <div className="space-y-3">
                                    {course.modules.map((module, index) => (
                                        <div key={module.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                                            <div className="flex items-center gap-4">
                                                <div className="w-8 h-8 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-semibold flex-shrink-0">
                                                    {index + 1}
                                                </div>
                                                <div>
                                                    <h4 className="font-semibold text-gray-800">{module.title}</h4>
                                                    <p className="text-sm text-gray-600">{module.description}</p>
                                                </div>
                                            </div>
                                            <div className="flex gap-2">
                                                <Button variant="ghost" size="icon" asChild>
                                                    <Link href={`/courses/${course.id}/modules/${module.id}`}>
                                                        <Eye className="h-4 w-4" />
                                                    </Link>
                                                </Button>
                                                <Button variant="ghost" size="icon" asChild>
                                                    <Link href={`/courses/${course.id}/modules/${module.id}/edit`}>
                                                        <Edit className="h-4 w-4" />
                                                    </Link>
                                                </Button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-center text-muted-foreground py-8">No modules added yet.</p>
                            )}
                        </CardContent>
                    </Card>

                    {/* Assignments */}
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between">
                            <CardTitle className="flex items-center gap-2">
                                <File className="h-5 w-5 text-primary" />
                                Assignments
                            </CardTitle>
                            <Button size="sm" asChild>
                                <Link href={`/courses/${course.id}/assignments/new`}>
                                    <Plus className="mr-2 h-4 w-4" /> Add Assignment
                                </Link>
                            </Button>
                        </CardHeader>
                        <CardContent>
                            {course.assignments.length > 0 ? (
                                <div className="space-y-3">
                                    {course.assignments.map((assignment) => (
                                        <div key={assignment.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                                            <div>
                                                <h4 className="font-semibold text-gray-800">{assignment.title}</h4>
                                                <div className="flex items-center gap-4 mt-1 text-sm text-gray-600">
                                                    <span className="flex items-center gap-1">
                                                        <Calendar className="h-3 w-3" /> Due: {assignment.dueDate}
                                                    </span>
                                                    <span className="flex items-center gap-1">
                                                        <Star className="h-3 w-3" /> {assignment.maxScore} points
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="flex gap-2">
                                                <Button variant="ghost" size="icon" asChild>
                                                    <Link href={`/courses/${course.id}/assignments/${assignment.id}`}>
                                                        <Eye className="h-4 w-4" />
                                                    </Link>
                                                </Button>
                                                <Button variant="ghost" size="icon" asChild>
                                                    <Link href={`/courses/${course.id}/assignments/${assignment.id}/edit`}>
                                                        <Edit className="h-4 w-4" />
                                                    </Link>
                                                </Button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-center text-muted-foreground py-8">No assignments created yet.</p>
                            )}
                        </CardContent>
                    </Card>
                </div>

                {/* Sidebar Info */}
                <div className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-lg">Course Details</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div>
                                <p className="text-sm text-muted-foreground mb-1">Course Code</p>
                                <p className="font-semibold">{course.code}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground mb-1">Credits</p>
                                <p className="font-semibold">{course.credits}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground mb-1">Department</p>
                                <p className="font-semibold">{course.department}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground mb-1">Semester</p>
                                <p className="font-semibold">{course.semester}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground mb-1">Academic Year</p>
                                <p className="font-semibold">{course.academicYear}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground mb-1">Created</p>
                                <p className="font-semibold">{course.createdAt}</p>
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-lg">Quick Actions</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            <Button variant="outline" className="w-full justify-start" asChild>
                                <Link href={`/courses/${course.id}/modules`}>
                                    <List className="mr-2 h-4 w-4" /> Manage Modules
                                </Link>
                            </Button>
                            <Button variant="outline" className="w-full justify-start" asChild>
                                <Link href={`/courses/${course.id}/assignments`}>
                                    <File className="mr-2 h-4 w-4" /> Manage Assignments
                                </Link>
                            </Button>
                            <Button variant="outline" className="w-full justify-start" asChild>
                                <Link href={`/courses/${course.id}/enrollments`}>
                                    <BookOpen className="mr-2 h-4 w-4" /> View Enrollments
                                </Link>
                            </Button>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
