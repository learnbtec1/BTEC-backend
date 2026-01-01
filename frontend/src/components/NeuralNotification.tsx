import { Info, AlertTriangle, CheckCircle2, X } from "lucide-react";

interface NotificationProps {
  message: string;
  type: 'success' | 'warning' | 'info';
  onClose: () => void;
}

export default function NeuralNotification({ message, type, onClose }: NotificationProps) {
  const config = {
    success: { icon: <CheckCircle2 className="text-green-400" />, border: "border-green-500/50", shadow: "shadow-green-500/20" },
    warning: { icon: <AlertTriangle className="text-yellow-400" />, border: "border-yellow-500/50", shadow: "shadow-yellow-500/20" },
    info: { icon: <Info className="text-cyan-400" />, border: "border-cyan-500/50", shadow: "shadow-cyan-500/20" }
  };

  const style = config[type] || config.info;

  return (
    <div className={`neural-alert holo-card p-4 rounded-2xl border-l-4 ${style.border} ${style.shadow} w-80 mb-4 flex gap-4 items-start z-[9999]`}>
      <div className="mt-1">{style.icon}</div>
      <div className="flex-1 text-right">
        <div className="text-[10px] font-mono text-slate-500 uppercase tracking-tighter">System Message //</div>
        <div className="text-sm text-white font-medium leading-relaxed">{message}</div>
      </div>
      <button onClick={onClose} className="text-slate-500 hover:text-white transition">
        <X size={14} />
      </button>
    </div>
  );
}