"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { toast } from "sonner";
import { getAcademicRecords, deleteAcademicRecord } from "@/services/academicRecordService";
import { getStudent } from "@/services/studentService";
import type { AcademicRecord, Student } from "@/types/student";
import { ArrowLeft, Plus, Pencil, Trash2, Loader2, TrendingUp } from "lucide-react";
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

export default function AcademicRecordsPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = Number(params.id);

    const [student, setStudent] = useState<Student | null>(null);
    const [records, setRecords] = useState<AcademicRecord[]>([]);
    const [loading, setLoading] = useState(true);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [recordToDelete, setRecordToDelete] = useState<AcademicRecord | null>(null);

    useEffect(() => {
        if (studentId) {
            loadData();
        }
    }, [studentId]);

    const loadData = async () => {
        try {
            setLoading(true);
            const [studentData, recordsData] = await Promise.all([
                getStudent(studentId),
                getAcademicRecords({ student: studentId }),
            ]);
            setStudent(studentData);
            setRecords(recordsData);
        } catch (error: any) {
            toast.error(error.message || "Failed to load data");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!recordToDelete) return;

        try {
            await deleteAcademicRecord(recordToDelete.id);
            toast.success("Academic record deleted successfully");
            loadData();
        } catch (error: any) {
            toast.error(error.message || "Failed to delete academic record");
        } finally {
            setDeleteDialogOpen(false);
            setRecordToDelete(null);
        }
    };

    const calculateCumulativeGPA = () => {
        if (records.length === 0) return "N/A";
        const total = records.reduce((sum, record) => sum + parseFloat(record.gpa), 0);
        return (total / records.length).toFixed(2);
    };

    const getTotalCredits = () => {
        return records.reduce((sum, record) => sum + record.total_credits, 0);
    };

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
                        <h3 className="text-2xl font-bold tracking-tight">Academic Records</h3>
                        {student && (
                            <p className="text-sm text-muted-foreground">
                                {student.first_name} {student.last_name}
                            </p>
                        )}
                    </div>
                </div>
                <Link href={`/students/${studentId}/academic-records/new`}>
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Record
                    </Button>
                </Link>
            </div>

            {/* Summary Cards */}
            <div className="grid gap-4 md:grid-cols-3">
                <Card>
                    <CardHeader className="pb-3">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            Cumulative GPA
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center gap-2">
                            <TrendingUp className="h-4 w-4 text-primary" />
                            <p className="text-3xl font-bold">{calculateCumulativeGPA()}</p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="pb-3">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            Total Credits
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-3xl font-bold">{getTotalCredits()}</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="pb-3">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            Semesters Completed
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-3xl font-bold">{records.length}</p>
                    </CardContent>
                </Card>
            </div>

            {/* Records Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Semester Records</CardTitle>
                    <CardDescription>Academic performance by semester</CardDescription>
                </CardHeader>
                <CardContent className="p-0">
                    {records.length === 0 ? (
                        <div className="flex flex-col items-center justify-center p-12 text-center">
                            <h3 className="text-lg font-semibold">No academic records found</h3>
                            <p className="text-sm text-muted-foreground mb-4">
                                Start adding academic records for each semester
                            </p>
                            <Link href={`/students/${studentId}/academic-records/new`}>
                                <Button>
                                    <Plus className="mr-2 h-4 w-4" />
                                    Add First Record
                                </Button>
                            </Link>
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Semester</TableHead>
                                    <TableHead>GPA</TableHead>
                                    <TableHead>Total Credits</TableHead>
                                    <TableHead>Remarks</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {records.map((record) => (
                                    <TableRow key={record.id}>
                                        <TableCell className="font-medium">{record.semester}</TableCell>
                                        <TableCell>
                                            <span className="font-mono text-lg">{record.gpa}</span>
                                        </TableCell>
                                        <TableCell>{record.total_credits}</TableCell>
                                        <TableCell className="max-w-xs truncate">
                                            {record.remarks || "—"}
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() =>
                                                        router.push(`/students/${studentId}/academic-records/${record.id}/edit`)
                                                    }
                                                >
                                                    <Pencil className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => {
                                                        setRecordToDelete(record);
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
                    )}
                </CardContent>
            </Card>

            {/* Delete Confirmation Dialog */}
            <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                        <AlertDialogDescription>
                            This will delete the academic record for{" "}
                            <strong>{recordToDelete?.semester}</strong>.
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
