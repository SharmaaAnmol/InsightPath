import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "InsightPath | Data Science Career-Readiness & Progression",
  description: "Evidence-based analytics and predictive modeling for data science career progression.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased font-sans bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
