"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Shield, Smartphone, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function Setup2FAPage() {
    const router = useRouter();
    const [step, setStep] = useState<"setup" | "verify">("setup");
    const [verificationCode, setVerificationCode] = useState("");
    const [qrCode] = useState("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0id2hpdGUiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxNiIgZmlsbD0iIzY2NiI+UVIgQ29kZTwvdGV4dD48L3N2Zz4=");
    const [secretKey] = useState("JBSWY3DPEHPK3PXP");

    const handleVerify = () => {
        if (verificationCode.length === 6) {
            // TODO: Verify with backend
            alert("2FA enabled successfully!");
            router.push("/profile");
        }
    };

    return (
        <div className="flex items-center justify-center min-h-[calc(100vh-200px)]">
            <Card className="w-full max-w-2xl">
                <CardHeader>
                    <div className="flex items-center gap-2">
                        <Shield className="h-6 w-6 text-primary" />
                        <CardTitle>Two-Factor Authentication</CardTitle>
                    </div>
                    <CardDescription>
                        Add an extra layer of security to your account
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    {step === "setup" ? (
                        <div className="space-y-6">
                            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                <h3 className="font-semibold text-blue-900 mb-2">Step 1: Install Authenticator App</h3>
                                <p className="text-sm text-blue-800">
                                    Install an authenticator app like Google Authenticator or Authy on your smartphone
                                </p>
                            </div>

                            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                                <h3 className="font-semibold text-green-900 mb-2">Step 2: Scan QR Code</h3>
                                <p className="text-sm text-green-800 mb-4">
                                    Open your authenticator app and scan this QR code
                                </p>
                                <div className="flex justify-center">
                                    <img src={qrCode} alt="QR Code" className="w-48 h-48 border-2 border-gray-300 rounded" />
                                </div>
                            </div>

                            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                                <h3 className="font-semibold text-purple-900 mb-2">Manual Entry</h3>
                                <p className="text-sm text-purple-800 mb-2">
                                    Can't scan? Enter this code manually:
                                </p>
                                <code className="bg-white px-3 py-2 rounded border border-purple-300 text-sm font-mono">
                                    {secretKey}
                                </code>
                            </div>

                            <Button onClick={() => setStep("verify")} className="w-full">
                                <Smartphone className="mr-2 h-4 w-4" />
                                Continue to Verification
                            </Button>
                        </div>
                    ) : (
                        <div className="space-y-6">
                            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                                <h3 className="font-semibold text-yellow-900 mb-2">Step 3: Verify</h3>
                                <p className="text-sm text-yellow-800">
                                    Enter the 6-digit code from your authenticator app
                                </p>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="code">Verification Code</Label>
                                <Input
                                    id="code"
                                    type="text"
                                    maxLength={6}
                                    placeholder="000000"
                                    value={verificationCode}
                                    onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, ""))}
                                    className="text-center text-2xl tracking-widest font-mono"
                                />
                            </div>

                            <div className="flex gap-3">
                                <Button variant="outline" className="flex-1" onClick={() => setStep("setup")}>
                                    Back
                                </Button>
                                <Button
                                    className="flex-1"
                                    onClick={handleVerify}
                                    disabled={verificationCode.length !== 6}
                                >
                                    <CheckCircle className="mr-2 h-4 w-4" />
                                    Enable 2FA
                                </Button>
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
