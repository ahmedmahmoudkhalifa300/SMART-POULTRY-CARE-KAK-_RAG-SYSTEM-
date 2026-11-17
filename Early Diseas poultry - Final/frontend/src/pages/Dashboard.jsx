import { useState, useEffect } from 'react';
import { Search, HeartCrack, Users, Calendar, Weight, Package, AlertTriangle, Info, TrendingUp, CheckCircle } from 'lucide-react';
import { useNotifications } from '../context/NotificationContext';
import { BarChart, Bar, XAxis, ResponsiveContainer, Cell } from 'recharts';
import WeightSample from '../components/WeightSample';
import SmartBanner from '../components/SmartBanner';

const API_BASE_URL = 'http://localhost:8000';

const financialData = [
   { name: '1', val: 0 },
   { name: '2', val: 0 },
   { name: '3', val: 0 },
   { name: '4', val: 0 },
   { name: '5', val: 0 },
];

export default function Dashboard() {
  const [flockData, setFlockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [cycleAge, setCycleAge] = useState(() => {
    const saved = localStorage.getItem('cycleAge');
    return saved ? parseInt(saved, 10) : 32;
  });
  
  const [initialFlockSize, setInitialFlockSize] = useState(() => {
    const saved = localStorage.getItem('flockSize');
    return saved ? parseInt(saved, 10) : 42500;
  });

  const [manualMortality, setManualMortality] = useState(() => {
    const saved = localStorage.getItem('manualMortality');
      return saved ? parseInt(saved, 10) : 0;
  });

  const [manualFeed, setManualFeed] = useState(() => {
    const saved = localStorage.getItem('manualFeed');
    return saved ? parseFloat(saved) : null;
  });

   const [financialTransactions, setFinancialTransactions] = useState(() => {
      const saved = localStorage.getItem('financialTransactions');
      return saved ? JSON.parse(saved) : [];
   });

  const [weightData, setWeightData] = useState({
    actualWeight: 0,
    standardWeight: 0,
    variance: 0,
    sampleCount: 0,
  });

  // تحميل بيانات القطيع من API عند التحميل
  useEffect(() => {
    const loadFlockData = async () => {
      try {
        setLoading(true);
        const flockId = localStorage.getItem('currentFlockId');
        
        if (flockId) {
          const response = await fetch(`${API_BASE_URL}/flocks/${flockId}`);
          if (response.ok) {
            const data = await response.json();
            setFlockData(data);
            
            // تحديث الـ state من البيانات المحمّلة
            setCycleAge(data.cycle_age);
            setInitialFlockSize(data.initial_size);
                  const currentMortality = data.mortality || 0;
                  setManualMortality(currentMortality);
                  localStorage.setItem('manualMortality', currentMortality.toString());
                  localStorage.setItem('mortalityInitialized', 'true');
            setManualFeed(data.feed_consumed || null);
            
            // تحديث localStorage أيضاً
            localStorage.setItem('cycleAge', data.cycle_age);
            localStorage.setItem('flockSize', data.initial_size);
          }
        }
        setLoading(false);
      } catch (err) {
        console.error('Error loading flock data:', err);
        setError('فشل في تحميل بيانات القطيع');
        setLoading(false);
      }
    };

    loadFlockData();
  }, []);

  useEffect(() => {
    const handleStorage = () => {
      const savedMortality = localStorage.getItem('manualMortality');
      if (savedMortality !== null) setManualMortality(parseInt(savedMortality, 10));
      
      const savedFeed = localStorage.getItem('manualFeed');
      if (savedFeed !== null) setManualFeed(parseFloat(savedFeed));

         const savedTransactions = localStorage.getItem('financialTransactions');
         setFinancialTransactions(savedTransactions ? JSON.parse(savedTransactions) : []);
    };
      window.addEventListener('storage', handleStorage);
      window.addEventListener('farm-data-updated', handleStorage);
      return () => {
         window.removeEventListener('storage', handleStorage);
         window.removeEventListener('farm-data-updated', handleStorage);
      };
  }, []);

  // دالة تحديث بيانات القطيع في الـ API
  const updateFlockData = async (updates) => {
    try {
      const flockId = localStorage.getItem('currentFlockId');
      if (!flockId) return;

      const response = await fetch(`${API_BASE_URL}/flocks/${flockId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
      });

      if (response.ok) {
        const updatedData = await response.json();
        setFlockData(updatedData);
      }
    } catch (err) {
      console.error('Error updating flock data:', err);
    }
  };

  // مراقبة تغييرات البيانات وتحديث الـ API
  useEffect(() => {
    if (flockData) {
      updateFlockData({
        cycle_age: cycleAge,
        mortality: manualMortality !== null ? manualMortality : undefined,
        feed_consumed: manualFeed !== null ? manualFeed : undefined,
      });
    }
  }, [cycleAge, manualMortality, manualFeed]);

  // Dynamic calculations based on onboarding and daily management
    const totalMortality = Number(manualMortality) || 0;
   const currentFlockSize = Math.max(0, initialFlockSize - totalMortality);
   const mortalityRate = initialFlockSize > 0
      ? ((totalMortality / initialFlockSize) * 100).toFixed(1)
      : '0.0';
  
  // W(t) = 9.51 * (t)^1.567
  const standardWeight = (9.51 * Math.pow(cycleAge, 1.567)).toFixed(0);
  
  // Feed = (Weight * FCR(1.6) * FlockSize) / 1,000,000 to get Tons
  const estimatedFeed = ((standardWeight * 1.6 * initialFlockSize) / 1000000).toFixed(1);
  const totalFeedConsumed = manualFeed !== null ? manualFeed.toFixed(1) : estimatedFeed;

   const totalFinancialRevenues = financialTransactions
      .filter((transaction) => transaction.type === 'income')
      .reduce((sum, transaction) => sum + Number(transaction.amount), 0);
   const totalFinancialExpenses = financialTransactions
      .filter((transaction) => transaction.type === 'expense')
      .reduce((sum, transaction) => sum + Number(transaction.amount), 0);
   const netFinancialProfit = totalFinancialRevenues - totalFinancialExpenses;
   const financialChartData = financialData.map((entry, index) => ({
      ...entry,
      val: index === financialData.length - 1
         ? totalFinancialRevenues + totalFinancialExpenses
         : 0,
   }));

  const mortalityScore = Math.max(0, 100 - (mortalityRate * 5));

  const healthIndex = Math.min(98, Math.max(70, Math.floor(mortalityScore - (32 - cycleAge)*0.1)));

  // Dynamic Alerts Logic
  const { alerts, markAllAsRead } = useNotifications();
  const dynamicAlerts = alerts;

  const hoverCardClass = "transition-all duration-300 ease-in-out hover:-translate-y-1 hover:shadow-lg cursor-pointer hover:border-gray-300 dark:hover:border-slate-600";

  return (
    <div className="flex flex-col gap-6 h-full pb-8 max-w-[1200px] mx-auto text-right" dir="rtl">
      
      {/* Header Search */}
      <div className="flex justify-center mb-2">
         <div className="w-full max-w-xl relative">
            <input 
               type="text" 
               placeholder="ابحث عن تقارير، عنابر، أو سجلات صحية..." 
               className="w-full bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-full py-3 px-12 text-sm focus:outline-none focus:border-[#B71C1C] shadow-sm"
            />
            <Search size={18} className="absolute right-5 top-3.5 text-gray-400" />
         </div>
      </div>

      {/* Row 1: Banner & Logo */}
      <div className="flex gap-6 h-[220px]">
         {/* Logo Card */}
         <div className={`w-[280px] bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl shadow-sm flex items-center justify-center relative overflow-hidden ${hoverCardClass}`}>
            <div className="absolute top-0 right-0 opacity-5">
               <svg width="200" height="200" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 22h20L12 2z"/></svg>
            </div>
            <div className="flex flex-col items-center z-10">
               <div className="w-24 h-24 rounded-full border-4 border-yellow-400 flex flex-col items-center justify-center bg-white dark:bg-slate-800 shadow-sm mb-2 hover:scale-105 transition-transform">
                  {/* Fake Chicken SVG for visual */}
                  <img src="https://api.iconify.design/twemoji:chicken.svg" alt="Chicken" className="w-12 h-12" />
               </div>
               <h2 className="text-[#B71C1C] font-extrabold text-xl tracking-wider">KAK</h2>
            </div>
         </div>

         {/* Smart Banner Card */}
         <SmartBanner healthIndex={healthIndex} mortalityRate={mortalityRate} hoverCardClass={hoverCardClass} />
      </div>

      {/* Row 2: Grid Stats */}
      <div className="grid grid-cols-6 gap-6">
         {/* Total Birds */}
         <div className={`bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm col-span-2 flex flex-col justify-between ${hoverCardClass}`}>
            <div className="flex justify-between items-start mb-6">
               <div className="text-green-600 text-[10px] font-bold bg-green-50 px-2 py-1 rounded flex items-center gap-1">
                  2.4%+ <TrendingUp size={12}/>
               </div>
               <div className="w-10 h-10 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center">
                  <Users size={20} />
               </div>
            </div>
            <div className="text-center">
               <div className="text-sm text-gray-500 dark:text-gray-400 font-bold mb-1">إجمالي عدد الطيور</div>
               <div className="text-3xl font-extrabold text-[#0F172A]">{currentFlockSize.toLocaleString()}</div>
            </div>
         </div>

         {/* Total Mortality */}
         <div className={`bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm col-span-2 flex flex-col justify-between ${hoverCardClass}`}>
            <div className="flex justify-end mb-6">
               <div className="w-10 h-10 bg-[#FEF2F2] text-[#B71C1C] rounded-xl flex items-center justify-center">
                  <HeartCrack size={20} />
               </div>
            </div>
            <div className="text-center">
               <div className="text-sm text-gray-500 dark:text-gray-400 font-bold mb-1">عدد النافق الكلي</div>
               <div className="text-3xl font-extrabold text-[#0F172A]">{totalMortality} <span className="text-lg font-bold">طائر</span></div>
            </div>
         </div>

         {/* Cycle Age (Left Red Border) */}
         <div className={`bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 border-l-4 border-l-[#B71C1C] rounded-3xl p-6 shadow-sm col-span-2 flex flex-col justify-between ${hoverCardClass}`}>
            <div className="flex justify-between items-start mb-6">
               <div className="text-[#B71C1C] text-xs font-bold bg-[#FEF2F2] px-3 py-1 rounded-full">عمر الدورة</div>
               <div className="w-10 h-10 bg-[#FEF2F2] text-[#B71C1C] rounded-xl flex items-center justify-center">
                  <Calendar size={20} />
               </div>
            </div>
            <div className="text-center">
               <div className="text-sm text-gray-500 dark:text-gray-400 font-bold mb-1">عمر القطيع اليوم</div>
               <div className="text-3xl font-extrabold text-[#0F172A]">اليوم {cycleAge}</div>
            </div>
         </div>

         {/* Average Weight */}
         <div className={`bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm col-span-2 flex flex-col justify-between ${hoverCardClass}`}>
            <div className="flex justify-between items-start mb-6">
               <div className="text-gray-400 text-xs font-bold">جرام</div>
               <div className="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center">
                  <Weight size={20} />
               </div>
            </div>
            <div className="text-center">
               <div className="text-sm text-gray-500 dark:text-gray-400 font-bold mb-1">متوسط وزن الفرخة</div>
               <div className="text-3xl font-extrabold text-[#0F172A]">{standardWeight.toLocaleString()} <span className="text-lg font-bold">جم</span></div>
            </div>
         </div>

         {/* Total Feed */}
         <div className={`bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm col-span-2 flex flex-col justify-between ${hoverCardClass}`}>
            <div className="flex justify-between items-start mb-6">
               <div className="text-gray-400 text-xs font-bold">طن</div>
               <div className="w-10 h-10 bg-orange-50 text-orange-600 rounded-xl flex items-center justify-center">
                  <Package size={20} />
               </div>
            </div>
            <div className="text-center">
               <div className="text-sm text-gray-500 dark:text-gray-400 font-bold mb-1">إجمالي العلف المستهلك</div>
               <div className="text-3xl font-extrabold text-[#0F172A]">{totalFeedConsumed} <span className="text-lg font-bold">طن</span></div>
            </div>
         </div>

         {/* Mortality Rate */}
         <div className={`bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm col-span-2 flex flex-col justify-between items-center text-center ${hoverCardClass}`}>
            <div className="relative w-20 h-20 mb-2 flex items-center justify-center hover:scale-110 transition-transform duration-500">
               <svg className="w-20 h-20 transform -rotate-90">
                  <circle cx="40" cy="40" r="34" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-gray-100" />
                  <circle cx="40" cy="40" r="34" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-[#B71C1C]" strokeDasharray={213} strokeDashoffset={213 - (213 * mortalityRate) / 100} strokeLinecap="round" />
               </svg>
               <div className="absolute text-xl font-extrabold text-[#0F172A]">{mortalityRate}%</div>
            </div>
            <div>
               <div className="text-sm text-gray-700 dark:text-gray-200 font-bold mb-1">نسبة النفوق</div>
               <div className="text-[10px] text-gray-400 font-bold">معدل تراكمي</div>
            </div>
         </div>
      </div>

      {/* Row 2.5: Weight Sample */}
      <WeightSample cycleAge={cycleAge} onWeightDataChange={setWeightData} />

      {/* Row 3: Bottom Split */}
      <div className="flex gap-6 h-[340px]">
         {/* Financial Overview */}
         <div className={`flex-[2] bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-8 shadow-sm flex flex-col ${hoverCardClass}`}>
            <div className="flex justify-between items-center mb-6">
               <span className="bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-gray-300 text-xs font-bold px-3 py-1 rounded-full">آخر 30 يوم</span>
               <div className="text-right">
                  <h3 className="font-bold text-lg text-[#0F172A]">نظرة على الحسابات</h3>
                  <p className="text-[10px] text-gray-500 dark:text-gray-400 font-bold">متابعة الأداء المالي الشهري</p>
               </div>
            </div>

            <div className="flex justify-between text-center mb-8 border-b border-gray-100 dark:border-slate-700 pb-6">
               <div className="flex-1 hover:scale-105 transition-transform cursor-default">
                  <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">الإيرادات</div>
                  <div className="text-xl font-extrabold text-[#0F172A]">${totalFinancialRevenues.toLocaleString()}</div>
               </div>
               <div className="w-px bg-gray-100 dark:bg-slate-700"></div>
               <div className="flex-1 hover:scale-105 transition-transform cursor-default">
                  <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">المصاريف</div>
                  <div className="text-xl font-extrabold text-[#0F172A]">${totalFinancialExpenses.toLocaleString()}</div>
               </div>
               <div className="w-px bg-gray-100 dark:bg-slate-700"></div>
               <div className="flex-1 hover:scale-105 transition-transform cursor-default">
                  <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">صافي الربح</div>
                  <div className={`text-xl font-extrabold ${netFinancialProfit >= 0 ? 'text-green-600' : 'text-[#B71C1C]'}`}>${netFinancialProfit.toLocaleString()}</div>
               </div>
            </div>

            <div className="flex-1 h-full w-full">
               <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={financialChartData} barGap={4} margin={{top: 0, right: 0, left: 0, bottom: 0}}>
                     <Bar dataKey="val" radius={[4,4,0,0]} barSize={40}>
                     {financialChartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={index === 1 || index === 3 ? '#B71C1C' : '#E5B4B4'} className="hover:opacity-80 transition-opacity cursor-pointer"/>
                        ))}
                     </Bar>
                  </BarChart>
               </ResponsiveContainer>
            </div>
         </div>

         {/* Health Index */}
         <div className={`flex-[1] bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-8 shadow-sm flex flex-col items-center text-center ${hoverCardClass}`}>
            <h3 className="font-bold text-lg text-[#0F172A] mb-1">مؤشر صحة القطيع</h3>
            <p className="text-[10px] text-gray-500 dark:text-gray-400 font-bold mb-8">تقييم الذكاء الاصطناعي للسلامة العامة</p>
            
            <div className="relative w-40 h-20 overflow-hidden mb-6 flex justify-center hover:scale-110 transition-transform duration-500 cursor-default">
               <svg className="w-40 h-40 absolute top-0" viewBox="0 0 100 100">
                  <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#F3F4F6" strokeWidth="12" strokeLinecap="round" />
                  <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke={healthIndex >= 90 ? "#16a34a" : healthIndex >= 80 ? "#ca8a04" : "#B71C1C"} strokeWidth="12" strokeLinecap="round" strokeDasharray="125.6" strokeDashoffset={125.6 - (125.6 * healthIndex) / 100} className="transition-all duration-1000 ease-out"/>
               </svg>
               <div className="absolute top-8 flex flex-col items-center text-center w-full">
                  <div className="text-4xl font-black text-[#0F172A] leading-none">{healthIndex}</div>
                  <div className={`text-xs font-bold mt-1 ${healthIndex >= 90 ? "text-green-600" : healthIndex >= 80 ? "text-yellow-600" : "text-[#B71C1C]"}`}>{healthIndex >= 90 ? 'ممتاز يا بطل' : healthIndex >= 80 ? 'انتبه للمؤشرات' : 'تدخل عاجل'}</div>
               </div>
            </div>

            <div className="w-full mt-auto">
               <div className="flex justify-between text-xs font-bold mb-2">
                  <span className="text-gray-700 dark:text-gray-200">دقة التحليل</span>
                  <span className="text-gray-700 dark:text-gray-200">98.2%</span>
               </div>
               <div className="w-full h-1.5 bg-gray-100 dark:bg-slate-700 rounded-full mb-3">
                  <div className="h-full bg-[#0F172A] rounded-full" style={{width: '98.2%'}}></div>
               </div>
               <p className="text-[10px] text-gray-500 dark:text-gray-400 font-bold leading-relaxed">
                  الثقة مبنية على أكثر من 2,400 نقطة بيانات اتجمعت في آخر 24 ساعة.
               </p>
            </div>
         </div>

         {/* Alerts */}
         <div className={`flex-[1] bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col ${hoverCardClass}`}>
            <div className="flex justify-between items-center mb-6">
               <button onClick={markAllAsRead} className="text-xs text-gray-500 dark:text-gray-400 font-bold hover:text-gray-800 transition-colors">مسح الكل</button>
               <h3 className="font-bold text-sm text-[#0F172A]">تنبيهات عاجلة</h3>
            </div>

            <div className="flex flex-col gap-3 overflow-y-auto custom-scrollbar flex-1 pr-1 mb-4">
               {dynamicAlerts.map((alert) => (
                  <div 
                     key={alert.id} 
                     className={`border rounded-2xl p-4 flex gap-3 text-right transition-colors hover:shadow-sm ${
                        alert.type === 'critical' ? 'bg-[#FEF2F2] border-red-100' : 
                        alert.type === 'warning' ? 'bg-orange-50 border-orange-100' :
                        alert.type === 'success' ? 'bg-green-50 border-green-100' :
                        'bg-gray-50 dark:bg-slate-900 border-gray-100 dark:border-slate-700'
                     }`}
                  >
                     <div className={`mt-0.5 ${
                        alert.type === 'critical' ? 'text-[#B71C1C]' : 
                        alert.type === 'warning' ? 'text-orange-600' :
                        alert.type === 'success' ? 'text-green-600' :
                        'text-gray-500 dark:text-gray-400'
                     }`}>
                        {alert.iconType === 'critical' && <HeartCrack size={18}/>}
                        {alert.iconType === 'warning' && <AlertTriangle size={18}/>}
                        {alert.iconType === 'info' && <Info size={18}/>}
                        {alert.iconType === 'success' && <CheckCircle size={18}/>}
                     </div>
                     <div className="flex-1">
                        <div className="flex justify-between items-center mb-1 flex-row-reverse">
                           <h4 className={`font-bold text-xs ${
                              alert.type === 'critical' ? 'text-[#B71C1C]' : 
                              alert.type === 'warning' ? 'text-orange-700' :
                              alert.type === 'success' ? 'text-green-700' :
                              'text-[#0F172A]'
                           }`}>{alert.title}</h4>
                           <span className={`text-[9px] font-bold ${
                              alert.type === 'critical' ? 'text-[#B71C1C]' : 
                              'text-gray-500 dark:text-gray-400'
                           }`}>{alert.time}</span>
                        </div>
                        <p className={`text-[10px] font-bold leading-relaxed ${
                           alert.type === 'critical' ? 'text-gray-700 dark:text-gray-200' : 
                           alert.type === 'warning' ? 'text-orange-800' :
                           alert.type === 'success' ? 'text-green-800' :
                           'text-gray-600 dark:text-gray-300'
                        }`}>{alert.text}</p>
                     </div>
                  </div>
               ))}
            </div>

            <button className="w-full py-2.5 border-t border-dashed border-gray-200 dark:border-slate-700 text-[#B71C1C] text-xs font-bold hover:bg-gray-50 dark:bg-slate-900 transition-colors rounded-b-xl">
               عرض أرشيف التنبيهات
            </button>
         </div>
      </div>

    </div>
  );
}
