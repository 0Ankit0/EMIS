"use client";

import { useParams } from "next/navigation";
import { Image as ImageIcon, Upload, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const galleryData = {
    title: "Sports Day 2024",
    description: "Photos from our annual sports day event",
    date: "2024-12-15",
    images: [
        { id: 1, url: null, caption: "Opening Ceremony" },
        { id: 2, url: null, caption: "Track Events" },
        { id: 3, url: null, caption: "Award Distribution" },
    ],
};

export default function GalleryDetailPage() {
    const params = useParams();

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <ImageIcon className="h-8 w-8 text-primary" />
                        {galleryData.title}
                    </h2>
                    <p className="text-muted-foreground mt-1">{galleryData.description}</p>
                </div>
                <Button>
                    <Upload className="mr-2 h-4 w-4" />
                    Upload Images
                </Button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {galleryData.images.map((image) => (
                    <Card key={image.id} className="group relative overflow-hidden">
                        <div className="aspect-square bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                            <ImageIcon className="h-16 w-16 text-white opacity-50" />
                        </div>
                        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition flex items-center justify-center opacity-0 group-hover:opacity-100">
                            <Button variant="destructive" size="sm">
                                <X className="h-4 w-4" />
                            </Button>
                        </div>
                        <CardContent className="p-3">
                            <p className="text-sm font-semibold truncate">{image.caption}</p>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
