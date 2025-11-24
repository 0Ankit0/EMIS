"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useRouter } from "next/navigation";
import { Image as ImageIcon, Save, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

const gallerySchema = z.object({
    title: z.string().min(1, "Title is required"),
    description: z.string(),
    date: z.string().min(1, "Date is required"),
});

export default function CreateGalleryPage() {
    const router = useRouter();

    const form = useForm<z.infer<typeof gallerySchema>>({
        resolver: zodResolver(gallerySchema),
        defaultValues: {
            title: "",
            description: "",
            date: new Date().toISOString().split('T')[0],
        },
    });

    const onSubmit = async (data: z.infer<typeof gallerySchema>) => {
        console.log("Creating gallery:", data);
        await new Promise(r => setTimeout(r, 1000));
        alert("Gallery created!");
        router.push("/cms/galleries");
    };

    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <ImageIcon className="h-8 w-8 text-primary" />
                Create Gallery
            </h2>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Gallery Information</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <FormField
                                control={form.control}
                                name="title"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Gallery Title *</FormLabel>
                                        <FormControl>
                                            <Input placeholder="Sports Day 2024" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="description"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Description</FormLabel>
                                        <FormControl>
                                            <Textarea className="min-h-[100px]" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="date"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Event Date *</FormLabel>
                                        <FormControl>
                                            <input type="date" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Upload Images</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
                                <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                                <p className="text-sm text-muted-foreground mb-2">
                                    Drag & drop images here, or click to select
                                </p>
                                <Button type="button" variant="outline">
                                    Select Images
                                </Button>
                            </div>
                        </CardContent>
                    </Card>

                    <Button type="submit" className="w-full">
                        <Save className="mr-2 h-4 w-4" />
                        Create Gallery
                    </Button>
                </form>
            </Form>
        </div>
    );
}
