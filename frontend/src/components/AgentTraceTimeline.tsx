import React from 'react';
import { Search, Code, Scale, PenTool, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';

interface Step {
  agent: string;
  action: string;
  details?: string;
}

interface Props {
  steps: Step[];
  isComplete: boolean;
}

const getAgentIcon = (agent: string) => {
  const name = agent.toLowerCase();
  if (name.includes('researcher')) return <Search className="w-4 h-4" />;
  if (name.includes('coder')) return <Code className="w-4 h-4" />;
  if (name.includes('critic')) return <Scale className="w-4 h-4" />;
  if (name.includes('writer') || name.includes('planner')) return <PenTool className="w-4 h-4" />;
  return <AlertCircle className="w-4 h-4" />;
};

const getColor = (agent: string) => {
  const name = agent.toLowerCase();
  if (name.includes('researcher')) return 'border-blue-400 bg-blue-50 text-blue-600';
  if (name.includes('coder')) return 'border-purple-400 bg-purple-50 text-purple-600';
  if (name.includes('critic')) return 'border-amber-400 bg-amber-50 text-amber-600';
  if (name.includes('writer') || name.includes('planner')) return 'border-emerald-400 bg-emerald-50 text-emerald-600';
  return 'border-gray-300 bg-gray-50 text-gray-600';
};

const AgentTraceTimeline: React.FC<Props> = ({ steps, isComplete }) => {
  if (!steps || steps.length === 0) {
    return <div className="text-sm text-stone-400 italic p-4 text-center">No agent reasoning available.</div>;
  }

  return (
    <div className="space-y-3 p-2">
      <h4 className="text-xs font-semibold text-stone-500 uppercase tracking-wider flex items-center gap-2">
        <span className="h-px flex-1 bg-stone-200"></span>
        <span>🧠 Agent Trace</span>
        <span className="h-px flex-1 bg-stone-200"></span>
      </h4>
      <div className="relative pl-4 border-l-2 border-dashed border-stone-200 space-y-4">
        {steps.map((step, index) => {
          const isLast = index === steps.length - 1;
          return (
            <div key={index} className="relative">
              <div className={`absolute -left-[9px] top-1 w-3 h-3 rounded-full border-2 ${getColor(step.agent)} bg-white`}>
                {isLast && isComplete ? (
                  <CheckCircle className="w-3 h-3 text-green-500 absolute -top-0.5 -left-0.5" />
                ) : (
                  getAgentIcon(step.agent)
                )}
              </div>
              <div className="ml-4">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono text-stone-500 bg-stone-100 px-2 py-0.5 rounded">
                    {step.agent}
                  </span>
                  <span className="text-xs text-stone-400">{step.action}</span>
                </div>
                {step.details && (
                  <div className="mt-1 text-xs text-stone-600 bg-stone-50 p-2 rounded border border-stone-100 font-mono break-all">
                    {step.details}
                  </div>
                )}
                {isLast && !isComplete && (
                  <div className="mt-2 flex items-center gap-2 text-xs text-blue-500">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    Processing...
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AgentTraceTimeline;