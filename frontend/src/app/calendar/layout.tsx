import { CalendarSidebar } from "@/components/calendar-sidebar";

export default function CalendarLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="container mx-auto flex-1 space-y-4 p-8 pt-6">
            <div className="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
                <aside className="-mx-4 lg:w-1/5">
                    <CalendarSidebar />
                </aside>
                <div className="flex-1 lg:max-w-4xl">{children}</div>
            </div>
        </div>
    );
}
