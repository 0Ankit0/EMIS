"use client";

import { useState } from "react";
import { format, eachMonthOfInterval, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isSameDay, isToday } from "date-fns";
import { cn } from "@/lib/utils";
import { EventModal } from "./event-modal";

interface CalendarInteractionProps {
    startDate: Date;
    endDate: Date;
    calendarTitle: string;
    onEventAdd: (event: any) => void;
}

export function CalendarInteraction({ startDate, endDate, calendarTitle, onEventAdd }: CalendarInteractionProps) {
    const [selectedDate, setSelectedDate] = useState<Date | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const months = eachMonthOfInterval({ start: startDate, end: endDate });

    const handleDateClick = (date: Date) => {
        setSelectedDate(date);
        setIsModalOpen(true);
    };

    const handleEventSave = (eventData: any) => {
        onEventAdd(eventData);
    };

    return (
        <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {months.map((month) => (
                    <div key={month.toString()} className="border rounded-lg p-4">
                        <h3 className="text-lg font-semibold mb-4 text-center">{format(month, "MMMM yyyy")}</h3>
                        <div className="grid grid-cols-7 gap-1 text-center text-sm">
                            {["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"].map((day) => (
                                <div key={day} className="font-medium text-muted-foreground">{day}</div>
                            ))}
                            {eachDayOfInterval({
                                start: startOfMonth(month),
                                end: endOfMonth(month)
                            }).map((day, dayIdx) => {
                                // Add empty cells for start of month
                                const startOffset = startOfMonth(month).getDay();
                                const isFirstDay = dayIdx === 0;

                                return (
                                    <div
                                        key={day.toString()}
                                        className={cn(
                                            "aspect-square flex items-center justify-center rounded-md cursor-pointer hover:bg-accent",
                                            !isSameMonth(day, month) && "invisible",
                                            isToday(day) && "bg-primary text-primary-foreground hover:bg-primary/90",
                                            selectedDate && isSameDay(day, selectedDate) && "ring-2 ring-ring",
                                            isFirstDay && `col-start-${startOffset + 1}` // This might need better handling for grid alignment
                                        )}
                                        style={isFirstDay ? { gridColumnStart: startOffset + 1 } : {}}
                                        onClick={() => handleDateClick(day)}
                                    >
                                        {format(day, "d")}
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                ))}
            </div>

            {selectedDate && (
                <EventModal
                    isOpen={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    selectedDate={selectedDate}
                    onSave={handleEventSave}
                />
            )}
        </div>
    );
}
