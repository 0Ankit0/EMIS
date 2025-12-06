"use client";

import { useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
    FormDescription,
} from "@/components/ui/form";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { createAcademicRecord } from "@/services/academicRecordService";
import { Loader2, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { academicRecordFormSchema, type AcademicRecordFormValues } from "@/types/student";

export default function NewAcademicRecordPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = params.id as string;
    const [isLoading, setIsLoading] = useState(false);

    const form = useForm<AcademicRecordFormValues>({
        resolver: zodResolver(academicRecordFormSchema) as any,
        defaultValues: {
            semester: "",
            gpa: 0,
            total_credits: 0,
            remarks: "",
        },
    });

    async function onSubmit(values: AcademicRecordFormValues) {
        setIsLoading(true);
        try {
            await createAcademicRecord({
                student: studentId,
                semester: values.semester,
                gpa: values.gpa.toFixed(2),
                total_credits: values.total_credits,
                remarks: values.remarks,
            });
            toast.success("Academic record created successfully");
            router.push(`/students/${studentId}/academic-records`);
        } catch (error: any) {
            toast.error(error.message || "Failed to create academic record");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-4">
                <Link href={`/students/${studentId}/academic-records`}>
                    <Button variant="ghost" size="sm">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back to Records
                    </Button>
                </Link>
            </div>

            <div>
                <h3 className="text-2xl font-bold tracking-tight">Add Academic Record</h3>
                <p className="text-sm text-muted-foreground">
                    Add semester GPA and credits
                </p>
            </div>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Academic Details</CardTitle>
                            <CardDescription>Semester performance information</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <FormField
                                control={form.control}
                                name="semester"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Semester</FormLabel>
                                        <FormControl>
                                            <Input placeholder="e.g., 1st Semester" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <div className="grid gap-4 md:grid-cols-2">
                                <FormField
                                    control={form.control}
                                    name="gpa"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>GPA</FormLabel>
                                            <FormControl>
                                                <Input
                                                    type="number"
                                                    step="0.01"
                                                    min="0"
                                                    max="4.00"
                                                    placeholder="3.75"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormDescription>On a scale of 0.00 to 4.00</FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="total_credits"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Total Credits</FormLabel>
                                            <FormControl>
                                                <Input type="number" min="0" placeholder="18" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <FormField
                                control={form.control}
                                name="remarks"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Remarks (Optional)</FormLabel>
                                        <FormControl>
                                            <Textarea
                                                placeholder="Any additional notes or remarks..."
                                                className="resize-none"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    <div className="flex justify-end gap-4">
                        <Link href={`/students/${studentId}/academic-records`}>
                            <Button type="button" variant="outline">
                                Cancel
                            </Button>
                        </Link>
                        <Button type="submit" disabled={isLoading}>
                            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            {isLoading ? "Creating..." : "Create Record"}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
