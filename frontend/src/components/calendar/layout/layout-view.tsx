"use client";

import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getAuthToken } from "@/lib/auth-utils";
import { CALENDAR_ENDPOINTS } from "@/lib/api-constants";
import { CalendarLayout, Category } from "@/types/calendar";
import { Sidebar } from "./sidebar";
import { ContentArea } from "./content-area";
import { Button } from "@/components/ui/button";
import { Save } from "lucide-react";
import { toast } from "sonner";

async function getLayouts(): Promise<CalendarLayout[]> {
    const token = getAuthToken();
    const res = await fetch(CALENDAR_ENDPOINTS.LAYOUTS, {
        headers: { Authorization: `Token ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch layouts");
    return res.json();
}

async function getCategories(): Promise<Category[]> {
    const token = getAuthToken();
    const res = await fetch(CALENDAR_ENDPOINTS.CATEGORIES, {
        headers: { Authorization: `Token ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch categories");
    return res.json();
}

async function saveLayout(layout: Partial<CalendarLayout>) {
    const token = getAuthToken();
    const url = layout.id
        ? `${CALENDAR_ENDPOINTS.LAYOUTS}${layout.id}/`
        : CALENDAR_ENDPOINTS.LAYOUTS;

    const method = layout.id ? "PUT" : "POST";

    const res = await fetch(url, {
        method,
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`
        },
        body: JSON.stringify(layout),
    });

    if (!res.ok) throw new Error("Failed to save layout");
    return res.json();
}

import { Input } from "@/components/ui/input";
import { useRouter } from "next/navigation";

interface LayoutViewProps {
    calendarId?: string;
    layoutId?: number;
    mode?: 'view' | 'edit';
}

export function LayoutView({ calendarId, layoutId, mode = 'view' }: LayoutViewProps) {
    const queryClient = useQueryClient();
    const router = useRouter();
    const [name, setName] = useState("My Custom Layout");
    const [config, setConfig] = useState<CalendarLayout['configuration']>({
        left_sidebar_categories: [],
        right_content_mode: 'monthly',
        right_content_categories: [],
    });

    // If viewing a specific calendar, we might want to load the active layout
    // If editing a layout, we load that specific layout
    const { data: layouts } = useQuery({
        queryKey: ["calendar-layouts"],
        queryFn: getLayouts,
    });

    const { data: categories } = useQuery({
        queryKey: ["calendar-categories"],
        queryFn: getCategories,
    });

    useEffect(() => {
        if (layouts) {
            if (layoutId) {
                const layout = layouts.find(l => l.id === layoutId);
                if (layout) {
                    setName(layout.name);
                    setConfig(layout.configuration);
                }
            } else if (mode === 'view' && layouts.length > 0) {
                // Load active layout for view mode
                const active = layouts.find(l => l.active) || layouts[0];
                setConfig(active.configuration);
            }
        }
    }, [layouts, layoutId, mode]);

    const mutation = useMutation({
        mutationFn: saveLayout,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["calendar-layouts"] });
            toast.success("Layout saved successfully");
            if (mode === 'edit') {
                router.push('/calendar/layout/list');
            }
        },
        onError: () => {
            toast.error("Failed to save layout");
        }
    });

    const handleSave = () => {
        mutation.mutate({
            id: layoutId,
            name: name,
            active: layoutId ? undefined : false, // Don't change active status on edit, default false on create
            configuration: config,
        });
    };

    if (!categories) return <div>Loading...</div>;

    return (
        <div className="flex h-[calc(100vh-100px)] gap-6">
            <div className="w-[70%] flex flex-col gap-4">
                <div className="flex flex-col gap-4">
                    <div className="flex justify-between items-center">
                        <h2 className="text-xl font-bold">Layout Config</h2>
                        {mode === 'edit' && (
                            <Button onClick={handleSave} size="sm">
                                <Save className="w-4 h-4 mr-2" />
                                Save
                            </Button>
                        )}
                    </div>
                    {mode === 'edit' && (
                        <Input
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Layout Name"
                        />
                    )}
                </div>
                <Sidebar
                    categories={categories}
                    selectedCategories={config.left_sidebar_categories}
                    onCategoryChange={(ids) => setConfig({ ...config, left_sidebar_categories: ids })}
                    calendarId={calendarId}
                />
            </div>
            <div className="w-[30%]">
                <ContentArea
                    categories={categories}
                    mode={config.right_content_mode}
                    selectedCategories={config.right_content_categories}
                    onModeChange={(mode) => setConfig({ ...config, right_content_mode: mode })}
                    onCategoryChange={(ids) => setConfig({ ...config, right_content_categories: ids })}
                    calendarId={calendarId}
                />
            </div>
        </div>
    );
}
