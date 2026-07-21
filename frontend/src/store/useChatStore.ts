import { create } from 'zustand';
import axios from 'axios';

const generateId = () => `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  trace_log?: any[];
}

export interface Thread {
  id: string;
  title: string;
  messages: Message[];
  lastUpdated: string;
}

interface Metrics {
  tokens: number;
  latency: number;
  tasks: number;
}

interface ChatState {
  threads: Thread[];
  currentThreadId: string | null;
  messages: Message[];
  isLoading: boolean;
  activeAgent: string | null;
  systemLogs: string[];
  metrics: Metrics;
  threadId: string | null;

  sendMessage: (text: string, deepThink?: boolean) => Promise<void>;
  addLog: (log: string) => void;
  clearChat: () => void;
  switchThread: (threadId: string) => void;
  newChat: () => void;
  setActiveAgent: (agent: string | null) => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  threads: [],
  currentThreadId: null,
  messages: [],
  isLoading: false,
  activeAgent: null,
  systemLogs: ["[SYSTEM] NexusAI Dashboard initialized.", "[SYSTEM] Connected to local Ollama."],
  metrics: { tokens: 0, latency: 0, tasks: 0 },
  threadId: null,

  addLog: (log: string) => {
    const time = new Date().toLocaleTimeString('en-US', { hour12: false });
    set((state) => ({
      systemLogs: [...state.systemLogs.slice(-20), `[${time}] ${log}`]
    }));
  },

  setActiveAgent: (agent: string | null) => set({ activeAgent: agent }),

  newChat: () => {
    const { messages, threads, currentThreadId } = get();
    if (messages.length > 0) {
      const title = messages[0]?.content?.slice(0, 30) || 'Untitled';
      const existingThreadIndex = threads.findIndex(t => t.id === currentThreadId);
      if (existingThreadIndex !== -1) {
        const updatedThreads = [...threads];
        updatedThreads[existingThreadIndex] = {
          ...updatedThreads[existingThreadIndex],
          messages: messages,
          lastUpdated: new Date().toISOString(),
          title: title,
        };
        set({ threads: updatedThreads });
      } else {
        const newThread: Thread = {
          id: generateId(),
          title: title,
          messages: messages,
          lastUpdated: new Date().toISOString(),
        };
        set({ threads: [newThread, ...threads] });
      }
    }
    set({
      messages: [],
      threadId: null,
      currentThreadId: null,
      metrics: { tokens: 0, latency: 0, tasks: 0 }
    });
    get().addLog("Started new chat.");
  },

  switchThread: (threadId: string) => {
    const { threads } = get();
    const thread = threads.find(t => t.id === threadId);
    if (!thread) return;

    const { messages, currentThreadId } = get();
    if (messages.length > 0 && currentThreadId) {
      const updatedThreads = threads.map(t => {
        if (t.id === currentThreadId) {
          return { ...t, messages: messages, lastUpdated: new Date().toISOString() };
        }
        return t;
      });
      set({ threads: updatedThreads });
    }

    set({
      messages: thread.messages,
      currentThreadId: thread.id,
      threadId: thread.id,
    });
    get().addLog(`Loaded: ${thread.title}`);
  },

  sendMessage: async (text: string, deepThink: boolean = false) => {
    if (!text.trim()) return;
    const startTime = Date.now();
    const { threadId } = get();

    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString()
    };

    set((state) => ({
      messages: [...state.messages, userMessage],
      isLoading: true,
      activeAgent: 'Planner',
    }));
    get().addLog(`USER: "${text.substring(0, 40)}..."`);

    let currentThreadIdToSend = threadId;
    if (!currentThreadIdToSend) {
      currentThreadIdToSend = generateId();
      set({ threadId: currentThreadIdToSend, currentThreadId: currentThreadIdToSend });
    }

    try {
      const res = await axios.post('http://localhost:8000/api/chat', {
        message: text,
        thread_id: currentThreadIdToSend,
        deep_think: deepThink,
      });

      const latency = Date.now() - startTime;
      const aiContent = res.data.response || "No response.";
      const trace = res.data.trace_log || [];
      const confidence = res.data.confidence_score || 0;

      const assistantMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: aiContent,
        timestamp: new Date().toLocaleTimeString(),
        trace_log: trace,
      };

      set((state) => {
        const newMessages = [...state.messages, assistantMessage];
        const updatedThreads = state.threads.map(t => {
          if (t.id === state.currentThreadId || t.id === state.threadId) {
            return {
              ...t,
              messages: newMessages,
              lastUpdated: new Date().toISOString(),
              title: newMessages[0]?.content?.slice(0, 30) || 'Untitled'
            };
          }
          return t;
        });

        const exists = updatedThreads.some(t => t.id === state.currentThreadId || t.id === state.threadId);
        const finalThreads = exists ? updatedThreads : [
          {
            id: state.threadId || generateId(),
            title: newMessages[0]?.content?.slice(0, 30) || 'Untitled',
            messages: newMessages,
            lastUpdated: new Date().toISOString()
          },
          ...updatedThreads
        ];

        return {
          messages: newMessages,
          isLoading: false,
          activeAgent: null,
          metrics: {
            tokens: state.metrics.tokens + Math.floor(aiContent.length / 4),
            latency: latency,
            tasks: state.metrics.tasks + 1
          },
          threads: finalThreads,
          threadId: state.threadId || finalThreads[0]?.id,
          currentThreadId: state.currentThreadId || finalThreads[0]?.id,
        };
      });
      get().addLog(`SUCCESS: ${latency}ms (Conf: ${confidence}%)`);

    } catch (err) {
      console.error(err);
      get().addLog("ERROR: Backend unreachable");
      set({ isLoading: false, activeAgent: null });
    }
  },

  clearChat: () => {
    get().newChat();
  },
}));