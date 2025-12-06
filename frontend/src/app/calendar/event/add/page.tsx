"use client";

import { useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useCreateEvent, useUpdateEvent, useEvent } from "@/hooks/use-event-queries";
import { useCategories } from "@/hooks/use-category-queries";
import { eventFormSchema, type EventFormValues, type Category } from "@/types/calendar";

function AddEventForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const id = searchParams.get("id");
    const isEditMode = !!id;

    const { data: categories = [], isLoading: categoriesLoading } = useCategories();
    const createEvent = useCreateEvent();
    const updateEvent = useUpdateEvent();
    const { data: eventData, isLoading: eventLoading } = useEvent(id || "");

    const { register, control, handleSubmit, watch, setValue, reset, formState: { errors } } = useForm<EventFormValues>({
        resolver: zodResolver(eventFormSchema) as any,
        defaultValues: {
            title: "",
            category: "",
            eventType: "single",
            startDate: "",
            endDate: "",
            startTime: "",
            endTime: "",
            duration: "",
            description: "",
        }
    });

    useEffect(() => {
        if (isEditMode && eventData) {
            reset({
                title: eventData.title,
                category: (eventData.category?.ukid || eventData.category || "").toString(),
                eventType: eventData.type as "single" | "multi",
                startDate: eventData.start_date,
                endDate: eventData.end_date,
                startTime: eventData.start_time,
                endTime: eventData.end_time,
                duration: eventData.event_duration || "",
                description: eventData.description || "",
            });
        }
    }, [isEditMode, eventData, reset]);

    const eventType = watch("eventType");
    const startDate = watch("startDate");

    // Update endDate when startDate changes for single day events
    useEffect(() => {
        if (eventType === "single" && startDate) {
            setValue("endDate", startDate);
        }
    }, [startDate, eventType, setValue]);

    const onSubmit = (data: EventFormValues) => {
        const payload = {
            title: data.title,
            category: data.category,
            type: data.eventType,
            start_date: data.startDate,
            end_date: data.eventType === "single" ? data.startDate : data.endDate,
            start_time: data.startTime,
            end_time: data.endTime,
            event_duration: data.duration || null,
            description: data.description,
            calendar: eventData?.calendar?.ukid || null // Preserve calendar link if editing
        };

        if (isEditMode && id) {
            updateEvent.mutate({ id, data: payload }, {
                onSuccess: () => {
                    router.push("/calendar/event/list");
                }
            });
        } else {
            createEvent.mutate(payload, {
                onSuccess: () => {
                    router.push("/calendar/event/list");
                }
            });
        }
    };

    if (isEditMode && eventLoading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="max-w-2xl mx-auto">
            <Card>
                <CardHeader>
                    <CardTitle>{isEditMode ? "Edit Event" : "Add New Event"}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="title">Event Title</Label>
                            <Input
                                id="title"
                                {...register("title")}
                                placeholder="Enter event title"
                            />
                            {errors.title && <p className="text-sm text-red-500">{errors.title.message}</p>}
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="category">Category</Label>
                                <Controller
                                    name="category"
                                    control={control}
                                    render={({ field }) => (
                                        <Select onValueChange={field.onChange} value={field.value}>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select category" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {categories.map((cat: Category) => (
                                                    <SelectItem key={cat.ukid} value={cat.ukid}>{cat.name}</SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    )}
                                />
                                {errors.category && <p className="text-sm text-red-500">{errors.category.message}</p>}
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="type">Event Type</Label>
                                <Controller
                                    name="eventType"
                                    control={control}
                                    render={({ field }) => (
                                        <Select onValueChange={field.onChange} value={field.value}>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select type" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="single">Single Day</SelectItem>
                                                <SelectItem value="multi">Multi Day</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    )}
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="start-date">Start Date</Label>
                                <Input
                                    id="start-date"
                                    type="date"
                                    {...register("startDate")}
                                />
                                {errors.startDate && <p className="text-sm text-red-500">{errors.startDate.message}</p>}
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="end-date">End Date</Label>
                                <Input
                                    id="end-date"
                                    type="date"
                                    {...register("endDate")}
                                    disabled={eventType === "single"}
                                />
                                {errors.endDate && <p className="text-sm text-red-500">{errors.endDate.message}</p>}
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="start-time">Start Time</Label>
                                <Input
                                    id="start-time"
                                    type="time"
                                    {...register("startTime")}
                                />
                                {errors.startTime && <p className="text-sm text-red-500">{errors.startTime.message}</p>}
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="end-time">End Time</Label>
                                <Input
                                    id="end-time"
                                    type="time"
                                    {...register("endTime")}
                                />
                                {errors.endTime && <p className="text-sm text-red-500">{errors.endTime.message}</p>}
                            </div>
                        </div>

                        {eventType === "multi" && (
                            <div className="space-y-2">
                                <Label htmlFor="duration">Duration (per day)</Label>
                                <Input
                                    id="duration"
                                    {...register("duration")}
                                    placeholder="e.g. 02:00:00"
                                />
                            </div>
                        )}

                        <div className="space-y-2">
                            <Label htmlFor="description">Description</Label>
                            <Textarea
                                id="description"
                                {...register("description")}
                                placeholder="Enter event details"
                            />
                        </div>

                        <Button type="submit" className="w-full" disabled={createEvent.isPending || updateEvent.isPending || categoriesLoading}>
                            {createEvent.isPending || updateEvent.isPending ? "Saving..." : (isEditMode ? "Update Event" : "Create Event")}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}

export default function AddEventPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <AddEventForm />
        </Suspense>
    );
}
