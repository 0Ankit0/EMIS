"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { CalendarDays, CalendarPlus, List, Plus, Tag } from "lucide-react";

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> { }

export function CalendarSidebar({ className }: SidebarProps) {
    const pathname = usePathname();

    const sections = [
        {
            title: "Calendar",
            icon: CalendarDays,
            items: [
                { title: "Add Calendar", href: "/calendar/calendar/add", icon: Plus },
                { title: "List Calendars", href: "/calendar/calendar/list", icon: List },
            ]
        },
        {
            title: "Event",
            icon: CalendarPlus,
            items: [
                { title: "Add Event", href: "/calendar/event/add", icon: Plus },
                { title: "List Events", href: "/calendar/event/list", icon: List },
            ]
        },
        {
            title: "Category",
            icon: Tag,
            items: [
                { title: "Add Category", href: "/calendar/category/add", icon: Plus },
                { title: "List Categories", href: "/calendar/category/list", icon: List },
            ]
        }
    ];

    return (
        <div className={cn("pb-12", className)}>
            <div className="space-y-4 py-4">
                <div className="px-3 py-2">
                    <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                        Calendar Module
                    </h2>
                    <div className="space-y-4">
                        {sections.map((section) => (
                            <div key={section.title} className="px-3">
                                <h3 className="mb-2 px-4 text-sm font-semibold tracking-tight flex items-center">
                                    <section.icon className="mr-2 h-4 w-4" />
                                    {section.title}
                                </h3>
                                <div className="space-y-1">
                                    {section.items.map((item) => (
                                        <Button
                                            key={item.href}
                                            variant={pathname === item.href ? "secondary" : "ghost"}
                                            className="w-full justify-start pl-8"
                                            asChild
                                        >
                                            <Link href={item.href}>
                                                <item.icon className="mr-2 h-4 w-4" />
                                                {item.title}
                                            </Link>
                                        </Button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
