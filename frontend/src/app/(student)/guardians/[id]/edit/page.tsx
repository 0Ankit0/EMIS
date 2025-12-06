"use client";

import { useState, useEffect } from "react";
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
} from "@/components/ui/form";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { getGuardian, updateGuardian } from "@/services/guardianService";
import { Loader2, ArrowLeft } from "lucide-react";
import Link from "next/link";

const formSchema = z.object({
    first_name: z.string().min(1, "First name is required"),
    last_name: z.string().min(1, "Last name is required"),
    relationship: z.string().min(1, "Relationship is required"),
    email: z.string().email("Invalid email address"),
    phone_number: z.string().min(1, "Phone number is required"),
    address: z.string().min(1, "Address is required"),
});

type FormValues = z.infer<typeof formSchema>;

export default function EditGuardianPage() {
    const router = useRouter();
    const params = useParams();
    const guardianId = params.id as string;
    const [isLoading, setIsLoading] = useState(false);
    const [loadingData, setLoadingData] = useState(true);

    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema) as any,
    });

    useEffect(() => {
        if (guardianId) {
            loadGuardian();
        }
    }, [guardianId]);

    const loadGuardian = async () => {
        try {
            setLoadingData(true);
            const guardian = await getGuardian(guardianId);
            form.reset({
                first_name: guardian.first_name,
                last_name: guardian.last_name,
                relationship: guardian.relationship,
                email: guardian.email,
                phone_number: guardian.phone_number,
                address: guardian.address,
            });
        } catch (error: any) {
            toast.error(error.message || "Failed to load guardian");
            router.push("/guardians");
        } finally {
            setLoadingData(false);
        }
    };

    async function onSubmit(values: FormValues) {
        setIsLoading(true);
        try {
            await updateGuardian(guardianId, values);
            toast.success("Guardian updated successfully");
            router.push("/guardians");
        } catch (error: any) {
            toast.error(error.message || "Failed to update guardian");
        } finally {
            setIsLoading(false);
        }
    }

    if (loadingData) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-4">
                <Link href="/guardians">
                    <Button variant="ghost" size="sm">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back to Guardians
                    </Button>
                </Link>
            </div>

            <div>
                <h3 className="text-2xl font-bold tracking-tight">Edit Guardian</h3>
                <p className="text-sm text-muted-foreground">
                    Update guardian information
                </p>
            </div>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Guardian Information</CardTitle>
                            <CardDescription>Personal and contact details</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid gap-4 md:grid-cols-2">
                                <FormField
                                    control={form.control}
                                    name="first_name"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>First Name</FormLabel>
                                            <FormControl>
                                                <Input {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={form.control}
                                    name="last_name"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Last Name</FormLabel>
                                            <FormControl>
                                                <Input {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <FormField
                                control={form.control}
                                name="relationship"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Relationship to Student</FormLabel>
                                        <FormControl>
                                            <Input placeholder="e.g., Father, Mother, Uncle" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <div className="grid gap-4 md:grid-cols-2">
                                <FormField
                                    control={form.control}
                                    name="email"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Email</FormLabel>
                                            <FormControl>
                                                <Input type="email" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={form.control}
                                    name="phone_number"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Phone Number</FormLabel>
                                            <FormControl>
                                                <Input {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <FormField
                                control={form.control}
                                name="address"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Address</FormLabel>
                                        <FormControl>
                                            <Input {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    <div className="flex justify-end gap-4">
                        <Link href="/guardians">
                            <Button type="button" variant="outline">
                                Cancel
                            </Button>
                        </Link>
                        <Button type="submit" disabled={isLoading}>
                            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            {isLoading ? "Updating..." : "Update Guardian"}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
