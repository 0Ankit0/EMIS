"use client";

import { LogIn, ArrowRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function HostelCheckInPage() {
    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <LogIn className="h-8 w-8 text-primary" />
                Student Check-In
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>New Check-In</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Student</Label>
                        <Select>
                            <SelectTrigger className="mt-2">
                                <SelectValue placeholder="Select Student" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="stu1">John Doe</SelectItem>
                                <SelectItem value="stu2">Jane Smith</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <Label>Room</Label>
                            <Input value="101" disabled className="mt-2" />
                        </div>
                        <div>
                            <Label>Check-In Date</Label>
                            <Input type="date" className="mt-2" />
                        </div>
                    </div>

                    <div>
                        <Label>Inventory Items Issued</Label>
                        <div className="mt-2 space-y-2">
                            <div className="flex items-center gap-2">
                                <input type="checkbox" id="keys" className="h-4 w-4" />
                                <label htmlFor="keys">Room Keys</label>
                            </div>
                            <div className="flex items-center gap-2">
                                <input type="checkbox" id="mattress" className="h-4 w-4" />
                                <label htmlFor="mattress">Mattress</label>
                            </div>
                        </div>
                    </div>

                    <Button className="w-full" size="lg">
                        Complete Check-In
                        <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
