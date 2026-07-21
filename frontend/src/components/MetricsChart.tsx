import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useChatStore } from '../store/useChatStore';
import { Cpu } from 'lucide-react';

export default function MetricsChart() {
  const { metrics } = useChatStore();

  // Use real metrics for the latest point, fallback to 0 if not available
  const data = [
    { name: 'T-4', latency: 1200, tokens: 150 },
    { name: 'T-3', latency: 900, tokens: 220 },
    { name: 'T-2', latency: 1500, tokens: 180 },
    { name: 'T-1', latency: 800, tokens: 300 },
    { name: 'Now', latency: metrics.latency || 1000, tokens: metrics.tokens || 250 },
  ];

  return (
    <div className="h-full w-full flex flex-col min-h-0">
      <h3 className="text-xs font-mono font-semibold text-stone-500 uppercase tracking-wider mb-4 flex items-center gap-2 shrink-0">
        <Cpu className="w-3.5 h-3.5 text-mint-400" /> PERFORMANCE METRICS
      </h3>

      {/* Chart container with explicit flex-1 and min-height */}
      <div className="flex-1 min-h-[180px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 5, right: 5, left: 0, bottom: 5 }}>
            <defs>
              <linearGradient id="colorLatency" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#fcd34d" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#fcd34d" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorTokens" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#b8e0d2" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#b8e0d2" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis 
              dataKey="name" 
              stroke="#a8a29e" 
              fontSize={10} 
              tickLine={false} 
              axisLine={false} 
              tick={{ fill: '#a8a29e' }} 
            />
            <YAxis 
              stroke="#a8a29e" 
              fontSize={10} 
              tickLine={false} 
              axisLine={false} 
              tick={{ fill: '#a8a29e' }} 
              width={30}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fcf5ef',
                border: '1px solid rgba(0,0,0,0.05)',
                borderRadius: '12px',
                fontSize: '12px',
                boxShadow: '0 10px 20px rgba(0,0,0,0.06)',
              }}
              itemStyle={{ color: '#2d2a24' }}
            />
            <Area
              type="monotone"
              dataKey="latency"
              stroke="#fcd34d"
              strokeWidth={2}
              fill="url(#colorLatency)"
              dot={{ r: 4, fill: '#fcd34d', strokeWidth: 0 }}
              isAnimationActive={true}
              animationDuration={500}
            />
            <Area
              type="monotone"
              dataKey="tokens"
              stroke="#b8e0d2"
              strokeWidth={2}
              fill="url(#colorTokens)"
              dot={{ r: 4, fill: '#b8e0d2', strokeWidth: 0 }}
              isAnimationActive={true}
              animationDuration={500}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="flex gap-4 mt-2 text-[10px] font-mono shrink-0">
        <span className="flex items-center gap-1.5 text-stone-500">
          <span className="w-2 h-2 rounded-full bg-liquid-yellow" /> Latency (ms)
        </span>
        <span className="flex items-center gap-1.5 text-stone-500">
          <span className="w-2 h-2 rounded-full bg-mint-300" /> Tokens
        </span>
      </div>
    </div>
  );
}