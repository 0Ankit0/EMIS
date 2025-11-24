"use client";

import Link from "next/link";
import { BarChart3, FileText, Download, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function ReportsDashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <BarChart3 className="h-8 w-8 text-primary" />
                    Reports
                </h2>
                <p className="text-muted-foreground">Generate and view system reports</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                    <Link href="/reports/academic"><FileText className="mr-2 h-5 w-5" />Academic Reports</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                    <Link href="/reports/financial"><TrendingUp className="mr-2 h-5 w-5" />Financial Reports</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                    <Link href="/reports/custom"><Download className="mr-2 h-5 w-5" />Custom Reports</Link>
                </Button>
            </div>
        </div>
    );
}
