"use client";

import { useEffect, useState } from "react";
import { Button } from "./ui/button";

type ThemeMode = "dark" | "light";

function nextTheme(current: ThemeMode): ThemeMode {
  return current === "dark" ? "light" : "dark";
}

export default function ThemeToggle() {
  const [theme, setTheme] = useState<ThemeMode>("dark");

  useEffect(() => {
    const saved = window.localStorage.getItem("theme-mode");
    if (saved === "light" || saved === "dark") {
      setTheme(saved);
      document.documentElement.dataset.theme = saved;
      return;
    }

    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const initialTheme: ThemeMode = prefersDark ? "dark" : "light";
    setTheme(initialTheme);
    document.documentElement.dataset.theme = initialTheme;
  }, []);

  function toggleTheme() {
    setTheme((prev) => {
      const updated = nextTheme(prev);
      document.documentElement.dataset.theme = updated;
      window.localStorage.setItem("theme-mode", updated);
      return updated;
    });
  }

  return (
    <Button type="button" variant="outline" onClick={toggleTheme}>
      Theme: {theme === "dark" ? "Dark" : "Light"}
    </Button>
  );
}
