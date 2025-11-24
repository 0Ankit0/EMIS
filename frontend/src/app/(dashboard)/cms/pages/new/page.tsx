"use client";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useRouter } from "next/navigation";
import { FileText, Save, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const pageSchema = z.object({
    title: z.string().min(1, "Title is required"),
    slug: z.string().min(1, "Slug is required").regex(/^[a-z0-9-]+$/, "Only lowercase letters, numbers, and hyphens"),
    content: z.string().min(1, "Content is required"),
    metaDescription: z.string().max(160, "Max 160 characters"),
    status: z.string(),
});

export default function CreatePagePage() {
    const router = useRouter();
    const [isSubmitting, setIsSubmitting] = useState(false);

    const form = useForm<z.infer<typeof pageSchema>>({
        resolver: zodResolver(pageSchema),
        defaultValues: {
            title: "",
            slug: "",
            content: "",
            metaDescription: "",
            status: "draft",
        },
    });

    const generateSlug = (title: string) => {
        return title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
    };

    const onSubmit = async (data: z.infer<typeof pageSchema>) => {
        setIsSubmitting(true);
        try {
            console.log("Creating page:", data);
            await new Promise(resolve => setTimeout(resolve, 1000));
            alert("Page created successfully!");
            router.push("/cms/pages");
        } catch (error) {
            console.error("Error creating page:", error);
            alert("Failed to create page");
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <FileText className="h-8 w-8 text-primary" />
                    Create New Page
                </h2>
                <p className="text-muted-foreground">Add a new page to your website</p>
            </div>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Page Details</CardTitle>
                            <CardDescription>Basic information about the page</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <FormField
                                control={form.control}
                                name="title"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Page Title *</FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="About Us"
                                                {...field}
                                                onChange={(e) => {
                                                    field.onChange(e);
                                                    if (!form.getValues("slug")) {
                                                        form.setValue("slug", generateSlug(e.target.value));
                                                    }
                                                }}
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="slug"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>URL Slug *</FormLabel>
                                        <FormControl>
                                            <Input placeholder="about-us" {...field} />
                                        </FormControl>
                                        <FormDescription>
                                            URL-friendly version (lowercase, hyphens only)
                                        </FormDescription>
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
                                                    <SelectValue />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="draft">Draft</SelectItem>
                                                <SelectItem value="published">Published</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Content</CardTitle>
                            <CardDescription>The main content of your page</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <FormField
                                control={form.control}
                                name="content"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Page Content *</FormLabel>
                                        <FormControl>
                                            <Textarea
                                                placeholder="Enter your page content here..."
                                                className="min-h-[300px]"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>SEO Settings</CardTitle>
                            <CardDescription>Optimize for search engines</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <FormField
                                control={form.control}
                                name="metaDescription"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Meta Description</FormLabel>
                                        <FormControl>
                                            <Textarea
                                                placeholder="Brief description for search engines..."
                                                className="min-h-[80px]"
                                                maxLength={160}
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormDescription>
                                            {field.value.length}/160 characters
                                        </FormDescription>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

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
                            {isSubmitting ? "Creating..." : "Create Page"}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
