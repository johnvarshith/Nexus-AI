import { Brain, Search, Code, FileText, Activity } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';

const agents = [
  { id: 'Planner', icon: Brain, color: 'text-blue-400', bg: 'bg-blue-50', border: 'border-blue-200' },
  { id: 'Researcher', icon: Search, color: 'text-mint-500', bg: 'bg-mint-50', border: 'border-mint-200' },
  { id: 'Coder', icon: Code, color: 'text-purple-400', bg: 'bg-purple-50', border: 'border-purple-200' },
  { id: 'Writer', icon: FileText, color: 'text-amber-400', bg: 'bg-amber-50', border: 'border-amber-200' },
];

export default function AgentTelemetry() {
  const { activeAgent, isLoading } = useChatStore();

  return (
    <div className="h-full flex flex-col">
      <h3 className="text-xs font-mono font-semibold text-stone-500 uppercase tracking-wider mb-4 px-1">Agent Telemetry</h3>
      <div className="grid grid-cols-2 gap-2 flex-1 content-start">
        {agents.map((agent) => {
          const isActive = activeAgent === agent.id && isLoading;
          const Icon = agent.icon;
          return (
            <div key={agent.id} className={`p-3 rounded border transition-all duration-300 ${isActive ? `${agent.bg} ${agent.border} shadow-lg` : 'bg-white/60 border-stone-200'}`}>
              <div className="flex items-center gap-2 mb-2">
                {isActive ? <Activity className={`w-4 h-4 ${agent.color} animate-pulse-fast`} /> : <Icon className={`w-4 h-4 ${isActive ? agent.color : 'text-stone-400'}`} />}
                <span className={`text-xs font-bold font-mono ${isActive ? 'text-stone-700' : 'text-stone-500'}`}>{agent.id.toUpperCase()}</span>
              </div>
              <div className="text-[10px] font-mono text-stone-400">
                {isActive ? 'EXECUTING...' : 'STANDBY'}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}