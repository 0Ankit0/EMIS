"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { toast } from "sonner";
import { processExamResults } from "@/services/examService";
import { Loader2 } from "lucide-react";

const formSchema = z.object({
    result_type: z.string().min(1, "Result Type is required"),
    year: z.string().min(1, "Year is required"),
    session: z.string().min(1, "Session is required"),
    semester: z.string().min(1, "Semester is required"),
    program: z.string().min(1, "Program is required"),
    delay: z.number().min(0).default(1),
    autofill: z.boolean().default(true),
    file: z.any(),
});

type FormValues = z.infer<typeof formSchema>;

export default function PUExamPage() {
    const [isLoading, setIsLoading] = useState(false);

    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema) as any,
        defaultValues: {
            result_type: "",
            year: "",
            session: "",
            semester: "",
            program: "",
            delay: 1,
            autofill: true,
        },
    });

    async function onSubmit(values: FormValues) {
        setIsLoading(true);
        try {
            const formData = new FormData();
            formData.append("result_type", values.result_type);
            formData.append("year", values.year);
            formData.append("session", values.session);
            formData.append("semester", values.semester);
            formData.append("program", values.program);
            formData.append("delay", String(values.delay));
            formData.append("autofill", String(values.autofill));
            formData.append("file", values.file[0]);

            const response = await processExamResults(formData);

            // Only download file if autofill is true
            if (values.autofill) {
                // Handle file download
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `processed_${values.file[0].name}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                toast.success("Exam results processed successfully!");
            } else {
                toast.success("Automation completed. Browser closed.");
            }
        } catch (error: any) {
            console.error(error);
            toast.error(error.message || "Something went wrong");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-medium">PU Exam Automation</h3>
                <p className="text-sm text-muted-foreground">
                    Automate fetching exam results from Pokhara University website.
                </p>
            </div>
            <div className="rounded-md border p-4">
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                            <FormField
                                control={form.control}
                                name="result_type"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Result Type</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select Result Type" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="Regular_Retake">Regular/Retake</SelectItem>
                                                <SelectItem value="Rechecking_Retotalling">Rechecking/Retotalling</SelectItem>
                                                <SelectItem value="Chance">Chance</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="year"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Year</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select Year" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="2025">2025</SelectItem>
                                                <SelectItem value="2024">2024</SelectItem>
                                                <SelectItem value="2023">2023</SelectItem>
                                                <SelectItem value="2022">2022</SelectItem>
                                                <SelectItem value="2021">2021</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="session"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Academic Session</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select Session" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="Fall">Fall</SelectItem>
                                                <SelectItem value="Spring">Spring</SelectItem>
                                                <SelectItem value="Winter">Winter</SelectItem>
                                                <SelectItem value="Annual">Annual</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="semester"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Year/Semester/Trimester</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select Semester" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="1st">First</SelectItem>
                                                <SelectItem value="2nd">Second</SelectItem>
                                                <SelectItem value="3rd">Third</SelectItem>
                                                <SelectItem value="4th">Fourth</SelectItem>
                                                <SelectItem value="5th">Fifth</SelectItem>
                                                <SelectItem value="6th">Sixth</SelectItem>
                                                <SelectItem value="7th">Seventh</SelectItem>
                                                <SelectItem value="8th">Eighth</SelectItem>
                                                <SelectItem value="9th">Ninth</SelectItem>
                                                <SelectItem value="10th">Tenth</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </div>

                        <FormField
                            control={form.control}
                            name="program"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Program</FormLabel>
                                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                                        <FormControl>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select Program" />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent>
                                            <SelectItem value="Bachelor of Business Administration">Bachelor of Business Administration</SelectItem>
                                            <SelectItem value="Bachelor of Computer Application">Bachelor of Computer Application</SelectItem>
                                        </SelectContent>
                                    </Select>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="delay"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Delay (seconds)</FormLabel>
                                    <FormControl>
                                        <Input
                                            type="number"
                                            min="0"
                                            step="0.1"
                                            {...field}
                                            onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : 0)}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        Delay between each request to allow manual verification.
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

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
                                            onChange={(e) => {
                                                onChange(e.target.files);
                                            }}
                                            {...rest}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        Upload an Excel file with headers in row 4. Required columns: 'Exam Roll No.' and either 'Date of Birth' or 'DD', 'MM', 'YYYY' columns.
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <Button type="submit" disabled={isLoading}>
                            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            {isLoading ? "Processing..." : "Start Automation"}
                        </Button>
                    </form>
                </Form>
            </div>
        </div>
    );
}
