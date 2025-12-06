import { Metadata } from "next";
import { LayoutView } from "@/components/calendar/layout/layout-view";

export const metadata: Metadata = {
    title: "Calendar Layout | EMIS",
    description: "Configure and view your calendar layout",
};

export default function CalendarLayoutPage() {
    return (
        <div className="container mx-auto py-6">
            <LayoutView />
        </div>
    );
}
