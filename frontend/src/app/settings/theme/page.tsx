"use client";

import { useEffect, useState } from "react";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import {
    colorPresets,
    applyColorPreset,
    getStoredColorPreset,
    setStoredColorPreset,
    type ColorPreset
} from "@/lib/theme-colors";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

export default function ThemeSettingsPage() {
    const { theme, setTheme, resolvedTheme } = useTheme();
    const [selectedColor, setSelectedColor] = useState<ColorPreset>("blue");
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
        const storedColor = getStoredColorPreset();
        setSelectedColor(storedColor);
        // Apply the stored color on mount
        applyColorPreset(storedColor, resolvedTheme === "dark");
    }, []);

    useEffect(() => {
        if (mounted && resolvedTheme) {
            applyColorPreset(selectedColor, resolvedTheme === "dark");
        }
    }, [resolvedTheme, selectedColor, mounted]);

    const handleColorChange = (color: ColorPreset) => {
        setSelectedColor(color);
        setStoredColorPreset(color);
        applyColorPreset(color, resolvedTheme === "dark");
    };

    if (!mounted) {
        return (
            <div className="space-y-6">
                <div>
                    <h3 className="text-lg font-medium">Appearance</h3>
                    <p className="text-sm text-muted-foreground">
                        Customize the appearance of the app. Automatically switch between day
                        and night themes.
                    </p>
                </div>
                <Separator />
                <div className="space-y-4">
                    <div className="space-y-2">
                        <div className="h-5 w-24 animate-pulse rounded bg-muted" />
                        <div className="h-4 w-64 animate-pulse rounded bg-muted" />
                    </div>
                    <div className="grid max-w-md grid-cols-2 gap-8 pt-2">
                        <div className="h-40 animate-pulse rounded-md bg-muted" />
                        <div className="h-40 animate-pulse rounded-md bg-muted" />
                    </div>
                </div>
                <Separator />
                <div className="space-y-4">
                    <div className="space-y-2">
                        <div className="h-5 w-24 animate-pulse rounded bg-muted" />
                        <div className="h-4 w-full max-w-md animate-pulse rounded bg-muted" />
                    </div>
                    <div className="grid grid-cols-4 gap-3 sm:grid-cols-7">
                        {Array.from({ length: 7 }).map((_, i) => (
                            <div key={i} className="h-24 animate-pulse rounded-lg bg-muted" />
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-medium">Appearance</h3>
                <p className="text-sm text-muted-foreground">
                    Customize the appearance of the app. Automatically switch between day
                    and night themes.
                </p>
            </div>
            <Separator />

            {/* Theme Mode Selection */}
            <div className="space-y-4">
                <div className="space-y-2">
                    <Label>Theme Mode</Label>
                    <p className="text-[0.8rem] text-muted-foreground">
                        Select light or dark mode for the dashboard.
                    </p>
                    <RadioGroup
                        defaultValue={theme}
                        onValueChange={setTheme}
                        className="grid max-w-md grid-cols-2 gap-8 pt-2"
                    >
                        <div className="space-y-2">
                            <Label className="[&:has([data-state=checked])>div]:border-primary">
                                <RadioGroupItem value="light" className="sr-only" />
                                <div className="items-center rounded-md border-2 border-muted p-1 hover:border-accent">
                                    <div className="space-y-2 rounded-sm bg-[#ecedef] p-2">
                                        <div className="space-y-2 rounded-md bg-white p-2 shadow-sm">
                                            <div className="h-2 w-[80px] rounded-lg bg-[#ecedef]" />
                                            <div className="h-2 w-[100px] rounded-lg bg-[#ecedef]" />
                                        </div>
                                        <div className="flex items-center space-x-2 rounded-md bg-white p-2 shadow-sm">
                                            <div className="h-4 w-4 rounded-full bg-[#ecedef]" />
                                            <div className="h-2 w-[100px] rounded-lg bg-[#ecedef]" />
                                        </div>
                                        <div className="flex items-center space-x-2 rounded-md bg-white p-2 shadow-sm">
                                            <div className="h-4 w-4 rounded-full bg-[#ecedef]" />
                                            <div className="h-2 w-[100px] rounded-lg bg-[#ecedef]" />
                                        </div>
                                    </div>
                                </div>
                                <span className="block w-full p-2 text-center font-normal">
                                    Light
                                </span>
                            </Label>
                        </div>
                        <div className="space-y-2">
                            <Label className="[&:has([data-state=checked])>div]:border-primary">
                                <RadioGroupItem value="dark" className="sr-only" />
                                <div className="items-center rounded-md border-2 border-muted bg-popover p-1 hover:bg-accent hover:text-accent-foreground">
                                    <div className="space-y-2 rounded-sm bg-slate-950 p-2">
                                        <div className="space-y-2 rounded-md bg-slate-800 p-2 shadow-sm">
                                            <div className="h-2 w-[80px] rounded-lg bg-slate-400" />
                                            <div className="h-2 w-[100px] rounded-lg bg-slate-400" />
                                        </div>
                                        <div className="flex items-center space-x-2 rounded-md bg-slate-800 p-2 shadow-sm">
                                            <div className="h-4 w-4 rounded-full bg-slate-400" />
                                            <div className="h-2 w-[100px] rounded-lg bg-slate-400" />
                                        </div>
                                        <div className="flex items-center space-x-2 rounded-md bg-slate-800 p-2 shadow-sm">
                                            <div className="h-4 w-4 rounded-full bg-slate-400" />
                                            <div className="h-2 w-[100px] rounded-lg bg-slate-400" />
                                        </div>
                                    </div>
                                </div>
                                <span className="block w-full p-2 text-center font-normal">
                                    Dark
                                </span>
                            </Label>
                        </div>
                    </RadioGroup>
                </div>
            </div>

            <Separator />

            {/* Color Customization */}
            <div className="space-y-4">
                <div className="space-y-2">
                    <Label>Theme Color</Label>
                    <p className="text-[0.8rem] text-muted-foreground">
                        Select your preferred primary color. This will update buttons, links, and other accent elements.
                    </p>
                </div>

                <div className="grid grid-cols-4 gap-3 sm:grid-cols-7">
                    {Object.entries(colorPresets).map(([key, preset]) => {
                        const isSelected = selectedColor === key;
                        return (
                            <button
                                key={key}
                                onClick={() => handleColorChange(key as ColorPreset)}
                                className={cn(
                                    "group relative flex flex-col items-center gap-2 rounded-lg border-2 p-3 transition-all hover:border-primary/50",
                                    isSelected ? "border-primary" : "border-muted"
                                )}
                                style={{
                                    backgroundColor: `hsl(${preset.light.primary} / 0.1)`,
                                }}
                            >
                                <div
                                    className="h-10 w-10 rounded-full shadow-md transition-transform group-hover:scale-110"
                                    style={{
                                        backgroundColor: `hsl(${preset.light.primary})`,
                                    }}
                                >
                                    {isSelected && (
                                        <div className="flex h-full items-center justify-center">
                                            <Check className="h-5 w-5 text-white" />
                                        </div>
                                    )}
                                </div>
                                <span className="text-xs font-medium">
                                    {preset.name}
                                </span>
                            </button>
                        );
                    })}
                </div>

                <div className="rounded-lg border bg-muted/50 p-4">
                    <p className="text-sm text-muted-foreground">
                        <strong className="text-foreground">Preview:</strong> The selected color will be applied to buttons, links, active navigation items, and other accent elements throughout the application. Changes are saved automatically.
                    </p>
                </div>
            </div>
        </div>
    );
}
