import type { Metadata } from "next";
import "./globals.css";
// استيراد الموصلات التي أرسلتها أنت سابقاً
import { Providers } from "@/components/providers";
import { Navbar } from "@/components/layout/Navbar";

export const metadata: Metadata = {
  title: "Neural Core 2200",
  description: "BTEC Educational Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl" suppressHydrationWarning>
      <body className="bg-[#020617] text-white antialiased">
        <Providers>
          <Navbar />
          <main>{children}</main>
        </Providers>
      </body>
    </html>
  );
}