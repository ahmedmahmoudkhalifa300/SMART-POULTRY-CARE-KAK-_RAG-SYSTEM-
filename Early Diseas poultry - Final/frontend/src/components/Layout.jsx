import { useState, useEffect, useRef } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useNotifications } from '../context/NotificationContext';
import { LayoutDashboard, ClipboardList, MessageSquare, Calendar, Syringe, Wallet, History, Search, Bell, Settings, HelpCircle, User, Bot, MessageCircle, Moon, Sun, LogOut } from 'lucide-react';

export default function Layout() {
  const navigate = useNavigate();
  const [isDarkMode, setIsDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark';
  });
  
  const [user, setUser] = useState(null);
  const [showNotifications, setShowNotifications] = useState(false);
  const { alerts, unreadCount, markAsRead, markAllAsRead } = useNotifications();
  const notificationRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (notificationRef.current && !notificationRef.current.contains(event.target)) {
        setShowNotifications(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
       setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogout = () => {
     // Save current state to the user's profile before clearing
     const users = JSON.parse(localStorage.getItem('registeredUsers')) || [];
     const userIndex = users.findIndex(u => u.email === user.email);
     if (userIndex !== -1) {
         users[userIndex].appData = {
             currentFlockId: localStorage.getItem('currentFlockId'),
             flockSize: localStorage.getItem('flockSize'),
             cycleAge: localStorage.getItem('cycleAge'),
             manualMortality: localStorage.getItem('manualMortality'),
             manualFeed: localStorage.getItem('manualFeed'),
             mortalityInitialized: localStorage.getItem('mortalityInitialized'),
             season: localStorage.getItem('season'),
             chicksNotReceived: localStorage.getItem('chicksNotReceived'),
             alerts: localStorage.getItem('alerts'),
             financial_transactions: localStorage.getItem('financial_transactions'),
             financial_categories: localStorage.getItem('financial_categories'),
             vaccinations: localStorage.getItem('vaccinations')
         };
         localStorage.setItem('registeredUsers', JSON.stringify(users));
     }

     // Clear global app data to ensure new users start fresh
     const keysToKeep = ['registeredUsers', 'theme'];
     Object.keys(localStorage).forEach(key => {
         if (!keysToKeep.includes(key)) {
             localStorage.removeItem(key);
         }
     });

     navigate('/');
  };

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDarkMode]);
  const menuItems = [
    { name: 'لوحة التحكم', path: '/dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'المساعد الذكي', path: '/assistant', icon: <Bot size={20} /> },
    { name: 'التشخيص الذكي', path: '/diagnostics', icon: <ClipboardList size={20} /> },
    { name: 'الإدارة اليومية', path: '/daily', icon: <Calendar size={20} /> },
    { name: 'التطعيمات', path: '/vaccinations', icon: <Syringe size={20} /> },
    { name: 'الإدارة المالية', path: '/financials', icon: <Wallet size={20} /> },
    { name: 'السجل التاريخي', path: '/history', icon: <History size={20} /> },
  ];

  return (
    <div className="flex min-h-screen bg-[#F9FAFB] dark:bg-slate-900" dir="rtl">
      {/* Sidebar */}
      <aside className="w-[280px] bg-white dark:bg-slate-800 border-l border-gray-200 dark:border-slate-700 flex flex-col py-8 z-10 shadow-sm transition-colors duration-200">
        <div className="flex items-center gap-3 px-8 mb-10">
          <div className="w-10 h-10 bg-[#B71C1C] rounded-xl flex items-center justify-center text-white shadow-sm">
            <Bot size={24} />
          </div>
          <div>
            <h1 className="font-extrabold text-xl text-[#0F172A] dark:text-white leading-tight transition-colors duration-200">KAK</h1>
            <p className="text-[10px] text-gray-500 dark:text-gray-400 font-bold">مساعدك الذكي</p>
          </div>
        </div>

        <nav className="flex-col gap-2 flex-1 px-4">
          {menuItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => 
                `flex items-center gap-4 px-4 py-3.5 my-1 rounded-xl transition-all font-bold text-sm ${
                  isActive 
                    ? 'bg-[#B71C1C] text-white shadow-md' 
                    : 'text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-slate-700 hover:text-gray-900 dark:hover:text-white'
                }`
              }
            >
              {item.icon}
              <span>{item.name}</span>
            </NavLink>
          ))}
        </nav>
        
        <div className="px-6 flex-col gap-3 mt-auto pt-6">
          <button className="w-full flex items-center justify-center gap-2 bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-3.5 px-4 rounded-xl transition-colors mb-4 shadow-sm text-sm">
             <span className="w-4 h-4 flex items-center justify-center rounded-full border border-white text-[10px] font-black">★</span>
             ترقية الخطة
          </button>
          
          <div className="flex items-center gap-4 px-4 py-3 text-gray-500 dark:text-gray-400 cursor-pointer hover:bg-gray-50 dark:hover:bg-slate-700 hover:text-gray-900 dark:hover:text-white rounded-xl transition-colors font-bold text-sm">
             <Settings size={20} />
             <span>الإعدادات</span>
          </div>
          <div 
             onClick={handleLogout}
             className="flex items-center gap-4 px-4 py-3 text-red-500 dark:text-red-400 cursor-pointer hover:bg-red-50 dark:hover:bg-slate-700 hover:text-red-600 dark:hover:text-red-300 rounded-xl transition-colors font-bold text-sm"
          >
             <LogOut size={20} />
             <span>تسجيل الخروج</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col bg-[#F9FAFB] dark:bg-slate-900 overflow-hidden relative transition-colors duration-200">
        <header className="px-10 py-6 flex justify-between items-center bg-[#F9FAFB] dark:bg-slate-900 transition-colors duration-200">
          <div className="flex items-center w-full max-w-xl relative">
             <Search className="absolute right-4 text-gray-400 dark:text-gray-500" size={20} />
             <input type="text" placeholder="البحث في السجلات المالية..." className="w-full bg-white dark:bg-slate-800 dark:text-white border border-gray-200 dark:border-slate-700 rounded-full py-3 pr-12 pl-4 text-sm focus:outline-none focus:border-[#B71C1C] shadow-sm transition-colors duration-200"/>
          </div>
          <div className="flex items-center gap-6" dir="ltr">
             <div className="flex items-center gap-3 pr-6">
                <div className="w-10 h-10 rounded-full bg-gray-200 dark:bg-slate-700 border-2 border-white dark:border-slate-800 shadow-sm overflow-hidden flex items-center justify-center">
                   <User size={20} className="text-gray-500 dark:text-gray-400" />
                </div>
                <div className="text-left">
                   <div className="font-bold text-sm text-[#0F172A] dark:text-white">
                      {user ? user.fullName : 'لوحة الإدارة'}
                   </div>
                   <div className="text-[10px] text-gray-500 dark:text-gray-400 font-bold">مدير المزرعة</div>
                </div>
             </div>
             
             {/* Dark Mode Toggle */}
             <div onClick={() => setIsDarkMode(!isDarkMode)} className="cursor-pointer text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white border-l border-gray-200 dark:border-slate-700 pl-6 transition-colors">
                {isDarkMode ? <Sun size={22} /> : <Moon size={22} />}
             </div>

             <div className="relative" ref={notificationRef}>
                <div 
                   onClick={() => setShowNotifications(!showNotifications)} 
                   className="cursor-pointer text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white relative"
                >
                   <Bell size={22} />
                   {unreadCount > 0 && (
                      <span className="absolute -top-1 -right-1 w-4 h-4 bg-[#B71C1C] text-white text-[10px] font-bold flex items-center justify-center rounded-full border border-[#F9FAFB] dark:border-slate-900">
                         {unreadCount}
                      </span>
                   )}
                </div>

                {/* Notification Dropdown */}
                {showNotifications && (
                   <div className="absolute top-10 left-0 w-[320px] bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-gray-100 dark:border-slate-700 overflow-hidden z-50">
                      <div className="flex justify-between items-center p-4 border-b border-gray-100 dark:border-slate-700 bg-gray-50 dark:bg-slate-900">
                         <h3 className="font-bold text-sm text-[#0F172A] dark:text-white">الإشعارات</h3>
                         {unreadCount > 0 && (
                            <button onClick={markAllAsRead} className="text-xs text-gray-500 dark:text-gray-400 hover:text-[#B71C1C] transition-colors font-bold">
                               تحديد الكل كمقروء
                            </button>
                         )}
                      </div>
                      <div className="max-h-[350px] overflow-y-auto custom-scrollbar">
                         {alerts.length > 0 ? (
                            alerts.map(alert => (
                               <div 
                                  key={alert.id}
                                  onClick={() => markAsRead(alert.id)}
                                  className={`p-4 border-b border-gray-50 dark:border-slate-700/50 hover:bg-gray-50 dark:hover:bg-slate-700/50 cursor-pointer transition-colors ${!alert.isRead ? 'bg-[#FEF2F2]/30 dark:bg-slate-700/30' : ''}`}
                               >
                                  <div className="flex justify-between items-start mb-1">
                                     <h4 className={`font-bold text-xs ${!alert.isRead ? 'text-[#0F172A] dark:text-white' : 'text-gray-600 dark:text-gray-300'}`}>
                                        {alert.title}
                                     </h4>
                                     <span className="text-[10px] text-gray-400 font-bold">{alert.time}</span>
                                  </div>
                                  <p className="text-[10px] text-gray-500 dark:text-gray-400 font-medium leading-relaxed">
                                     {alert.text}
                                  </p>
                               </div>
                            ))
                         ) : (
                            <div className="p-8 text-center text-gray-500 dark:text-gray-400 text-sm font-bold">
                               لا توجد إشعارات حالياً
                            </div>
                         )}
                      </div>
                   </div>
                )}
             </div>
          </div>
        </header>
        <div className="flex-1 overflow-y-auto px-10 pb-10 pt-2">
          <Outlet />
        </div>
        
      </main>
    </div>
  );
}
