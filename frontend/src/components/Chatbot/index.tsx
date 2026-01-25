import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import AuthModal from '../AuthModal';
import styles from './styles.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  toolCalls?: ToolCall[];
  model?: string;
}

interface Citation {
  id: number;
  source: string;
  chapter: string;
  score: number;
}

interface ToolCall {
  tool: string;
  status: string;
}

interface ChatSession {
  id: string;
  title: string;
  message_count: number;
}

// API helper
const getApiBaseUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:8000';
  return window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : `${window.location.protocol}//${window.location.hostname}:8000`;
};

export default function Chatbot(): JSX.Element {
  const { user, signOut } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [showAuth, setShowAuth] = useState(false);
  const [showSidebar, setShowSidebar] = useState(false);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! I\'m your AI learning assistant. Ask me anything about the book content!'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load sessions when user logs in
  useEffect(() => {
    if (user) {
      loadSessions();
    } else {
      setSessions([]);
      setCurrentSessionId(null);
    }
  }, [user]);

  // Listen for text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim().length > 0) {
        setSelectedText(selection.toString().trim());
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  const loadSessions = async () => {
    try {
      const response = await fetch(`${getApiBaseUrl()}/api/chat/sessions`, {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setSessions(data);
      }
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const loadSession = async (sessionId: string) => {
    try {
      const response = await fetch(`${getApiBaseUrl()}/api/chat/sessions/${sessionId}`, {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setCurrentSessionId(sessionId);
        setMessages(data.messages.map((m: any) => ({
          role: m.role,
          content: m.content,
          model: m.model
        })));
        setShowSidebar(false);
      }
    } catch (error) {
      console.error('Failed to load session:', error);
    }
  };

  const startNewChat = () => {
    setCurrentSessionId(null);
    setMessages([{
      role: 'assistant',
      content: 'Hello! I\'m your AI learning assistant. Ask me anything about the book content!'
    }]);
    setShowSidebar(false);
  };

  const deleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await fetch(`${getApiBaseUrl()}/api/chat/sessions/${sessionId}`, {
        method: 'DELETE',
        credentials: 'include',
      });
      setSessions(prev => prev.filter(s => s.id !== sessionId));
      if (currentSessionId === sessionId) {
        startNewChat();
      }
    } catch (error) {
      console.error('Failed to delete session:', error);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() && !selectedText) return;

    const userMessage: Message = {
      role: 'user',
      content: selectedText
        ? `Regarding this text: "${selectedText.substring(0, 200)}${selectedText.length > 200 ? '...' : ''}"\n\n${input}`
        : input
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setSelectedText('');
    setIsLoading(true);

    try {
      const response = await fetch(`${getApiBaseUrl()}/api/chat/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          query: userMessage.content,
          selected_text: selectedText || undefined,
          chapter_id: getCurrentChapterId(),
          session_id: currentSessionId || undefined,
        }),
      });

      if (response.ok) {
        const data = await response.json();

        // Update session ID if new session was created
        if (data.session_id && !currentSessionId) {
          setCurrentSessionId(data.session_id);
          loadSessions(); // Refresh session list
        }

        const assistantMessage: Message = {
          role: 'assistant',
          content: data.answer,
          citations: data.citations,
          toolCalls: data.tool_calls,
          model: data.model,
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        throw new Error('Failed to get response');
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again later.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const getCurrentChapterId = (): string | undefined => {
    const path = window.location.pathname;
    const match = path.match(/chapter-(\d+)/);
    return match ? `chapter-${match[1]}` : undefined;
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearSelectedText = () => {
    setSelectedText('');
    window.getSelection()?.removeAllRanges();
  };

  return (
    <>
      {/* Chat Toggle Button */}
      <button
        className={styles.chatToggle}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chat"
      >
        {isOpen ? 'X' : '?'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <div className={styles.headerLeft}>
              {user && (
                <button
                  className={styles.menuBtn}
                  onClick={() => setShowSidebar(!showSidebar)}
                  title="Chat History"
                >
                  =
                </button>
              )}
              <h3>AI Assistant</h3>
            </div>
            <div className={styles.headerRight}>
              {user ? (
                <div className={styles.userInfo}>
                  <span className={styles.userName}>{user.name || user.email}</span>
                  <button onClick={signOut} className={styles.logoutBtn}>Logout</button>
                </div>
              ) : (
                <button onClick={() => setShowAuth(true)} className={styles.loginBtn}>
                  Login
                </button>
              )}
            </div>
          </div>

          {/* Sidebar for chat history */}
          {showSidebar && user && (
            <div className={styles.sidebar}>
              <div className={styles.sidebarHeader}>
                <h4>Chat History</h4>
                <button onClick={startNewChat} className={styles.newChatBtn}>+ New Chat</button>
              </div>
              <div className={styles.sessionList}>
                {sessions.length === 0 ? (
                  <p className={styles.noSessions}>No previous chats</p>
                ) : (
                  sessions.map(session => (
                    <div
                      key={session.id}
                      className={`${styles.sessionItem} ${session.id === currentSessionId ? styles.active : ''}`}
                      onClick={() => loadSession(session.id)}
                    >
                      <span className={styles.sessionTitle}>{session.title}</span>
                      <button
                        className={styles.deleteBtn}
                        onClick={(e) => deleteSession(session.id, e)}
                      >
                        x
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          <div className={styles.messagesContainer}>
            {!user && (
              <div className={styles.loginPrompt}>
                <p><strong>Login to save your chat history!</strong></p>
                <button onClick={() => setShowAuth(true)}>Login / Sign Up</button>
              </div>
            )}
            {messages.map((msg, idx) => (
              <div key={idx} className={`${styles.message} ${styles[msg.role]}`}>
                <div className={styles.messageContent}>
                  {msg.content}
                </div>
                {msg.toolCalls && msg.toolCalls.length > 0 && (
                  <div className={styles.toolCalls}>
                    <span className={styles.toolCallsLabel}>Tools used:</span>
                    {msg.toolCalls.map((tc, i) => (
                      <span key={i} className={styles.toolCall}>
                        {tc.tool}
                      </span>
                    ))}
                  </div>
                )}
                {msg.citations && msg.citations.length > 0 && (
                  <div className={styles.citations}>
                    <span className={styles.citationsLabel}>Sources:</span>
                    {msg.citations.map((cite) => (
                      <a key={cite.id} href={`/book/${cite.chapter}`} className={styles.citation}>
                        [{cite.id}] {cite.source}
                      </a>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.typing}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {selectedText && (
            <div className={styles.selectedTextBanner}>
              <span>Selected: "{selectedText.substring(0, 50)}..."</span>
              <button onClick={clearSelectedText}>X</button>
            </div>
          )}

          <div className={styles.inputContainer}>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={selectedText ? "Ask about the selected text..." : "Ask a question..."}
              rows={1}
              className={styles.input}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || (!input.trim() && !selectedText)}
              className={styles.sendButton}
            >
              &gt;
            </button>
          </div>
        </div>
      )}

      {/* Auth Modal */}
      <AuthModal isOpen={showAuth} onClose={() => setShowAuth(false)} />
    </>
  );
}
