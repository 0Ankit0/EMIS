"use client";

import Link from "next/link";
import { Bell, Mail, MessageSquare, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function NotificationsDashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Bell className="h-8 w-8 text-primary" />
                    Notifications
                </h2>
                <p className="text-muted-foreground">Manage alerts and messaging</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                    <Link href="/notifications/all"><Bell className="mr-2 h-5 w-5" />All Notifications</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                    <Link href="/notifications/send"><Mail className="mr-2 h-5 w-5" />Send Message</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                    <Link href="/notifications/settings"><Settings className="mr-2 h-5 w-5" />Settings</Link>
                </Button>
            </div>
        </div>
    );
}
