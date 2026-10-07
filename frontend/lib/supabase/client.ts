/**
 * frontend/lib/supabase/client.ts
 * ------------------------------
 * Supabase browser client initialized with public environment variables.
 * Never uses or exposes the private service-role key.
 */

import { createBrowserClient } from "@supabase/ssr";
import type { Database } from "./types.ts";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export function isSupabaseConfigured(): boolean {
  return Boolean(
    supabaseUrl &&
    supabaseAnonKey &&
    supabaseUrl.startsWith("http") &&
    !supabaseUrl.includes("placeholder")
  );
}

export function createClient() {
  if (!isSupabaseConfigured()) {
    // Return standard client with fallback or fallback dummy url to avoid SSR crashes
    return createBrowserClient<Database>(
      supabaseUrl || "https://placeholder-project.supabase.co",
      supabaseAnonKey || "placeholder-anon-key"
    );
  }

  return createBrowserClient<Database>(supabaseUrl!, supabaseAnonKey!);
}
