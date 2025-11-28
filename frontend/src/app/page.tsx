"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Calendar, Shield, Settings, BookOpen, Users, BarChart3 } from "lucide-react";
import { getAuthToken } from "@/lib/auth-utils";
import { useRouter } from "next/navigation";

// Module configuration - in a real app, this would come from the backend based on user permissions
const modules = [
  {
    id: "calendar",
    name: "Calendar",
    description: "Manage events, schedules, and academic calendar",
    icon: Calendar,
    href: "/calendar",
    gradient: "bg-gradient-primary",
  },
  {
    id: "admin",
    name: "Administration",
    description: "Administrative tools and user management",
    icon: Shield,
    href: "/admin",
    gradient: "bg-gradient-primary",
  },
  {
    id: "students",
    name: "Students",
    description: "Student information and records management",
    icon: Users,
    href: "/students",
    gradient: "bg-gradient-primary",
  },
  {
    id: "courses",
    name: "Courses",
    description: "Course catalog and curriculum management",
    icon: BookOpen,
    href: "/courses",
    gradient: "bg-gradient-primary",
  },
  {
    id: "reports",
    name: "Reports",
    description: "Analytics and reporting dashboard",
    icon: BarChart3,
    href: "/reports",
    gradient: "bg-gradient-primary",
  },
  {
    id: "settings",
    name: "Settings",
    description: "System configuration and preferences",
    icon: Settings,
    href: "/settings/theme",
    gradient: "bg-gradient-primary",
  },
];

// Force re-compile
export default function Home() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      router.push("/login");
      return;
    }

    // In a real app, fetch user and their accessible modules from the backend
    setUser({ username: "User" });
    setLoading(false);
  }, [router]);

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Header */}
      <div className="mb-12 space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">
          Welcome to EMIS
        </h1>
        <p className="text-xl text-muted-foreground">
          Select a module to get started
        </p>
      </div>

      {/* Module Grid */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {modules.map((module) => {
          const Icon = module.icon;
          return (
            <Link key={module.id} href={module.href}>
              <Card className="group h-full transition-all duration-300 hover:shadow-lg hover:shadow-primary/10 hover:-translate-y-1">
                <CardHeader>
                  <div className={`mb-4 inline-flex h-16 w-16 items-center justify-center rounded-2xl ${module.gradient} p-3 shadow-lg transition-transform group-hover:scale-110`}>
                    <Icon className="h-8 w-8 text-white" />
                  </div>
                  <CardTitle className="text-xl">{module.name}</CardTitle>
                  <CardDescription className="text-base">
                    {module.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center text-sm font-medium text-primary">
                    Open module
                    <svg
                      className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </div>
                </CardContent>
              </Card>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
