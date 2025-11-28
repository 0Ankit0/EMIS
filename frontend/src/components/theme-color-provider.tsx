"use client";

import { useEffect, useState } from "react";
import { useTheme } from "next-themes";
import { applyColorPreset, getStoredColorPreset } from "@/lib/theme-colors";

export function ThemeColorProvider({
    children,
}: {
    children: React.ReactNode;
}) {
    const { resolvedTheme } = useTheme();
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
        const storedColor = getStoredColorPreset();
        applyColorPreset(storedColor, resolvedTheme === "dark");
    }, []);

    useEffect(() => {
        if (mounted && resolvedTheme) {
            const storedColor = getStoredColorPreset();
            applyColorPreset(storedColor, resolvedTheme === "dark");
        }
    }, [resolvedTheme, mounted]);

    return <>{children}</>;
}
