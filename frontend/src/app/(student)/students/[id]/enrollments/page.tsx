"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { toast } from "sonner";
import { getEnrollments, deleteEnrollment } from "@/services/enrollmentService";
import { getStudent } from "@/services/studentService";
import type { Enrollment, Student } from "@/types/student";
import { ArrowLeft, Plus, Pencil, Trash2, Loader2 } from "lucide-react";
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

export default function EnrollmentsPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = params.id as string;

    const [student, setStudent] = useState<Student | null>(null);
    const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
    const [loading, setLoading] = useState(true);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [enrollmentToDelete, setEnrollmentToDelete] = useState<Enrollment | null>(null);

    useEffect(() => {
        if (studentId) {
            loadData();
        }
    }, [studentId]);

    const loadData = async () => {
        try {
            setLoading(true);
            const [studentData, enrollmentData] = await Promise.all([
                getStudent(studentId),
                getEnrollments({ student: studentId }),
            ]);
            setStudent(studentData);
            setEnrollments(enrollmentData);
        } catch (error: any) {
            toast.error(error.message || "Failed to load data");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!enrollmentToDelete) return;

        try {
            await deleteEnrollment(enrollmentToDelete.id);
            toast.success("Enrollment deleted successfully");
            loadData();
        } catch (error: any) {
            toast.error(error.message || "Failed to delete enrollment");
        } finally {
            setDeleteDialogOpen(false);
            setEnrollmentToDelete(null);
        }
    };

    const getStatusVariant = (status: string) => {
        switch (status) {
            case "enrolled":
                return "default";
            case "completed":
                return "default";
            case "dropped":
                return "destructive";
            case "repeated":
                return "secondary";
            default:
                return "secondary";
        }
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
                        <h3 className="text-2xl font-bold tracking-tight">Enrollments</h3>
                        {student && (
                            <p className="text-sm text-muted-foreground">
                                {student.first_name} {student.last_name}
                            </p>
                        )}
                    </div>
                </div>
                <Link href={`/students/${studentId}/enrollments/new`}>
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Enrollment
                    </Button>
                </Link>
            </div>

            {/* Enrollments Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Program Enrollments</CardTitle>
                    <CardDescription>All program enrollments for this student</CardDescription>
                </CardHeader>
                <CardContent className="p-0">
                    {enrollments.length === 0 ? (
                        <div className="flex flex-col items-center justify-center p-12 text-center">
                            <h3 className="text-lg font-semibold">No enrollments found</h3>
                            <p className="text-sm text-muted-foreground mb-4">
                                This student has no program enrollments yet
                            </p>
                            <Link href={`/students/${studentId}/enrollments/new`}>
                                <Button>
                                    <Plus className="mr-2 h-4 w-4" />
                                    Add First Enrollment
                                </Button>
                            </Link>
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Program</TableHead>
                                    <TableHead>Semester</TableHead>
                                    <TableHead>Enrollment Date</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {enrollments.map((enrollment) => (
                                    <TableRow key={enrollment.id}>
                                        <TableCell className="font-medium">{enrollment.program}</TableCell>
                                        <TableCell>{enrollment.semester}</TableCell>
                                        <TableCell>{new Date(enrollment.enrollment_date).toLocaleDateString()}</TableCell>
                                        <TableCell>
                                            <Badge variant={getStatusVariant(enrollment.status)}>
                                                {enrollment.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() =>
                                                        router.push(`/students/${studentId}/enrollments/${enrollment.id}/edit`)
                                                    }
                                                >
                                                    <Pencil className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => {
                                                        setEnrollmentToDelete(enrollment);
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
                            This will delete the enrollment for{" "}
                            <strong>{enrollmentToDelete?.program}</strong> ({enrollmentToDelete?.semester}).
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
