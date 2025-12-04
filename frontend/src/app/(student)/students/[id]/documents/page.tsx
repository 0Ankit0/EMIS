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
import { getDocuments, deleteDocument, downloadDocument } from "@/services/documentService";
import { getStudent } from "@/services/studentService";
import type { Document as StudentDocument, Student } from "@/types/student";
import { ArrowLeft, Plus, Trash2, Loader2, Download, CheckCircle, XCircle, FileText } from "lucide-react";
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
import { DOCUMENT_TYPE_OPTIONS } from "@/types/student";

export default function DocumentsPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = Number(params.id);

    const [student, setStudent] = useState<Student | null>(null);
    const [documents, setDocuments] = useState<StudentDocument[]>([]);
    const [loading, setLoading] = useState(true);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [documentToDelete, setDocumentToDelete] = useState<StudentDocument | null>(null);

    useEffect(() => {
        if (studentId) {
            loadData();
        }
    }, [studentId]);

    const loadData = async () => {
        try {
            setLoading(true);
            const [studentData, documentsData] = await Promise.all([
                getStudent(studentId),
                getDocuments(studentId),
            ]);
            setStudent(studentData);
            setDocuments(documentsData);
        } catch (error: any) {
            toast.error(error.message || "Failed to load data");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!documentToDelete) return;

        try {
            await deleteDocument(documentToDelete.id);
            toast.success("Document deleted successfully");
            loadData();
        } catch (error: any) {
            toast.error(error.message || "Failed to delete document");
        } finally {
            setDeleteDialogOpen(false);
            setDocumentToDelete(null);
        }
    };

    const handleDownload = async (doc: StudentDocument) => {
        try {
            const blob = await downloadDocument(doc.id);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = doc.file.split("/").pop() || "document";
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            toast.success("Document downloaded");
        } catch (error: any) {
            toast.error(error.message || "Failed to download document");
        }
    };

    const getDocumentTypeName = (type: string) => {
        const option = DOCUMENT_TYPE_OPTIONS.find(opt => opt.value === type);
        return option?.label || type;
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
                        <h3 className="text-2xl font-bold tracking-tight">Documents</h3>
                        {student && (
                            <p className="text-sm text-muted-foreground">
                                {student.first_name} {student.last_name}
                            </p>
                        )}
                    </div>
                </div>
                <Link href={`/students/${studentId}/documents/upload`}>
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Upload Document
                    </Button>
                </Link>
            </div>

            {/* Documents Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Student Documents</CardTitle>
                    <CardDescription>All uploaded documents for this student</CardDescription>
                </CardHeader>
                <CardContent className="p-0">
                    {documents.length === 0 ? (
                        <div className="flex flex-col items-center justify-center p-12 text-center">
                            <FileText className="h-12 w-12 text-muted-foreground mb-4" />
                            <h3 className="text-lg font-semibold">No documents found</h3>
                            <p className="text-sm text-muted-foreground mb-4">
                                Upload documents for this student
                            </p>
                            <Link href={`/students/${studentId}/documents/upload`}>
                                <Button>
                                    <Plus className="mr-2 h-4 w-4" />
                                    Upload First Document
                                </Button>
                            </Link>
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Document Type</TableHead>
                                    <TableHead>Uploaded Date</TableHead>
                                    <TableHead>Verification Status</TableHead>
                                    <TableHead>Verified By</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {documents.map((document) => (
                                    <TableRow key={document.id}>
                                        <TableCell className="font-medium">
                                            {getDocumentTypeName(document.document_type)}
                                        </TableCell>
                                        <TableCell>
                                            {new Date(document.uploaded_at).toLocaleDateString()}
                                        </TableCell>
                                        <TableCell>
                                            {document.is_verified ? (
                                                <Badge variant="default" className="gap-1">
                                                    <CheckCircle className="h-3 w-3" />
                                                    Verified
                                                </Badge>
                                            ) : (
                                                <Badge variant="secondary" className="gap-1">
                                                    <XCircle className="h-3 w-3" />
                                                    Not Verified
                                                </Badge>
                                            )}
                                        </TableCell>
                                        <TableCell>{document.verified_by || "—"}</TableCell>
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => handleDownload(document)}
                                                >
                                                    <Download className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => {
                                                        setDocumentToDelete(document);
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
                            This will permanently delete this document.
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
