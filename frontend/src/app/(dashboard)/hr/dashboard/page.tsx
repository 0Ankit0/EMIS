"use client";

import Link from "next/link";
import { Users, Briefcase, DollarSign, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function HRDashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Briefcase className="h-8 w-8 text-primary" />
                    Human Resources
                </h2>
                <p className="text-muted-foreground">Manage employees, payroll, and leave requests</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                    <Link href="/hr/employees"><Users className="mr-2 h-5 w-5" />Employees</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                    <Link href="/hr/payroll"><DollarSign className="mr-2 h-5 w-5" />Payroll</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                    <Link href="/hr/leave"><Calendar className="mr-2 h-5 w-5" />Leave Management</Link>
                </Button>
            </div>
        </div>
    );
}
