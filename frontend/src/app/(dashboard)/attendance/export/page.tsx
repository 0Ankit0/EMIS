"use client";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Download, FileText, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";

const exportSchema = z.object({
    format: z.string().min(1, "Please select a format"),
    dateFrom: z.string().min(1, "Start date is required"),
    dateTo: z.string().min(1, "End date is required"),
    course: z.string(),
    includeStatistics: z.boolean(),
    includeSummary: z.boolean(),
});

export default function AttendanceExportPage() {
    const [isExporting, setIsExporting] = useState(false);

    const form = useForm<z.infer<typeof exportSchema>>({
        resolver: zodResolver(exportSchema),
        defaultValues: {
            format: "",
            dateFrom: "",
            dateTo: "",
            course: "all",
            includeStatistics: true,
            includeSummary: true,
        },
    });

    const onSubmit = async (data: z.infer<typeof exportSchema>) => {
        setIsExporting(true);
        try {
            // TODO: API call to generate export
            console.log("Exporting attendance data:", data);
            await new Promise(resolve => setTimeout(resolve, 2000));
            alert("Export generated successfully! Download will start shortly.");
        } catch (error) {
            console.error("Export error:", error);
            alert("Failed to generate export");
        } finally {
            setIsExporting(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Download className="h-8 w-8 text-primary" />
                    Export Attendance Data
                </h2>
                <p className="text-muted-foreground">Generate attendance reports in various formats</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Export Settings</CardTitle>
                    <CardDescription>
                        Configure your export preferences and download attendance data
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                            <FormField
                                control={form.control}
                                name="format"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Export Format *</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select format" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="pdf">
                                                    <div className="flex items-center gap-2">
                                                        <FileText className="h-4 w-4" />
                                                        PDF Document
                                                    </div>
                                                </SelectItem>
                                                <SelectItem value="excel">
                                                    <div className="flex items-center gap-2">
                                                        <FileText className="h-4 w-4" />
                                                        Excel Spreadsheet (.xlsx)
                                                    </div>
                                                </SelectItem>
                                                <SelectItem value="csv">
                                                    <div className="flex items-center gap-2">
                                                        <FileText className="h-4 w-4" />
                                                        CSV File
                                                    </div>
                                                </SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <div className="grid grid-cols-2 gap-4">
                                <FormField
                                    control={form.control}
                                    name="dateFrom"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>From Date *</FormLabel>
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
                                    name="dateTo"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>To Date *</FormLabel>
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
                            </div>

                            <FormField
                                control={form.control}
                                name="course"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Filter by Course</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="all">All Courses</SelectItem>
                                                <SelectItem value="CS101">CS101 - Intro to Programming</SelectItem>
                                                <SelectItem value="MATH201">MATH201 - Calculus II</SelectItem>
                                                <SelectItem value="ENG102">ENG102 - English Literature</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <div className="space-y-3">
                                <p className="text-sm font-medium">Include in Export</p>

                                <FormField
                                    control={form.control}
                                    name="includeStatistics"
                                    render={({ field }) => (
                                        <FormItem className="flex items-center space-x-2 space-y-0">
                                            <FormControl>
                                                <Checkbox
                                                    checked={field.value}
                                                    onCheckedChange={field.onChange}
                                                />
                                            </FormControl>
                                            <FormLabel className="font-normal cursor-pointer">
                                                Include statistics and summary
                                            </FormLabel>
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="includeSummary"
                                    render={({ field }) => (
                                        <FormItem className="flex items-center space-x-2 space-y-0">
                                            <FormControl>
                                                <Checkbox
                                                    checked={field.value}
                                                    onCheckedChange={field.onChange}
                                                />
                                            </FormControl>
                                            <FormLabel className="font-normal cursor-pointer">
                                                Include executive summary
                                            </FormLabel>
                                        </FormItem>
                                    )}
                                />
                            </div>

                            <Button type="submit" className="w-full" size="lg" disabled={isExporting}>
                                <Download className="mr-2 h-5 w-5" />
                                {isExporting ? "Generating Export..." : "Generate Export"}
                            </Button>
                        </form>
                    </Form>
                </CardContent>
            </Card>

            {/* Quick Export Options */}
            <Card>
                <CardHeader>
                    <CardTitle>Quick Export</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-2 gap-4">
                    <Button variant="outline" className="h-auto py-4 flex-col gap-2">
                        <Calendar className="h-6 w-6" />
                        <span className="font-semibold">Today's Report</span>
                        <span className="text-xs text-muted-foreground">PDF</span>
                    </Button>
                    <Button variant="outline" className="h-auto py-4 flex-col gap-2">
                        <Calendar className="h-6 w-6" />
                        <span className="font-semibold">This Week</span>
                        <span className="text-xs text-muted-foreground">Excel</span>
                    </Button>
                    <Button variant="outline" className="h-auto py-4 flex-col gap-2">
                        <Calendar className="h-6 w-6" />
                        <span className="font-semibold">This Month</span>
                        <span className="text-xs text-muted-foreground">PDF</span>
                    </Button>
                    <Button variant="outline" className="h-auto py-4 flex-col gap-2">
                        <Calendar className="h-6 w-6" />
                        <span className="font-semibold">This Semester</span>
                        <span className="text-xs text-muted-foreground">Excel</span>
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
