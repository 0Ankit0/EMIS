"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { GraduationCap, Users, UserPlus, List, ChevronDown } from "lucide-react";
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion";

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> { }

export function StudentSidebar({ className }: SidebarProps) {
    const pathname = usePathname();

    const sections = [
        {
            title: "Students",
            icon: GraduationCap,
            value: "students",
            items: [
                { title: "All Students", href: "/students", icon: List },
                { title: "Add Student", href: "/students/new", icon: UserPlus },
            ]
        },
        {
            title: "Guardians",
            icon: Users,
            value: "guardians",
            items: [
                { title: "All Guardians", href: "/guardians", icon: List },
                { title: "Add Guardian", href: "/guardians/new", icon: UserPlus },
            ]
        },
    ];

    return (
        <div className={cn("pb-12", className)}>
            <div className="space-y-4 py-4">
                <div className="px-3 py-2">
                    <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                        Student Module
                    </h2>
                    <Accordion type="single" collapsible className="w-full" defaultValue="students">
                        {sections.map((section) => (
                            <AccordionItem value={section.value} key={section.value} className="border-none">
                                <AccordionTrigger className="px-4 py-2 hover:no-underline hover:bg-accent hover:text-accent-foreground rounded-md">
                                    <div className="flex items-center text-sm font-semibold">
                                        <section.icon className="mr-2 h-4 w-4" />
                                        {section.title}
                                    </div>
                                </AccordionTrigger>
                                <AccordionContent>
                                    <div className="space-y-1 pt-1 pl-4">
                                        {section.items.map((item) => (
                                            <Button
                                                key={item.href}
                                                variant={pathname === item.href ? "secondary" : "ghost"}
                                                className="w-full justify-start pl-8 h-9"
                                                asChild
                                            >
                                                <Link href={item.href}>
                                                    <item.icon className="mr-2 h-4 w-4" />
                                                    {item.title}
                                                </Link>
                                            </Button>
                                        ))}
                                    </div>
                                </AccordionContent>
                            </AccordionItem>
                        ))}
                    </Accordion>
                </div>
            </div>
        </div>
    );
}
