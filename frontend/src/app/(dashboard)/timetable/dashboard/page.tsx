"use client";

import Link from "next/link";
import { Calendar, Plus, List, Users } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function TimetableDashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Calendar className="h-8 w-8 text-primary" />
                    Timetable Management
                </h2>
                <p className="text-muted-foreground">Manage class schedules and timetables</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                    <Link href="/timetable/view"><Calendar className="mr-2 h-5 w-5" />View Timetable</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                    <Link href="/timetable/create"><Plus className="mr-2 h-5 w-5" />Create Schedule</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                    <Link href="/timetable/classes"><List className="mr-2 h-5 w-5" />Class Schedules</Link>
                </Button>
            </div>
        </div>
    );
}
