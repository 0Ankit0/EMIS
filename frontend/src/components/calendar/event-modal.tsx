"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Plus } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { format } from "date-fns";
import { toast } from "sonner";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useCreateEvent, useLinkEvent, useEvents } from "@/hooks/use-event-queries";
import { useCategories } from "@/hooks/use-category-queries";

interface EventModalProps {
    isOpen: boolean;
    onClose: () => void;
    selectedDate: Date;
    onSave: (eventData: any) => void;
}

const eventSchema = z.object({
    title: z.string().min(1, "Title is required"),
    category: z.string().min(1, "Category is required"),
    eventType: z.enum(["single", "multi"]),
    startDate: z.string().min(1, "Start date is required"),
    endDate: z.string().optional(),
    startTime: z.string().min(1, "Start time is required"),
    endTime: z.string().min(1, "End time is required"),
    duration: z.string().optional(),
    description: z.string().optional(),
    entry_form_required: z.boolean(),
    registration_url: z.string().optional(),
    registration_limit: z.coerce.number().optional(),
    reminder_enabled: z.boolean(),
    remainder_time_before_event: z.string().optional(),
    status: z.enum(['draft', 'published', 'postponed', 'cancelled']),
}).refine(data => {
    if (data.eventType === "multi" && !data.endDate) {
        return false;
    }
    return true;
}, {
    message: "End date is required for multi-day events",
    path: ["endDate"],
}).refine(data => {
    if (data.entry_form_required && !data.registration_url) {
        return false;
    }
    return true;
}, {
    message: "Registration URL is required when entry form is required",
    path: ["registration_url"],
});

type EventFormValues = {
    title: string;
    category: string;
    eventType: "single" | "multi";
    startDate: string;
    endDate?: string;
    startTime: string;
    endTime: string;
    duration?: string;
    description?: string;
    entry_form_required: boolean;
    registration_url?: string;
    registration_limit?: number;
    reminder_enabled: boolean;
    remainder_time_before_event?: string;
    status: "draft" | "published" | "postponed" | "cancelled";
};

