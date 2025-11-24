"use client";

import Link from "next/link";
import { FileText, Plus, Megaphone, Calendar as CalendarIcon, Image, Menu, File } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// Mock data
const stats = {
    totalPages: 45,
    publishedPages: 38,
    totalAnnouncements: 12,
    activeAnnouncements: 8,
    totalEvents: 25,
    upcomingEvents: 15,
    totalGalleries: 10,
    totalMenus: 6,
};

const recentPages = [
    { id: 1, title: "About Us", status: "published", createdAt: "Oct 20, 2025" },
    { id: 2, title: "Academic Programs", status: "published", createdAt: "Oct 19, 2025" },
    { id: 3, title: "Contact Information", status: "draft", createdAt: "Oct 18, 2025" },
];

const upcomingEvents = [
    { id: 1, title: "Annual Sports Day", startDate: "Nov 15, 2025", eventType: "Sports" },
    { id: 2, title: "Parent Teacher Meeting", startDate: "Nov 10, 2025", eventType: "Academic" },
    { id: 3, title: "Science Fair 2025", startDate: "Dec 01, 2025", eventType: "Competition" },
];

export default function CMSDashboardPage() {
    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <FileText className="h-8 w-8 text-primary" />
                    Content Management System
                </h2>
                <p className="text-muted-foreground">Manage pages, announcements, events, galleries, and navigation menus</p>
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card className="border-l-4 border-blue-500 hover:shadow-lg transition-all">
                    <CardContent className="p-6">
                        <div className="flex justify-between items-start">
                            <div className="flex-grow">
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Total Pages</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.totalPages}</h3>
                                <p className="text-sm text-green-600 mt-1">{stats.publishedPages} published</p>
                            </div>
                            <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center">
                                <File className="h-6 w-6 text-blue-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-green-500 hover:shadow-lg transition-all">
                    <CardContent className="p-6">
                        <div className="flex justify-between items-start">
                            <div className="flex-grow">
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Announcements</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.totalAnnouncements}</h3>
                                <p className="text-sm text-green-600 mt-1">{stats.activeAnnouncements} active</p>
                            </div>
                            <div className="w-14 h-14 bg-green-100 rounded-lg flex items-center justify-center">
                                <Megaphone className="h-6 w-6 text-green-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-purple-500 hover:shadow-lg transition-all">
                    <CardContent className="p-6">
                        <div className="flex justify-between items-start">
                            <div className="flex-grow">
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Events</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.totalEvents}</h3>
                                <p className="text-sm text-green-600 mt-1">{stats.upcomingEvents} upcoming</p>
                            </div>
                            <div className="w-14 h-14 bg-purple-100 rounded-lg flex items-center justify-center">
                                <CalendarIcon className="h-6 w-6 text-purple-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-l-4 border-yellow-500 hover:shadow-lg transition-all">
                    <CardContent className="p-6">
                        <div className="flex justify-between items-start">
                            <div className="flex-grow">
                                <p className="text-sm text-muted-foreground font-semibold uppercase">Galleries</p>
                                <h3 className="text-3xl font-bold mt-2">{stats.totalGalleries}</h3>
                                <p className="text-sm text-gray-500 mt-1">{stats.totalMenus} menu items</p>
                            </div>
                            <div className="w-14 h-14 bg-yellow-100 rounded-lg flex items-center justify-center">
                                <Image className="h-6 w-6 text-yellow-600" />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Quick Actions */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        Quick Actions
                    </CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-5 gap-4">
                    <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                        <Link href="/cms/pages/new">
                            <Plus className="mr-2 h-5 w-5" />
                            New Page
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                        <Link href="/cms/announcements/new">
                            <Plus className="mr-2 h-5 w-5" />
                            New Announcement
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-purple-600 hover:bg-purple-700" asChild>
                        <Link href="/cms/events/new">
                            <Plus className="mr-2 h-5 w-5" />
                            New Event
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-yellow-600 hover:bg-yellow-700" asChild>
                        <Link href="/cms/galleries/new">
                            <Plus className="mr-2 h-5 w-5" />
                            New Gallery
                        </Link>
                    </Button>
                    <Button className="h-auto py-4 justify-start bg-red-600 hover:bg-red-700" asChild>
                        <Link href="/cms/menus/new">
                            <Plus className="mr-2 h-5 w-5" />
                            New Menu
                        </Link>
                    </Button>
                </CardContent>
            </Card>

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Recent Pages */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <File className="h-5 w-5 text-blue-600" />
                            Recent Pages
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {recentPages.length > 0 ? (
                            <div className="space-y-3">
                                {recentPages.map((page) => (
                                    <div key={page.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                                        <div className="flex-grow">
                                            <Link href={`/cms/pages/${page.id}`} className="font-semibold text-gray-800 hover:text-primary">
                                                {page.title}
                                            </Link>
                                            <p className="text-xs text-muted-foreground mt-1">{page.createdAt}</p>
                                        </div>
                                        <Badge variant={page.status === "published" ? "default" : "secondary"}>
                                            {page.status}
                                        </Badge>
                                    </div>
                                ))}
                                <div className="text-center mt-4">
                                    <Link href="/cms/pages" className="text-primary hover:text-primary/80 font-semibold text-sm">
                                        View All Pages →
                                    </Link>
                                </div>
                            </div>
                        ) : (
                            <div className="text-center py-8 text-muted-foreground">No pages yet</div>
                        )}
                    </CardContent>
                </Card>

                {/* Upcoming Events */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <CalendarIcon className="h-5 w-5 text-purple-600" />
                            Upcoming Events
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {upcomingEvents.length > 0 ? (
                            <div className="space-y-3">
                                {upcomingEvents.map((event) => (
                                    <div key={event.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                                        <div className="flex-grow">
                                            <Link href={`/cms/events/${event.id}`} className="font-semibold text-gray-800 hover:text-primary">
                                                {event.title}
                                            </Link>
                                            <p className="text-xs text-muted-foreground mt-1">{event.startDate}</p>
                                        </div>
                                        <Badge className="bg-purple-100 text-purple-800 hover:bg-purple-200 border-purple-200">
                                            {event.eventType}
                                        </Badge>
                                    </div>
                                ))}
                                <div className="text-center mt-4">
                                    <Link href="/cms/events" className="text-primary hover:text-primary/80 font-semibold text-sm">
                                        View All Events →
                                    </Link>
                                </div>
                            </div>
                        ) : (
                            <div className="text-center py-8 text-muted-foreground">No upcoming events</div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
