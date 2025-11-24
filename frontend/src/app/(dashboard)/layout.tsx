import { Header } from "@/components/layout/Header";
import { Sidebar } from "@/components/layout/Sidebar";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-gray-50/50 dark:bg-gray-900/50">
            <Header />
            <div className="flex pt-[65px]">
                <Sidebar />
                <main className="flex-1 lg:pl-[260px]">
                    <div className="container mx-auto p-6 max-w-7xl">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
