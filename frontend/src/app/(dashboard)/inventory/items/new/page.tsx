"use client";

import { PackagePlus, Save } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function AddInventoryItemPage() {
    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <PackagePlus className="h-8 w-8 text-primary" />
                Add New Item
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Item Details</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Item Name</Label>
                        <Input placeholder="e.g. Whiteboard Marker" className="mt-2" />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <Label>SKU / Code</Label>
                            <Input placeholder="INV-001" className="mt-2" />
                        </div>
                        <div>
                            <Label>Category</Label>
                            <Select>
                                <SelectTrigger className="mt-2">
                                    <SelectValue placeholder="Select Category" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="stationery">Stationery</SelectItem>
                                    <SelectItem value="furniture">Furniture</SelectItem>
                                    <SelectItem value="electronics">Electronics</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                        <div>
                            <Label>Quantity</Label>
                            <Input type="number" placeholder="0" className="mt-2" />
                        </div>
                        <div>
                            <Label>Min Level</Label>
                            <Input type="number" placeholder="10" className="mt-2" />
                        </div>
                        <div>
                            <Label>Unit Price</Label>
                            <Input type="number" placeholder="0.00" className="mt-2" />
                        </div>
                    </div>

                    <div>
                        <Label>Description</Label>
                        <Textarea placeholder="Item description..." className="mt-2" />
                    </div>

                    <Button className="w-full" size="lg">
                        <Save className="mr-2 h-4 w-4" />
                        Save Item
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
