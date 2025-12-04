// Calendar module - Zod schemas and inferred types
import * as z from "zod";

// ============================================
// CATEGORY
// ============================================
export const categoryFormSchema = z.object({
    name: z.string().min(1, "Name is required"),
    color: z.string().optional(),
    description: z.string().optional(),
});

export type CategoryFormValues = z.infer<typeof categoryFormSchema>;

export type Category = CategoryFormValues & {
    id: number;
    created_at?: string;
    updated_at?: string;
};

export type CategoryCreateInput = CategoryFormValues;
export type CategoryUpdateInput = Partial<CategoryFormValues>;

// ============================================
// CALENDAR
// ============================================
export const calendarFormSchema = z.object({
    title: z.string().min(1, "Title is required"),
    start_date: z.string().min(1, "Start date is required"),
    end_date: z.string().min(1, "End date is required"),
});

export type CalendarFormValues = z.infer<typeof calendarFormSchema>;

export type Calendar = CalendarFormValues & {
    id: number;
    events?: Event[];
    created_at: string;
    updated_at: string;
};

export type CalendarCreateInput = CalendarFormValues;
export type CalendarUpdateInput = Partial<CalendarFormValues>;

// ============================================
// EVENT
// ============================================
export const eventTypeEnum = z.enum(["single", "multi"]);

export const eventFormSchema = z.object({
    title: z.string().min(1, "Title is required"),
    category: z.string().min(1, "Category is required"),
    eventType: eventTypeEnum,
    startDate: z.string().min(1, "Start date is required"),
    endDate: z.string().optional(),
    startTime: z.string().min(1, "Start time is required"),
    endTime: z.string().min(1, "End time is required"),
    duration: z.string().optional(),
    description: z.string().optional(),
}).refine(data => {
    if (data.eventType === "multi" && !data.endDate) {
        return false;
    }
    return true;
}, {
    message: "End date is required for multi-day events",
    path: ["endDate"],
});

export type EventFormValues = z.infer<typeof eventFormSchema>;

export type Event = {
    id: number;
    title: string;
    category: number;
    category_name?: string;
    category_color?: string;
    type: z.infer<typeof eventTypeEnum>;
    start_date: string;
    end_date: string;
    start_time: string;
    end_time: string;
    event_duration?: string;
    description?: string;
    calendar?: number;
    created_at: string;
    updated_at: string;
};

export type EventCreateInput = {
    title: string;
    category: number;
    type: z.infer<typeof eventTypeEnum>;
    start_date: string;
    end_date: string;
    start_time: string;
    end_time: string;
    event_duration?: string;
    description?: string;
    calendar?: number;
};

export type EventUpdateInput = Partial<EventCreateInput>;

// ============================================
// FILTERS
// ============================================
export interface CalendarFilters {
    start_date_from?: string;
    start_date_to?: string;
    title?: string;
}

export interface EventFilters {
    category?: number;
    type?: "single" | "multi";
    start_date_from?: string;
    start_date_to?: string;
    calendar?: number;
}

// ============================================
// CONSTANTS
// ============================================
export const EVENT_TYPE_OPTIONS = [
    { value: "single", label: "Single Day" },
    { value: "multi", label: "Multi Day" },
] as const;
