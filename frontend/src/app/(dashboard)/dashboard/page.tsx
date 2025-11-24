import Link from "next/link";
import {
    FileSignature,
    Users,
    BookOpen,
    Building2,
    Wallet,
    Library,
    Calendar,
    Bus,
    Shield,
    BarChart3,
    LayoutDashboard,
    User
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const modules = [
    {
        title: "Admissions",
        description: "Manage applications, merit lists, and enrollments",
        icon: FileSignature,
        href: "/admissions/dashboard",
        color: "text-blue-600",
        bg: "bg-blue-100",
    },
    {
        title: "Students",
        description: "Student profiles, academic records, and history",
        icon: Users,
        href: "/students/dashboard",
        color: "text-green-600",
        bg: "bg-green-100",
    },
    {
        title: "Academics",
        description: "Courses, classes, and curriculum management",
        icon: BookOpen,
        href: "/academics/dashboard",
        color: "text-purple-600",
        bg: "bg-purple-100",
    },
    {
        title: "HR & Faculty",
        description: "Staff management, payroll, and attendance",
        icon: Building2,
        href: "/hr/dashboard",
        color: "text-orange-600",
        bg: "bg-orange-100",
    },
    {
        title: "Finance",
        description: "Fee collection, expenses, and financial reports",
        icon: Wallet,
        href: "/finance/dashboard",
        color: "text-teal-600",
        bg: "bg-teal-100",
    },
    {
        title: "Library",
        description: "Book inventory, issuing, and cataloging",
        icon: Library,
        href: "/library/dashboard",
        color: "text-indigo-600",
        bg: "bg-indigo-100",
    },
    {
        title: "Timetable",
        description: "Class scheduling and resource allocation",
        icon: Calendar,
        href: "/timetable/dashboard",
        color: "text-pink-600",
        bg: "bg-pink-100",
    },
    {
        title: "Transport",
        description: "Route management and vehicle tracking",
        icon: Bus,
        href: "/transport/dashboard",
        color: "text-yellow-600",
        bg: "bg-yellow-100",
    },
];

export default function DashboardHome() {
    // Mock user data
    const user = {
        name: "Admin User",
        role: "System Administrator",
    };

    // Mock stats
    const stats = [
        { label: "Total Students", value: "1,250", icon: Users, color: "text-blue-600", bg: "bg-blue-100", border: "border-blue-500" },
        { label: "Total Faculty", value: "120", icon: Users, color: "text-green-600", bg: "bg-green-100", border: "border-green-500" },
        { label: "Active Courses", value: "45", icon: BookOpen, color: "text-purple-600", bg: "bg-purple-100", border: "border-purple-500" },
        { label: "Pending Applications", value: "12", icon: FileSignature, color: "text-yellow-600", bg: "bg-yellow-100", border: "border-yellow-500" },
    ];

    return (
        <div className="space-y-8">
            {/* Welcome Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b pb-6">
                <div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent mb-2">
                        Welcome back, {user.name}!
                    </h1>
                    <p className="text-muted-foreground flex items-center gap-2">
                        <Shield className="h-4 w-4" />
                        {user.role}
                    </p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" asChild>
                        <Link href="/profile">
                            <User className="mr-2 h-4 w-4" />
                            Profile
                        </Link>
                    </Button>
                </div>
            </div>

            {/* Quick Stats */}
            <div>
                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <BarChart3 className="h-5 w-5 text-primary" />
                    Quick Statistics
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {stats.map((stat, index) => (
                        <Card key={index} className={`border-l-4 shadow-sm hover:shadow-md transition-all ${stat.border}`}>
                            <CardContent className="p-6 flex justify-between items-start">
                                <div>
                                    <p className="text-muted-foreground text-sm font-semibold uppercase tracking-wide mb-2">{stat.label}</p>
                                    <h3 className="text-3xl font-bold">{stat.value}</h3>
                                </div>
                                <div className={`w-12 h-12 rounded-lg ${stat.bg} flex items-center justify-center`}>
                                    <stat.icon className={`h-6 w-6 ${stat.color}`} />
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>

            {/* Modules Grid */}
            <div>
                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <LayoutDashboard className="h-5 w-5 text-primary" />
                    Your Modules
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {modules.map((module) => (
                        <Link key={module.title} href={module.href} className="block group">
                            <Card className="h-full hover:shadow-lg transition-all border-2 border-transparent hover:border-primary/20 hover:-translate-y-1">
                                <CardHeader className="pb-4 text-center">
                                    <div className={`w-16 h-16 mx-auto rounded-full ${module.bg} flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-6 transition-transform duration-300`}>
                                        <module.icon className={`h-8 w-8 ${module.color}`} />
                                    </div>
                                    <CardTitle className="text-lg group-hover:text-primary transition-colors">
                                        {module.title}
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="text-center">
                                    <p className="text-sm text-muted-foreground">
                                        {module.description}
                                    </p>
                                </CardContent>
                            </Card>
                        </Link>
                    ))}
                </div>
            </div>
        </div>
    );
}
