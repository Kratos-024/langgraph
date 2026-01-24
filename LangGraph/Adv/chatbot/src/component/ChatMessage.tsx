import React, { useEffect, useRef } from 'react';
import { Copy, ThumbsUp } from 'lucide-react';
import type { ChatMessageProps, ChatMessagesProps } from '../types';

const ChatMessage: React.FC<ChatMessageProps> = ({ content, isUser }) => {
  if (isUser) {
    return (
      <div className="flex justify-end mb-6">
        <div className="bg-[#2a2a2a] text-gray-200 rounded-2xl px-4 py-2 max-w-md">
          {content}
        </div>
      </div>
    );
  }

  return (
    <div className="mb-6">
      <div className="text-gray-200 mb-2">{content}</div>
      <div className="flex items-center space-x-2 text-gray-500">
        <button className="hover:text-gray-300">
          <Copy className="w-4 h-4" />
        </button>
        <button className="hover:text-gray-300">
          <ThumbsUp className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

const ChatMessages: React.FC<ChatMessagesProps> = ({ messages }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto px-6 py-8">
      {messages.map((msg, index) => (
        <ChatMessage key={index} content={msg.content} isUser={msg.isUser} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export  {ChatMessage,ChatMessages};
  ;