"use client";

import { BookPlus, Save } from "lucide-react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

const bookSchema = z.object({
    isbn: z.string().min(1, "ISBN is required"),
    title: z.string().min(1, "Title is required"),
    author: z.string().min(1, "Author is required"),
    category: z.string(),
    copies: z.string().regex(/^\d+$/, "Must be a number"),
});

export default function AddBookPage() {
    const router = useRouter();

    const form = useForm<z.infer<typeof bookSchema>>({
        resolver: zodResolver(bookSchema),
        defaultValues: { isbn: "", title: "", author: "", category: "", copies: "" },
    });

    const onSubmit = async (data: z.infer<typeof bookSchema>) => {
        console.log("Adding book:", data);
        await new Promise(r => setTimeout(r, 1000));
        alert("Book added successfully!");
        router.push("/library/books");
    };

    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <BookPlus className="h-8 w-8 text-primary" />
                Add New Book
            </h2>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Book Information</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <FormField
                                control={form.control}
                                name="isbn"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>ISBN *</FormLabel>
                                        <FormControl>
                                            <Input placeholder="978-0-123-45678-9" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="title"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Title *</FormLabel>
                                        <FormControl>
                                            <Input placeholder="Introduction to Programming" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="author"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Author *</FormLabel>
                                        <FormControl>
                                            <Input placeholder="John Smith" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="category"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Category</FormLabel>
                                        <FormControl>
                                            <Input placeholder="Computer Science" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="copies"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Number of Copies *</FormLabel>
                                        <FormControl>
                                            <Input type="number" placeholder="10" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    <Button type="submit" className="w-full" size="lg">
                        <Save className="mr-2 h-4 w-4" />
                        Add Book
                    </Button>
                </form>
            </Form>
        </div>
    );
}
