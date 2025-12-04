"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
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
import { getEnrollment, updateEnrollment } from "@/services/enrollmentService";
import { Loader2, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { ENROLLMENT_STATUS_OPTIONS } from "@/types/student";

const formSchema = z.object({
    program: z.string().min(1, "Program is required"),
    semester: z.string().min(1, "Semester is required"),
    enrollment_date: z.string().min(1, "Enrollment date is required"),
    status: z.enum(["enrolled", "completed", "dropped", "repeated"]),
});

type FormValues = z.infer<typeof formSchema>;

export default function EditEnrollmentPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = Number(params.id);
    const enrollmentId = Number(params.enrollmentId);
    const [isLoading, setIsLoading] = useState(false);
    const [loadingData, setLoadingData] = useState(true);

    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema) as any,
    });

    useEffect(() => {
        if (enrollmentId) {
            loadEnrollment();
        }
    }, [enrollmentId]);

    const loadEnrollment = async () => {
        try {
            setLoadingData(true);
            const enrollment = await getEnrollment(enrollmentId);
            form.reset({
                program: enrollment.program,
                semester: enrollment.semester,
                enrollment_date: enrollment.enrollment_date,
                status: enrollment.status,
            });
        } catch (error: any) {
            toast.error(error.message || "Failed to load enrollment");
            router.push(`/students/${studentId}/enrollments`);
        } finally {
            setLoadingData(false);
        }
    };

    async function onSubmit(values: FormValues) {
        setIsLoading(true);
        try {
            await updateEnrollment(enrollmentId, values);
            toast.success("Enrollment updated successfully");
            router.push(`/students/${studentId}/enrollments`);
        } catch (error: any) {
            toast.error(error.message || "Failed to update enrollment");
        } finally {
            setIsLoading(false);
        }
    }

    if (loadingData) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
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
                <h3 className="text-2xl font-bold tracking-tight">Edit Enrollment</h3>
                <p className="text-sm text-muted-foreground">
                    Update enrollment information
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
                                        <Select onValueChange={field.onChange} value={field.value}>
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
                            {isLoading ? "Updating..." : "Update Enrollment"}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
