"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";

export default function Page() {
  const [data, setData] = useState({ users: 1250, status: "ONLINE" });
  return (
    <div className="min-h-screen bg-[#000205] p-10 font-mono text-cyan-400">
      <nav className="flex gap-8 border-b border-cyan-900 pb-6 mb-10">
        <Link href="/" className="hover:text-white">🏠 الرئيسة</Link>
        <Link href="/dashboard" className="text-white border-b border-cyan-400">📊 ملف المستخدم</Link>
        <Link href="/simulation" className="hover:text-white">🧪 المحاكاة</Link>
        <Link href="/profile" className="hover:text-white">👤 الملف الشخصي</Link>
      </nav>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-8 bg-slate-900/40 border border-cyan-500/20 rounded-3xl">
          <p className="text-xs text-slate-500">حالة النظام</p>
          <p className="text-3xl font-black text-green-400 animate-pulse">{data.status}</p>
        </div>
        <div className="p-8 bg-slate-900/40 border border-cyan-500/20 rounded-3xl">
          <p className="text-xs text-slate-500">المستخدمين</p>
          <p className="text-3xl font-black text-white">{data.users}</p>
        </div>
      </div>
      <div className="mt-10 p-10 border border-dashed border-cyan-900 rounded-3xl text-center">
        <p className="text-slate-600 italic font-light">مرحباً بك يا قائد حمزة.. النظام تحت تصرفك الآن.</p>
      </div>
    </div>
);
}
