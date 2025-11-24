"use client";

import Link from "next/link";
import { UserPlus, Info, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";

export default function RegisterPage() {
    return (
        <Card className="border-none shadow-2xl">
            <CardHeader className="bg-green-600 text-white rounded-t-xl p-6">
                <CardTitle className="flex items-center gap-2 text-xl">
                    <UserPlus className="h-6 w-6" />
                    Register
                </CardTitle>
            </CardHeader>
            <CardContent className="p-6 space-y-6">
                <Alert className="bg-blue-50 text-blue-800 border-blue-200">
                    <Info className="h-4 w-4" />
                    <AlertDescription>
                        Registration is currently handled by administrators only. Please contact your institution.
                    </AlertDescription>
                </Alert>

                <Button asChild variant="outline" className="w-full">
                    <Link href="/login">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back to Login
                    </Link>
                </Button>
            </CardContent>
        </Card>
    );
}
