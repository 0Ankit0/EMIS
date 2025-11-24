"use client";

import { Settings } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export default function CMSSettingsPage() {
    return (
        <div className="max-w-3xl mx-auto space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Settings className="h-8 w-8 text-primary" />
                    CMS Settings
                </h2>
                <p className="text-muted-foreground">Configure content management preferences</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Site Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Site Title</Label>
                        <Input defaultValue="EMIS - Education Management System" className="mt-2" />
                    </div>
                    <div>
                        <Label>Site Description</Label>
                        <Textarea defaultValue="Comprehensive education management platform" className="mt-2" />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>SEO Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Meta Keywords</Label>
                        <Input placeholder="education, management, school" className="mt-2" />
                    </div>
                    <div>
                        <Label>Google Analytics ID</Label>
                        <Input placeholder="UA-XXXXXXXXX-X" className="mt-2" />
                    </div>
                </CardContent>
            </Card>

            <Button className="w-full" size="lg">Save Settings</Button>
        </div>
    );
}
