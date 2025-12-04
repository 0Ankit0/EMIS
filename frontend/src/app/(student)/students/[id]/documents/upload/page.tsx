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
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { uploadDocument } from "@/services/documentService";
import { Loader2, ArrowLeft, Upload } from "lucide-react";
import Link from "next/link";
import { DOCUMENT_TYPE_OPTIONS } from "@/types/student";

const formSchema = z.object({
    document_type: z.enum(["id_proof", "birth_cert", "transcript", "photo", "medical", "transfer", "other"]),
    file: z.any().refine((files) => files?.length > 0, "File is required"),
});

type FormValues = z.infer<typeof formSchema>;

export default function UploadDocumentPage() {
    const router = useRouter();
    const params = useParams();
    const studentId = Number(params.id);
    const [isLoading, setIsLoading] = useState(false);

    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema) as any,
        defaultValues: {
            document_type: "other",
        },
    });

    async function onSubmit(values: FormValues) {
        setIsLoading(true);
        try {
            const file = values.file[0];
            await uploadDocument({
                student: studentId,
                document_type: values.document_type,
                file,
            });
            toast.success("Document uploaded successfully");
            router.push(`/students/${studentId}/documents`);
        } catch (error: any) {
            toast.error(error.message || "Failed to upload document");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-4">
                <Link href={`/students/${studentId}/documents`}>
                    <Button variant="ghost" size="sm">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back to Documents
                    </Button>
                </Link>
            </div>

            <div>
                <h3 className="text-2xl font-bold tracking-tight">Upload Document</h3>
                <p className="text-sm text-muted-foreground">
                    Upload a new document for the student
                </p>
            </div>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <div className="flex items-center gap-3">
                                <Upload className="h-5 w-5 text-primary" />
                                <div>
                                    <CardTitle>Document Details</CardTitle>
                                    <CardDescription>Select document type and file</CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <FormField
                                control={form.control}
                                name="document_type"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Document Type</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select document type" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                {DOCUMENT_TYPE_OPTIONS.map((option) => (
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
                                name="file"
                                render={({ field: { onChange, value, ...rest } }) => (
                                    <FormItem>
                                        <FormLabel>File</FormLabel>
                                        <FormControl>
                                            <Input
                                                type="file"
                                                accept=".pdf,.jpg,.jpeg,.png"
                                                onChange={(e) => onChange(e.target.files)}
                                                {...rest}
                                            />
                                        </FormControl>
                                        <FormDescription>
                                            Accepted formats: PDF, JPG, JPEG, PNG (Max size: 10MB)
                                        </FormDescription>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    <div className="flex justify-end gap-4">
                        <Link href={`/students/${studentId}/documents`}>
                            <Button type="button" variant="outline">
                                Cancel
                            </Button>
                        </Link>
                        <Button type="submit" disabled={isLoading}>
                            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            {isLoading ? "Uploading..." : "Upload Document"}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
