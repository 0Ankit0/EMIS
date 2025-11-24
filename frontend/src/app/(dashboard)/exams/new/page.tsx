"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useRouter } from "next/navigation";
import { FileText, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const examSchema = z.object({
    name: z.string().min(1, "Exam name is required"),
    course: z.string().min(1, "Course is required"),
    date: z.string().min(1, "Date is required"),
    duration: z.string().min(1, "Duration is required"),
    totalMarks: z.string().regex(/^\d+$/, "Must be a number"),
});

export default function CreateExamPage() {
    const router = useRouter();

    const form = useForm<z.infer<typeof examSchema>>({
        resolver: zodResolver(examSchema),
        defaultValues: { name: "", course: "", date: "", duration: "", totalMarks: "" },
    });

    const onSubmit = async (data: z.infer<typeof examSchema>) => {
        console.log("Creating exam:", data);
        await new Promise(r => setTimeout(r, 1000));
        alert("Exam created successfully!");
        router.push("/exams/list");
    };

    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <FileText className="h-8 w-8 text-primary" />
                Create Examination
            </h2>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Exam Details</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <FormField
                                control={form.control}
                                name="name"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Exam Name *</FormLabel>
                                        <FormControl>
                                            <Input placeholder="Mid-term Examination" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
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
                                                <SelectItem value="CS101">CS101 - Programming</SelectItem>
                                                <SelectItem value="MATH201">MATH201 - Calculus</SelectItem>
                                                <SelectItem value="ENG102">ENG102 - English</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <div className="grid grid-cols-2 gap-4">
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
                                    name="duration"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Duration *</FormLabel>
                                            <FormControl>
                                                <Input placeholder="3 hours" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                            <FormField
                                control={form.control}
                                name="totalMarks"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Total Marks *</FormLabel>
                                        <FormControl>
                                            <Input type="number" placeholder="100" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    <Button type="submit" className="w-full" size="lg">
                        <Save className="mr-2 h-4 w-4" />
                        Create Exam
                    </Button>
                </form>
            </Form>
        </div>
    );
}
