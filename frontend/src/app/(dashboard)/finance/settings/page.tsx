"use client";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Settings, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";

const settingsSchema = z.object({
    currency: z.string(),
    lateFeePercentage: z.string().regex(/^\d+(\.\d+)?$/, "Must be a valid number"),
    gracePeriod: z.string().regex(/^\d+$/, "Must be a number"),
    paymentMethods: z.array(z.string()).min(1, "Select at least one payment method"),
    autoReminders: z.boolean(),
    reminderFrequency: z.string(),
    invoicePrefix: z.string().min(1, "Prefix is required"),
    taxRate: z.string().regex(/^\d+(\.\d+)?$/, "Must be a valid number"),
});

export default function FinanceSettingsPage() {
    const [isSaving, setIsSaving] = useState(false);

    const form = useForm<z.infer<typeof settingsSchema>>({
        resolver: zodResolver(settingsSchema),
        defaultValues: {
            currency: "USD",
            lateFeePercentage: "5",
            gracePeriod: "7",
            paymentMethods: ["credit_card", "bank_transfer"],
            autoReminders: true,
            reminderFrequency: "weekly",
            invoicePrefix: "INV",
            taxRate: "0",
        },
    });

    const onSubmit = async (data: z.infer<typeof settingsSchema>) => {
        setIsSaving(true);
        try {
            // TODO: API call to save settings
            console.log("Saving settings:", data);
            await new Promise(resolve => setTimeout(resolve, 1000));
            alert("Settings saved successfully!");
        } catch (error) {
            console.error("Error saving settings:", error);
            alert("Failed to save settings");
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Settings className="h-8 w-8 text-primary" />
                    Finance Settings
                </h2>
                <p className="text-muted-foreground">Configure financial system preferences</p>
            </div>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    {/* General Settings */}
                    <Card>
                        <CardHeader>
                            <CardTitle>General Settings</CardTitle>
                            <CardDescription>Basic configuration for the finance module</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <FormField
                                    control={form.control}
                                    name="currency"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Currency</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    <SelectItem value="USD">USD ($)</SelectItem>
                                                    <SelectItem value="EUR">EUR (€)</SelectItem>
                                                    <SelectItem value="GBP">GBP (£)</SelectItem>
                                                    <SelectItem value="INR">INR (₹)</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="invoicePrefix"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Invoice Prefix</FormLabel>
                                            <FormControl>
                                                <Input placeholder="INV" {...field} />
                                            </FormControl>
                                            <FormDescription>Prefix for invoice numbers</FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <FormField
                                control={form.control}
                                name="taxRate"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Tax Rate (%)</FormLabel>
                                        <FormControl>
                                            <Input type="number" step="0.1" placeholder="0" {...field} />
                                        </FormControl>
                                        <FormDescription>Default tax percentage for fees</FormDescription>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    {/* Late Fee Settings */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Late Fee Settings</CardTitle>
                            <CardDescription>Configure penalties for overdue payments</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <FormField
                                    control={form.control}
                                    name="lateFeePercentage"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Late Fee Percentage</FormLabel>
                                            <FormControl>
                                                <Input type="number" step="0.1" placeholder="5" {...field} />
                                            </FormControl>
                                            <FormDescription>Percentage charged on overdue amount</FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="gracePeriod"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Grace Period (days)</FormLabel>
                                            <FormControl>
                                                <Input type="number" placeholder="7" {...field} />
                                            </FormControl>
                                            <FormDescription>Days before late fee applies</FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                        </CardContent>
                    </Card>

                    {/* Payment Methods */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Payment Methods</CardTitle>
                            <CardDescription>Enable accepted payment methods</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <FormField
                                control={form.control}
                                name="paymentMethods"
                                render={() => (
                                    <FormItem>
                                        <div className="space-y-3">
                                            {[
                                                { id: "credit_card", label: "Credit/Debit Card" },
                                                { id: "bank_transfer", label: "Bank Transfer" },
                                                { id: "cash", label: "Cash" },
                                                { id: "check", label: "Check" },
                                                { id: "online", label: "Online Payment Gateway" },
                                            ].map((method) => (
                                                <FormField
                                                    key={method.id}
                                                    control={form.control}
                                                    name="paymentMethods"
                                                    render={({ field }) => (
                                                        <FormItem className="flex items-center space-x-2 space-y-0">
                                                            <FormControl>
                                                                <Checkbox
                                                                    checked={field.value?.includes(method.id)}
                                                                    onCheckedChange={(checked) => {
                                                                        return checked
                                                                            ? field.onChange([...field.value, method.id])
                                                                            : field.onChange(
                                                                                field.value?.filter((value) => value !== method.id)
                                                                            );
                                                                    }}
                                                                />
                                                            </FormControl>
                                                            <FormLabel className="font-normal cursor-pointer">
                                                                {method.label}
                                                            </FormLabel>
                                                        </FormItem>
                                                    )}
                                                />
                                            ))}
                                        </div>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    {/* Reminder Settings */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Reminder Settings</CardTitle>
                            <CardDescription>Configure automatic payment reminders</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <FormField
                                control={form.control}
                                name="autoReminders"
                                render={({ field }) => (
                                    <FormItem className="flex items-center justify-between space-y-0">
                                        <div>
                                            <FormLabel>Enable Automatic Reminders</FormLabel>
                                            <FormDescription>Send automated payment reminders to students</FormDescription>
                                        </div>
                                        <FormControl>
                                            <Checkbox
                                                checked={field.value}
                                                onCheckedChange={field.onChange}
                                            />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />

                            <FormField
                                control={form.control}
                                name="reminderFrequency"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Reminder Frequency</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="daily">Daily</SelectItem>
                                                <SelectItem value="weekly">Weekly</SelectItem>
                                                <SelectItem value="biweekly">Bi-weekly</SelectItem>
                                                <SelectItem value="monthly">Monthly</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </CardContent>
                    </Card>

                    <Button type="submit" size="lg" className="w-full" disabled={isSaving}>
                        <Save className="mr-2 h-5 w-5" />
                        {isSaving ? "Saving..." : "Save Settings"}
                    </Button>
                </form>
            </Form>
        </div>
    );
}
