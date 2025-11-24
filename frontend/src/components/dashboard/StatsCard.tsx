import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface StatsCardProps {
    title: string;
    value: string | number;
    icon: any;
    color: "blue" | "purple" | "yellow" | "green" | "red";
}

const colorMap = {
    blue: "border-blue-500 text-blue-500 bg-blue-100",
    purple: "border-purple-500 text-purple-500 bg-purple-100",
    yellow: "border-yellow-500 text-yellow-500 bg-yellow-100",
    green: "border-green-500 text-green-500 bg-green-100",
    red: "border-red-500 text-red-500 bg-red-100",
};

export function StatsCard({ title, value, icon: Icon, color }: StatsCardProps) {
    const colorClass = colorMap[color];
    // Extract border color for the left border
    const borderColor = colorClass.split(" ")[0];
    // Extract icon colors (text and bg)
    const iconColors = colorClass.split(" ").slice(1).join(" ");

    return (
        <Card className={cn("border-l-4 shadow-md hover:shadow-lg transition-all", borderColor)}>
            <CardContent className="p-6 flex items-center justify-between">
                <div>
                    <p className="text-sm text-muted-foreground font-semibold uppercase">{title}</p>
                    <h3 className="text-3xl font-bold mt-2">{value}</h3>
                </div>
                <div className={cn("rounded-full p-4", iconColors)}>
                    <Icon className="h-6 w-6" />
                </div>
            </CardContent>
        </Card>
    );
}
