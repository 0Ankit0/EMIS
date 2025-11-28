"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Separator } from "@/components/ui/separator";

const sidebarNavItems = [
    {
        title: "Profile",
        href: "/settings/profile",
    },
    {
        title: "Theme",
        href: "/settings/theme",
    },
    {
        title: "Change Password",
        href: "/password-change",
    },
];

interface SettingsLayoutProps {
    children: React.ReactNode;
}

export default function SettingsLayout({ children }: SettingsLayoutProps) {
    return (
        <div className="container mx-auto space-y-6 px-4 py-10 pb-16">
            <div className="space-y-0.5">
                <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
                <p className="text-base text-muted-foreground">
                    Manage your account settings and preferences.
                </p>
            </div>
            <Separator className="my-6" />
            <div className="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
                <aside className="-mx-4 lg:w-1/5">
                    <nav className="flex space-x-2 lg:flex-col lg:space-x-0 lg:space-y-1">
                        {sidebarNavItems.map((item) => (
                            <SidebarNavItem key={item.href} item={item} />
                        ))}
                    </nav>
                </aside>
                <div className="flex-1 lg:max-w-2xl">{children}</div>
            </div>
        </div>
    );
}

function SidebarNavItem({ item }: { item: { title: string; href: string } }) {
    const pathname = usePathname();

    return (
        <Link
            href={item.href}
            className={cn(
                "inline-flex items-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
                "h-10 px-4 py-2",
                pathname === item.href
                    ? "bg-primary/10 text-primary hover:bg-primary/15"
                    : "hover:bg-accent hover:text-accent-foreground text-muted-foreground",
                "justify-start"
            )}
        >
            {item.title}
        </Link>
    );
}
