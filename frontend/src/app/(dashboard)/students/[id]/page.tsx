"use client";

import Link from "next/link";
import { User, ArrowLeft, Edit, MapPin, Phone, GraduationCap, Info, Settings, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

export default function StudentDetailPage({ params }: { params: { id: string } }) {
    // Mock data - in a real app, fetch based on params.id
    const student = {
        id: params.id,
        studentId: "STU-2025-001",
        firstName: "John",
        lastName: "Doe",
        email: "john.doe@example.com",
        phone: "+1 234 567 8900",
        dob: "January 15, 2003",
        age: 22,
        gender: "Male",
        nationality: "American",
        status: "active",
        address: "123 Main St",
        city: "New York",
        state: "NY",
        postalCode: "10001",
        country: "USA",
        emergencyContact: {
            name: "Jane Doe",
            phone: "+1 987 654 3210",
            relationship: "Mother",
        },
        academic: {
            admissionDate: "September 1, 2023",
            gpa: "3.8",
            degreeEarned: null,
            graduationDate: null,
            honors: null,
        },
        system: {
            createdAt: "August 15, 2023 10:00 AM",
            createdBy: "Admin User",
            updatedAt: "October 20, 2025 2:30 PM",
            updatedBy: "Staff Member",
        },
    };

    const getStatusBadge = (status: string) => {
        switch (status) {
            case "active":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Active</Badge>;
            case "applicant":
                return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-yellow-200">Applicant</Badge>;
            case "graduated":
                return <Badge className="bg-purple-100 text-purple-800 hover:bg-purple-200 border-purple-200">Graduated</Badge>;
            default:
                return <Badge variant="secondary">{status}</Badge>;
        }
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <User className="h-8 w-8 text-primary" />
                        {student.firstName} {student.lastName}
                    </h2>
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <span>{student.studentId}</span>
                        <span>•</span>
                        {getStatusBadge(student.status)}
                    </div>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" asChild>
                        <Link href="/students">
                            <ArrowLeft className="mr-2 h-4 w-4" /> Back to List
                        </Link>
                    </Button>
                    <Button className="bg-yellow-600 hover:bg-yellow-700" asChild>
                        <Link href={`/students/${student.id}/edit`}>
                            <Edit className="mr-2 h-4 w-4" /> Edit
                        </Link>
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left Column */}
                <div className="md:col-span-2 space-y-6">
                    {/* Basic Info */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Info className="h-5 w-5 text-primary" />
                                Basic Information
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">Full Name</p>
                                    <p className="font-semibold">{student.firstName} {student.lastName}</p>
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">Email</p>
                                    <a href={`mailto:${student.email}`} className="text-blue-600 hover:underline">{student.email}</a>
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">Phone</p>
                                    <p>{student.phone}</p>
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">Date of Birth</p>
                                    <p>{student.dob} (Age: {student.age})</p>
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">Gender</p>
                                    <p>{student.gender}</p>
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">Nationality</p>
                                    <p>{student.nationality}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Address */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <MapPin className="h-5 w-5 text-primary" />
                                Address
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div>
                                <p className="text-sm font-medium text-muted-foreground">Street Address</p>
                                <p>{student.address}</p>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">City</p>
                                    <p>{student.city}</p>
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">State</p>
                                    <p>{student.state}</p>
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">Postal Code</p>
                                    <p>{student.postalCode}</p>
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground">Country</p>
                                    <p>{student.country}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Emergency Contact */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Phone className="h-5 w-5 text-primary" />
                                Emergency Contact
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <p className="text-sm font-medium text-muted-foreground">Name</p>
                                <p>{student.emergencyContact.name}</p>
                            </div>
                            <div>
                                <p className="text-sm font-medium text-muted-foreground">Phone</p>
                                <p>{student.emergencyContact.phone}</p>
                            </div>
                            <div>
                                <p className="text-sm font-medium text-muted-foreground">Relationship</p>
                                <p>{student.emergencyContact.relationship}</p>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Right Column */}
                <div className="space-y-6">
                    {/* Academic Info */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <GraduationCap className="h-5 w-5 text-primary" />
                                Academic Information
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div>
                                <p className="text-sm font-medium text-muted-foreground">Admission Date</p>
                                <p>{student.academic.admissionDate}</p>
                            </div>
                            <div>
                                <p className="text-sm font-medium text-muted-foreground">Current GPA</p>
                                <p className="font-bold text-lg">{student.academic.gpa}</p>
                            </div>
                            {student.status === "graduated" && (
                                <>
                                    <Separator />
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Graduation Date</p>
                                        <p>{student.academic.graduationDate}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Degree Earned</p>
                                        <p>{student.academic.degreeEarned}</p>
                                    </div>
                                </>
                            )}
                        </CardContent>
                    </Card>

                    {/* Actions */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Settings className="h-5 w-5 text-primary" />
                                Actions
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3">
                            {student.status === "applicant" && (
                                <Button className="w-full bg-green-600 hover:bg-green-700">
                                    <Check className="mr-2 h-4 w-4" /> Admit Student
                                </Button>
                            )}
                            {student.status === "active" && (
                                <Button className="w-full bg-purple-600 hover:bg-purple-700">
                                    <GraduationCap className="mr-2 h-4 w-4" /> Graduate Student
                                </Button>
                            )}
                        </CardContent>
                    </Card>

                    {/* System Info */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-sm">
                                <Info className="h-4 w-4" />
                                System Information
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3 text-sm">
                            <div>
                                <p className="text-muted-foreground">Created</p>
                                <p>{student.system.createdAt}</p>
                                <p className="text-xs text-muted-foreground">by {student.system.createdBy}</p>
                            </div>
                            <Separator />
                            <div>
                                <p className="text-muted-foreground">Last Updated</p>
                                <p>{student.system.updatedAt}</p>
                                <p className="text-xs text-muted-foreground">by {student.system.updatedBy}</p>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
