"use client";

import Link from "next/link";
import { GraduationCap, BookOpen, Video, FileText, Award, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function LMSDashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <GraduationCap className="h-8 w-8 text-primary" />
                    Learning Management System
                </h2>
                <p className="text-muted-foreground">Manage courses, lessons, and student progress</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                    <Link href="/lms/courses"><BookOpen className="mr-2 h-5 w-5" />Courses</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                    <Link href="/lms/lessons"><Video className="mr-2 h-5 w-5" />Lessons</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                    <Link href="/lms/assignments"><FileText className="mr-2 h-5 w-5" />Assignments</Link>
                </Button>
            </div>
        </div>
    );
}
