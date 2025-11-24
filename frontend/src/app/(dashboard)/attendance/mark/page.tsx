"use client";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Calendar, Save, UserCheck, UserX, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";

const attendanceSchema = z.object({
    course: z.string().min(1, "Please select a course"),
    date: z.string().min(1, "Please select a date"),
    session: z.string().min(1, "Please select a session"),
});

const mockStudents = [
    { id: "1", studentId: "STU001", name: "John Doe", status: null as "present" | "absent" | "late" | null },
    { id: "2", studentId: "STU002", name: "Jane Smith", status: null as "present" | "absent" | "late" | null },
    { id: "3", studentId: "STU003", name: "Mike Johnson", status: null as "present" | "absent" | "late" | null },
    { id: "4", studentId: "STU004", name: "Sarah Williams", status: null as "present" | "absent" | "late" | null },
    { id: "5", studentId: "STU005", name: "Tom Brown", status: null as "present" | "absent" | "late" | null },
];

export default function MarkAttendancePage() {
    const [students, setStudents] = useState(mockStudents);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const form = useForm<z.infer<typeof attendanceSchema>>({
        resolver: zodResolver(attendanceSchema),
        defaultValues: {
            course: "",
            date: new Date().toISOString().split('T')[0],
            session: "",
        },
    });

    const markStatus = (studentId: string, status: "present" | "absent" | "late") => {
        setStudents(students.map(s =>
            s.id === studentId ? { ...s, status } : s
        ));
    };

    const markAllPresent = () => {
        setStudents(students.map(s => ({ ...s, status: "present" as const })));
    };

    const onSubmit = async (data: z.infer<typeof attendanceSchema>) => {
        setIsSubmitting(true);
        try {
            const attendanceData = students.map(s => ({
                student_id: s.id,
                status: s.status || "absent",
            }));

            // TODO: API call to save attendance
            console.log("Saving attendance:", { ...data, attendance: attendanceData });
            await new Promise(resolve => setTimeout(resolve, 1000));
            alert("Attendance marked successfully!");
        } catch (error) {
            console.error("Error saving attendance:", error);
            alert("Failed to save attendance");
        } finally {
            setIsSubmitting(false);
        }
    };

    const getStats = () => {
        const present = students.filter(s => s.status === "present").length;
        const absent = students.filter(s => s.status === "absent").length;
        const late = students.filter(s => s.status === "late").length;
        const notMarked = students.filter(s => !s.status).length;
        return { present, absent, late, notMarked };
    };

    const stats = getStats();

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Calendar className="h-8 w-8 text-primary" />
                    Mark Attendance
                </h2>
                <p className="text-muted-foreground">Record student attendance for classes</p>
            </div>

            {/* Session Selection */}
            <Card>
                <CardHeader>
                    <CardTitle>Session Details</CardTitle>
                </CardHeader>
                <CardContent>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                            <div className="grid grid-cols-3 gap-4">
                                <FormField
                                    control={form.control}
                                    name="course"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Course *</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select course" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    <SelectItem value="CS101">CS101 - Intro to Programming</SelectItem>
                                                    <SelectItem value="MATH201">MATH201 - Calculus II</SelectItem>
                                                    <SelectItem value="ENG102">ENG102 - English Literature</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="date"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Date *</FormLabel>
                                            <FormControl>
                                                <input type="date" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="session"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Session *</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select session" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    <SelectItem value="morning">Morning (9:00 AM - 12:00 PM)</SelectItem>
                                                    <SelectItem value="afternoon">Afternoon (1:00 PM - 4:00 PM)</SelectItem>
                                                    <SelectItem value="evening">Evening (5:00 PM - 8:00 PM)</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                        </form>
                    </Form>
                </CardContent>
            </Card>

            {/* Statistics */}
            <div className="grid grid-cols-4 gap-4">
                <Card>
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Present</p>
                                <p className="text-2xl font-bold text-green-600">{stats.present}</p>
                            </div>
                            <UserCheck className="h-8 w-8 text-green-600" />
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Absent</p>
                                <p className="text-2xl font-bold text-red-600">{stats.absent}</p>
                            </div>
                            <UserX className="h-8 w-8 text-red-600" />
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Late</p>
                                <p className="text-2xl font-bold text-yellow-600">{stats.late}</p>
                            </div>
                            <Clock className="h-8 w-8 text-yellow-600" />
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground">Not Marked</p>
                                <p className="text-2xl font-bold text-gray-600">{stats.notMarked}</p>
                            </div>
                            <Calendar className="h-8 w-8 text-gray-600" />
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Student List */}
            <Card>
                <CardHeader>
                    <div className="flex justify-between items-center">
                        <CardTitle>Students ({students.length})</CardTitle>
                        <Button variant="outline" size="sm" onClick={markAllPresent}>
                            <UserCheck className="mr-2 h-4 w-4" />
                            Mark All Present
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead className="w-24">Student ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {students.map((student) => (
                                <TableRow key={student.id}>
                                    <TableCell className="font-mono text-sm">{student.studentId}</TableCell>
                                    <TableCell className="font-semibold">{student.name}</TableCell>
                                    <TableCell>
                                        {student.status ? (
                                            <Badge className={
                                                student.status === "present" ? "bg-green-100 text-green-800" :
                                                    student.status === "absent" ? "bg-red-100 text-red-800" :
                                                        "bg-yellow-100 text-yellow-800"
                                            }>
                                                {student.status.toUpperCase()}
                                            </Badge>
                                        ) : (
                                            <Badge variant="outline">Not Marked</Badge>
                                        )}
                                    </TableCell>
                                    <TableCell className="text-right space-x-2">
                                        <Button
                                            variant={student.status === "present" ? "default" : "outline"}
                                            size="sm"
                                            onClick={() => markStatus(student.id, "present")}
                                            className={student.status === "present" ? "bg-green-600 hover:bg-green-700" : ""}
                                        >
                                            Present
                                        </Button>
                                        <Button
                                            variant={student.status === "late" ? "default" : "outline"}
                                            size="sm"
                                            onClick={() => markStatus(student.id, "late")}
                                            className={student.status === "late" ? "bg-yellow-600 hover:bg-yellow-700" : ""}
                                        >
                                            Late
                                        </Button>
                                        <Button
                                            variant={student.status === "absent" ? "default" : "outline"}
                                            size="sm"
                                            onClick={() => markStatus(student.id, "absent")}
                                            className={student.status === "absent" ? "bg-red-600 hover:bg-red-700" : ""}
                                        >
                                            Absent
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

            {/* Submit Button */}
            <div className="flex justify-end">
                <Button
                    size="lg"
                    onClick={form.handleSubmit(onSubmit)}
                    disabled={isSubmitting || stats.notMarked > 0}
                >
                    <Save className="mr-2 h-5 w-5" />
                    {isSubmitting ? "Saving..." : "Save Attendance"}
                </Button>
            </div>
        </div>
    );
}
