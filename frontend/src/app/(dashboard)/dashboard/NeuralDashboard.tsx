"use client";
import React from "react";
import { motion } from "framer-motion";

interface DashboardProps {
  data: { users: number; status: string };
}

export default function NeuralDashboard({ data }: DashboardProps) {
  return (
    <div className="min-h-screen bg-[#000205] p-10 font-mono text-cyan-400">
      {/* رأس النظام */}
      <div className="flex justify-between items-center border-b border-cyan-500/20 pb-6">
        <div>
          <h1 className="text-3xl font-black italic tracking-tighter text-white">
            NEURAL_<span className="text-cyan-400">INTERFACE</span>
          </h1>
          <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-[0.3em]">
            Authorized Access Only // System_v2200
          </p>
        </div>
        
        <div className="flex items-center gap-4 bg-cyan-950/20 px-6 py-2 rounded-full border border-cyan-500/30">
          <motion.div 
            animate={{ opacity: [1, 0.5, 1] }} 
            transition={{ duration: 1.5, repeat: Infinity }}
            className={`w-2 h-2 rounded-full ${data.status === "ONLINE" ? "bg-green-500" : "bg-red-500"}`} 
          />
          <span className="text-xs font-bold tracking-[0.2em]">{data.status}</span>
        </div>
      </div>

      {/* بطاقات البيانات الذكية */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
        {[
          { label: "Active_Students", value: data.users, unit: "NET" },
          { label: "Processing_Power", value: "98.2", unit: "GHZ" },
          { label: "Security_Level", value: "MAX", unit: "PRO" }
        ].map((item, i) => (
          <motion.div 
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.2 }}
            whileHover={{ scale: 1.02, borderColor: "rgba(34,211,238,0.4)" }}
            className="p-8 bg-slate-900/20 border border-white/5 rounded-[2rem] backdrop-blur-xl relative overflow-hidden group"
          >
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-30 transition-opacity">
              <div className="w-12 h-12 border-2 border-cyan-400 rounded-full" />
            </div>
            <p className="text-[10px] text-slate-500 mb-2 uppercase tracking-widest">{item.label}</p>
            <p className="text-5xl font-black text-white tracking-tighter">
              {item.value}<span className="text-sm text-cyan-500 ml-2">{item.unit}</span>
            </p>
          </motion.div>
        ))}
      </div>

      <div className="mt-12 h-64 border border-dashed border-cyan-900/30 rounded-[3rem] flex items-center justify-center">
        <motion.p 
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 3, repeat: Infinity }}
          className="text-slate-600 italic font-light tracking-widest uppercase text-xs"
        >
          Scanning for new neural signals...
        </motion.p>
      </div>
    </div>
  );
}