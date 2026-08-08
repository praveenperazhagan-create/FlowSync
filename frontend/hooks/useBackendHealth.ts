"use client";
import { useState, useEffect, useCallback } from "react";
import { checkHealth } from "@/services/api";

export function useBackendHealth() {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);

  const check = useCallback(async () => {
    try {
      await checkHealth();
      setIsOnline(true);
    } catch {
      setIsOnline(false);
    }
  }, []);

  useEffect(() => {
    check();
    const id = setInterval(check, 30000);
    return () => clearInterval(id);
  }, [check]);

  return { isOnline, check };
}
