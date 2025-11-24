"use client";

import { MapPin, Navigation } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function TransportTrackingPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <MapPin className="h-8 w-8 text-primary" />
                    Live Tracking
                </h2>
                <div className="w-64">
                    <Select>
                        <SelectTrigger>
                            <SelectValue placeholder="Select Vehicle" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="bus-001">BUS-001 (Route A)</SelectItem>
                            <SelectItem value="bus-002">BUS-002 (Route B)</SelectItem>
                            <SelectItem value="van-001">VAN-001 (Staff)</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </div>

            <Card className="h-[600px] relative overflow-hidden">
                <CardContent className="p-0 h-full bg-slate-100 flex items-center justify-center">
                    <div className="text-center text-muted-foreground">
                        <Navigation className="h-16 w-16 mx-auto mb-4 opacity-50" />
                        <p className="text-lg font-medium">Map Interface Placeholder</p>
                        <p>Google Maps / Leaflet integration would go here</p>
                    </div>

                    <div className="absolute bottom-4 left-4 right-4 bg-white p-4 rounded-lg shadow-lg max-w-sm">
                        <div className="flex items-center justify-between mb-2">
                            <h4 className="font-bold">BUS-001</h4>
                            <span className="text-green-600 text-sm font-medium">Moving • 45 km/h</span>
                        </div>
                        <p className="text-sm text-muted-foreground">Next Stop: Central Station (5 mins)</p>
                        <p className="text-sm text-muted-foreground">Driver: John Doe</p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
