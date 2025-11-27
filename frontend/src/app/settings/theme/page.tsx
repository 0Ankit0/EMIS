"use client";

import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

export default function ThemeSettingsPage() {
    const { theme, setTheme } = useTheme();

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
            <div className="space-y-8">
                <div className="space-y-2">
                    <Label>Theme</Label>
                    <p className="text-[0.8rem] text-muted-foreground">
                        Select the theme for the dashboard.
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
        </div>
    );
}
