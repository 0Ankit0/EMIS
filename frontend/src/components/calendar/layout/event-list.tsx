"use client";

import { useQuery } from "@tanstack/react-query";
import { getAuthToken } from "@/lib/auth-utils";
import { CALENDAR_ENDPOINTS } from "@/lib/api-constants";
import { Event } from "@/types/calendar";
import { format } from "date-fns";
import { Badge } from "@/components/ui/badge";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

interface EventListProps {
    mode: 'monthly' | 'category';
    categoryIds?: number[];
    calendarId?: string;
}

async function getEvents(params: URLSearchParams): Promise<Event[]> {
    const token = getAuthToken();
    const res = await fetch(`${CALENDAR_ENDPOINTS.EVENTS}?${params.toString()}`, {
        headers: { Authorization: `Token ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch events");
    return res.json();
}

export function EventList({ mode, categoryIds, calendarId }: EventListProps) {
    const params = new URLSearchParams();
    if (mode === 'category' && categoryIds && categoryIds.length > 0) {
        // Assuming the backend supports filtering by multiple categories, 
        // or we filter client side. For now, let's try passing them.
        // If backend expects ?category=1&category=2, we append multiple times.
        categoryIds.forEach(id => params.append('category', id.toString()));
    }
    if (calendarId) {
        params.append('calendar', calendarId);
    }

    const { data: events, isLoading } = useQuery({
        queryKey: ["calendar-events", mode, categoryIds, calendarId],
        queryFn: () => getEvents(params),
    });

    if (isLoading) return <div>Loading events...</div>;
    if (!events || events.length === 0) return <div className="text-muted-foreground p-4">No events found.</div>;

    // Sort events by start date
    const sortedEvents = [...events].sort((a, b) =>
        new Date(a.start_date).getTime() - new Date(b.start_date).getTime()
    );

    // Group by month for monthly view
    const groupedEvents: { [key: string]: Event[] } = {};
    if (mode === 'monthly') {
        sortedEvents.forEach(event => {
            const monthYear = format(new Date(event.start_date), 'MMMM yyyy');
            if (!groupedEvents[monthYear]) {
                groupedEvents[monthYear] = [];
            }
            groupedEvents[monthYear].push(event);
        });
    } else {
        groupedEvents['All Events'] = sortedEvents;
    }

    return (
        <div className="space-y-8">
            {Object.entries(groupedEvents).map(([groupTitle, groupEvents]) => (
                <div key={groupTitle} className="space-y-4">
                    {mode === 'monthly' && (
                        <h3 className="text-lg font-semibold sticky top-0 bg-background py-2 z-10 border-b">
                            {groupTitle}
                        </h3>
                    )}
                    <div className="space-y-2">
                        {groupEvents.map(event => (
                            <div key={event.id} className="flex items-center justify-between border-b pb-2 last:border-0">
                                <div className="flex items-center gap-4">
                                    <div className="w-16 text-sm font-medium text-muted-foreground">
                                        {event.type === 'single' ? (
                                            <div>{format(new Date(event.start_date), 'd')}</div>
                                        ) : (
                                            <div className="flex items-center gap-1 text-xs whitespace-nowrap">
                                                <span>{format(new Date(event.start_date), 'd')}</span>
                                                <span>-</span>
                                                <span>{format(new Date(event.end_date), 'd')}</span>
                                            </div>
                                        )}
                                    </div>

                                    <Dialog>
                                        <DialogTrigger asChild>
                                            <Button variant="link" className="p-0 h-auto font-semibold text-foreground hover:underline">
                                                {event.title}
                                            </Button>
                                        </DialogTrigger>
                                        <DialogContent>
                                            <DialogHeader>
                                                <DialogTitle>{event.title}</DialogTitle>
                                                <DialogDescription>
                                                    {event.type === 'single'
                                                        ? format(new Date(event.start_date), 'EEEE, MMMM d, yyyy')
                                                        : `${format(new Date(event.start_date), 'MMM d')} - ${format(new Date(event.end_date), 'MMM d, yyyy')}`
                                                    }
                                                </DialogDescription>
                                            </DialogHeader>
                                            <div className="space-y-4 pt-4">
                                                <div className="flex items-center gap-2">
                                                    <Badge variant="outline" style={{
                                                        borderColor: event.category_color,
                                                        color: event.category_color
                                                    }}>
                                                        {event.category_name}
                                                    </Badge>
                                                    <span className="text-sm text-muted-foreground">
                                                        {event.start_time.substring(0, 5)} - {event.end_time.substring(0, 5)}
                                                    </span>
                                                </div>
                                                {event.description && (
                                                    <p className="text-sm">{event.description}</p>
                                                )}
                                                {event.location && (
                                                    <p className="text-sm text-muted-foreground">📍 {event.location}</p>
                                                )}
                                            </div>
                                        </DialogContent>
                                    </Dialog>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}
