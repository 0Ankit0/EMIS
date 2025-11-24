"use client";

import { Calendar, Plus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function CreateTimetablePage() {
    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Calendar className="h-8 w-8 text-primary" />
                    Create Timetable
                </h2>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Configuration</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-3 gap-4">
                    <div>
                        <label className="text-sm font-medium mb-2 block">Grade</label>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="Select Grade" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="10">Grade 10</SelectItem>
                                <SelectItem value="11">Grade 11</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div>
                        <label className="text-sm font-medium mb-2 block">Section</label>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="Select Section" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="A">Section A</SelectItem>
                                <SelectItem value="B">Section B</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div>
                        <label className="text-sm font-medium mb-2 block">Term</label>
                        <Select>
                            <SelectTrigger>
                                <SelectValue placeholder="Select Term" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="1">Term 1</SelectItem>
                                <SelectItem value="2">Term 2</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>

            <div className="grid grid-cols-5 gap-4">
                {["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].map((day) => (
                    <Card key={day} className="h-96">
                        <CardHeader className="py-3 bg-muted/50">
                            <CardTitle className="text-center text-base">{day}</CardTitle>
                        </CardHeader>
                        <CardContent className="p-2 space-y-2">
                            <Button variant="outline" className="w-full h-20 border-dashed">
                                <Plus className="h-4 w-4 mr-2" />
                                Add Period
                            </Button>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <div className="flex justify-end gap-4">
                <Button variant="outline">Cancel</Button>
                <Button>Save Timetable</Button>
            </div>
        </div>
    );
}
