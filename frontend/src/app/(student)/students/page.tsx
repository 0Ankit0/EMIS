"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
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
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { getStudents, deleteStudent } from "@/services/studentService";
import type { Student } from "@/types/student";
import { Search, Plus, Eye, Pencil, Trash2, Loader2, UserX, UserCheck, FileUp } from "lucide-react";
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
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { uploadDocument } from "@/services/documentService";
import { DOCUMENT_TYPE_OPTIONS } from "@/types/student";

export default function StudentsPage() {
    const router = useRouter();
    const [students, setStudents] = useState<Student[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");
    const [statusFilter, setStatusFilter] = useState<string>("all");
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [studentToDelete, setStudentToDelete] = useState<Student | null>(null);
    const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
    const [studentForUpload, setStudentForUpload] = useState<Student | null>(null);
    const [uploadFile, setUploadFile] = useState<File | null>(null);
    const [documentType, setDocumentType] = useState<string>("");
    const [uploading, setUploading] = useState(false);

    useEffect(() => {
        loadStudents();
    }, []);

    const loadStudents = async () => {
        try {
            setLoading(true);
            const data = await getStudents();
            setStudents(data);
        } catch (error: any) {
            toast.error(error.message || "Failed to load students");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!studentToDelete) return;

        try {
            await deleteStudent(studentToDelete.ukid);
            toast.success("Student deleted successfully");
            loadStudents();
        } catch (error: any) {
            toast.error(error.message || "Failed to delete student");
        } finally {
            setDeleteDialogOpen(false);
            setStudentToDelete(null);
        }
    };

    const handleUploadDocument = async () => {
        if (!studentForUpload || !uploadFile || !documentType) return;

        try {
            setUploading(true);
            await uploadDocument({
                student: studentForUpload.ukid,
                document_type: documentType as any,
                file: uploadFile,
            });
            toast.success("Document uploaded successfully");
            setUploadDialogOpen(false);
            setStudentForUpload(null);
            setUploadFile(null);
            setDocumentType("");
        } catch (error: any) {
            toast.error(error.message || "Failed to upload document");
        } finally {
            setUploading(false);
        }
    };

    const filteredStudents = students.filter((student) => {
        const matchesSearch =
            searchQuery === "" ||
            student.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            student.last_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            student.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
            (student.registration_number?.toString() || "").includes(searchQuery) ||
            (student.roll_number?.toLowerCase() || "").includes(searchQuery.toLowerCase());

        const matchesStatus =
            statusFilter === "all" ||
            (statusFilter === "active" && student.is_active) ||
            (statusFilter === "inactive" && !student.is_active);

        return matchesSearch && matchesStatus;
    });

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-2xl font-bold tracking-tight">Students</h3>
                    <p className="text-sm text-muted-foreground">
                        Manage student information and records
                    </p>
                </div>
                <Link href="/students/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Add Student
                    </Button>
                </Link>
            </div>

            {/* Filters */}
            <Card>
                <CardHeader>
                    <CardTitle>Filters</CardTitle>
                    <CardDescription>Search and filter students</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="grid gap-4 md:grid-cols-2">
                        <div className="relative">
                            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search by name, email, registration number..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-9"
                            />
                        </div>
                        <Select value={statusFilter} onValueChange={setStatusFilter}>
                            <SelectTrigger>
                                <SelectValue placeholder="Filter by status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Students</SelectItem>
                                <SelectItem value="active">Active Only</SelectItem>
                                <SelectItem value="inactive">Inactive Only</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>

            {/* Students Table */}
            <Card>
                <CardContent className="p-0">
                    {loading ? (
                        <div className="flex items-center justify-center p-12">
                            <Loader2 className="h-8 w-8 animate-spin text-primary" />
                        </div>
                    ) : filteredStudents.length === 0 ? (
                        <div className="flex flex-col items-center justify-center p-12 text-center">
                            <UserX className="h-12 w-12 text-muted-foreground mb-4" />
                            <h3 className="text-lg font-semibold">No students found</h3>
                            <p className="text-sm text-muted-foreground">
                                {searchQuery || statusFilter !== "all"
                                    ? "Try adjusting your search or filters"
                                    : "Get started by adding your first student"}
                            </p>
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Reg No.</TableHead>
                                    <TableHead>Roll No.</TableHead>
                                    <TableHead>Name</TableHead>
                                    <TableHead>Email</TableHead>
                                    <TableHead>Phone</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredStudents.map((student) => (
                                    <TableRow key={student.ukid}>
                                        <TableCell className="font-mono">{student.registration_number ?? "-"}</TableCell>
                                        <TableCell className="font-mono">{student.roll_number ?? "-"}</TableCell>
                                        <TableCell className="font-medium">
                                            {student.first_name} {student.middle_name} {student.last_name}
                                        </TableCell>
                                        <TableCell>{student.email}</TableCell>
                                        <TableCell>{student.phone_number}</TableCell>
                                        <TableCell>
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
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => router.push(`/students/${student.ukid}`)}
                                                >
                                                    <Eye className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => router.push(`/students/${student.ukid}/edit`)}
                                                >
                                                    <Pencil className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => {
                                                        setStudentForUpload(student);
                                                        setUploadDialogOpen(true);
                                                    }}
                                                    title="Upload Document"
                                                >
                                                    <FileUp className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => {
                                                        setStudentToDelete(student);
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
                            This will delete the student record for{" "}
                            <strong>
                                {studentToDelete?.first_name} {studentToDelete?.last_name}
                            </strong>
                            . This action cannot be undone.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                            Delete
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>

            {/* Document Upload Dialog */}
            <Dialog open={uploadDialogOpen} onOpenChange={setUploadDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Upload Document</DialogTitle>
                        <DialogDescription>
                            Upload a document for{" "}
                            <strong>
                                {studentForUpload?.first_name} {studentForUpload?.last_name}
                            </strong>
                        </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                        <div className="space-y-2">
                            <Label htmlFor="document_type">Document Type</Label>
                            <Select value={documentType} onValueChange={setDocumentType}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select document type" />
                                </SelectTrigger>
                                <SelectContent>
                                    {DOCUMENT_TYPE_OPTIONS.map((option) => (
                                        <SelectItem key={option.value} value={option.value}>
                                            {option.label}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="file">File</Label>
                            <Input
                                id="file"
                                type="file"
                                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button
                            variant="outline"
                            onClick={() => {
                                setUploadDialogOpen(false);
                                setStudentForUpload(null);
                                setUploadFile(null);
                                setDocumentType("");
                            }}
                        >
                            Cancel
                        </Button>
                        <Button
                            onClick={handleUploadDocument}
                            disabled={uploading || !uploadFile || !documentType}
                        >
                            {uploading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            {uploading ? "Uploading..." : "Upload"}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}
