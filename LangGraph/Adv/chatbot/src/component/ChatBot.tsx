import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import type { Message } from '../types';
import { ChatMessages } from './ChatMessage';
import Header from './Header';
import { InputArea, Sidebar } from './Sidebar';

const Chatbot: React.FC = () => {
  const { id: currentSessionId } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [sessions, setSessions] = useState<string[]>([]);

  useEffect(() => {
    const fetchChatHistory = async () => {
      if (!currentSessionId) {
        setMessages([]);
        return;
      }

      setIsLoading(true);
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/getChats?currentSessionId=${encodeURIComponent(currentSessionId)}`,
          {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
          }
        );
      
        if (!response.ok) {
          const errorData = await response.json();
          console.error('Validation Error Details:', errorData);
          return;
        }

        const data = await response.json();
      
        if (data.history) {
          setMessages(data.history);
        }
      } catch (error) {
        console.error('Error fetching chat history:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchChatHistory();
  }, [currentSessionId]);

  useEffect(() => {
    const getAllSessions = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/getChatSessions');
        const data = await response.json();
        if (data.statusCode === 200) {
          setSessions(data.sessions);
        }
      } catch (error) {
        console.error('Error fetching sessions:', error);
      }
    };
    getAllSessions();
  }, [messages]); 

  const handleNewSession = () => {
    const myUUID = crypto.randomUUID();
 
    navigate(`/session/${myUUID}`);
  };

  const handleSendMessage = async (message: string) => {
    const activeId = currentSessionId || crypto.randomUUID();
    
    if (!currentSessionId) {
        navigate(`/session/${activeId}`);
    }

    setMessages(prev => [...prev, { content: message, isUser: true }]);
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, sessionId: activeId }),
      });

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader');

      const decoder = new TextDecoder();
      let aiMessage = '';
      
      setMessages(prev => [...prev, { content: '', isUser: false }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        aiMessage += chunk;
        
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1] = { content: aiMessage, isUser: false };
          return newMessages;
        });
      }
    } catch (error) {
      console.error('Streaming error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-[#212121] h-screen flex">
      <Sidebar sessions={sessions} onNewSession={handleNewSession} />
      <div className="flex-1 flex flex-col">
        <Header />
        <ChatMessages messages={messages} />
        <InputArea onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default Chatbot;