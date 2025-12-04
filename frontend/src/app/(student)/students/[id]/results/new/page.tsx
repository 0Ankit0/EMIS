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
import { createSubjectResult } from "@/services/subjectResultService";
import { Loader2, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { subjectResultFormSchema, GRADE_OPTIONS, ATTEMPT_TYPE_OPTIONS, type SubjectResultFormValues } from "@/types/student";

export default function NewSubjectResultPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = Number(params.id);
    const [isLoading, setIsLoading] = useState(false);

    const form = useForm<SubjectResultFormValues>({
        resolver: zodResolver(subjectResultFormSchema) as any,
        defaultValues: {
            subject_name: "",
            marks_obtained: "",
            maximum_marks: "",
            grade: "",
            credit_hours: 3,
            semester: "",
            attempt_type: "regular",
        },
    });

    async function onSubmit(values: SubjectResultFormValues) {
        setIsLoading(true);
        try {
            await createSubjectResult({
                student: studentId,
                ...values,
            });
            toast.success("Subject result created successfully");
            router.push(`/students/${studentId}/results`);
        } catch (error: any) {
            toast.error(error.message || "Failed to create subject result");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-4">
                <Link href={`/students/${studentId}/results`}>
                    <Button variant="ghost" size="sm">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back to Results
                    </Button>
                </Link>
            </div>

            <div>
                <h3 className="text-2xl font-bold tracking-tight">Add Subject Result</h3>
                <p className="text-sm text-muted-foreground">
                    Add a new subject result for the student
                </p>
            </div>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Subject Information</CardTitle>
                            <CardDescription>Enter subject details and result</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <FormField
                                control={form.control}
                                name="subject_name"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Subject Name</FormLabel>
                                        <FormControl>
                                            <Input placeholder="e.g., Database Management System" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <div className="grid gap-4 md:grid-cols-2">
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

                                <FormField
                                    control={form.control}
                                    name="credit_hours"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Credit Hours</FormLabel>
                                            <FormControl>
                                                <Input type="number" min="0" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <div className="grid gap-4 md:grid-cols-2">
                                <FormField
                                    control={form.control}
                                    name="marks_obtained"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Marks Obtained (Optional)</FormLabel>
                                            <FormControl>
                                                <Input placeholder="85" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="maximum_marks"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Maximum Marks (Optional)</FormLabel>
                                            <FormControl>
                                                <Input placeholder="100" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <div className="grid gap-4 md:grid-cols-2">
                                <FormField
                                    control={form.control}
                                    name="grade"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Grade (Optional)</FormLabel>
                                            <Select onValueChange={field.onChange} value={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select grade" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    {GRADE_OPTIONS.map((option) => (
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

                                <FormField
                                    control={form.control}
                                    name="attempt_type"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Attempt Type</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select attempt type" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    {ATTEMPT_TYPE_OPTIONS.map((option) => (
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
                            </div>
                        </CardContent>
                    </Card>

                    <div className="flex justify-end gap-4">
                        <Link href={`/students/${studentId}/results`}>
                            <Button type="button" variant="outline">
                                Cancel
                            </Button>
                        </Link>
                        <Button type="submit" disabled={isLoading}>
                            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            {isLoading ? "Creating..." : "Create Result"}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
