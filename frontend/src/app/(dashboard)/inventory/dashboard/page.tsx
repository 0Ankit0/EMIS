"use client";

import Link from "next/link";
import { Package, List, Plus, TrendingDown } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function InventoryDashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                    <Package className="h-8 w-8 text-primary" />
                    Inventory Management
                </h2>
                <p className="text-muted-foreground">Manage assets and track inventory</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button className="h-auto py-4 justify-start bg-blue-600 hover:bg-blue-700" asChild>
                    <Link href="/inventory/items"><List className="mr-2 h-5 w-5" />All Items</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-green-600 hover:bg-green-700" asChild>
                    <Link href="/inventory/add"><Plus className="mr-2 h-5 w-5" />Add Item</Link>
                </Button>
                <Button className="h-auto py-4 justify-start bg-red-600 hover:bg-red-700" asChild>
                    <Link href="/inventory/low-stock"><TrendingDown className="mr-2 h-5 w-5" />Low Stock</Link>
                </Button>
            </div>
        </div>
    );
}