export function EventModal({ isOpen, onClose, selectedDate, onSave }: EventModalProps) {
    const [mode, setMode] = useState<"create" | "link">("create");
    const [existingEventId, setExistingEventId] = useState("");

    const { data: categories = [] } = useCategories();
    const { data: allEvents = [] } = useEvents();

    // Filter for unlinked events
    const existingEvents = allEvents.filter((e: any) => e.calendar === null);

    const { register, control, handleSubmit, watch, setValue, reset, formState: { errors } } = useForm<EventFormValues>({
        resolver: zodResolver(eventSchema) as any,
        defaultValues: {
            title: "",
            category: "",
            eventType: "single",
            startDate: format(new Date(), "yyyy-MM-dd"),
            endDate: format(new Date(), "yyyy-MM-dd"),
            startTime: "",
            endTime: "",
            duration: "",
            description: "",
            entry_form_required: false,
            registration_url: "",
            registration_limit: undefined,
            reminder_enabled: false,
            remainder_time_before_event: "",
            status: "draft",
        }
    });

    const eventType = watch("eventType");
    const startDate = watch("startDate");
    const entryFormRequired = watch("entry_form_required");
    const reminderEnabled = watch("reminder_enabled");

    useEffect(() => {
        if (isOpen) {
            const formattedDate = format(selectedDate, "yyyy-MM-dd");
            reset({
                title: "",
                category: "",
                eventType: "single",
                startDate: formattedDate,
                endDate: formattedDate,
                startTime: "",
                endTime: "",
                duration: "",
                description: "",
                entry_form_required: false,
                registration_url: "",
                registration_limit: undefined,
                reminder_enabled: false,
                remainder_time_before_event: "",
                status: "draft",
            });
        }
    }, [isOpen, selectedDate, reset]);

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
            entry_form_required: data.entry_form_required,
            registration_url: data.registration_url,
            registration_limit: data.registration_limit,
            reminder_enabled: data.reminder_enabled,
            remainder_time_before_event: data.remainder_time_before_event || null,
            status: data.status,
        };
        onSave(payload);
        onClose();
    };

    const handleLinkSubmit = () => {
        if (!existingEventId) {
            toast.error("Please select an event to link.");
            return;
        }
        onSave({ existingEventId });
        onClose();
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[600px] max-h-[85vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>
                        {mode === "create" ? `Add Event - ${format(selectedDate, "PPP")}` : "Link Existing Event"}
                    </DialogTitle>
                </DialogHeader>

                <div className="flex justify-center gap-4 mb-4">
                    <Button
                        variant={mode === "create" ? "default" : "outline"}
                        onClick={() => setMode("create")}
                        size="sm"
                    >
                        Create New
                    </Button>
                    <Button
                        variant={mode === "link" ? "default" : "outline"}
                        onClick={() => setMode("link")}
                        size="sm"
                    >
                        Link Existing
                    </Button>
                </div>

                {mode === "link" ? (
                    <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="existing-event" className="text-right">
                                Select Event
                            </Label>
                            <div className="col-span-3 flex gap-2">
                                <Select value={existingEventId} onValueChange={setExistingEventId}>
                                    <SelectTrigger className="flex-1">
                                        <SelectValue placeholder="Select an unlinked event" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {existingEvents.map((e: any) => (
                                            <SelectItem key={e.ukid} value={e.ukid}>{e.title}</SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                                <Button size="icon" variant="outline" asChild title="Add New Event">
                                    <Link href="/calendar/event/add">
                                        <Plus className="h-4 w-4" />
                                    </Link>
                                </Button>
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={onClose}>Cancel</Button>
                            <Button onClick={handleLinkSubmit}>Link Event</Button>
                        </DialogFooter>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit(onSubmit)}>
                        <div className="grid gap-4 py-4">
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="title" className="text-right">
                                    Title
                                </Label>
                                <div className="col-span-3">
                                    <Input
                                        id="title"
                                        {...register("title")}
                                    />
                                    {errors.title && <p className="text-sm text-red-500">{errors.title.message}</p>}
                                </div>
                            </div>
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="category" className="text-right">
                                    Category
                                </Label>
                                <div className="col-span-3">
                                    <div className="flex gap-2">
                                        <Controller
                                            name="category"
                                            control={control}
                                            render={({ field }) => (
                                                <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                    <SelectTrigger className="flex-1">
                                                        <SelectValue placeholder="Select category" />
                                                    </SelectTrigger>
                                                    <SelectContent>
                                                        {categories.map((cat: any) => (
                                                            <SelectItem key={cat.ukid} value={cat.ukid}>{cat.name}</SelectItem>
                                                        ))}
                                                    </SelectContent>
                                                </Select>
                                            )}
                                        />
                                        <Button size="icon" variant="outline" asChild title="Add New Category">
                                            <Link href="/calendar/category/add">
                                                <Plus className="h-4 w-4" />
                                            </Link>
                                        </Button>
                                    </div>
                                    {errors.category && <p className="text-sm text-red-500 mt-1">{errors.category.message}</p>}
                                </div>
                            </div>
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="type" className="text-right">
                                    Type
                                </Label>
                                <div className="col-span-3">
                                    <Controller
                                        name="eventType"
                                        control={control}
                                        render={({ field }) => (
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
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

                            {eventType === "single" ? (
                                <>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label className="text-right">Date</Label>
                                        <div className="col-span-3 text-sm font-medium">
                                            {format(selectedDate, "PPP")}
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="start-time" className="text-right">
                                            Start Time
                                        </Label>
                                        <div className="col-span-3">
                                            <Input
                                                id="start-time"
                                                type="time"
                                                {...register("startTime")}
                                            />
                                            {errors.startTime && <p className="text-sm text-red-500">{errors.startTime.message}</p>}
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="end-time" className="text-right">
                                            End Time
                                        </Label>
                                        <div className="col-span-3">
                                            <Input
                                                id="end-time"
                                                type="time"
                                                {...register("endTime")}
                                            />
                                            {errors.endTime && <p className="text-sm text-red-500">{errors.endTime.message}</p>}
                                        </div>
                                    </div>
                                </>
                            ) : (
                                <>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="start-date" className="text-right">
                                            Start Date
                                        </Label>
                                        <div className="col-span-3">
                                            <Input
                                                id="start-date"
                                                type="date"
                                                {...register("startDate")}
                                            />
                                            {errors.startDate && <p className="text-sm text-red-500">{errors.startDate.message}</p>}
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="end-date" className="text-right">
                                            End Date
                                        </Label>
                                        <div className="col-span-3">
                                            <Input
                                                id="end-date"
                                                type="date"
                                                {...register("endDate")}
                                            />
                                            {errors.endDate && <p className="text-sm text-red-500">{errors.endDate.message}</p>}
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="start-time" className="text-right">
                                            Start Time
                                        </Label>
                                        <div className="col-span-3">
                                            <Input
                                                id="start-time"
                                                type="time"
                                                {...register("startTime")}
                                            />
                                            {errors.startTime && <p className="text-sm text-red-500">{errors.startTime.message}</p>}
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="end-time" className="text-right">
                                            End Time
                                        </Label>
                                        <div className="col-span-3">
                                            <Input
                                                id="end-time"
                                                type="time"
                                                {...register("endTime")}
                                            />
                                            {errors.endTime && <p className="text-sm text-red-500">{errors.endTime.message}</p>}
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="duration" className="text-right">
                                            Duration
                                        </Label>
                                        <Input
                                            id="duration"
                                            {...register("duration")}
                                            placeholder="e.g. 02:00:00"
                                            className="col-span-3"
                                        />
                                    </div>
                                </>
                            )}

                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="status" className="text-right">
                                    Status
                                </Label>
                                <div className="col-span-3">
                                    <Controller
                                        name="status"
                                        control={control}
                                        render={({ field }) => (
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select status" />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    <SelectItem value="draft">Draft</SelectItem>
                                                    <SelectItem value="published">Published</SelectItem>
                                                    <SelectItem value="postponed">Postponed</SelectItem>
                                                    <SelectItem value="cancelled">Cancelled</SelectItem>
                                                </SelectContent>
                                            </Select>
                                        )}
                                    />
                                </div>
                            </div>

                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="entry_form_required" className="text-right">
                                    Entry Form
                                </Label>
                                <div className="col-span-3 flex items-center gap-2">
                                    <input
                                        type="checkbox"
                                        id="entry_form_required"
                                        className="h-4 w-4"
                                        {...register("entry_form_required")}
                                    />
                                    <Label htmlFor="entry_form_required" className="font-normal">Required</Label>
                                </div>
                            </div>

                            {entryFormRequired && (
                                <>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="registration_url" className="text-right">
                                            Reg. URL
                                        </Label>
                                        <div className="col-span-3">
                                            <Input
                                                id="registration_url"
                                                {...register("registration_url")}
                                                placeholder="https://..."
                                            />
                                            {errors.registration_url && <p className="text-sm text-red-500">{errors.registration_url.message}</p>}
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="registration_limit" className="text-right">
                                            Limit
                                        </Label>
                                        <div className="col-span-3">
                                            <Input
                                                id="registration_limit"
                                                type="number"
                                                {...register("registration_limit")}
                                                placeholder="Max participants"
                                            />
                                        </div>
                                    </div>
                                </>
                            )}

                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="reminder_enabled" className="text-right">
                                    Reminder
                                </Label>
                                <div className="col-span-3 flex items-center gap-2">
                                    <input
                                        type="checkbox"
                                        id="reminder_enabled"
                                        className="h-4 w-4"
                                        {...register("reminder_enabled")}
                                    />
                                    <Label htmlFor="reminder_enabled" className="font-normal">Enabled</Label>
                                </div>
                            </div>

                            {reminderEnabled && (
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="remainder_time_before_event" className="text-right">
                                        Time Before
                                    </Label>
                                    <div className="col-span-3">
                                        <Input
                                            id="remainder_time_before_event"
                                            {...register("remainder_time_before_event")}
                                            placeholder="e.g. 00:30:00"
                                        />
                                    </div>
                                </div>
                            )}

                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="description" className="text-right">
                                    Description
                                </Label>
                                <Textarea
                                    id="description"
                                    {...register("description")}
                                    className="col-span-3"
                                />
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={onClose} type="button">Cancel</Button>
                            <Button type="submit">Save Event</Button>
                        </DialogFooter>
                    </form>
                )}
            </DialogContent>
        </Dialog>
    );
}
