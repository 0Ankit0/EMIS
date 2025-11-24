"use client";

import { LogOut, ArrowRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function HostelCheckOutPage() {
    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <LogOut className="h-8 w-8 text-primary" />
                Student Check-Out
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Process Check-Out</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Student</Label>
                        <Select>
                            <SelectTrigger className="mt-2">
                                <SelectValue placeholder="Select Student" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="stu1">John Doe (Room 101)</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <Label>Check-Out Date</Label>
                            <Input type="date" className="mt-2" />
                        </div>
                        <div>
                            <Label>Reason</Label>
                            <Select>
                                <SelectTrigger className="mt-2">
                                    <SelectValue placeholder="Select Reason" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="end">End of Term</SelectItem>
                                    <SelectItem value="transfer">Transfer</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <div>
                        <Label>Clearance Check</Label>
                        <div className="mt-2 space-y-2">
                            <div className="flex items-center gap-2">
                                <input type="checkbox" id="keys" className="h-4 w-4" />
                                <label htmlFor="keys">Keys Returned</label>
                            </div>
                            <div className="flex items-center gap-2">
                                <input type="checkbox" id="damage" className="h-4 w-4" />
                                <label htmlFor="damage">No Room Damage</label>
                            </div>
                            <div className="flex items-center gap-2">
                                <input type="checkbox" id="dues" className="h-4 w-4" />
                                <label htmlFor="dues">No Pending Dues</label>
                            </div>
                        </div>
                    </div>

                    <Button className="w-full" variant="destructive" size="lg">
                        Complete Check-Out
                        <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
