"use client";
import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

// 👥 قاعدة بيانات المستخدمين الوهمية
const USERS_DB = [
  { id: 1, name: "HAMZA_ROOT", role: "ADMIN", status: "ONLINE", location: "عمان, الأردن", avatar: "👑" },
  { id: 2, name: "SARAH_DEV", role: "DEVELOPER", status: "AWAY", location: "دبي, الإمارات", avatar: "💻" },
  { id: 3, name: "ALI_STUDENT", role: "STUDENT", status: "ONLINE", location: "القاهرة, مصر", avatar: "📚" }
];

export default function NeuralSystem() {
  const [page, setPage] = useState("dashboard");
  const [currentUser, setCurrentUser] = useState(USERS_DB[0]); // الأدمن هو الافتراضي

  return (
    <main className="min-h-screen bg-[#000205] text-cyan-400 font-mono p-6 md:p-12 overflow-hidden">
      
      {/* 🟢 شريط التحكم العلوي */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-12 border-b border-cyan-900/50 pb-6 gap-6">
        <h1 className="text-2xl font-black italic tracking-tighter text-white">NEURAL_<span className="text-cyan-400">CORE</span></h1>
        
        {/* أزرار التنقل */}
        <nav className="flex gap-4">
          {["dashboard", "simulation", "users"].map((item) => (
            <button 
              key={item}
              onClick={() => setPage(item)} 
              className={`px-5 py-2 rounded-full transition-all border text-xs uppercase ${page === item ? 'bg-cyan-500 text-black border-cyan-500 font-bold shadow-[0_0_15px_rgba(34,211,238,0.5)]' : 'border-cyan-900 hover:border-cyan-400'}`}
            >
              {item === 'dashboard' ? '📊 لوحة القيادة' : item === 'simulation' ? '🧪 المحاكاة' : '👥 المستخدمين'}
            </button>
          ))}
        </nav>

        {/* محول المستخدمين (User Switcher) */}
        <div className="flex items-center gap-3 bg-slate-900/50 p-2 rounded-full border border-white/5">
          <span className="text-[10px] text-slate-500 ml-2">تبديل الهوية:</span>
          {USERS_DB.map((u) => (
            <button 
              key={u.id}
              onClick={() => setCurrentUser(u)}
              className={`w-8 h-8 rounded-full flex items-center justify-center border transition-all ${currentUser.id === u.id ? 'border-cyan-400 scale-110 bg-cyan-400/20' : 'border-transparent opacity-50 hover:opacity-100'}`}
              title={u.name}
            >
              {u.avatar}
            </button>
          ))}
        </div>
      </div>

      <AnimatePresence mode="wait">
        <motion.div 
          key={page + currentUser.id}
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -10 }}
          className="max-w-6xl mx-auto"
        >
          {page === "dashboard" && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* بطاقة المستخدم الحالي */}
              <div className="lg:col-span-1 p-8 bg-slate-900/40 border border-cyan-500/20 rounded-[2.5rem]">
                <div className="text-5xl mb-4">{currentUser.avatar}</div>
                <h2 className="text-2xl font-black text-white italic">{currentUser.name}</h2>
                <p className="text-cyan-500 text-xs mt-1 uppercase tracking-widest">{currentUser.role}</p>
                <div className="mt-6 pt-6 border-t border-white/5 space-y-3 text-xs text-slate-400">
                  <p>الموقع: {currentUser.location}</p>
                  <p>الحالة: <span className={currentUser.status === 'ONLINE' ? 'text-green-400' : 'text-yellow-400'}>{currentUser.status}</span></p>
                </div>
              </div>

              {/* بيانات النظام المتغيرة */}
              <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-8 bg-cyan-950/10 border border-cyan-500/10 rounded-[2.5rem]">
                  <h3 className="text-slate-500 text-xs mb-4 uppercase">صلاحيات الوصول</h3>
                  <p className="text-3xl font-bold text-white leading-tight">
                    {currentUser.role === 'ADMIN' ? 'التحكم الكامل بالبروتوكول' : 'عرض البيانات فقط'}
                  </p>
                </div>
                <div className="p-8 bg-slate-900/40 border border-cyan-500/10 rounded-[2.5rem]">
                  <h3 className="text-slate-500 text-xs mb-4 uppercase">استهلاك المعالج</h3>
                  <p className="text-5xl font-black text-cyan-400 tracking-tighter">
                    {currentUser.role === 'ADMIN' ? '98.2' : '12.5'}<span className="text-sm ml-2">GHZ</span>
                  </p>
                </div>
              </div>
            </div>
          )}

          {page === "users" && (
            <div className="bg-slate-900/20 border border-cyan-500/10 rounded-[3rem] overflow-hidden">
              <table className="w-full text-right">
                <thead className="bg-cyan-500/10 text-cyan-400 text-xs uppercase font-black">
                  <tr>
                    <th className="p-6">المستخدم</th>
                    <th className="p-6">الرتبة</th>
                    <th className="p-6">الحالة</th>
                    <th className="p-6">الإجراء</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 text-sm">
                  {USERS_DB.map((u) => (
                    <tr key={u.id} className="hover:bg-white/5 transition-colors">
                      <td className="p-6 flex items-center gap-3">
                        <span className="text-xl">{u.avatar}</span>
                        <span className="font-bold text-white">{u.name}</span>
                      </td>
                      <td className="p-6 text-slate-400">{u.role}</td>
                      <td className="p-6">
                        <span className={`px-3 py-1 rounded-full text-[10px] ${u.status === 'ONLINE' ? 'bg-green-500/10 text-green-500 border border-green-500/20' : 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'}`}>
                          {u.status}
                        </span>
                      </td>
                      <td className="p-6">
                        <button onClick={() => setCurrentUser(u)} className="text-cyan-400 hover:underline text-xs">انتحال الشخصية</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {page === "simulation" && (
            <div className="text-center p-20 border-2 border-dashed border-cyan-500/20 rounded-[3rem]">
               <h2 className="text-3xl font-bold mb-4 italic text-white underline decoration-cyan-500">مختبر المحاكاة</h2>
               <p className="text-slate-500">مرحباً {currentUser.name}، جاري تخصيص البيئة لرتبة {currentUser.role}...</p>
               <div className="mt-10 flex justify-center gap-2">
                 {[1,2,3,4,5].map(i => <motion.div key={i} animate={{ height: [10, 40, 10] }} transition={{ repeat: Infinity, duration: 1, delay: i*0.1 }} className="w-1 bg-cyan-400" />)}
               </div>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </main>
  );
}