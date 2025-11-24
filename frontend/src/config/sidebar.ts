import {
    LayoutDashboard,
    FileText,
    PlusCircle,
    Clock,
    FileSignature,
    ClipboardList,
    BarChart3
} from "lucide-react";

export type SidebarItem = {
    title: string;
    href: string;
    icon?: any;
    variant?: "default" | "ghost";
};

export type SidebarSection = {
    title?: string;
    items: SidebarItem[];
};

export type ModuleSidebar = {
    title: string;
    icon?: any;
    sections: SidebarSection[];
};

export const sidebarConfig: Record<string, ModuleSidebar> = {
    admissions: {
        title: "Admissions",
        icon: FileSignature,
        sections: [
            {
                items: [
                    {
                        title: "Dashboard",
                        href: "/admissions/dashboard",
                        icon: LayoutDashboard,
                    },
                ],
            },
            {
                title: "Applications",
                items: [
                    {
                        title: "All Applications",
                        href: "/admissions/applications",
                        icon: ClipboardList,
                    },
                    {
                        title: "New Application",
                        href: "/admissions/applications/new",
                        icon: PlusCircle,
                    },
                    {
                        title: "Pending Review",
                        href: "/admissions/applications/pending",
                        icon: Clock,
                    },
                ],
            },
            {
                title: "Management",
                items: [
                    {
                        title: "Application Forms",
                        href: "/admissions/forms",
                        icon: FileText,
                    },
                    {
                        title: "Requirements",
                        href: "/admissions/requirements",
                        icon: ClipboardList,
                    },
                    {
                        title: "Reports",
                        href: "/admissions/reports",
                        icon: BarChart3,
                    },
                ],
            },
        ],
    },
    // Add other modules here as we migrate them
    default: {
        title: "EMIS",
        sections: [
            {
                items: [
                    {
                        title: "Dashboard",
                        href: "/dashboard",
                        icon: LayoutDashboard,
                    },
                ],
            },
        ],
    },
};
