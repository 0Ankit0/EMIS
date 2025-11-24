"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, Edit, Trash, CheckCircle, XCircle, FileText, User, Mail, Phone, MapPin, Calendar, GraduationCap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

// Mock data - replace with API call
const applicationData = {
    id: 1,
    application_number: "APP-2025-001",
    status: "pending",
    submission_date: "2025-01-15",
    applicant: {
        first_name: "John",
        last_name: "Doe",
        email: "john.doe@example.com",
        phone: "+1 234 567 8900",
        date_of_birth: "2005-03-15",
        gender: "Male",
        nationality: "American",
    },
    address: {
        street: "123 Main St",
        city: "New York",
        state: "NY",
        postal_code: "10001",
        country: "USA",
    },
    academic: {
        previous_school: "ABC High School",
        gpa: "3.8",
        graduation_year: "2024",
        test_scores: {
            SAT: "1450",
            ACT: "32",
        },
    },
    program: {
        name: "Computer Science",
        degree: "Bachelor of Science",
        intake: "Fall 2025",
    },
    documents: [
        { name: "Transcript", status: "verified", uploaded_date: "2025-01-10" },
        { name: "Recommendation Letter", status: "pending", uploaded_date: "2025-01-12" },
        { name: "Personal Statement", status: "verified", uploaded_date: "2025-01-14" },
    ],
    reviewer_notes: "",
};

