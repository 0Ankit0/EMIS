// Color presets for theme customization
export const colorPresets = {
    blue: {
        name: "Blue",
        light: {
            primary: "221.2 83.2% 53.3%",
            primaryForeground: "210 40% 98%",
            gradientStart: "221.2 83.2% 53.3%", // Blue 500
            gradientEnd: "188.7 94.5% 42.7%",   // Cyan 500
        },
        dark: {
            primary: "217.2 91.2% 59.8%",
            primaryForeground: "222.2 47.4% 11.2%",
            gradientStart: "217.2 91.2% 59.8%",
            gradientEnd: "188.7 94.5% 42.7%",
        },
    },
    purple: {
        name: "Purple",
        light: {
            primary: "262.1 83.3% 57.8%",
            primaryForeground: "210 40% 98%",
            gradientStart: "262.1 83.3% 57.8%", // Purple 500
            gradientEnd: "316.6 73.8% 65.1%",   // Pink 500
        },
        dark: {
            primary: "263.4 70% 50.4%",
            primaryForeground: "210 40% 98%",
            gradientStart: "263.4 70% 50.4%",
            gradientEnd: "316.6 73.8% 65.1%",
        },
    },
    green: {
        name: "Green",
        light: {
            primary: "142.1 76.2% 36.3%",
            primaryForeground: "355.7 100% 97.3%",
            gradientStart: "142.1 76.2% 36.3%", // Green 500
            gradientEnd: "160.1 84.1% 39.4%",   // Emerald 500
        },
        dark: {
            primary: "142.1 70.6% 45.3%",
            primaryForeground: "144.9 80.4% 10%",
            gradientStart: "142.1 70.6% 45.3%",
            gradientEnd: "160.1 84.1% 39.4%",
        },
    },
    orange: {
        name: "Orange",
        light: {
            primary: "24.6 95% 53.1%",
            primaryForeground: "60 9.1% 97.8%",
            gradientStart: "24.6 95% 53.1%", // Orange 500
            gradientEnd: "0 84.2% 60.2%",    // Red 500
        },
        dark: {
            primary: "20.5 90.2% 48.2%",
            primaryForeground: "60 9.1% 97.8%",
            gradientStart: "20.5 90.2% 48.2%",
            gradientEnd: "0 84.2% 60.2%",
        },
    },
    red: {
        name: "Red",
        light: {
            primary: "0 84.2% 60.2%",
            primaryForeground: "210 40% 98%",
            gradientStart: "0 84.2% 60.2%",  // Red 500
            gradientEnd: "24.6 95% 53.1%",   // Orange 500
        },
        dark: {
            primary: "0 72.2% 50.6%",
            primaryForeground: "210 40% 98%",
            gradientStart: "0 72.2% 50.6%",
            gradientEnd: "24.6 95% 53.1%",
        },
    },
    pink: {
        name: "Pink",
        light: {
            primary: "330.4 81.2% 60.4%",
            primaryForeground: "210 40% 98%",
            gradientStart: "330.4 81.2% 60.4%", // Pink 500
            gradientEnd: "349.7 89.2% 60.2%",   // Rose 500
        },
        dark: {
            primary: "330.4 70% 50.4%",
            primaryForeground: "210 40% 98%",
            gradientStart: "330.4 70% 50.4%",
            gradientEnd: "349.7 89.2% 60.2%",
        },
    },
    slate: {
        name: "Slate",
        light: {
            primary: "222.2 47.4% 11.2%",
            primaryForeground: "210 40% 98%",
            gradientStart: "215.4 16.3% 46.9%", // Slate 500
            gradientEnd: "220 8.9% 46.1%",      // Gray 500
        },
        dark: {
            primary: "210 40% 98%",
            primaryForeground: "222.2 47.4% 11.2%",
            gradientStart: "210 40% 98%",
            gradientEnd: "215.4 16.3% 46.9%",
        },
    },
};

export type ColorPreset = keyof typeof colorPresets;

export function applyColorPreset(preset: ColorPreset, isDark: boolean) {
    const colors = colorPresets[preset];
    const mode = isDark ? "dark" : "light";
    const root = document.documentElement;

    root.style.setProperty("--primary", `hsl(${colors[mode].primary})`);
    root.style.setProperty("--primary-foreground", `hsl(${colors[mode].primaryForeground})`);
    root.style.setProperty("--gradient-start", `hsl(${colors[mode].gradientStart})`);
    root.style.setProperty("--gradient-end", `hsl(${colors[mode].gradientEnd})`);

    // Also update sidebar primary to match
    const sidebarPrimary = isDark
        ? colors[mode].primary
        : colors.light.primary;
    const sidebarPrimaryForeground = isDark
        ? colors[mode].primaryForeground
        : colors.light.primaryForeground;

    root.style.setProperty("--sidebar-primary", `hsl(${sidebarPrimary})`);
    root.style.setProperty("--sidebar-primary-foreground", `hsl(${sidebarPrimaryForeground})`);
}

export function getStoredColorPreset(): ColorPreset {
    if (typeof window === "undefined") return "blue";
    return (localStorage.getItem("color-preset") as ColorPreset) || "blue";
}

export function setStoredColorPreset(preset: ColorPreset) {
    localStorage.setItem("color-preset", preset);
}
