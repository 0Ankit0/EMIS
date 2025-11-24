"use client";

import { Plus, BookOpen } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function CreateCoursePage() {
    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <BookOpen className="h-8 w-8 text-primary" />
                Create New Course
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Course Details</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Course Name</Label>
                        <Input placeholder="e.g. Introduction to Computer Science" className="mt-2" />
                    </div>
                    <div>
                        <Label>Course Code</Label>
                        <Input placeholder="e.g. CS101" className="mt-2" />
                    </div>
                    <div>
                        <Label>Description</Label>
                        <Textarea placeholder="Course description..." className="mt-2" />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <Label>Credits</Label>
                            <Input type="number" placeholder="3" className="mt-2" />
                        </div>
                        <div>
                            <Label>Department</Label>
                            <Select>
                                <SelectTrigger className="mt-2">
                                    <SelectValue placeholder="Select Department" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="cs">Computer Science</SelectItem>
                                    <SelectItem value="math">Mathematics</SelectItem>
                                    <SelectItem value="eng">Engineering</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Button className="w-full" size="lg">
                <Plus className="mr-2 h-4 w-4" />
                Create Course
            </Button>
        </div>
    );
}
