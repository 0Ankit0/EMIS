"use client";

import Link from "next/link";
import { User, ArrowLeft, Edit, MapPin, Phone, Briefcase, GraduationCap, BookOpen, Award, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function FacultyDetailPage({ params }: { params: { id: string } }) {
    // Mock data based on Faculty model
    const faculty = {
        id: params.id,
        employeeId: "FAC-001",
        firstName: "Robert",
        lastName: "Langdon",
        designation: "Professor",
        department: "History",
        specialization: "Symbology",
        email: "robert.langdon@emis.edu",
        phone: "+1 234 567 8901",
        status: "active",
        dob: "June 22, 1964",
        joiningDate: "September 1, 2005",
        address: "123 Harvard Square, Cambridge, MA",
        qualifications: [
            { degree: "Ph.D.", field: "Religious Symbology", institution: "Harvard University", year: 1995 },
            { degree: "Masters", field: "Art History", institution: "Princeton University", year: 1990 },
        ],
        experience: [
            { role: "Professor", organization: "Harvard University", duration: "2005 - Present" },
            { role: "Associate Professor", organization: "Oxford University", duration: "2000 - 2005" },
        ],
        publications: [
            { title: "Symbols of the Lost Sacred Feminine", year: 2003, type: "Book" },
            { title: "The Art of the Illuminati", year: 2000, type: "Book" },
        ],
    };

    const getStatusBadge = (status: string) => {
        switch (status) {
            case "active":
                return <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Active</Badge>;
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
                        {faculty.firstName} {faculty.lastName}
                    </h2>
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <span>{faculty.designation}</span>
                        <span>•</span>
                        <span>{faculty.department}</span>
                        <span>•</span>
                        {getStatusBadge(faculty.status)}
                    </div>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" asChild>
                        <Link href="/faculty">
                            <ArrowLeft className="mr-2 h-4 w-4" /> Back to List
                        </Link>
                    </Button>
                    <Button className="bg-yellow-600 hover:bg-yellow-700" asChild>
                        <Link href={`/faculty/${faculty.id}/edit`}>
                            <Edit className="mr-2 h-4 w-4" /> Edit Profile
                        </Link>
                    </Button>
                </div>
            </div>

            <Tabs defaultValue="overview" className="space-y-6">
                <TabsList>
                    <TabsTrigger value="overview">Overview</TabsTrigger>
                    <TabsTrigger value="qualifications">Qualifications</TabsTrigger>
                    <TabsTrigger value="experience">Experience</TabsTrigger>
                    <TabsTrigger value="publications">Publications</TabsTrigger>
                </TabsList>

                <TabsContent value="overview" className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <User className="h-5 w-5 text-primary" />
                                    Personal Information
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Employee ID</p>
                                        <p>{faculty.employeeId}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Date of Birth</p>
                                        <p>{faculty.dob}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Email</p>
                                        <p>{faculty.email}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Phone</p>
                                        <p>{faculty.phone}</p>
                                    </div>
                                </div>
                                <Separator />
                                <div>
                                    <p className="text-sm font-medium text-muted-foreground mb-1">Address</p>
                                    <div className="flex items-start gap-2">
                                        <MapPin className="h-4 w-4 text-muted-foreground mt-1" />
                                        <p>{faculty.address}</p>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Briefcase className="h-5 w-5 text-primary" />
                                    Professional Details
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Department</p>
                                        <p>{faculty.department}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Designation</p>
                                        <p>{faculty.designation}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Specialization</p>
                                        <p>{faculty.specialization}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-muted-foreground">Joining Date</p>
                                        <p>{faculty.joiningDate}</p>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </TabsContent>

                <TabsContent value="qualifications">
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <GraduationCap className="h-5 w-5 text-primary" />
                                Educational Qualifications
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-6">
                                {faculty.qualifications.map((qual, index) => (
                                    <div key={index} className="flex justify-between items-start border-b last:border-0 pb-4 last:pb-0">
                                        <div>
                                            <h4 className="font-semibold text-lg">{qual.degree} in {qual.field}</h4>
                                            <p className="text-muted-foreground">{qual.institution}</p>
                                        </div>
                                        <Badge variant="outline">{qual.year}</Badge>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="experience">
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Briefcase className="h-5 w-5 text-primary" />
                                Work Experience
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-6">
                                {faculty.experience.map((exp, index) => (
                                    <div key={index} className="flex justify-between items-start border-b last:border-0 pb-4 last:pb-0">
                                        <div>
                                            <h4 className="font-semibold text-lg">{exp.role}</h4>
                                            <p className="text-muted-foreground">{exp.organization}</p>
                                        </div>
                                        <Badge variant="secondary">{exp.duration}</Badge>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="publications">
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <BookOpen className="h-5 w-5 text-primary" />
                                Publications
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-6">
                                {faculty.publications.map((pub, index) => (
                                    <div key={index} className="flex justify-between items-start border-b last:border-0 pb-4 last:pb-0">
                                        <div className="flex items-start gap-3">
                                            <FileText className="h-5 w-5 text-muted-foreground mt-1" />
                                            <div>
                                                <h4 className="font-semibold text-lg">{pub.title}</h4>
                                                <p className="text-muted-foreground text-sm">{pub.type}</p>
                                            </div>
                                        </div>
                                        <Badge variant="outline">{pub.year}</Badge>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}
