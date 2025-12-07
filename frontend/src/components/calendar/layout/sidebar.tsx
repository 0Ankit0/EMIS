"use client";

import { Calendar } from "@/components/ui/calendar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Category, Event } from "@/types/calendar";
import { eachMonthOfInterval, format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isToday } from "date-fns";
import { cn } from "@/lib/utils";
import { useCalendar } from "@/hooks/use-calendar-queries";

import { useQuery } from "@tanstack/react-query";
import { getAuthToken } from "@/lib/auth-utils";
import { CALENDAR_ENDPOINTS } from "@/lib/api-constants";

interface SidebarProps {
    categories: Category[];
    selectedCategories: number[];
    onCategoryChange: (ids: number[]) => void;
    calendarId?: string;
}

async function getYearlyEvents(year: number, calendarId?: string): Promise<Event[]> {
    const token = getAuthToken();
    const startDate = `${year}-01-01`;
    const endDate = `${year}-12-31`;
    const params = new URLSearchParams({
        start_date_from: startDate,
        start_date_to: endDate
    });
    if (calendarId) {
        params.append('calendar', calendarId);
    }

    const res = await fetch(`${CALENDAR_ENDPOINTS.EVENTS}?${params.toString()}`, {
        headers: { Authorization: `Token ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch events");
    return res.json();
}

export function Sidebar({ categories, selectedCategories, onCategoryChange, calendarId }: SidebarProps) {
    const handleCheck = (id: number, checked: boolean) => {
        if (checked) {
            onCategoryChange([...selectedCategories, id]);
        } else {
            onCategoryChange(selectedCategories.filter(c => c !== id));
        }
    };

    const { data: calendar } = useCalendar(calendarId || "");

    // Determine date range
    // If calendarId is present and we have calendar data, use its start/end dates
    // Otherwise (e.g. layout config), use current year or a placeholder range
    const currentYear = new Date().getFullYear();
    let start = new Date(currentYear, 0, 1);
    let end = new Date(currentYear, 11, 31);

    if (calendarId && calendar) {
        start = new Date(calendar.start_date);
        end = new Date(calendar.end_date);
    }

    const months = eachMonthOfInterval({ start, end });

    // Fetch events for the determined range
    // We need to pass the actual start/end dates to the API
    const { data: events = [] } = useQuery({
        queryKey: ["calendar-events-range", start.toISOString(), end.toISOString(), calendarId],
        queryFn: async () => {
            const token = getAuthToken();
            const params = new URLSearchParams({
                start_date_from: format(start, 'yyyy-MM-dd'),
                start_date_to: format(end, 'yyyy-MM-dd')
            });
            if (calendarId) {
                params.append('calendar', calendarId);
            }
            const res = await fetch(`${CALENDAR_ENDPOINTS.EVENTS}?${params.toString()}`, {
                headers: { Authorization: `Token ${token}` },
            });
            if (!res.ok) throw new Error("Failed to fetch events");
            return res.json();
        },
        enabled: !!start && !!end // Only fetch if we have valid dates
    });

    // Create a map of date -> color
    const dateColors: { [key: string]: string } = {};
    events.forEach((event: Event) => {
        const dateStr = event.start_date; // YYYY-MM-DD
        // Only color if category is selected? Or always?
        // User requirement: "color-code calendar dates in the sidebar based on event category colors"
        // If we want to filter coloring by selected categories in sidebar:
        // if (selectedCategories.includes(event.category?.id)) ...
        // But usually sidebar selection filters the *content area*, not necessarily the sidebar calendar itself.
        // Let's assume it shows all, or maybe filters. Let's show all for now to be safe, or match user intent.
        // Actually, if I uncheck a category, I probably expect it to disappear from the calendar view too?
        // Let's stick to showing all for now, as the sidebar selection is primarily for the "Content Area" filter.
        if (event.category_color) {
            dateColors[dateStr] = event.category_color;
        }
    });

    return (
        <div className="flex flex-col gap-4 h-full overflow-hidden">
            <div className="flex-1 overflow-y-auto pr-2">
                <div className="grid grid-cols-3 gap-4">
                    {months.map((month) => (
                        <div key={month.toString()} className="border rounded-md p-2 text-xs">
                            <div className="font-semibold text-center mb-2">
                                {format(month, "MMMM yyyy")}
                            </div>
                            <div className="grid grid-cols-7 gap-1 text-center text-[10px] text-muted-foreground mb-1">
                                <div>Su</div><div>Mo</div><div>Tu</div><div>We</div><div>Th</div><div>Fr</div><div>Sa</div>
                            </div>
                            <div className="grid grid-cols-7 gap-1 text-center">
                                {eachDayOfInterval({
                                    start: startOfMonth(month),
                                    end: endOfMonth(month)
                                }).map((day) => {
                                    const dateStr = format(day, "yyyy-MM-dd");
                                    const color = dateColors[dateStr];
                                    const isCurrentMonth = isSameMonth(day, month);

                                    return (
                                        <div
                                            key={day.toString()}
                                            className={cn(
                                                "aspect-square flex items-center justify-center rounded-full w-5 h-5 mx-auto",
                                                isToday(day) && "bg-primary text-primary-foreground",
                                                !isCurrentMonth && "opacity-30"
                                            )}
                                            style={{
                                                backgroundColor: color,
                                                color: color ? '#fff' : undefined
                                            }}
                                        >
                                            {format(day, "d")}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="border-t pt-4">
                <h3 className="font-semibold mb-2">Categories</h3>
                <div className="space-y-2 max-h-[200px] overflow-y-auto">
                    {categories.map(category => (
                        <div key={category.id} className="flex items-center space-x-2">
                            <Checkbox
                                id={`cat-${category.id}`}
                                checked={selectedCategories.includes(category.id)}
                                onCheckedChange={(checked) => handleCheck(category.id, checked as boolean)}
                            />
                            <label
                                htmlFor={`cat-${category.id}`}
                                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 flex items-center gap-2"
                            >
                                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: category.color }} />
                                {category.name}
                            </label>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
