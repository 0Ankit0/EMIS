"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { toast } from "sonner";
import { getStudent, deleteStudent, activateStudent } from "@/services/studentService";
import { getEnrollments } from "@/services/enrollmentService";
import { getAcademicRecords } from "@/services/academicRecordService";
import type { Student, Enrollment, AcademicRecord } from "@/types/student";
import {
    ArrowLeft,
    Pencil,
    Trash2,
    Loader2,
    Mail,
    Phone,
    MapPin,
    Calendar,
    UserCheck,
    UserX,
    GraduationCap,
    FileText,
    Users,
    Award,
} from "lucide-react";
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

export default function StudentDetailPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = Number(params.id);

    const [student, setStudent] = useState<Student | null>(null);
    const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
    const [academicRecords, setAcademicRecords] = useState<AcademicRecord[]>([]);
    const [loading, setLoading] = useState(true);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

    useEffect(() => {
        if (studentId) {
            loadData();
        }
    }, [studentId]);

    const loadData = async () => {
        try {
            setLoading(true);
            const [studentData, enrollmentData, recordsData] = await Promise.all([
                getStudent(studentId),
                getEnrollments({ student: studentId }).catch(() => []),
                getAcademicRecords({ student: studentId }).catch(() => []),
            ]);
            setStudent(studentData);
            setEnrollments(enrollmentData);
            setAcademicRecords(recordsData);
        } catch (error: any) {
            toast.error(error.message || "Failed to load student details");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async () => {
        try {
            await deleteStudent(studentId);
            toast.success("Student deleted successfully");
            router.push("/students");
        } catch (error: any) {
            toast.error(error.message || "Failed to delete student");
        }
    };

    const handleToggleActive = async () => {
        if (!student) return;

        try {
            if (!student.is_active) {
                await activateStudent(studentId);
                toast.success("Student activated successfully");
            } else {
                // For deactivation, we'll use update with is_active: false
                toast.info("Deactivation feature coming soon");
            }
            loadData();
        } catch (error: any) {
            toast.error(error.message || "Failed to update student status");
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    if (!student) {
        return (
            <div className="space-y-6">
                <div className="text-center">
                    <h3 className="text-lg font-semibold">Student not found</h3>
                    <p className="text-sm text-muted-foreground">
                        The student you're looking for doesn't exist.
                    </p>
                    <Link href="/students">
                        <Button className="mt-4">Back to Students</Button>
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link href="/students">
                        <Button variant="ghost" size="sm">
                            <ArrowLeft className="h-4 w-4 mr-2" />
                            Back
                        </Button>
                    </Link>
                </div>
                <div className="flex gap-2">
                    <Button
                        variant="outline"
                        onClick={handleToggleActive}
                    >
                        {student.is_active ? (
                            <>
                                <UserX className="h-4 w-4 mr-2" />
                                Deactivate
                            </>
                        ) : (
                            <>
                                <UserCheck className="h-4 w-4 mr-2" />
                                Activate
                            </>
                        )}
                    </Button>
                    <Link href={`/students/${studentId}/edit`}>
                        <Button variant="outline">
                            <Pencil className="h-4 w-4 mr-2" />
                            Edit
                        </Button>
                    </Link>
                    <Button variant="destructive" onClick={() => setDeleteDialogOpen(true)}>
                        <Trash2 className="h-4 w-4 mr-2" />
                        Delete
                    </Button>
                </div>
            </div>

            {/* Student Info Header */}
            <Card>
                <CardHeader>
                    <div className="flex items-start justify-between">
                        <div>
                            <CardTitle className="text-3xl">
                                {student.first_name} {student.middle_name} {student.last_name}
                            </CardTitle>
                            <CardDescription className="text-base mt-2">
                                Reg. No: {student.registration_number} | Roll No: {student.roll_number}
                            </CardDescription>
                        </div>
                        {student.is_active ? (
                            <Badge variant="default" className="gap-1">
                                <UserCheck className="h-3 w-3" />
                                Active
                            </Badge>
                        ) : (
                            <Badge variant="secondary" className="gap-1">
                                <UserX className="h-3 w-3" />
                                Inactive
                            </Badge>
                        )}
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        <div className="flex items-center gap-3">
                            <Mail className="h-4 w-4 text-muted-foreground" />
                            <div>
                                <p className="text-sm text-muted-foreground">Email</p>
                                <p className="font-medium">{student.email}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <Phone className="h-4 w-4 text-muted-foreground" />
                            <div>
                                <p className="text-sm text-muted-foreground">Phone</p>
                                <p className="font-medium">{student.phone_number}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <Calendar className="h-4 w-4 text-muted-foreground" />
                            <div>
                                <p className="text-sm text-muted-foreground">Date of Birth</p>
                                <p className="font-medium">{new Date(student.date_of_birth).toLocaleDateString()}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <MapPin className="h-4 w-4 text-muted-foreground" />
                            <div>
                                <p className="text-sm text-muted-foreground">Location</p>
                                <p className="font-medium">
                                    {student.city}, {student.state}
                                </p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <Calendar className="h-4 w-4 text-muted-foreground" />
                            <div>
                                <p className="text-sm text-muted-foreground">Enrollment Date</p>
                                <p className="font-medium">{new Date(student.enrollment_date).toLocaleDateString()}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <MapPin className="h-4 w-4 text-muted-foreground" />
                            <div>
                                <p className="text-sm text-muted-foreground">Address</p>
                                <p className="font-medium">{student.address}</p>
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Quick Actions */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Link href={`/students/${studentId}/enrollments`}>
                    <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
                        <CardHeader className="pb-3">
                            <CardTitle className="text-base font-medium flex items-center gap-2">
                                <GraduationCap className="h-4 w-4" />
                                Enrollments
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-2xl font-bold">{enrollments.length}</p>
                        </CardContent>
                    </Card>
                </Link>

                <Link href={`/students/${studentId}/academic-records`}>
                    <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
                        <CardHeader className="pb-3">
                            <CardTitle className="text-base font-medium flex items-center gap-2">
                                <Award className="h-4 w-4" />
                                Academic Records
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-2xl font-bold">{academicRecords.length}</p>
                        </CardContent>
                    </Card>
                </Link>

                <Link href={`/students/${studentId}/results`}>
                    <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
                        <CardHeader className="pb-3">
                            <CardTitle className="text-base font-medium flex items-center gap-2">
                                <FileText className="h-4 w-4" />
                                Subject Results
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-2xl font-bold">View</p>
                        </CardContent>
                    </Card>
                </Link>

                <Link href={`/students/${studentId}/documents`}>
                    <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
                        <CardHeader className="pb-3">
                            <CardTitle className="text-base font-medium flex items-center gap-2">
                                <Users className="h-4 w-4" />
                                Documents
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-2xl font-bold">Manage</p>
                        </CardContent>
                    </Card>
                </Link>
            </div>

            {/* Recent Enrollments */}
            {enrollments.length > 0 && (
                <Card>
                    <CardHeader>
                        <CardTitle>Recent Enrollments</CardTitle>
                        <CardDescription>Latest program enrollments</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {enrollments.slice(0, 3).map((enrollment) => (
                                <div key={enrollment.id} className="flex items-center justify-between border-b pb-3 last:border-0">
                                    <div>
                                        <p className="font-medium">{enrollment.program}</p>
                                        <p className="text-sm text-muted-foreground">{enrollment.semester}</p>
                                    </div>
                                    <Badge>{enrollment.status}</Badge>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Delete Confirmation Dialog */}
            <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                        <AlertDialogDescription>
                            This will permanently delete {student.first_name} {student.last_name}'s record.
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
