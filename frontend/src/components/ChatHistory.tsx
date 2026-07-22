import React, { useState } from 'react';
import { useChatStore } from '../store/useChatStore';
import { Plus, Trash2, Clock, MoreVertical, Pencil } from 'lucide-react';

interface ChatHistoryProps {
  onNewChat: () => void;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ onNewChat }) => {
  const { threads, currentThreadId, switchThread, messages, clearChat, deleteThread, renameThread } = useChatStore();
  const [openMenuId, setOpenMenuId] = useState<string | null>(null);
  const hasMessages = messages.length > 0;

  const handleRename = (id: string, currentTitle: string) => {
    const newTitle = window.prompt('Enter new chat name:', currentTitle);
    if (newTitle && newTitle.trim()) {
      renameThread(id, newTitle.trim());
    }
    setOpenMenuId(null);
  };

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
                className={`px-2 py-1.5 rounded-lg border transition-all hover:bg-white/10 ${
                  thread.id === currentThreadId && !hasMessages
                    ? 'bg-white/10 border-white/20'
                    : 'bg-white/5 border-white/5'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0 cursor-pointer" onClick={() => switchThread(thread.id)}>
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
                  <div className="relative flex-shrink-0">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setOpenMenuId(openMenuId === thread.id ? null : thread.id);
                      }}
                      className="p-1 hover:bg-white/10 rounded"
                    >
                      <MoreVertical className="w-3.5 h-3.5 text-stone-500" />
                    </button>
                    {openMenuId === thread.id && (
                      <div className="absolute right-0 mt-1 w-32 bg-stone-900 border border-white/10 rounded-lg shadow-lg z-10">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleRename(thread.id, thread.title);
                          }}
                          className="flex items-center gap-2 w-full px-3 py-1.5 text-xs text-stone-300 hover:bg-white/10"
                        >
                          <Pencil className="w-3 h-3" /> Rename
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteThread(thread.id);
                            setOpenMenuId(null);
                          }}
                          className="flex items-center gap-2 w-full px-3 py-1.5 text-xs text-rose-400 hover:bg-white/10"
                        >
                          <Trash2 className="w-3 h-3" /> Delete
                        </button>
                      </div>
                    )}
                  </div>
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