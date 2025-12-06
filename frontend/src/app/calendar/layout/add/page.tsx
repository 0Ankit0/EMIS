"use client";

import { LayoutView } from "@/components/calendar/layout/layout-view";
import { useSearchParams } from "next/navigation";

export default function LayoutAddPage() {
    const searchParams = useSearchParams();
    const id = searchParams.get("id");

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold tracking-tight">
                    {id ? "Edit Layout" : "Add Layout"}
                </h1>
            </div>
            <LayoutView layoutId={id ? parseInt(id) : undefined} mode="edit" />
        </div>
    );
}
