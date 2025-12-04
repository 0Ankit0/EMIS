"use client";

import { useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
    FormDescription,
} from "@/components/ui/form";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { createEnrollment } from "@/services/enrollmentService";
import { Loader2, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { enrollmentFormSchema, ENROLLMENT_STATUS_OPTIONS, type EnrollmentFormValues } from "@/types/student";

export default function NewEnrollmentPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = Number(params.id);
    const [isLoading, setIsLoading] = useState(false);

    const form = useForm<EnrollmentFormValues>({
        resolver: zodResolver(enrollmentFormSchema) as any,
        defaultValues: {
            program: "",
            semester: "",
            enrollment_date: "",
            status: "enrolled",
        },
    });

    async function onSubmit(values: EnrollmentFormValues) {
        setIsLoading(true);
        try {
            await createEnrollment({
                student: studentId,
                ...values,
            });
            toast.success("Enrollment created successfully");
            router.push(`/students/${studentId}/enrollments`);
        } catch (error: any) {
            toast.error(error.message || "Failed to create enrollment");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center gap-4">
                <Link href={`/students/${studentId}/enrollments`}>
                    <Button variant="ghost" size="sm">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back to Enrollments
                    </Button>
                </Link>
            </div>

            <div>
                <h3 className="text-2xl font-bold tracking-tight">Add New Enrollment</h3>
                <p className="text-sm text-muted-foreground">
                    Enroll student in a new program
                </p>
            </div>

            {/* Form */}
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Enrollment Details</CardTitle>
                            <CardDescription>Program enrollment information</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <FormField
                                control={form.control}
                                name="program"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Program</FormLabel>
                                        <FormControl>
                                            <Input placeholder="e.g., Bachelor of Computer Application" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="semester"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Semester</FormLabel>
                                        <FormControl>
                                            <Input placeholder="e.g., 1st Semester" {...field} />
                                        </FormControl>
                                        <FormDescription>
                                            The semester/year the student is enrolling in
                                        </FormDescription>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="enrollment_date"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Enrollment Date</FormLabel>
                                        <FormControl>
                                            <Input type="date" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="status"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Status</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select status" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                {ENROLLMENT_STATUS_OPTIONS.map((option) => (
                                                    <SelectItem key={option.value} value={option.value}>
                                                        {option.label}
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    {/* Form Actions */}
                    <div className="flex justify-end gap-4">
                        <Link href={`/students/${studentId}/enrollments`}>
                            <Button type="button" variant="outline">
                                Cancel
                            </Button>
                        </Link>
                        <Button type="submit" disabled={isLoading}>
                            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            {isLoading ? "Creating..." : "Create Enrollment"}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
