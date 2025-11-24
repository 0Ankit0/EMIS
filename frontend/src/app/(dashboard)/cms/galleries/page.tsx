"use client";

import { useState } from "react";
import Link from "next/link";
import { Image as ImageIcon, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const galleriesData = [
    { id: 1, title: "Sports Day 2024", images: 45, date: "2024-12-15", cover: null },
    { id: 2, title: "Science Fair", images: 32, date: "2024-12-20", cover: null },
    { id: 3, title: "Cultural Fest", images: 68, date: "2024-11-10", cover: null },
];

export default function GalleriesListPage() {
    const [galleries] = useState(galleriesData);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <ImageIcon className="h-8 w-8 text-primary" />
                        Galleries
                    </h2>
                    <p className="text-muted-foreground">Manage photo galleries and albums</p>
                </div>
                <Link href="/cms/galleries/new">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        New Gallery
                    </Button>
                </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {galleries.map((gallery) => (
                    <Card key={gallery.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                        <div className="h-48 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                            <ImageIcon className="h-16 w-16 text-white opacity-50" />
                        </div>
                        <CardHeader>
                            <CardTitle>{gallery.title}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="flex justify-between items-center mb-4">
                                <span className="text-sm text-muted-foreground">{gallery.images} images</span>
                                <span className="text-sm text-muted-foreground">{gallery.date}</span>
                            </div>
                            <div className="flex gap-2">
                                <Link href={`/cms/galleries/${gallery.id}`} className="flex-1">
                                    <Button variant="outline" size="sm" className="w-full">View</Button>
                                </Link>
                                <Link href={`/cms/galleries/${gallery.id}/edit`} className="flex-1">
                                    <Button size="sm" className="w-full">Edit</Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
