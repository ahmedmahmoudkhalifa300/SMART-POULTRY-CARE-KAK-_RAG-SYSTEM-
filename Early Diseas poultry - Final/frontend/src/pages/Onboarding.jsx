import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LayoutDashboard, PlusCircle, ClipboardList, Calendar, Settings, Bell, User, BarChart2, PawPrint, Sun, Snowflake, ArrowLeft, ClipboardCheck } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

export default function Onboarding() {
  const navigate = useNavigate();
  const [chicksNotReceived, setChicksNotReceived] = useState(false);
  const [season, setSeason] = useState('summer'); // 'summer' or 'winter'
  const [alerts, setAlerts] = useState(true);
  const [flockSize, setFlockSize] = useState('');
  const [cycleAge, setCycleAge] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCompleteSetup = async () => {
    if (!flockSize || !cycleAge) {
      setError('يرجى ملء جميع الحقول المطلوبة');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // إرسال البيانات إلى Backend
      const response = await fetch(`${API_BASE_URL}/flocks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: `قطيع - ${new Date().toLocaleDateString('ar-EG')}`,
          initial_size: parseInt(flockSize),
          cycle_age: parseInt(cycleAge),
          mortality: 0,
          feed_consumed: 0.0,
          season: season,
        }),
      });

      if (!response.ok) {
        throw new Error('فشل في حفظ بيانات القطيع');
      }

      const flockData = await response.json();

      // حفظ معرف القطيع في localStorage للرجوع إليه لاحقاً
      localStorage.setItem('currentFlockId', flockData.id);
      localStorage.setItem('flockSize', flockSize);
      localStorage.setItem('cycleAge', cycleAge);
      localStorage.setItem('manualMortality', '0');
      localStorage.setItem('manualFeed', '0');
      localStorage.removeItem('mortalityInitialized');
      localStorage.setItem('season', season);
      localStorage.setItem('chicksNotReceived', chicksNotReceived);
      localStorage.setItem('alerts', alerts);

      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'حدث خطأ ما');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#F9FAFB]" dir="rtl">
      {/* Sidebar */}
      <aside className="w-[280px] bg-white dark:bg-slate-800 border-l border-gray-200 dark:border-slate-700 flex flex-col py-8 z-10 shadow-sm relative">
        <div className="flex items-center gap-3 px-8 mb-12">
          <div className="w-10 h-10 bg-[#B71C1C] rounded-xl flex items-center justify-center text-white shadow-sm">
             {/* KAK Logo */}
             <div className="font-black text-xl">K</div>
          </div>
          <div>
            <h1 className="font-extrabold text-xl text-[#0F172A] leading-tight text-right">KAK</h1>
            <p className="text-[10px] text-gray-500 dark:text-gray-400 font-bold text-right">مساعدك الذكي للدواجن</p>
          </div>
        </div>

        <nav className="flex-col gap-2 flex-1 px-4">
          <div className="flex items-center gap-4 px-4 py-3.5 my-1 rounded-xl text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:bg-slate-900 cursor-pointer font-bold text-sm transition-colors">
            <LayoutDashboard size={20} />
            <span>لوحة التحكم</span>
          </div>
          <div className="flex items-center gap-4 px-4 py-3.5 my-1 rounded-xl bg-[#B71C1C] text-white shadow-md font-bold text-sm cursor-pointer transition-colors">
            <PlusCircle size={20} />
            <span>إنشاء قطيع</span>
          </div>
          <div className="flex items-center gap-4 px-4 py-3.5 my-1 rounded-xl text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:bg-slate-900 cursor-pointer font-bold text-sm transition-colors">
            <ClipboardList size={20} />
            <span>التشخيص الذكي</span>
          </div>
          <div className="flex items-center gap-4 px-4 py-3.5 my-1 rounded-xl text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:bg-slate-900 cursor-pointer font-bold text-sm transition-colors">
            <Calendar size={20} />
            <span>إدارة المزرعة</span>
          </div>
        </nav>
        
        <div className="px-6 flex-col gap-3 mt-auto pt-6 border-t border-gray-50">
          <div className="bg-[#FEF2F2] rounded-xl p-4 text-center mb-4 border border-red-50">
             <div className="text-[#B71C1C] font-bold text-sm mb-1">الحالة الحالية</div>
             <div className="text-gray-600 dark:text-gray-300 text-xs font-bold">بانتظار إتمام الإعداد</div>
          </div>
          <div className="flex items-center justify-center gap-3 px-4 py-3 text-gray-600 dark:text-gray-300 cursor-pointer hover:bg-gray-50 dark:bg-slate-900 rounded-xl transition-colors font-bold text-sm">
             <Settings size={18} />
             <span>الإعدادات</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col bg-[#F9FAFB] overflow-y-auto">
        {/* Header */}
        <header className="px-10 py-8 flex justify-between items-center w-full">
           <div className="flex items-center gap-3 text-[#0F172A]">
              <BarChart2 size={24} className="text-[#B71C1C]" />
              <h2 className="text-xl font-bold">إنشاء أول قطيع</h2>
           </div>
           
           <div className="flex items-center gap-6" dir="ltr">
              <div className="w-10 h-10 rounded-full bg-gray-200 dark:bg-slate-700 border-2 border-white shadow-sm overflow-hidden flex items-center justify-center">
                 <User size={20} className="text-gray-500 dark:text-gray-400" />
              </div>
              <div className="cursor-pointer text-gray-600 dark:text-gray-300 relative">
                 <Bell size={22} />
                 <span className="absolute top-0 right-5 w-2 h-2 bg-[#B71C1C] rounded-full border border-[#F9FAFB]"></span>
              </div>
           </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 px-10 pb-12 max-w-[1000px] w-full mx-auto flex flex-col">
           
           {/* Progress Bar */}
           <div className="flex items-center justify-end gap-6 mb-12">
              <div className="flex-1 h-1 bg-gray-200 dark:bg-slate-700 rounded-full flex justify-end">
                 <div className="h-full bg-[#B71C1C] rounded-full" style={{width: '66%'}}></div>
              </div>
              <div className="text-[#B71C1C] font-bold text-sm whitespace-nowrap">الخطوة 2 من 3</div>
           </div>

           <div className="flex gap-12 mt-4 items-start justify-end">
              
              {/* Form Section (Right Side) */}
              <div className="w-[500px] flex flex-col text-right">
                 <h1 className="text-[34px] font-extrabold text-[#0F172A] mb-3">تفاصيل القطيع</h1>
                 <p className="text-gray-500 dark:text-gray-400 text-sm font-bold mb-10 leading-relaxed">
                    ساعد محركنا الذكي على معايرة التوصيات المناسبة لدورتك الإنتاجية.
                 </p>

                 <div className="flex gap-4 mb-6 w-full">
                    <div className="flex-1 text-right">
                       <label className="block text-sm font-bold text-[#0F172A] mb-2">العمر بالأيام</label>
                       <div className="relative">
                          <input type="number" value={cycleAge} onChange={(e) => setCycleAge(e.target.value)} placeholder="مثلاً: 1" className="w-full border border-gray-200 dark:border-slate-700 rounded-xl py-3 px-4 pl-10 text-left font-bold text-gray-700 dark:text-gray-200 focus:outline-none focus:border-[#B71C1C] shadow-sm"/>
                          <Calendar size={18} className="absolute left-4 top-3.5 text-gray-400" />
                       </div>
                    </div>
                    <div className="flex-1 text-right">
                       <label className="block text-sm font-bold text-[#0F172A] mb-2">عدد الطيور</label>
                       <div className="relative">
                          <input type="number" value={flockSize} onChange={(e) => setFlockSize(e.target.value)} placeholder="مثلاً: 5000" className="w-full border border-gray-200 dark:border-slate-700 rounded-xl py-3 px-4 pl-10 text-left font-bold text-gray-700 dark:text-gray-200 focus:outline-none focus:border-[#B71C1C] shadow-sm"/>
                          <PawPrint size={18} className="absolute left-4 top-3.5 text-gray-400" />
                       </div>
                    </div>
                 </div>

                 <div 
                    className={`bg-[#FEF2F2] border ${chicksNotReceived ? 'border-[#B71C1C]' : 'border-red-100'} rounded-xl p-5 mb-8 flex items-center justify-end gap-4 cursor-pointer transition-colors shadow-sm`}
                    onClick={() => setChicksNotReceived(!chicksNotReceived)}
                 >
                    <div className="text-right">
                       <h4 className="font-bold text-[#B71C1C] mb-1">لم يتم استلام الكتاكيت بعد</h4>
                       <p className="text-xs text-[#B71C1C] opacity-80 font-bold">أقوم حالياً بتجهيز عنبر الدواجن لوصول الكتاكيت.</p>
                    </div>
                    <div className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${chicksNotReceived ? 'bg-[#B71C1C] border-[#B71C1C]' : 'bg-white dark:bg-slate-800 border-red-200'}`}>
                       {chicksNotReceived && <div className="w-2.5 h-2.5 bg-white dark:bg-slate-800 rounded-sm"></div>}
                    </div>
                 </div>

                 <div className="flex gap-4 mb-10 w-full">
                    {/* Daily Alerts Toggle */}
                    <div className="flex-1 border border-gray-200 dark:border-slate-700 rounded-xl p-4 flex items-center justify-between shadow-sm">
                       <div className="text-right">
                          <div className="font-bold text-[#0F172A] text-sm mb-1">تنبيهات يومية</div>
                          <div className="text-[10px] text-gray-500 dark:text-gray-400 font-bold">نصائح بيطرية وإدارية</div>
                       </div>
                       <div 
                          className={`w-12 h-6 rounded-full p-1 cursor-pointer transition-colors flex ${alerts ? 'bg-[#B71C1C] justify-end' : 'bg-gray-300 justify-start'}`}
                          onClick={() => setAlerts(!alerts)}
                       >
                          <div className="w-4 h-4 bg-white dark:bg-slate-800 rounded-full shadow-sm"></div>
                       </div>
                    </div>

                    {/* Season Toggle */}
                    <div className="flex-1 border border-gray-200 dark:border-slate-700 rounded-xl p-1 flex bg-gray-50 dark:bg-slate-900 shadow-sm relative pt-6">
                       <div className="absolute top-2 right-4 text-[10px] font-bold text-[#0F172A]">الموسم الحالي</div>
                       <div className="flex w-full mt-2 gap-1 p-1">
                          <button 
                             onClick={() => setSeason('winter')}
                             className={`flex-1 flex items-center justify-center gap-2 rounded-lg py-2 transition-colors ${season === 'winter' ? 'bg-white dark:bg-slate-800 shadow-sm border border-gray-200 dark:border-slate-700 text-[#0F172A]' : 'text-gray-400 hover:text-gray-600 dark:text-gray-300'}`}
                          >
                             <span className="text-sm font-bold">شتاء</span>
                             <Snowflake size={16} />
                          </button>
                          <button 
                             onClick={() => setSeason('summer')}
                             className={`flex-1 flex items-center justify-center gap-2 rounded-lg py-2 transition-colors ${season === 'summer' ? 'bg-white dark:bg-slate-800 shadow-sm border border-red-100 text-[#B71C1C]' : 'text-gray-400 hover:text-gray-600 dark:text-gray-300'}`}
                          >
                             <span className="text-sm font-bold">صيف</span>
                             <Sun size={16} />
                          </button>
                       </div>
                    </div>
                 </div>

                 {error && (
                    <div className="bg-[#FEF2F2] border border-[#B71C1C] rounded-xl p-4 mb-6 flex items-center justify-end gap-3">
                       <div className="text-right flex-1">
                          <div className="font-bold text-[#B71C1C] text-sm">{error}</div>
                       </div>
                    </div>
                 )}

                 <button 
                    onClick={handleCompleteSetup}
                    disabled={loading}
                    className={`w-full ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-[#B71C1C] hover:bg-[#991616]'} text-white font-bold py-4 rounded-xl flex items-center justify-center gap-3 transition-colors shadow-sm`}
                 >
                    {loading ? (
                       <>
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          <span>جاري الحفظ...</span>
                       </>
                    ) : (
                       <>
                          <ArrowLeft size={20} />
                          <span>إكمال الإعداد</span>
                       </>
                    )}
                 </button>
              </div>
              
              {/* Left Side (Placeholder Info Box) */}
              <div className="w-[320px] mt-4">
                 <div className="border-2 border-dashed border-[#BFDBFE] bg-blue-50/30 rounded-3xl p-10 flex flex-col items-center justify-center text-center h-[300px]">
                    <div className="text-blue-200 mb-6">
                       <ClipboardCheck size={64} strokeWidth={1.5} />
                    </div>
                    <h3 className="text-lg font-bold text-[#0F172A] mb-3">بانتظار البيانات</h3>
                    <p className="text-gray-500 dark:text-gray-400 text-sm font-medium leading-relaxed">
                       املأ التفاصيل للحصول على رؤى مخصصة وخطط إدارة دقيقة.
                    </p>
                 </div>
              </div>

           </div>
        </div>
      </main>
    </div>
  );
}
