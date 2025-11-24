"use client";

import { Utensils, Calendar } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const menuData = {
    monday: { breakfast: "Eggs & Toast", lunch: "Rice & Curry", dinner: "Pasta" },
    tuesday: { breakfast: "Pancakes", lunch: "Sandwiches", dinner: "Roast Chicken" },
};

export default function MessManagementPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold flex items-center gap-2">
                <Utensils className="h-8 w-8 text-primary" />
                Mess Management
            </h2>

            <Tabs defaultValue="menu" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="menu">Weekly Menu</TabsTrigger>
                    <TabsTrigger value="inventory">Kitchen Inventory</TabsTrigger>
                </TabsList>

                <TabsContent value="menu">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {Object.entries(menuData).map(([day, meals]) => (
                            <Card key={day}>
                                <CardHeader>
                                    <CardTitle className="capitalize">{day}</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-2">
                                    <div className="flex justify-between">
                                        <span className="text-muted-foreground">Breakfast:</span>
                                        <span className="font-medium">{meals.breakfast}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-muted-foreground">Lunch:</span>
                                        <span className="font-medium">{meals.lunch}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-muted-foreground">Dinner:</span>
                                        <span className="font-medium">{meals.dinner}</span>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </TabsContent>

                <TabsContent value="inventory">
                    <Card>
                        <CardContent className="p-6 text-center text-muted-foreground">
                            Kitchen inventory tracking interface would go here.
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}
