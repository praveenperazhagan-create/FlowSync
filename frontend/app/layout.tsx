import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "FlowSync — AI Smart Traffic Management",
  description:
    "Upload traffic images, detect congestion, optimize traffic signals and prioritize emergency vehicles using Artificial Intelligence.",
  keywords: ["smart traffic", "AI", "YOLOv8", "congestion detection", "signal optimization"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${inter.variable} font-sans bg-slate-950 text-white antialiased min-h-screen`}
      >
        {children}
        <Toaster
          theme="dark"
          position="top-right"
          toastOptions={{
            style: {
              background: "#0f172a",
              border: "1px solid rgba(255,255,255,0.08)",
              color: "#f1f5f9",
            },
          }}
        />
      </body>
    </html>
  );
}
