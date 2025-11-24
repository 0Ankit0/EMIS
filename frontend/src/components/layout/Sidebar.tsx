"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { sidebarConfig } from "@/config/sidebar";

export function Sidebar() {
    const pathname = usePathname();

    // Determine which module we are in
    const moduleKey = Object.keys(sidebarConfig).find((key) =>
        pathname.startsWith(`/${key}`)
    ) || "default";

    const config = sidebarConfig[moduleKey];

    return (
        <div className="hidden border-r bg-gray-100/40 lg:block dark:bg-gray-800/40 w-[260px] fixed top-[65px] bottom-0 left-0 z-30">
            <ScrollArea className="h-full py-6 pl-4 pr-6">
                <div className="mb-6 px-2 flex items-center gap-2 text-lg font-semibold text-primary">
                    {config.icon && <config.icon className="h-6 w-6" />}
                    {config.title}
                </div>

                <div className="space-y-6">
                    {config.sections.map((section, index) => (
                        <div key={index} className="px-2">
                            {section.title && (
                                <h4 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                                    {section.title}
                                </h4>
                            )}
                            <div className="space-y-1">
                                {section.items.map((item) => (
                                    <Button
                                        key={item.href}
                                        variant={pathname === item.href ? "secondary" : "ghost"}
                                        className={cn(
                                            "w-full justify-start",
                                            pathname === item.href && "bg-secondary/50"
                                        )}
                                        asChild
                                    >
                                        <Link href={item.href}>
                                            {item.icon && <item.icon className="mr-2 h-4 w-4" />}
                                            {item.title}
                                        </Link>
                                    </Button>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </ScrollArea>
        </div>
    );
}
