export interface Message {
  content: string;
  isUser: boolean;
}

export interface ChatMessageProps {
  content: string;
  isUser: boolean;
}

export interface SidebarProps {
  onNewSession: () => void;
  sessions: string[]
}

export interface ChatMessagesProps {
  messages: Message[];
}

export interface InputAreaProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}