import { useEffect, useRef } from 'react';
import { useChatStore } from '../store/useChatStore';
import { TerminalSquare } from 'lucide-react';

// SystemLog.tsx
export default function SystemLog() {
  const { systemLogs } = useChatStore(); // use hook
  const logEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [systemLogs]);

  return (
    <div className="h-full flex flex-col bg-bg border-t border-border lg:border-t-0 lg:border-l">
      <div className="h-10 border-b border-border flex items-center px-3 gap-2 bg-surface/50 shrink-0">
        <TerminalSquare className="w-3 h-3 text-zinc-400" />
        <span className="text-[10px] font-mono font-semibold tracking-wider text-zinc-400">SYSTEM_LOGS</span>
      </div>
      <div className="flex-1 min-h-0 overflow-y-auto p-3 font-mono text-[11px] space-y-1">
        {systemLogs.map((log, idx) => (
          <div key={idx} className="text-zinc-400 break-all">
            <span className="text-zinc-600 mr-2">{log.split(']')[0]}]</span>
            <span className={log.includes('ERROR') ? 'text-danger' : log.includes('USER') ? 'text-primary' : 'text-success'}>
              {log.split(']')[1]}
            </span>
          </div>
        ))}
        <div ref={logEndRef} />
      </div>
    </div>
  );
}