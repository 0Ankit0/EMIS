"use client";

import { useState } from "react";
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
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { bulkImportResults } from "@/services/subjectResultService";
import { Loader2, ArrowLeft, FileSpreadsheet } from "lucide-react";
import Link from "next/link";

const formSchema = z.object({
    file: z.any().refine((files) => files?.length > 0, "Excel file is required"),
});

type FormValues = z.infer<typeof formSchema>;

export default function ImportResultsPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = params.id as string;
    const [isLoading, setIsLoading] = useState(false);

    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema) as any,
    });

    async function onSubmit(values: FormValues) {
        setIsLoading(true);
        try {
            const file = values.file[0];
            const result = await bulkImportResults(file);
            toast.success(`Successfully imported ${result.imported} subject results`);
            router.push(`/students/${studentId}/results`);
        } catch (error: any) {
            toast.error(error.message || "Failed to import results");
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
                <h3 className="text-2xl font-bold tracking-tight">Import Subject Results</h3>
                <p className="text-sm text-muted-foreground">
                    Bulk import subject results from an Excel file
                </p>
            </div>

            <Card className="border-dashed">
                <CardHeader>
                    <div className="flex items-center gap-3">
                        <FileSpreadsheet className="h-5 w-5 text-primary" />
                        <div>
                            <CardTitle>Excel File Format</CardTitle>
                            <CardDescription>Required columns in the Excel file</CardDescription>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="space-y-2 text-sm">
                        <p className="font-medium">The Excel file should contain the following columns:</p>
                        <ul className="list-disc list-inside space-y-1 text-muted-foreground ml-2">
                            <li>Subject Name (required)</li>
                            <li>Semester (required)</li>
                            <li>Marks Obtained (optional)</li>
                            <li>Maximum Marks (optional)</li>
                            <li>Grade (optional: A+, A, B+, B, C+, C, D, F, I, W)</li>
                            <li>Credit Hours (default: 3)</li>
                            <li>Attempt Type (optional: Regular or Re-examination)</li>
                        </ul>
                    </div>
                </CardContent>
            </Card>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Upload File</CardTitle>
                            <CardDescription>Select an Excel file to import</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <FormField
                                control={form.control}
                                name="file"
                                render={({ field: { onChange, value, ...rest } }) => (
                                    <FormItem>
                                        <FormLabel>Excel File</FormLabel>
                                        <FormControl>
                                            <Input
                                                type="file"
                                                accept=".xlsx, .xls"
                                                onChange={(e) => onChange(e.target.files)}
                                                {...rest}
                                            />
                                        </FormControl>
                                        <FormDescription>
                                            Upload an Excel file (.xlsx or .xls) containing subject results
                                        </FormDescription>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
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
                            {isLoading ? "Importing..." : "Import Results"}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
