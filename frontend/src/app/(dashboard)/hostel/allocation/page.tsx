"use client";

import { UserPlus, ArrowRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function HostelAllocationPage() {
    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <UserPlus className="h-8 w-8 text-primary" />
                Room Allocation
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Allocate Room</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Student</Label>
                        <Select>
                            <SelectTrigger className="mt-2">
                                <SelectValue placeholder="Select Student" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="stu1">John Doe (Grade 10)</SelectItem>
                                <SelectItem value="stu2">Jane Smith (Grade 11)</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <Label>Room Type</Label>
                            <Select>
                                <SelectTrigger className="mt-2">
                                    <SelectValue placeholder="Select Type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="single">Single</SelectItem>
                                    <SelectItem value="double">Double</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div>
                            <Label>Room Number</Label>
                            <Select>
                                <SelectTrigger className="mt-2">
                                    <SelectValue placeholder="Select Room" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="101">101 (Available)</SelectItem>
                                    <SelectItem value="102">102 (1 bed available)</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <div>
                        <Label>Allocation Date</Label>
                        <Input type="date" className="mt-2" />
                    </div>

                    <Button className="w-full" size="lg">
                        Allocate Room
                        <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
