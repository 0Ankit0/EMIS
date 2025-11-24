"use client";

import { Calendar as CalendarIcon } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const timetableData = [
    {
        day: "Monday", slots: [
            { time: "09:00-10:30", subject: "Mathematics", room: "Room 101", teacher: "Dr. Smith" },
            { time: "11:00-12:30", subject: "Physics", room: "Lab 2", teacher: "Prof. Johnson" },
        ]
    },
    {
        day: "Tuesday", slots: [
            { time: "09:00-10:30", subject: "Chemistry", room: "Lab 1", teacher: "Dr. Williams" },
            { time: "11:00-12:30", subject: "English", room: "Room 205", teacher: "Ms. Brown" },
        ]
    },
];

export default function TimetableViewPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <CalendarIcon className="h-8 w-8 text-primary" />
                    Class Schedule
                </h2>
                <p className="text-muted-foreground">Weekly timetable for Grade 10-A</p>
            </div>

            <div className="grid grid-cols-1 gap-6">
                {timetableData.map((day) => (
                    <Card key={day.day}>
                        <CardHeader className="bg-blue-50">
                            <CardTitle>{day.day}</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-6">
                            <div className="space-y-3">
                                {day.slots.map((slot, idx) => (
                                    <div key={idx} className="flex justify-between items-center p-4 border border-gray-200 rounded-lg">
                                        <div>
                                            <h4 className="font-bold text-lg">{slot.subject}</h4>
                                            <p className="text-sm text-muted-foreground">{slot.teacher}</p>
                                        </div>
                                        <div className="text-right">
                                            <p className="font-semibold">{slot.time}</p>
                                            <p className="text-sm text-muted-foreground">{slot.room}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
