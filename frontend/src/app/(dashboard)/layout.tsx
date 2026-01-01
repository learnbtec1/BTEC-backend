import React from "react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    // نستخدم div أو React Fragment بدلاً من html
    <section className="dashboard-wrapper">
      {children}
    </section>
  );
}