"use client";

import React, { useState, useEffect } from "react";
import { ShieldCheck, Fingerprint, Cpu, Lock, ArrowRight } from "lucide-react";
// 1. استيراد أداة الانتقال من Next.js
import { useRouter } from "next/navigation";

export default function NeuralLoginPage() {
  const [loading, setLoading] = useState(false);
  // 2. تفعيل أداة الانتقال
  const router = useRouter();

  const handleSync = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // محاكاة عملية فحص أمنية سريعة قبل الانتقال
    setTimeout(() => {
      router.push("/dashboard");
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-[#020617] flex items-center justify-center relative overflow-hidden font-sans">
      {/* تأثيرات الخلفية المستقبلية */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-cyan-500/10 blur-[120px] rounded-full animate-pulse"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-500/10 blur-[120px] rounded-full animate-pulse"></div>
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-soft-light"></div>
      </div>

      <div className="w-full max-auto max-w-[450px] p-4 relative z-10">
        <div className="bg-slate-900/40 backdrop-blur-2xl border border-white/5 rounded-[40px] p-8 shadow-2xl shadow-cyan-500/5">
          
          {/* شعار النظام */}
          <div className="flex flex-col items-center mb-10">
            <div className={`w-16 h-16 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-2xl flex items-center justify-center shadow-[0_0_30px_rgba(34,211,238,0.4)] mb-4 group cursor-pointer transition-transform hover:rotate-12 ${loading ? 'animate-spin' : ''}`}>
              <Cpu className="text-white" size={32} />
            </div>
            <h1 className="text-2xl font-black text-white tracking-[0.2em] uppercase">
              Neural <span className="text-cyan-400">Core</span>
            </h1>
            <div className="text-[10px] font-mono text-cyan-500/50 mt-2 tracking-widest uppercase">
              {loading ? "INITIALIZING_SYNC_STREAM..." : "IDENTITY_VERIFICATION_REQUIRED"}
            </div>
          </div>

          <form onSubmit={handleSync} className="space-y-6">
            <div className="space-y-2 group">
              <label className="text-[10px] font-mono text-slate-500 uppercase ml-2 tracking-widest group-hover:text-cyan-400 transition-colors italic">Node Identifier</label>
              <div className="relative">
                <Fingerprint className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600 group-hover:text-cyan-500 transition-colors" size={18} />
                <input 
                  required
                  type="text" 
                  placeholder="ID_0x712..." 
                  className="w-full bg-slate-950/50 border border-slate-800 rounded-2xl py-4 pl-12 pr-4 text-white text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all placeholder:text-slate-700"
                />
              </div>
            </div>

            <div className="space-y-2 group">
              <label className="text-[10px] font-mono text-slate-500 uppercase ml-2 tracking-widest group-hover:text-cyan-400 transition-colors italic">Neural Key</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600 group-hover:text-cyan-500 transition-colors" size={18} />
                <input 
                  required
                  type="password" 
                  placeholder="••••••••" 
                  className="w-full bg-slate-950/50 border border-slate-800 rounded-2xl py-4 pl-12 pr-4 text-white text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all"
                />
              </div>
            </div>

            <button 
              disabled={loading}
              type="submit"
              className="w-full group relative overflow-hidden bg-white text-black font-black py-4 rounded-2xl transition-all hover:shadow-[0_0_20px_rgba(255,255,255,0.4)] active:scale-95 disabled:opacity-50"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-500 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <span className="relative z-10 flex items-center justify-center gap-2">
                {loading ? "SYNCING..." : "INITIATE SYNC"} <ArrowRight size={18} className={loading ? 'animate-ping' : ''} />
              </span>
            </button>
          </form>

          {/* تذييل الصفحة */}
          <div className="mt-8 pt-8 border-t border-white/5 flex flex-col items-center gap-4">
            <div className="flex gap-6">
               <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-500">
                  <ShieldCheck size={12} className="text-green-500" /> AES_256
               </div>
               <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-500">
                  <div className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse"></div> ENCRYPTED
               </div>
            </div>
            <p className="text-[10px] text-slate-600 text-center font-mono italic">
              بمجرد الدخول، أنت توافق على بروتوكولات المزامنة العصبية لعام 2200
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}