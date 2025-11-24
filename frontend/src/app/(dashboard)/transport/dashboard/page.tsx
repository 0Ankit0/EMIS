"use client";

import Link from "next/link";
import { Bus, MapPin, Users, Route } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function TransportDashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Bus className="h-8 w-8 text-primary" />
                    Transport Management
                </h2>
                <p className="text-muted-foreground">Manage vehicles, routes, and transportation</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                    <Link href="/transport/vehicles"><Bus className="mr-2 h-5 w-5" />Vehicles</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                    <Link href="/transport/routes"><Route className="mr-2 h-5 w-5" />Routes</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                    <Link href="/transport/students"><Users className="mr-2 h-5 w-5" />Student Assignment</Link>
                </Button>
            </div>
        </div>
    );
}
