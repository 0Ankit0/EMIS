"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { toast } from "sonner";
import { getSubjectResults, deleteSubjectResult } from "@/services/subjectResultService";
import { getStudent } from "@/services/studentService";
import type { SubjectResult, Student } from "@/types/student";
import { ArrowLeft, Plus, Pencil, Trash2, Loader2, Upload, Filter } from "lucide-react";
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from "@/components/ui/alert-dialog";

export default function SubjectResultsPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = Number(params.id);

    const [student, setStudent] = useState<Student | null>(null);
    const [results, setResults] = useState<SubjectResult[]>([]);
    const [loading, setLoading] = useState(true);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [resultToDelete, setResultToDelete] = useState<SubjectResult | null>(null);
    const [semesterFilter, setSemesterFilter] = useState<string>("all");

    useEffect(() => {
        if (studentId) {
            loadData();
        }
    }, [studentId]);

    const loadData = async () => {
        try {
            setLoading(true);
            const [studentData, resultsData] = await Promise.all([
                getStudent(studentId),
                getSubjectResults({ student: studentId }),
            ]);
            setStudent(studentData);
            setResults(resultsData);
        } catch (error: any) {
            toast.error(error.message || "Failed to load data");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!resultToDelete) return;

        try {
            await deleteSubjectResult(resultToDelete.id);
            toast.success("Subject result deleted successfully");
            loadData();
        } catch (error: any) {
            toast.error(error.message || "Failed to delete subject result");
        } finally {
            setDeleteDialogOpen(false);
            setResultToDelete(null);
        }
    };

    const getGradeColor = (grade?: string) => {
        if (!grade) return "secondary";
        if (["A+", "A"].includes(grade)) return "default";
        if (["B+", "B"].includes(grade)) return "default";
        if (["C+", "C"].includes(grade)) return "secondary";
        if (grade === "D") return "secondary";
        if (grade === "F") return "destructive";
        return "secondary";
    };

    const uniqueSemesters = Array.from(new Set(results.map(r => r.semester)));

    const filteredResults = results.filter(result =>
        semesterFilter === "all" || result.semester === semesterFilter
    );

    const groupedResults = filteredResults.reduce((acc, result) => {
        const sem = result.semester;
        if (!acc[sem]) acc[sem] = [];
        acc[sem].push(result);
        return acc;
    }, {} as Record<string, SubjectResult[]>);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link href={`/students/${studentId}`}>
                        <Button variant="ghost" size="sm">
                            <ArrowLeft className="h-4 w-4 mr-2" />
                            Back to Student
                        </Button>
                    </Link>
                    <div>
                        <h3 className="text-2xl font-bold tracking-tight">Subject Results</h3>
                        {student && (
                            <p className="text-sm text-muted-foreground">
                                {student.first_name} {student.last_name}
                            </p>
                        )}
                    </div>
                </div>
                <div className="flex gap-2">
                    <Link href={`/students/${studentId}/results/import`}>
                        <Button variant="outline">
                            <Upload className="mr-2 h-4 w-4" />
                            Import from Excel
                        </Button>
                    </Link>
                    <Link href={`/students/${studentId}/results/new`}>
                        <Button>
                            <Plus className="mr-2 h-4 w-4" />
                            Add Result
                        </Button>
                    </Link>
                </div>
            </div>

            {/* Filters */}
            <Card>
                <CardContent className="pt-6">
                    <div className="flex items-center gap-4">
                        <Filter className="h-4 w-4 text-muted-foreground" />
                        <Select value={semesterFilter} onValueChange={setSemesterFilter}>
                            <SelectTrigger className="w-[200px]">
                                <SelectValue placeholder="Filter by semester" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Semesters</SelectItem>
                                {uniqueSemesters.map((semester) => (
                                    <SelectItem key={semester} value={semester}>
                                        {semester}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>

            {/* Results by Semester */}
            {results.length === 0 ? (
                <Card>
                    <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                        <h3 className="text-lg font-semibold">No subject results found</h3>
                        <p className="text-sm text-muted-foreground mb-4">
                            Start adding subject results or import from Excel
                        </p>
                        <div className="flex gap-2">
                            <Link href={`/students/${studentId}/results/import`}>
                                <Button variant="outline">
                                    <Upload className="mr-2 h-4 w-4" />
                                    Import from Excel
                                </Button>
                            </Link>
                            <Link href={`/students/${studentId}/results/new`}>
                                <Button>
                                    <Plus className="mr-2 h-4 w-4" />
                                    Add Result
                                </Button>
                            </Link>
                        </div>
                    </CardContent>
                </Card>
            ) : (
                Object.entries(groupedResults).map(([semester, semesterResults]) => (
                    <Card key={semester}>
                        <CardHeader>
                            <CardTitle>{semester}</CardTitle>
                            <CardDescription>{semesterResults.length} subjects</CardDescription>
                        </CardHeader>
                        <CardContent className="p-0">
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Subject</TableHead>
                                        <TableHead>Marks</TableHead>
                                        <TableHead>Grade</TableHead>
                                        <TableHead>Credits</TableHead>
                                        <TableHead>Attempt</TableHead>
                                        <TableHead className="text-right">Actions</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {semesterResults.map((result) => (
                                        <TableRow key={result.id}>
                                            <TableCell className="font-medium">{result.subject_name}</TableCell>
                                            <TableCell>
                                                {result.marks_obtained && result.maximum_marks ? (
                                                    <span className="font-mono">
                                                        {result.marks_obtained}/{result.maximum_marks}
                                                    </span>
                                                ) : (
                                                    "—"
                                                )}
                                            </TableCell>
                                            <TableCell>
                                                {result.grade ? (
                                                    <Badge variant={getGradeColor(result.grade)}>
                                                        {result.grade}
                                                    </Badge>
                                                ) : (
                                                    "—"
                                                )}
                                            </TableCell>
                                            <TableCell>{result.credit_hours}</TableCell>
                                            <TableCell>
                                                <Badge variant="outline">
                                                    {result.attempt_type === "regular" ? "Regular" : "Re-exam"}
                                                </Badge>
                                            </TableCell>
                                            <TableCell className="text-right">
                                                <div className="flex justify-end gap-2">
                                                    <Button
                                                        variant="ghost"
                                                        size="sm"
                                                        onClick={() =>
                                                            router.push(`/students/${studentId}/results/${result.id}/edit`)
                                                        }
                                                    >
                                                        <Pencil className="h-4 w-4" />
                                                    </Button>
                                                    <Button
                                                        variant="ghost"
                                                        size="sm"
                                                        onClick={() => {
                                                            setResultToDelete(result);
                                                            setDeleteDialogOpen(true);
                                                        }}
                                                    >
                                                        <Trash2 className="h-4 w-4 text-destructive" />
                                                    </Button>
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                ))
            )}

            {/* Delete Confirmation Dialog */}
            <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                        <AlertDialogDescription>
                            This will delete the result for{" "}
                            <strong>{resultToDelete?.subject_name}</strong>.
                            This action cannot be undone.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction
                            onClick={handleDelete}
                            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                        >
                            Delete
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </div>
    );
}
