"use client";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useRouter } from "next/navigation";
import { Calendar, Save, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const meritListSchema = z.object({
    name: z.string().min(1, "Name is required"),
    program: z.string().min(1, "Program is required"),
    academic_year: z.string().min(1, "Academic year is required"),
    semester: z.string().min(1, "Semester is required"),
    cutoff_rank: z.string().min(1, "Cutoff rank is required").regex(/^\d+$/, "Must be a number"),
    cutoff_score: z.string().min(1, "Cutoff score is required").regex(/^\d+(\.\d+)?$/, "Must be a valid number"),
});

type MeritListFormData = z.infer<typeof meritListSchema>;

export default function CreateMeritListPage() {
    const router = useRouter();
    const [isSubmitting, setIsSubmitting] = useState(false);

    const form = useForm<MeritListFormData>({
        resolver: zodResolver(meritListSchema),
        defaultValues: {
            name: "",
            program: "",
            academic_year: "",
            semester: "",
            cutoff_rank: "",
            cutoff_score: "",
        },
    });

    const onSubmit = async (data: MeritListFormData) => {
        setIsSubmitting(true);
        try {
            // TODO: API call to create merit list
            console.log("Creating merit list:", data);
            await new Promise(resolve => setTimeout(resolve, 1000));
            alert("Merit list created successfully!");
            router.push("/admissions/merit-lists");
        } catch (error) {
            console.error("Error creating merit list:", error);
            alert("Failed to create merit list");
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Calendar className="h-8 w-8 text-primary" />
                    Create Merit List
                </h2>
                <p className="text-muted-foreground">Generate a merit list for admissions</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Merit List Details</CardTitle>
                    <CardDescription>
                        Enter the details to generate a merit list based on application scores
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                            <FormField
                                control={form.control}
                                name="name"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Merit List Name *</FormLabel>
                                        <FormControl>
                                            <Input placeholder="e.g., Fall 2025 - Computer Science" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <div className="grid grid-cols-2 gap-4">
                                <FormField
                                    control={form.control}
                                    name="program"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Program *</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select program" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    <SelectItem value="computer-science">Computer Science</SelectItem>
                                                    <SelectItem value="business-admin">Business Administration</SelectItem>
                                                    <SelectItem value="engineering">Engineering</SelectItem>
                                                    <SelectItem value="medicine">Medicine</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="academic_year"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Academic Year *</FormLabel>
                                            <FormControl>
                                                <Input placeholder="e.g., 2024-2025" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <FormField
                                control={form.control}
                                name="semester"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Semester *</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select semester" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="fall">Fall</SelectItem>
                                                <SelectItem value="spring">Spring</SelectItem>
                                                <SelectItem value="summer">Summer</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <div className="grid grid-cols-2 gap-4">
                                <FormField
                                    control={form.control}
                                    name="cutoff_rank"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Cutoff Rank *</FormLabel>
                                            <FormControl>
                                                <Input type="number" placeholder="e.g., 50" {...field} />
                                            </FormControl>
                                            <FormDescription>
                                                Top N candidates to select
                                            </FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="cutoff_score"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Cutoff Score *</FormLabel>
                                            <FormControl>
                                                <Input type="number" step="0.1" placeholder="e.g., 85.5" {...field} />
                                            </FormControl>
                                            <FormDescription>
                                                Minimum merit score
                                            </FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <div className="flex gap-3">
                                <Button
                                    type="button"
                                    variant="outline"
                                    className="flex-1"
                                    onClick={() => router.back()}
                                >
                                    <X className="mr-2 h-4 w-4" />
                                    Cancel
                                </Button>
                                <Button type="submit" className="flex-1" disabled={isSubmitting}>
                                    <Save className="mr-2 h-4 w-4" />
                                    {isSubmitting ? "Creating..." : "Create Merit List"}
                                </Button>
                            </div>
                        </form>
                    </Form>
                </CardContent>
            </Card>
        </div>
    );
}
