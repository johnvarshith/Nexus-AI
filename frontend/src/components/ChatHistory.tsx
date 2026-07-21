import React from 'react';
import { useChatStore } from '../store/useChatStore';
import { Plus, Trash2, Clock } from 'lucide-react';

interface ChatHistoryProps {
  onNewChat: () => void;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ onNewChat }) => {
  const { threads, currentThreadId, switchThread, messages, clearChat } = useChatStore();
  const hasMessages = messages.length > 0;

  return (
    <div className="h-full flex flex-col p-3 overflow-hidden">
      <button
        onClick={onNewChat}
        className="w-full mb-4 flex items-center justify-center gap-2 py-2.5 px-4 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 rounded-xl text-sm font-medium text-emerald-300 transition-all flex-shrink-0"
      >
        <Plus className="w-4 h-4" />
        New Chat
      </button>

      <div className="flex-1 min-h-0 overflow-y-auto space-y-2">
        {threads.length === 0 && !hasMessages ? (
          <div className="text-xs text-stone-500 italic text-center py-8">No previous chats</div>
        ) : (
          <>
            {hasMessages && (
              <div className="px-2 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-emerald-400 truncate">Active Chat</span>
                  <span className="text-[10px] text-stone-500">{messages.length} msgs</span>
                </div>
                <div className="mt-1 text-xs text-stone-400 truncate">
                  {messages[0]?.content?.slice(0, 40)}...
                </div>
              </div>
            )}
            {threads.map((thread) => (
              <div
                key={thread.id}
                onClick={() => switchThread(thread.id)}
                className={`px-2 py-1.5 rounded-lg border cursor-pointer transition-all hover:bg-white/10 ${
                  thread.id === currentThreadId && !hasMessages
                    ? 'bg-white/10 border-white/20'
                    : 'bg-white/5 border-white/5'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-stone-400 truncate">
                    {thread.title || 'Untitled'}
                  </span>
                  <span className="text-[10px] text-stone-600">{thread.messages.length} msgs</span>
                </div>
                <div className="mt-1 text-xs text-stone-500 truncate">
                  {thread.messages[thread.messages.length - 1]?.content?.slice(0, 40)}...
                </div>
                <div className="mt-0.5 text-[9px] text-stone-600 flex items-center gap-1">
                  <Clock className="w-2.5 h-2.5" />
                  {new Date(thread.lastUpdated).toLocaleDateString()}
                </div>
              </div>
            ))}
          </>
        )}
      </div>

      <button
        onClick={clearChat}
        className="border-t border-white/5 pt-3 mt-2 w-full flex items-center justify-center gap-2 py-2 text-xs text-stone-500 hover:text-rose-400 transition-colors flex-shrink-0"
      >
        <Trash2 className="w-3.5 h-3.5" />
        Clear History
      </button>
    </div>
  );
};

export default ChatHistory;