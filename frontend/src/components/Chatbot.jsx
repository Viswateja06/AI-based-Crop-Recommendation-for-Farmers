import React, { useState, useEffect, useRef } from 'react';
import { chatWithBot } from '../services/api';
import { Send, Bot, User } from 'lucide-react';

const TypewriterText = ({ text, isTyping, onTyping }) => {
  const [displayedText, setDisplayedText] = useState(isTyping ? '' : text);
  
  useEffect(() => {
    if (!isTyping) {
      setDisplayedText(text);
      return;
    }
    let i = 0;
    const words = text.split(' ');
    const interval = setInterval(() => {
      setDisplayedText(words.slice(0, i + 1).join(' '));
      i++;
      if (onTyping) onTyping();
      if (i >= words.length) {
        clearInterval(interval);
        if (onTyping) onTyping();
      }
    }, 100); // 100ms per word
    return () => clearInterval(interval);
  }, [text, isTyping]);

  return <span>{displayedText}</span>;
};

const Chatbot = ({ t, language }) => {
  const [messages, setMessages] = useState([
    { text: t.chatbotWelcome || "Hello! I am the AI Farmer Advisory Bot. How can I help you today?", isBot: true, isTyping: false }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim()) return;

    // Remove typing status from older messages
    setMessages(prev => prev.map(m => ({ ...m, isTyping: false })));

    const userMessage = input;
    setMessages(prev => [...prev, { text: userMessage, isBot: false, isTyping: false }]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await chatWithBot(userMessage, language);
      setMessages(prev => [...prev, { text: data.response, isBot: true, isTyping: true }]);
    } catch (error) {
      setMessages(prev => [...prev, { text: "Error connecting to the advisory system.", isBot: true, isTyping: true }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-240px)] min-h-[400px] w-full max-w-2xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden border border-green-100">
      <div className="bg-green-600 p-4 text-white flex items-center shadow-md">
        <Bot className="mr-2" />
        <h2 className="text-xl font-bold">{t.chatbotTitle}</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.isBot ? 'justify-start' : 'justify-end'}`}>
            <div className={`flex max-w-[80%] rounded-2xl p-3 ${
              msg.isBot ? 'bg-white border border-gray-200 text-gray-800 rounded-tl-none shadow-sm' : 'bg-green-500 text-white rounded-tr-none shadow-md'
            }`}>
              {msg.isBot && <Bot className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0 text-green-600" />}
              {!msg.isBot && <User className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0 text-green-200" />}
              {msg.isBot ? (
                <p className="text-sm md:text-base whitespace-pre-wrap"><TypewriterText text={msg.text} isTyping={msg.isTyping} onTyping={scrollToBottom} /></p>
              ) : (
                <p className="text-sm md:text-base whitespace-pre-wrap">{msg.text}</p>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
             <div className="bg-white border border-gray-200 text-gray-800 rounded-2xl rounded-tl-none p-4 shadow-sm flex items-center space-x-2">
               <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce"></div>
               <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce" style={{ animationDelay: "0.2s"}}></div>
               <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: "0.4s"}}></div>
             </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="p-4 bg-white border-t border-gray-200 flex items-center space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 p-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="bg-green-600 text-white p-3 rounded-full hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center h-12 w-12"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>
    </div>
  );
};

export default Chatbot;
