"use client";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useRouter } from "next/navigation";
import { BookOpen, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const issueSchema = z.object({
    bookId: z.string().min(1, "Please select a book"),
    studentId: z.string().min(1, "Student ID is required"),
    issueDate: z.string().min(1, "Issue date is required"),
    dueDate: z.string().min(1, "Due date is required"),
});

export default function IssueBookPage() {
    const router = useRouter();
    const [isSubmitting, setIsSubmitting] = useState(false);

    const form = useForm<z.infer<typeof issueSchema>>({
        resolver: zodResolver(issueSchema),
        defaultValues: {
            bookId: "",
            studentId: "",
            issueDate: new Date().toISOString().split('T')[0],
            dueDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 14 days from now
        },
    });

    const onSubmit = async (data: z.infer<typeof issueSchema>) => {
        setIsSubmitting(true);
        try {
            console.log("Issuing book:", data);
            await new Promise(resolve => setTimeout(resolve, 1000));
            alert("Book issued successfully!");
            router.push("/library/issued");
        } catch (error) {
            console.error("Error issuing book:", error);
            alert("Failed to issue book");
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <BookOpen className="h-8 w-8 text-primary" />
                    Issue Book
                </h2>
                <p className="text-muted-foreground">Issue a book to a student</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Issue Details</CardTitle>
                    <CardDescription>Fill in the book issue information</CardDescription>
                </CardHeader>
                <CardContent>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                            <FormField
                                control={form.control}
                                name="bookId"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Book *</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select a book" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="1">Introduction to Programming - John Smith</SelectItem>
                                                <SelectItem value="2">Advanced Mathematics - Jane Doe</SelectItem>
                                                <SelectItem value="3">World History - Mike Johnson</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="studentId"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Student ID *</FormLabel>
                                        <FormControl>
                                            <Input placeholder="STU001" {...field} />
                                        </FormControl>
                                        <FormDescription>Enter the student's ID number</FormDescription>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <div className="grid grid-cols-2 gap-4">
                                <FormField
                                    control={form.control}
                                    name="issueDate"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Issue Date *</FormLabel>
                                            <FormControl>
                                                <input
                                                    type="date"
                                                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="dueDate"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Due Date *</FormLabel>
                                            <FormControl>
                                                <input
                                                    type="date"
                                                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormDescription>Typically 14 days</FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <Button type="submit" className="w-full" size="lg" disabled={isSubmitting}>
                                <Save className="mr-2 h-5 w-5" />
                                {isSubmitting ? "Issuing..." : "Issue Book"}
                            </Button>
                        </form>
                    </Form>
                </CardContent>
            </Card>
        </div>
    );
}
