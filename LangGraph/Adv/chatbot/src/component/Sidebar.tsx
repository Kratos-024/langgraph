import React, { useRef, useState } from 'react';
import { Plus, Send } from 'lucide-react';
import type { InputAreaProps, SidebarProps } from '../types';
import { NavLink } from 'react-router-dom';

const Sidebar: React.FC<SidebarProps> = ({ onNewSession, sessions }) => {
  return (
    <div className="w-16 bg-[#1a1a1a] border-r border-gray-800 flex flex-col items-center py-4 space-y-4">
      <button
        onClick={onNewSession}
        className="w-10 h-10 rounded-lg bg-[#2a2a2a6b] hover:bg-[#3a3a3a] flex items-center justify-center text-gray-400 transition-colors border border-transparent hover:border-gray-600"
        aria-label="New Session"
      >
        <Plus className="w-5 h-5" />
      </button>

      <div className="w-full border-t border-gray-800 my-2" />

      <div className='gap-y-3 flex items-center justify-center flex-col w-full px-2'>
        {sessions.map((sessionId) => (
          <NavLink 
            key={sessionId}
            to={`/session/${sessionId}`} 
            className={({ isActive }) => `
              w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-200 group
              ${isActive 
                ? 'bg-orange-500 text-white shadow-lg shadow-orange-500/20' 
                : 'bg-[#2a2a2a6b] text-gray-400 hover:bg-[#3a3a3a] hover:text-white'
              }
            `}
            title={`Session: ${sessionId}`}
          >
            <span className="text-[10px] font-bold uppercase">
              {sessionId.toString().slice(0, 2)}
            </span>
            
            <div className="absolute left-16 scale-0 group-hover:scale-100 transition-transform bg-gray-800 text-white text-xs py-1 px-2 rounded ml-2 whitespace-nowrap z-50 pointer-events-none">
              Session {sessionId.slice(0, 8)}...
            </div>
          </NavLink>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;

const InputArea: React.FC<InputAreaProps> = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState<string>('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (message.trim() && !isLoading) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-800 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Reply..."
            rows={1}
            className="w-full bg-[#2a2a2a] text-gray-200 rounded-lg px-4 py-3 pr-32 resize-none focus:outline-none focus:ring-1 focus:ring-gray-600 placeholder-gray-500"
            disabled={isLoading}
          />
          <div className="absolute right-2 bottom-2 flex items-center space-x-2">
            <select className="bg-transparent text-gray-400 text-xs border-none focus:outline-none">
              <option>sonnet 4.5</option>
            </select>
            <button
              onClick={handleSend}
              disabled={isLoading}
              className="bg-orange-500 hover:bg-orange-600 text-white rounded p-1.5 disabled:opacity-50"
              aria-label="Send message"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
        <div className="text-center text-xs text-gray-600 mt-2">
          Claude is AI and can make mistakes. Please double-check responses.
        </div>
      </div>
    </div>
  );
};

export  {InputArea,Sidebar};
