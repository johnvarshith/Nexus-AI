import React, { useState, useRef, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { useChatStore } from './store/useChatStore';
import {
  Send, Bot, User, MessageSquare, Copy, Pencil, ChevronDown,
  Menu, X, Zap, Brain, Sparkles
} from 'lucide-react';
import LiquidGlassCard from './components/LiquidGlassCard';
import ChatHistory from './components/ChatHistory';
import AgentTraceTimeline from './components/AgentTraceTimeline';

// ---- Loading Dots ----
const LoadingDots = () => (
  <div className="flex items-center gap-1 px-2">
    <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
    <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
    <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" />
  </div>
);

// ---- Message Bubble ----
const MessageBubble = ({ msg, onEdit }: { msg: any; onEdit: (text: string) => void }) => {
  const content = typeof msg.content === 'string' ? msg.content : String(msg.content ?? '');
  const isClarification = content.includes("🛑 CLARIFICATION NEEDED:");
  const isUser = msg.role === 'user';

  const handleCopy = () => navigator.clipboard.writeText(content);
  const handleEdit = () => onEdit(content);

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex items-start gap-3 max-w-[85%] ${isUser ? 'flex-row-reverse' : ''}`}>
        <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 ${
          isUser ? 'bg-emerald-500/20 border border-emerald-500/30 text-emerald-400' : 'bg-white/5 border border-white/10 text-stone-400'
        }`}>
          {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
        </div>
        <div className={`relative p-4 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap break-words ${
          isClarification
            ? 'bg-yellow-500/10 border border-yellow-500/30 text-yellow-200 shadow-[0_0_30px_rgba(252,211,77,0.05)]'
            : isUser
              ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-100'
              : 'bg-white/5 border border-white/10 text-stone-200'
        }`}>
          <div className="text-[10px] font-mono text-stone-500 mb-1 uppercase tracking-widest">
            {isUser ? 'OPERATOR' : 'NEXUS_AI'} 
            {msg.timestamp && <span className="font-normal lowercase ml-1 text-stone-600">// {msg.timestamp}</span>}
          </div>
          <div className="prose prose-sm max-w-none">
            {content}
          </div>
          <div className="absolute top-2 right-2 flex gap-1 opacity-0 hover:opacity-100 transition-opacity">
            {isUser ? (
              <button onClick={handleEdit} className="p-1 rounded-lg hover:bg-white/10 text-stone-500 hover:text-stone-300">
                <Pencil className="w-3.5 h-3.5" />
              </button>
            ) : (
              <button onClick={handleCopy} className="p-1 rounded-lg hover:bg-white/10 text-stone-500 hover:text-stone-300">
                <Copy className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// ---- Main App ----
function App() {
  const {
    messages,
    isLoading,
    metrics,
    sendMessage,
    systemLogs,
    activeAgent,
    newChat
  } = useChatStore();

  const [input, setInput] = useState('');
  const [deepThink, setDeepThink] = useState(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState(true);
  const [expandedTrace, setExpandedTrace] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const inputBarRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll
  useEffect(() => {
    const el = messagesContainerRef.current;
    if (!el) return;
    el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
  }, [messages.length, isLoading]);

  useEffect(() => {
    if (!isLoading && messages.length === 0) inputRef.current?.focus();
  }, [isLoading, messages.length]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input, deepThink);
    setInput('');
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  const handleNewChat = () => {
    newChat();
    setInput('');
    inputRef.current?.focus();
  };

  const handleEdit = (text: string) => {
    setInput(text);
    inputRef.current?.focus();
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden bg-[#0c0c0f]">
      {/* ---- Aurora Background ---- */}
      <div className="aurora-bg">
        <div className="aurora-blob blob-1" />
        <div className="aurora-blob blob-2" />
        <div className="aurora-blob blob-3" />
      </div>
      <div className="glass-orb orb-1" />
      <div className="glass-orb orb-2" />

      {/* ---- HEADER ---- */}
      <header className="h-14 flex items-center justify-between px-4 shrink-0 z-20 border-b border-white/5 bg-black/40 backdrop-blur-xl">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsHistoryOpen(!isHistoryOpen)}
            className="p-1.5 rounded-lg hover:bg-white/10 transition-colors text-stone-400"
          >
            {isHistoryOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-yellow-400 animate-pulse' : 'bg-emerald-400'}`} />
            <span className="text-sm font-bold tracking-widest text-white">NEXUS<span className="text-emerald-400">AI</span></span>
          </div>
          <span className="text-[10px] font-mono text-stone-500 bg-white/5 px-2 py-0.5 rounded-full border border-white/5">
            Ops
          </span>
        </div>

        <div className="flex items-center gap-4">
          <label className="relative inline-flex items-center cursor-pointer group">
            <input
              type="checkbox"
              className="sr-only peer"
              checked={deepThink}
              onChange={(e) => setDeepThink(e.target.checked)}
            />
            <div className="w-10 h-5 bg-stone-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-emerald-500 shadow-sm" />
            <span className="ml-2 text-xs font-medium text-stone-400 flex items-center gap-1">
              {deepThink ? <Brain className="w-3 h-3 text-emerald-400" /> : <Zap className="w-3 h-3 text-stone-500" />}
              {deepThink ? 'Deep' : 'Fast'}
            </span>
          </label>
          <span className="text-[8px] font-mono text-stone-600 bg-white/5 px-1.5 py-0.5 rounded border border-white/5">
            {deepThink ? 'phi3:3.8b' : 'qwen2.5:3b'}
          </span>
          <button
            onClick={handleNewChat}
            className="px-3 py-1.5 text-xs font-medium bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-stone-300 transition-all"
          >
            + New Chat
          </button>
        </div>
      </header>

      {/* ---- MAIN GRID ---- */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-[auto_1fr_auto] min-h-0 overflow-hidden">
        
        {/* LEFT SIDEBAR */}
        <aside className={`
          ${isHistoryOpen ? 'w-64' : 'w-0'}
          transition-all duration-300 ease-in-out overflow-hidden border-r border-white/5 bg-black/20 backdrop-blur-sm
        `}>
          {isHistoryOpen && <ChatHistory onNewChat={handleNewChat} />}
        </aside>

        {/* CENTER: CHAT */}
        <main className="flex-1 min-w-0 flex flex-col bg-black/20 backdrop-blur-sm min-h-0">
          <div className="flex-1 flex flex-col min-h-0 mx-2 my-2 bg-white/5 backdrop-blur-2xl border border-white/5 rounded-2xl shadow-clay overflow-hidden">
            
            {!hasMessages ? (
              /* ---- EMPTY STATE ---- */
              <div className="flex-1 flex flex-col items-center justify-center gap-6 p-6">
                <div className="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center">
                  <MessageSquare className="w-8 h-8 text-emerald-400" />
                </div>
                <h2 className="text-xl font-bold text-white">Investigate an Incident</h2>
                <p className="text-sm text-stone-400 text-center max-w-md">
                  Describe a system error, latency spike, or infrastructure problem.
                </p>
                <div className="flex flex-wrap gap-2 justify-center">
                  {['Redis connection pool error', 'PostgreSQL deadlock', 'OOMKilled container', 'DNS resolution failure'].map((s) => (
                    <button
                      key={s}
                      onClick={() => { setInput(s); setTimeout(() => inputRef.current?.focus(), 100); }}
                      className="px-3 py-1.5 text-xs bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-stone-300 transition-all"
                    >
                      {s}
                    </button>
                  ))}
                </div>
                <form onSubmit={handleSubmit} className="w-full max-w-2xl relative mt-4">
                  <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="e.g., 'checkout-service ConnectionPoolError'"
                    disabled={isLoading}
                    className="w-full bg-white/5 backdrop-blur-2xl border border-white/10 rounded-2xl px-6 py-4 pr-14 text-base font-mono text-white placeholder-stone-500 focus:outline-none focus:border-emerald-500/50 focus:ring-2 focus:ring-emerald-500/20 transition-all"
                  />
                  <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-2.5 bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/30 rounded-xl text-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </form>
              </div>
            ) : (
              /* ---- ACTIVE CHAT ---- */
              <div className="flex-1 flex flex-col min-h-0">
                <div ref={messagesContainerRef} className="flex-1 overflow-y-auto p-4 space-y-4 chat-scroll">
                  <AnimatePresence>
                    {messages.map((msg) => (
                      <div key={msg.id} className="flex flex-col gap-2">
                        <MessageBubble msg={msg} onEdit={handleEdit} />
                        {msg.role === 'assistant' && (msg.trace_log?.length ?? 0) > 0 && (
                          <>
                            <button
                              onClick={() => setExpandedTrace(expandedTrace === msg.id ? null : msg.id)}
                              className="self-start flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] font-mono text-stone-400 hover:bg-white/10 transition-all"
                            >
                              {expandedTrace === msg.id ? 'Hide Trace' : 'Show Agent Trace'}
                              <ChevronDown className={`w-3 h-3 transition-transform ${expandedTrace === msg.id ? 'rotate-180' : ''}`} />
                            </button>
                            {expandedTrace === msg.id && (
                              <div className="p-3 rounded-xl bg-black/40 border border-white/5 backdrop-blur-2xl max-h-[300px] overflow-y-auto">
                                <AgentTraceTimeline steps={msg.trace_log ?? []} isComplete={!isLoading} />
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    ))}
                  </AnimatePresence>
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="px-4 py-3 rounded-2xl flex items-center gap-3 bg-white/5 border border-white/5">
                        <LoadingDots />
                        <span className="text-xs font-mono text-stone-400">
                          {activeAgent ? `${activeAgent} agent working...` : 'Processing...'}
                        </span>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>

                {/* ---- COMPACT INPUT BAR (FIXED HEIGHT) ---- */}
                <div ref={inputBarRef} className="p-3 border-t border-white/5 shrink-0 bg-black/40 backdrop-blur-2xl">
                  <form onSubmit={handleSubmit} className="relative w-full">
                    <input
                      ref={inputRef}
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      placeholder="Follow-up or new query…"
                      disabled={isLoading}
                      className="w-full bg-white/5 backdrop-blur-2xl border border-white/10 rounded-xl px-4 py-2.5 pr-12 text-sm font-mono text-white placeholder-stone-500 focus:outline-none focus:border-emerald-500/50 focus:ring-2 focus:ring-emerald-500/20 transition-all"
                    />
                    <button
                      type="submit"
                      disabled={isLoading || !input.trim()}
                      className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/30 rounded-lg text-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                      <Send className="w-4 h-4" />
                    </button>
                  </form>
                </div>
              </div>
            )}
          </div>
        </main>

        {/* RIGHT PANEL: TELEMETRY */}
        <aside className="w-72 lg:w-80 xl:w-96 shrink-0 flex flex-col gap-2 p-2 overflow-hidden bg-black/20 backdrop-blur-sm border-l border-white/5 min-h-0">
          <LiquidGlassCard className="p-3 bg-white/5 border-white/10 flex-shrink-0">
            <div className="grid grid-cols-3 gap-2">
              {['Planner', 'Researcher', 'Coder', 'Critic', 'Writer'].map((agent) => {
                const isActive = activeAgent === agent && isLoading;
                return (
                  <div
                    key={agent}
                    className={`p-2 rounded-lg text-center transition-all ${
                      isActive ? 'bg-emerald-500/20 border border-emerald-500/40 shadow-[0_0_20px_rgba(16,185,129,0.1)]' : 'bg-white/5 border border-white/5'
                    }`}
                  >
                    <div className={`text-[10px] font-mono font-bold ${isActive ? 'text-emerald-400' : 'text-stone-500'}`}>
                      {agent.toUpperCase()}
                    </div>
                    <div className="text-[8px] font-mono text-stone-600 mt-0.5">
                      {isActive ? <Sparkles className="w-3 h-3 mx-auto text-emerald-400" /> : '●'}
                    </div>
                  </div>
                );
              })}
            </div>
          </LiquidGlassCard>

          <LiquidGlassCard className="flex-1 min-h-0 p-2 bg-white/5 border-white/10 flex flex-col">
            <div className="flex items-center justify-between mb-1.5 px-1 flex-shrink-0">
              <span className="text-[10px] font-mono font-semibold text-stone-400">📟 SYSTEM LOGS</span>
              <span className="text-[8px] text-stone-600">{systemLogs.length} entries</span>
            </div>
            <div className="flex-1 min-h-0 overflow-y-auto font-mono text-[10px] space-y-0.5 bg-black/40 rounded-lg p-2 border border-white/5">
              {systemLogs.slice(-12).map((log, idx) => {
                const isError = log.toLowerCase().includes('error');
                return (
                  <div key={idx} className={`${isError ? 'text-rose-400' : 'text-stone-400'} leading-relaxed font-mono`}>
                    {log}
                  </div>
                );
              })}
            </div>
          </LiquidGlassCard>

          <LiquidGlassCard className="p-2 bg-white/5 border-white/10 flex-shrink-0">
            <div className="flex justify-around text-[10px] font-mono text-stone-500">
              <span>Tokens: <span className="text-white">{metrics.tokens ?? 0}</span></span>
              <span>Latency: <span className="text-white">{metrics.latency ?? 0}ms</span></span>
              <span>Tasks: <span className="text-white">{metrics.tasks ?? 0}</span></span>
            </div>
          </LiquidGlassCard>
        </aside>
      </div>
    </div>
  );
}

export default App;