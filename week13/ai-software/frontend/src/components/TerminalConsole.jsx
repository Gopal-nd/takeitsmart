import React, { useEffect, useRef } from 'react';
import { Terminal, Shield, Cpu, RefreshCw, XCircle } from 'lucide-react';

export default function TerminalConsole({ logs, onClear }) {
  const terminalEndRef = useRef(null);

  const scrollToBottom = () => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [logs]);

  const parseLogLine = (log) => {
    if (typeof log !== 'object') {
      return { tag: 'SYSTEM', text: log, color: 'text-cyan-700' };
    }
    return log;
  };

  const getLightModeColor = (darkColorClass) => {
    if (!darkColorClass) return 'text-slate-700 bg-slate-100 border-slate-200';
    if (darkColorClass.includes('cyan')) return 'text-cyan-700 bg-cyan-50 border-cyan-200';
    if (darkColorClass.includes('emerald')) return 'text-emerald-700 bg-emerald-50 border-emerald-200';
    if (darkColorClass.includes('amber')) return 'text-amber-700 bg-amber-50 border-amber-200';
    if (darkColorClass.includes('rose')) return 'text-rose-700 bg-rose-50 border-rose-200';
    if (darkColorClass.includes('indigo')) return 'text-indigo-700 bg-indigo-50 border-indigo-200';
    return 'text-slate-700 bg-slate-100 border-slate-200';
  };

  return (
    <div className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm flex flex-col h-[280px]">
      {/* Terminal Title Bar */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-3 mb-3">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500/80 inline-block shadow-sm"></span>
            <span className="w-3 h-3 rounded-full bg-amber-500/80 inline-block shadow-sm"></span>
            <span className="w-3 h-3 rounded-full bg-emerald-500/80 inline-block shadow-sm"></span>
          </div>
          <span className="text-xs font-mono font-bold text-indigo-600 flex items-center gap-1.5 ml-2">
            <Terminal size={14} /> agent-network-monologue.log
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-mono text-slate-500 flex items-center gap-1">
            <Cpu size={12} className="animate-spin text-indigo-500" /> Bedrock Streaming
          </span>
          <button 
            onClick={onClear} 
            className="text-[10px] font-mono font-semibold px-2 py-0.5 border border-slate-200 text-slate-500 rounded hover:bg-slate-200 hover:text-slate-800 transition-colors"
          >
            Clear logs
          </button>
        </div>
      </div>

      {/* Terminal Screen Console */}
      <div className="flex-1 overflow-y-auto pr-2 font-mono text-xs leading-relaxed space-y-1.5 custom-scrollbar">
        {logs.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-400 italic">
            &gt; Terminal idle. Run a pipeline stage to begin listening to agent channels...
          </div>
        ) : (
          logs.map((log, index) => {
            const parsed = parseLogLine(log);
            const lightColor = getLightModeColor(parsed.color);
            return (
              <div key={index} className="flex items-start gap-2 hover:bg-slate-100/50 py-0.5 rounded transition-all">
                <span className="text-slate-400 select-none shrink-0">&gt;</span>
                {parsed.tag && (
                  <span className={`font-bold shrink-0 px-1.5 py-0.5 text-[9px] rounded font-mono uppercase border ${lightColor}`}>
                    [{parsed.tag}]
                  </span>
                )}
                <span className="text-slate-800 break-all select-text font-mono font-medium">
                  {parsed.text}
                </span>
              </div>
            );
          })
        )}
        <div ref={terminalEndRef} />
      </div>
    </div>
  );
}
