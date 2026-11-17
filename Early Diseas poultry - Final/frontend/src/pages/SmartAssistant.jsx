import { useState, useRef, useEffect } from 'react';
import { Send, Image as ImageIcon, Bot, User, Loader2 } from 'lucide-react';
import { useLocation } from 'react-router-dom';

export default function SmartAssistant() {
  const location = useLocation();
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      type: 'text',
      content: 'مرحباً بك في المساعد الذكي KAK! 🐔\nيمكنك طرح أي سؤال حول أمراض الدواجن أو رعاية القطيع، وسأجيبك بناءً على قاعدة المعرفة الخاصة بي. كما يمكنك إرفاق صورة لفضلات الطيور وسأقوم بتشخيصها وتقديم نصائح العلاج.'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle incoming symptoms from Diagnostics
  useEffect(() => {
    if (location.state && location.state.symptoms && location.state.symptoms.length > 0) {
      let initialMessageText = 'ألاحظ الأعراض التالية على قطيعي:\n- ' + location.state.symptoms.join('\n- ');
      
      if (location.state.notes && location.state.notes.trim() !== '') {
        initialMessageText += '\n\nملاحظات إضافية:\n' + location.state.notes;
      }
      
      const userMessage = { id: Date.now(), sender: 'user', type: 'text', content: initialMessageText };
      setMessages(prev => [...prev, userMessage]);
      setIsLoading(true);

      // Call the API
      fetch('http://localhost:8001/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: initialMessageText, session_id: 'user_session' })
      })
      .then(res => {
        if (!res.ok) throw new Error('فشل الاتصال بالمساعد الذكي');
        return res.json();
      })
      .then(data => {
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          sender: 'bot',
          type: 'text',
          content: data.answer || "لم أتمكن من العثور على إجابة."
        }]);
      })
      .catch(error => {
        console.error(error);
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          sender: 'bot',
          type: 'text',
          content: "عذراً، الخادم غير متصل حالياً. الرجاء التأكد من تشغيل خادم المساعد الذكي."
        }]);
      })
      .finally(() => {
        setIsLoading(false);
      });

      // Clear the state so it doesn't trigger again on refresh
      window.history.replaceState({}, document.title);
    }
  }, [location.state]);

  const handleSendText = async () => {
    if (!input.trim()) return;

    const userMessage = { id: Date.now(), sender: 'user', type: 'text', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // TODO: Connect to backend RAG
      const response = await fetch('http://localhost:8001/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input, session_id: 'user_session' })
      });
      
      if (!response.ok) throw new Error('فشل الاتصال بالمساعد الذكي');
      
      const data = await response.json();
      
      setMessages(prev => [...prev, {
        id: Date.now(),
        sender: 'bot',
        type: 'text',
        content: data.answer || "لم أتمكن من العثور على إجابة."
      }]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        id: Date.now(),
        sender: 'bot',
        type: 'text',
        content: "عذراً، الخادم غير متصل حالياً. الرجاء التأكد من تشغيل خادم المساعد الذكي."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const imageUrl = URL.createObjectURL(file);
    const userMessage = { id: Date.now(), sender: 'user', type: 'image', content: imageUrl };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // TODO: Connect to backend RAG image diagnose
      const response = await fetch('http://localhost:8001/image/diagnose', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) throw new Error('فشل الاتصال بالمساعد الذكي');
      
      const data = await response.json();
      
      const botResponse = `التشخيص: **${data.disease}** (بدقة ${Math.round(data.confidence * 100)}%)\n\n${data.explanation}`;
      
      setMessages(prev => [...prev, {
        id: Date.now(),
        sender: 'bot',
        type: 'text',
        content: botResponse
      }]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        id: Date.now(),
        sender: 'bot',
        type: 'text',
        content: "عذراً، حدث خطأ أثناء فحص الصورة. تأكد من تشغيل خادم المساعد الذكي."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-slate-800 rounded-3xl shadow-sm overflow-hidden border border-gray-200 dark:border-slate-700">
      
      {/* Header */}
      <div className="bg-[#B71C1C] p-4 text-white flex justify-between items-center shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
            <Bot size={24} />
          </div>
          <div>
            <h2 className="font-bold text-lg">المساعد الذكي (KAK AI)</h2>
            <p className="text-xs text-white/80">مدعوم بنظام RAG الطبي للرد على استفساراتك</p>
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 p-6 overflow-y-auto bg-[#F9FAFB] dark:bg-slate-900 flex flex-col gap-6">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex gap-4 max-w-[80%] ${msg.sender === 'user' ? 'mr-auto flex-row-reverse' : 'ml-auto'}`}>
            
            <div className={`w-10 h-10 shrink-0 rounded-full flex items-center justify-center text-white shadow-sm ${msg.sender === 'user' ? 'bg-[#0F172A]' : 'bg-[#B71C1C]'}`}>
              {msg.sender === 'user' ? <User size={20} /> : <Bot size={20} />}
            </div>

            <div className={`p-4 rounded-2xl shadow-sm text-sm leading-relaxed ${
              msg.sender === 'user' 
                ? 'bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-800 dark:text-gray-200 rounded-tl-none'
                : 'bg-white dark:bg-slate-800 border border-red-100 dark:border-slate-700 text-gray-800 dark:text-gray-200 rounded-tr-none'
            }`}>
              {msg.type === 'text' ? (
                <div className="whitespace-pre-wrap">{msg.content}</div>
              ) : (
                <img src={msg.content} alt="User Upload" className="max-w-xs rounded-xl" />
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-4 max-w-[80%] ml-auto">
            <div className="w-10 h-10 shrink-0 rounded-full flex items-center justify-center text-white shadow-sm bg-[#B71C1C]">
              <Bot size={20} />
            </div>
            <div className="p-4 rounded-2xl rounded-tr-none bg-white dark:bg-slate-800 border border-red-100 dark:border-slate-700 shadow-sm flex items-center gap-3">
              <Loader2 size={18} className="animate-spin text-[#B71C1C]" />
              <span className="text-gray-500 text-sm">المساعد يكتب...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white dark:bg-slate-800 border-t border-gray-200 dark:border-slate-700 shrink-0">
        <div className="flex items-center gap-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-2xl p-2 px-4 focus-within:border-[#B71C1C] transition-colors">
          
          <button onClick={() => fileInputRef.current?.click()} className="text-gray-400 hover:text-[#B71C1C] transition-colors p-2" title="إرفاق صورة">
            <ImageIcon size={22} />
          </button>
          <input type="file" ref={fileInputRef} className="hidden" accept="image/*" onChange={handleImageUpload} />
          
          <input 
            type="text" 
            placeholder="اسأل المساعد الذكي عن أي شيء..." 
            className="flex-1 bg-transparent border-none outline-none text-sm p-2 text-gray-800 dark:text-gray-200"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendText()}
            disabled={isLoading}
          />
          
          <button 
            onClick={handleSendText}
            disabled={!input.trim() || isLoading}
            className={`p-2 rounded-xl flex items-center justify-center transition-colors ${input.trim() ? 'bg-[#B71C1C] text-white' : 'bg-gray-200 text-gray-400'}`}
          >
            <Send size={18} className="rtl:rotate-180" />
          </button>
        </div>
      </div>

    </div>
  );
}
