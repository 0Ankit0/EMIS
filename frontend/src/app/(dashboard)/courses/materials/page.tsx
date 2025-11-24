"use client";

import { FolderOpen } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const materialsData = [
    { id: 1, title: "Lecture Slides - Week 1", type: "PDF", size: "2.5 MB", uploaded: "2025-01-15" },
    { id: 2, title: "Assignment Instructions", type: "PDF", size: "500 KB", uploaded: "2025-01-16" },
    { id: 3, title: "Video Tutorial", type: "MP4", size: "45 MB", uploaded: "2025-01-17" },
];

export default function CourseMaterialsPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <FolderOpen className="h-8 w-8 text-primary" />
                Course Materials
            </h2>

            <div className="grid grid-cols-1 gap-4">
                {materialsData.map((material) => (
                    <Card key={material.id}>
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <div>
                                    <CardTitle className="text-lg">{material.title}</CardTitle>
                                    <p className="text-sm text-muted-foreground mt-1">
                                        {material.type} • {material.size} • Uploaded {material.uploaded}
                                    </p>
                                </div>
                                <Button variant="outline" size="sm">Download</Button>
                            </div>
                        </CardHeader>
                    </Card>
                ))}
            </div>
        </div>
    );
}
