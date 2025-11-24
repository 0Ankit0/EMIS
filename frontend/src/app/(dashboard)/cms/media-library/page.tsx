"use client";

import { Image as ImageIcon, Upload, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

const mediaItems = [
    { id: 1, name: "sports-day.jpg", type: "image", size: "2.5 MB", date: "2025-01-20" },
    { id: 2, name: "announcement.pdf", type: "document", size: "1.2 MB", date: "2025-01-18" },
    { id: 3, name: "event-banner.png", type: "image", size: "3.1 MB", date: "2025-01-15" },
];

export default function MediaLibraryPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <ImageIcon className="h-8 w-8 text-primary" />
                        Media Library
                    </h2>
                    <p className="text-muted-foreground">Manage images and files</p>
                </div>
                <Button>
                    <Upload className="mr-2 h-4 w-4" />
                    Upload File
                </Button>
            </div>

            <Card>
                <CardContent className="p-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input placeholder="Search files..." className="pl-10" />
                    </div>
                </CardContent>
            </Card>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {mediaItems.map((item) => (
                    <Card key={item.id} className="cursor-pointer hover:shadow-lg transition">
                        <CardContent className="p-4">
                            <div className="aspect-square bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg mb-3 flex items-center justify-center">
                                <ImageIcon className="h-12 w-12 text-white opacity-50" />
                            </div>
                            <p className="font-semibold text-sm truncate">{item.name}</p>
                            <p className="text-xs text-muted-foreground">{item.size}</p>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