export default function ApplicationDetailPage({ params }: { params: { id: string } }) {
    const [application] = useState(applicationData);
    const [showApproveDialog, setShowApproveDialog] = useState(false);
    const [showRejectDialog, setShowRejectDialog] = useState(false);
    const [notes, setNotes] = useState("");

    const handleApprove = () => {
        // TODO: API call to approve
        console.log("Approving application:", params.id, notes);
        alert("Application approved!");
        setShowApproveDialog(false);
    };

    const handleReject = () => {
        // TODO: API call to reject
        console.log("Rejecting application:", params.id, notes);
        alert("Application rejected!");
        setShowRejectDialog(false);
    };

    const getStatusBadge = (status: string) => {
        const variants = {
            pending: "bg-yellow-100 text-yellow-800 border-yellow-200",
            approved: "bg-green-100 text-green-800 border-green-200",
            rejected: "bg-red-100 text-red-800 border-red-200",
            submitted: "bg-blue-100 text-blue-800 border-blue-200",
        };
        return <Badge className={variants[status as keyof typeof variants] || "bg-gray-100 text-gray-800"} variant="outline">{status.toUpperCase()}</Badge>;
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link href="/admissions/applications">
                        <Button variant="ghost" size="icon">
                            <ArrowLeft className="h-5 w-5" />
                        </Button>
                    </Link>
                    <div>
                        <h2 className="text-3xl font-bold text-gray-800">Application Details</h2>
                        <p className="text-muted-foreground">#{application.application_number}</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    {getStatusBadge(application.status)}
                    <Link href={`/admissions/applications/${params.id}/edit`}>
                        <Button variant="outline">
                            <Edit className="mr-2 h-4 w-4" />
                            Edit
                        </Button>
                    </Link>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Main Content */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Personal Information */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <User className="h-5 w-5" />
                                Personal Information
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-sm text-muted-foreground">Full Name</p>
                                <p className="font-semibold">{application.applicant.first_name} {application.applicant.last_name}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Email</p>
                                <p className="font-semibold flex items-center gap-1">
                                    <Mail className="h-4 w-4" />
                                    {application.applicant.email}
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Phone</p>
                                <p className="font-semibold flex items-center gap-1">
                                    <Phone className="h-4 w-4" />
                                    {application.applicant.phone}
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Date of Birth</p>
                                <p className="font-semibold flex items-center gap-1">
                                    <Calendar className="h-4 w-4" />
                                    {application.applicant.date_of_birth}
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Gender</p>
                                <p className="font-semibold">{application.applicant.gender}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Nationality</p>
                                <p className="font-semibold">{application.applicant.nationality}</p>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Address */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <MapPin className="h-5 w-5" />
                                Address
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="font-semibold">{application.address.street}</p>
                            <p className="text-muted-foreground">
                                {application.address.city}, {application.address.state} {application.address.postal_code}
                            </p>
                            <p className="text-muted-foreground">{application.address.country}</p>
                        </CardContent>
                    </Card>

                    {/* Academic Background */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <GraduationCap className="h-5 w-5" />
                                Academic Background
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <p className="text-sm text-muted-foreground">Previous School</p>
                                    <p className="font-semibold">{application.academic.previous_school}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-muted-foreground">Graduation Year</p>
                                    <p className="font-semibold">{application.academic.graduation_year}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-muted-foreground">GPA</p>
                                    <p className="font-semibold">{application.academic.gpa} / 4.0</p>
                                </div>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground mb-2">Test Scores</p>
                                <div className="grid grid-cols-2 gap-2">
                                    {Object.entries(application.academic.test_scores).map(([test, score]) => (
                                        <div key={test} className="bg-gray-50 p-2 rounded">
                                            <span className="text-sm font-semibold">{test}:</span> {score}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Documents */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <FileText className="h-5 w-5" />
                                Documents
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-2">
                                {application.documents.map((doc, index) => (
                                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                                        <div>
                                            <p className="font-semibold">{doc.name}</p>
                                            <p className="text-sm text-muted-foreground">Uploaded: {doc.uploaded_date}</p>
                                        </div>
                                        <Badge variant={doc.status === "verified" ? "default" : "secondary"}>
                                            {doc.status}
                                        </Badge>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Sidebar */}
                <div className="space-y-6">
                    {/* Program Details */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Program Applied</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3">
                            <div>
                                <p className="text-sm text-muted-foreground">Program</p>
                                <p className="font-semibold">{application.program.name}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Degree</p>
                                <p className="font-semibold">{application.program.degree}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Intake</p>
                                <p className="font-semibold">{application.program.intake}</p>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Actions */}
                    {application.status === "pending" && (
                        <Card>
                            <CardHeader>
                                <CardTitle>Review Actions</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-3">
                                <Button className="w-full bg-green-600 hover:bg-green-700" onClick={() => setShowApproveDialog(true)}>
                                    <CheckCircle className="mr-2 h-4 w-4" />
                                    Approve Application
                                </Button>
                                <Button className="w-full bg-red-600 hover:bg-red-700" onClick={() => setShowRejectDialog(true)}>
                                    <XCircle className="mr-2 h-4 w-4" />
                                    Reject Application
                                </Button>
                            </CardContent>
                        </Card>
                    )}

                    {/* Timeline */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Timeline</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-3">
                                <div className="border-l-2 border-blue-500 pl-3">
                                    <p className="text-sm font-semibold">Submitted</p>
                                    <p className="text-xs text-muted-foreground">{application.submission_date}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>

            {/* Approve Dialog */}
            <Dialog open={showApproveDialog} onOpenChange={setShowApproveDialog}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Approve Application</DialogTitle>
                        <DialogDescription>
                            Are you sure you want to approve this application? This action cannot be undone.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-2">
                        <Label htmlFor="approve-notes">Approval Notes (Optional)</Label>
                        <Textarea
                            id="approve-notes"
                            placeholder="Enter any notes..."
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                        />
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setShowApproveDialog(false)}>Cancel</Button>
                        <Button className="bg-green-600 hover:bg-green-700" onClick={handleApprove}>Approve</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* Reject Dialog */}
            <Dialog open={showRejectDialog} onOpenChange={setShowRejectDialog}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Reject Application</DialogTitle>
                        <DialogDescription>
                            Are you sure you want to reject this application? Please provide a reason.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-2">
                        <Label htmlFor="reject-notes">Rejection Reason *</Label>
                        <Textarea
                            id="reject-notes"
                            placeholder="Enter reason for rejection..."
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                            required
                        />
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setShowRejectDialog(false)}>Cancel</Button>
                        <Button className="bg-red-600 hover:bg-red-700" onClick={handleReject} disabled={!notes.trim()}>
                            Reject
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}
