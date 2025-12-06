"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Category } from "@/types/calendar";
import { EventList } from "./event-list";

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

interface ContentAreaProps {
    categories: Category[];
    mode: 'monthly' | 'category';
    selectedCategories: number[];
    onModeChange: (mode: 'monthly' | 'category') => void;
    onCategoryChange: (ids: number[]) => void;
    calendarId?: string;
}

export function ContentArea({
    categories,
    mode,
    selectedCategories,
    onModeChange,
    onCategoryChange,
    calendarId
}: ContentAreaProps) {

    const handleCategorySelect = (index: number, value: string) => {
        const newCategories = [...(selectedCategories || [])];
        // Ensure array has at least 2 elements if we are setting index 1
        if (index === 1 && newCategories.length < 1) newCategories[0] = -1; // Placeholder if skipped

        newCategories[index] = parseInt(value);

        // Clean up: if we have [id1, id2], great.
        // If we have [undefined, id2], that's fine, we just filter out non-numbers or handle it.
        // But let's just keep the array as is, and filter when rendering.
        onCategoryChange(newCategories);
    };

    const getCategory = (index: number) => {
        if (!selectedCategories || selectedCategories.length <= index) return undefined;
        return selectedCategories[index]?.toString();
    };

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="py-3 px-4">
                <Tabs value={mode} onValueChange={(v) => onModeChange(v as 'monthly' | 'category')}>
                    <TabsList className="grid w-full grid-cols-2">
                        <TabsTrigger value="monthly">Monthly</TabsTrigger>
                        <TabsTrigger value="category">Category</TabsTrigger>
                    </TabsList>
                </Tabs>
            </CardHeader>
            <CardContent className="flex-1 overflow-hidden flex flex-col p-0">
                {mode === 'monthly' ? (
                    <div className="h-full overflow-y-auto p-4">
                        <h3 className="text-lg font-semibold mb-4">All Events</h3>
                        <EventList mode="monthly" calendarId={calendarId} />
                    </div>
                ) : (
                    <div className="h-full flex flex-col divide-y">
                        {/* Section 1 */}
                        <div className="flex-1 flex flex-col overflow-hidden">
                            <div className="p-2 border-b bg-muted/20">
                                <Select
                                    value={getCategory(0)}
                                    onValueChange={(v) => handleCategorySelect(0, v)}
                                >
                                    <SelectTrigger className="h-8 w-full">
                                        <SelectValue placeholder="Select Category 1" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {categories.map(category => (
                                            <SelectItem key={category.id} value={category.id.toString()}>
                                                <div className="flex items-center gap-2">
                                                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: category.color }} />
                                                    {category.name}
                                                </div>
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="flex-1 overflow-y-auto p-2">
                                {getCategory(0) ? (
                                    <EventList
                                        mode="category"
                                        categoryIds={[parseInt(getCategory(0)!)]}
                                        calendarId={calendarId}
                                    />
                                ) : (
                                    <div className="text-sm text-muted-foreground text-center py-4">Select a category</div>
                                )}
                            </div>
                        </div>

                        {/* Section 2 */}
                        <div className="flex-1 flex flex-col overflow-hidden">
                            <div className="p-2 border-b bg-muted/20">
                                <Select
                                    value={getCategory(1)}
                                    onValueChange={(v) => handleCategorySelect(1, v)}
                                >
                                    <SelectTrigger className="h-8 w-full">
                                        <SelectValue placeholder="Select Category 2" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {categories.map(category => (
                                            <SelectItem key={category.id} value={category.id.toString()}>
                                                <div className="flex items-center gap-2">
                                                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: category.color }} />
                                                    {category.name}
                                                </div>
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="flex-1 overflow-y-auto p-2">
                                {getCategory(1) ? (
                                    <EventList
                                        mode="category"
                                        categoryIds={[parseInt(getCategory(1)!)]}
                                        calendarId={calendarId}
                                    />
                                ) : (
                                    <div className="text-sm text-muted-foreground text-center py-4">Select a category</div>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
