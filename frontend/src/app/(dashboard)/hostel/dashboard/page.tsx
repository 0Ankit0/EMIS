"use client";

import Link from "next/link";
import { Home, Users, Bed, DollarSign } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function HostelDashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Home className="h-8 w-8 text-primary" />
                    Hostel Management
                </h2>
                <p className="text-muted-foreground">Manage hostel rooms, residents, and facilities</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                    <Link href="/hostel/rooms"><Bed className="mr-2 h-5 w-5" />Rooms</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                    <Link href="/hostel/residents"><Users className="mr-2 h-5 w-5" />Residents</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                    <Link href="/hostel/fees"><DollarSign className="mr-2 h-5 w-5" />Fees</Link>
                </Button>
            </div>
        </div>
    );
}
