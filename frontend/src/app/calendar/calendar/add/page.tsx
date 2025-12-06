"use client";

import { useState, useEffect, Suspense } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CalendarInteraction } from "@/components/calendar/calendar-interaction";
import { addYears, format, isBefore, parseISO } from "date-fns";
import { toast } from "sonner";
import { useRouter, useSearchParams } from "next/navigation";
import { CALENDAR_ENDPOINTS } from "@/lib/api-constants";
import { getAuthToken } from "@/lib/auth-utils";
import { useCalendar } from "@/hooks/use-calendar-queries";

function AddCalendarForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const id = searchParams.get("id");
    const isEditMode = !!id;

    const { data: calendarData, isLoading: calendarLoading } = useCalendar(id || "");

    const [formData, setFormData] = useState({
        startDate: "",
        endDate: "",
        title: ""
    });
    const [showCalendar, setShowCalendar] = useState(false);
    const [events, setEvents] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isEditMode && calendarData) {
            setFormData({
                startDate: calendarData.start_date,
                endDate: calendarData.end_date,
                title: calendarData.title
            });
            setShowCalendar(true);
        }
    }, [isEditMode, calendarData]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleGetDetails = () => {
        const { startDate, endDate } = formData;
        if (!startDate || !endDate) {
            toast.error("Please select both start and end dates.");
            return;
        }

        const start = parseISO(startDate);
        const end = parseISO(endDate);

        if (isBefore(end, start)) {
            toast.error("End date must be after start date.");
            return;
        }

        if (isBefore(addYears(start, 1), end)) {
            toast.error("Date range cannot exceed one year.");
            return;
        }

        setShowCalendar(true);
    };

    const handleEventAdd = (eventData: any) => {
        setEvents([...events, eventData]);
        toast.success("Event added to draft");
    };

    const handleSaveCalendar = async () => {
        const { title, startDate, endDate } = formData;
        if (!title) {
            toast.error("Please enter a calendar title.");
            return;
        }

        setLoading(true);
        try {
            const token = getAuthToken();
            let calendarId = id;

            if (isEditMode && id) {
                // Update Calendar
                const calRes = await fetch(`${CALENDAR_ENDPOINTS.CALENDARS}${id}/`, {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        title,
                        start_date: startDate,
                        end_date: endDate
                    })
                });

                if (!calRes.ok) {
                    const data = await calRes.json();
                    throw new Error(data.detail || "Failed to update calendar");
                }
            } else {
                // Create Calendar
                const calRes = await fetch(CALENDAR_ENDPOINTS.CALENDARS, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        title,
                        start_date: startDate,
                        end_date: endDate
                    })
                });

                if (!calRes.ok) {
                    const data = await calRes.json();
                    throw new Error(data.detail || "Failed to create calendar");
                }

                const calendarData = await calRes.json();
                calendarId = calendarData.ukid;
            }

            // 2. Create/Link Events (Only new ones added in this session)
            if (calendarId) {
                for (const event of events) {
                    if (event.existingEventId) {
                        // Link existing event
                        await fetch(`${CALENDAR_ENDPOINTS.EVENTS}${event.existingEventId}/`, {
                            method: 'PATCH',
                            headers: {
                                'Authorization': `Token ${token}`,
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ calendar: calendarId })
                        });
                    } else {
                        // Create new event linked to calendar
                        await fetch(CALENDAR_ENDPOINTS.EVENTS, {
                            method: 'POST',
                            headers: {
                                'Authorization': `Token ${token}`,
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ ...event, calendar: calendarId })
                        });
                    }
                }
            }

            toast.success(`Calendar ${isEditMode ? 'updated' : 'created'} successfully`);
            router.push("/calendar/calendar/list");

        } catch (error: any) {
            console.error(error);
            toast.error(error.message || "An error occurred");
        } finally {
            setLoading(false);
        }
    };

    if (isEditMode && calendarLoading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>{isEditMode ? "Edit Calendar" : "Add New Calendar"}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
                        <div className="space-y-2">
                            <Label htmlFor="start-date">Start Date</Label>
                            <Input
                                id="start-date"
                                name="startDate"
                                type="date"
                                value={formData.startDate}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="end-date">End Date</Label>
                            <Input
                                id="end-date"
                                name="endDate"
                                type="date"
                                value={formData.endDate}
                                onChange={handleChange}
                            />
                        </div>
                        <Button onClick={handleGetDetails}>Get Details</Button>
                    </div>
                </CardContent>
            </Card>

            {showCalendar && (
                <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <Card>
                        <CardContent className="pt-6">
                            <div className="max-w-md mx-auto space-y-2 mb-8">
                                <Label htmlFor="title">Calendar Title</Label>
                                <Input
                                    id="title"
                                    name="title"
                                    value={formData.title}
                                    onChange={handleChange}
                                    placeholder="e.g. Academic Year 2024-2025"
                                />
                            </div>

                            <CalendarInteraction
                                startDate={parseISO(formData.startDate)}
                                endDate={parseISO(formData.endDate)}
                                calendarTitle={formData.title}
                                onEventAdd={handleEventAdd}
                            />

                            <div className="flex justify-end mt-8">
                                <Button size="lg" onClick={handleSaveCalendar} disabled={loading}>
                                    {loading ? "Saving..." : (isEditMode ? "Update Calendar" : "Save Calendar")}
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            )}
        </div>
    );
}

export default function AddCalendarPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <AddCalendarForm />
        </Suspense>
    );
}
