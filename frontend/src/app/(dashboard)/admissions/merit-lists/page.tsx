"use client";

import Link from "next/link";
import { Trophy, Plus, Eye, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// Mock data
const meritLists = [
    {
        id: 1,
        name: "BSCS Fall 2025 - First Merit List",
        program: "BS Computer Science",
        year: "2025",
        semester: "Fall",
        totalApplications: 150,
        cutoffRank: 50,
        isPublished: true,
        generatedAt: "Oct 20, 2025 10:00 AM",
    },
    {
        id: 2,
        name: "BBA Fall 2025 - First Merit List",
        program: "BBA",
        year: "2025",
        semester: "Fall",
        totalApplications: 80,
        cutoffRank: 40,
        isPublished: true,
        generatedAt: "Oct 21, 2025 11:30 AM",
    },
    {
        id: 3,
        name: "BSCS Fall 2025 - Second Merit List",
        program: "BS Computer Science",
        year: "2025",
        semester: "Fall",
        totalApplications: 150,
        cutoffRank: 80,
        isPublished: false,
        generatedAt: "Oct 25, 2025 09:15 AM",
    },
];

export default function MeritListsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <Trophy className="h-8 w-8 text-primary" />
                        Merit Lists
                    </h2>
                    <p className="text-muted-foreground">View and manage merit lists</p>
                </div>
                <Button asChild className="bg-blue-600 hover:bg-blue-700">
                    <Link href="/admissions/merit-lists/new">
                        <Plus className="mr-2 h-4 w-4" /> Generate Merit List
                    </Link>
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {meritLists.map((list) => (
                    <Card key={list.id} className="hover:shadow-lg transition-shadow">
                        <CardContent className="p-6">
                            <div className="flex items-start justify-between mb-4">
                                <div>
                                    <h3 className="text-xl font-bold text-gray-800 line-clamp-1" title={list.name}>
                                        {list.name}
                                    </h3>
                                    <p className="text-muted-foreground text-sm mt-1">{list.program}</p>
                                </div>
                                {list.isPublished ? (
                                    <Badge className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">Published</Badge>
                                ) : (
                                    <Badge variant="secondary">Draft</Badge>
                                )}
                            </div>

                            <div className="space-y-2 mb-6">
                                <div className="flex justify-between text-sm">
                                    <span className="text-muted-foreground">Year:</span>
                                    <span className="font-semibold">{list.year}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-muted-foreground">Semester:</span>
                                    <span className="font-semibold">{list.semester}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-muted-foreground">Total Applications:</span>
                                    <span className="font-semibold">{list.totalApplications}</span>
                                </div>
                                {list.cutoffRank && (
                                    <div className="flex justify-between text-sm">
                                        <span className="text-muted-foreground">Cutoff Rank:</span>
                                        <span className="font-semibold">{list.cutoffRank}</span>
                                    </div>
                                )}
                            </div>

                            <div className="flex space-x-2">
                                <Button asChild className="flex-1 bg-blue-600 hover:bg-blue-700">
                                    <Link href={`/admissions/merit-lists/${list.id}`}>
                                        <Eye className="mr-2 h-4 w-4" /> View
                                    </Link>
                                </Button>
                                {!list.isPublished && (
                                    <Button className="flex-1 bg-green-600 hover:bg-green-700">
                                        <Check className="mr-2 h-4 w-4" /> Publish
                                    </Button>
                                )}
                            </div>

                            <p className="text-xs text-muted-foreground mt-4 text-center">
                                Generated on {list.generatedAt}
                            </p>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
