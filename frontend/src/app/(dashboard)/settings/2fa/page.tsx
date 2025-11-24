"use client";

import { ShieldCheck, Smartphone } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function TwoFactorSetupPage() {
    return (
        <div className="max-w-md mx-auto space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <ShieldCheck className="h-8 w-8 text-primary" />
                Two-Factor Authentication
            </h2>

            <Card>
                <CardHeader>
                    <CardTitle>Configure 2FA</CardTitle>
                    <CardDescription>
                        Add an extra layer of security to your account.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    <div className="flex justify-center p-4 bg-white rounded-lg border">
                        {/* Placeholder for QR Code */}
                        <div className="h-48 w-48 bg-gray-200 flex items-center justify-center text-muted-foreground">
                            QR Code
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label>Scan the QR code with your authenticator app</Label>
                        <p className="text-xs text-muted-foreground">
                            Use apps like Google Authenticator or Authy.
                        </p>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="code">Enter Verification Code</Label>
                        <div className="flex gap-2">
                            <Input id="code" placeholder="000000" className="text-center tracking-widest text-lg" maxLength={6} />
                        </div>
                    </div>

                    <Button className="w-full">
                        <Smartphone className="mr-2 h-4 w-4" />
                        Verify & Enable
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
