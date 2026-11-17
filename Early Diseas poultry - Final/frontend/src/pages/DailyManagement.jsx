import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { Utensils, HeartCrack, ChevronLeft, Droplets, Eye, Sliders, Sun, ChevronDown, ArrowUpRight, TrendingUp, X } from 'lucide-react';
import { BarChart, Bar, XAxis, ResponsiveContainer, Cell } from 'recharts';

const API_BASE_URL = 'http://localhost:8000';

const chartData = [
   { name: 'اثنين', val: 50 },
   { name: 'ثلاث', val: 70 },
   { name: 'أربع', val: 90 },
   { name: 'خميس', val: 30 },
   { name: 'جمعة', val: 60 },
   { name: 'سبت', val: 100 },
   { name: 'أحد', val: 50 },
];

export default function DailyManagement() {
   const [filter, setFilter] = useState('active');
   const [showMortalityModal, setShowMortalityModal] = useState(false);
   const [showFeedModal, setShowFeedModal] = useState(false);
   const [showTaskModal, setShowTaskModal] = useState(false);
   const [activeTask, setActiveTask] = useState('');
   const [mortalityInput, setMortalityInput] = useState('');
   const [feedInput, setFeedInput] = useState('');
   const [taskGuidance, setTaskGuidance] = useState('');
   const [isTaskLoading, setIsTaskLoading] = useState(false);

   const handleTaskClick = async (taskName) => {
      setActiveTask(taskName);
      setShowTaskModal(true);
      setTaskGuidance('');
      setIsTaskLoading(true);

      try {
         const response = await fetch('http://localhost:8001/chat/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: `أعطني توجيهات يومية مختصرة بخصوص ${taskName} في مزارع الدواجن`, session_id: 'daily_tasks' })
         });
         const data = await response.json();
         setTaskGuidance(data.answer || 'لم يتم العثور على توجيهات.');
      } catch (error) {
         console.error(error);
         setTaskGuidance('عذراً، تعذر الاتصال بقاعدة المعرفة.');
      } finally {
         setIsTaskLoading(false);
      }
   };

   const handleMortalitySubmit = async () => {
      const addedMortality = parseInt(mortalityInput, 10);
      if (!addedMortality || addedMortality <= 0) return;

      const currentMortality = parseInt(localStorage.getItem('manualMortality') || '0', 10);
      const totalMortality = currentMortality + addedMortality;
      localStorage.setItem('manualMortality', totalMortality);

      const flockId = localStorage.getItem('currentFlockId');
      if (flockId) {
         await fetch(`${API_BASE_URL}/flocks/${flockId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mortality: totalMortality }),
         });
      }

      setShowMortalityModal(false);
      setMortalityInput('');
      window.dispatchEvent(new Event("storage"));
      window.dispatchEvent(new Event('farm-data-updated'));
      toast.success("تم تسجيل النافق بنجاح!");
   };

   const handleFeedSubmit = async () => {
      if (!feedInput) return;
      const currentFeed = parseFloat(localStorage.getItem('manualFeed') || '0');
      const totalFeed = currentFeed + parseFloat(feedInput);
      localStorage.setItem('manualFeed', totalFeed.toFixed(2));

      const flockId = localStorage.getItem('currentFlockId');
      if (flockId) {
         await fetch(`${API_BASE_URL}/flocks/${flockId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ feed_consumed: totalFeed }),
         });
      }

      setShowFeedModal(false);
      setFeedInput('');
      window.dispatchEvent(new Event("storage"));
      toast.success("تم تسجيل استهلاك العلف بنجاح!");
   };

   return (
      <div className="flex flex-col gap-8 h-full pb-8 max-w-[1200px] mx-auto w-full text-right" dir="rtl">

         {/* Top Section */}
         <div className="flex gap-6">
            {/* Barn Status Banner */}
            <div className="flex-1 bg-gradient-to-r from-[#D32F2F] to-[#E57373] rounded-3xl p-8 relative overflow-hidden shadow-sm flex flex-col justify-between" style={{ height: "auto" }}>
               <div className="relative z-10 text-white">
                  <h2 className="text-3xl font-extrabold mb-3">حالة العنبر والبيئة</h2>
                  <p className="text-white/90 text-sm font-medium leading-relaxed max-w-lg mb-6">
                     المحافظة على درجة الحرارة المناسبة تحسن الإنتاج، تقلل الإجهاد الحراري، وتقلل النفوق. خد بالك إن كل زيادة بمقدار 5% في الرطوبة عن المعدل المطلوب تقابلها زيادة تقارب درجة مئوية واحدة في الحرارة المحسوسة للطائر.
                  </p>

                  <div className="flex gap-4">
                     {/* Light Box */}
                     <div className="bg-white dark:bg-slate-800/20 backdrop-blur-md border border-white/20 rounded-2xl p-4 flex-1 text-[#0F172A]">
                        <div className="text-gray-600 text-xs font-bold mb-1">شدة الإضاءة</div>
                        <div className="text-3xl font-extrabold mb-1 flex items-baseline gap-1">40 <span className="text-sm font-bold text-gray-500">لوكس</span></div>
                        <div className="text-gray-500 text-[10px] font-bold">المثالي: 30-50 لوكس</div>
                     </div>

                     {/* Humidity Box */}
                     <div className="bg-white dark:bg-slate-800/20 backdrop-blur-md border border-white/20 rounded-2xl p-4 flex-1 text-[#0F172A]">
                        <div className="text-gray-600 text-xs font-bold mb-1">الرطوبة النسبية</div>
                        <div className="text-3xl font-extrabold mb-1">62%</div>
                        <div className="text-gray-500 text-[10px] font-bold">توصية: قلل الرطوبة لـ 55%</div>
                     </div>

                     {/* Temp Box */}
                     <div className="bg-white dark:bg-slate-800/20 backdrop-blur-md border border-white/20 rounded-2xl p-4 flex-1 text-[#0F172A]">
                        <div className="text-gray-600 text-xs font-bold mb-1">الحرارة الحالية</div>
                        <div className="text-3xl font-extrabold mb-1 flex items-baseline gap-1">24.5 <span className="text-sm font-bold text-gray-500">°م</span></div>
                        <div className="text-gray-500 text-[10px] font-bold">الهدف: 24.0 °م</div>
                     </div>
                  </div>
               </div>

               {/* Decorative Background Element */}
               <div className="absolute -bottom-10 -left-10 opacity-10">
                  <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
               </div>
            </div>

            {/* Quick Actions (إنجز حالك) */}
            <div className="w-[280px] bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col h-[300px]">
               <div className="mb-auto">
                  <h3 className="font-extrabold text-xl text-[#0F172A] mb-1 text-center">إنجز حالك</h3>
                  <p className="text-gray-400 text-xs text-center font-bold">تسجيلات سريعة</p>
               </div>

               <div className="flex flex-col gap-4">
                  <button onClick={() => setShowFeedModal(true)} className="bg-gray-50 dark:bg-slate-900 hover:bg-gray-100 dark:bg-slate-700 border border-gray-100 dark:border-slate-700 rounded-2xl p-4 flex items-center justify-between transition-colors shadow-sm group w-full">
                     <div className="w-8 h-8 rounded-full bg-white dark:bg-slate-800 flex items-center justify-center group-hover:bg-gray-50 dark:bg-slate-900 transition-colors">
                        <ChevronLeft size={16} className="text-gray-400" />
                     </div>
                     <div className="flex items-center gap-3">
                        <span className="font-bold text-sm text-[#0F172A] text-right">تسجيل استهلاك<br />العلف</span>
                        <div className="text-[#D32F2F]"><Utensils size={20} /></div>
                     </div>
                  </button>

                  <button onClick={() => setShowMortalityModal(true)} className="bg-gray-50 dark:bg-slate-900 hover:bg-gray-100 dark:bg-slate-700 border border-gray-100 dark:border-slate-700 rounded-2xl p-4 flex items-center justify-between transition-colors shadow-sm group w-full">
                     <div className="w-8 h-8 rounded-full bg-white dark:bg-slate-800 flex items-center justify-center group-hover:bg-gray-50 dark:bg-slate-900 transition-colors">
                        <ChevronLeft size={16} className="text-gray-400" />
                     </div>
                     <div className="flex items-center gap-3">
                        <span className="font-bold text-sm text-[#0F172A] text-right">تسجيل حالات<br />النافق</span>
                        <div className="text-[#D32F2F]"><HeartCrack size={20} /></div>
                     </div>
                  </button>
               </div>
            </div>
         </div>

         {/* Middle Section (Tasks Grid) */}
         <div>
            <div className="flex justify-between items-end mb-6">
               <div className="flex gap-2">
                  <button
                     onClick={() => setFilter('scheduled')}
                     className={`px-6 py-2 rounded-full text-sm font-bold transition-colors ${filter === 'scheduled' ? 'bg-[#0F172A] text-white shadow-sm' : 'bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:bg-slate-900'}`}
                  >
                     مجدول
                  </button>
                  <button
                     onClick={() => setFilter('active')}
                     className={`px-6 py-2 rounded-full text-sm font-bold transition-colors ${filter === 'active' ? 'bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-[#0F172A] shadow-sm' : 'bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:bg-slate-900'}`}
                  >
                     شغال
                  </button>
               </div>
               <div>
                  <h3 className="text-2xl font-extrabold text-[#0F172A] mb-1">قائمة المهام اليومية</h3>
                  <p className="text-gray-500 dark:text-gray-400 text-sm font-bold">خلص مهامك عشان دنيتك تبقى زي الفل.</p>
               </div>
            </div>

            <div className="grid grid-cols-3 gap-6">
               {/* Task 1 */}
               <div onClick={() => handleTaskClick('إدارة التغذية')} className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col items-center text-center relative group cursor-pointer hover:border-gray-300 transition-colors">
                  <div className="absolute top-4 left-4 text-gray-400">
                     <ChevronDown size={20} />
                  </div>
                  <div className="w-14 h-14 rounded-full bg-red-50 flex items-center justify-center text-[#D32F2F] mb-4">
                     <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
                  </div>
                  <h4 className="font-extrabold text-[#0F172A] text-lg mb-1">إدارة التغذية</h4>
                  <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">توصيات فحص العلف وتوزيعه.</p>
               </div>

               {/* Task 2 */}
               <div onClick={() => handleTaskClick('إدارة المياه')} className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col items-center text-center relative group cursor-pointer hover:border-gray-300 transition-colors">
                  <div className="absolute top-4 left-4 text-gray-400">
                     <ChevronDown size={20} />
                  </div>
                  <div className="w-14 h-14 rounded-full bg-red-50 flex items-center justify-center text-[#D32F2F] mb-4">
                     <Droplets size={24} />
                  </div>
                  <h4 className="font-extrabold text-[#0F172A] text-lg mb-1">إدارة المياه</h4>
                  <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">جودة ونظافة مياه الشرب.</p>
               </div>

               {/* Task 3 */}
               <div onClick={() => handleTaskClick('المرور الصحي')} className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col items-center text-center relative group cursor-pointer hover:border-gray-300 transition-colors">
                  <div className="absolute top-4 left-4 text-gray-400">
                     <ChevronDown size={20} />
                  </div>
                  <div className="w-14 h-14 rounded-full bg-gray-100 dark:bg-slate-700 flex items-center justify-center text-gray-700 dark:text-gray-200 mb-4">
                     <Eye size={24} />
                  </div>
                  <h4 className="font-extrabold text-[#0F172A] text-lg mb-1">المرور الصحي</h4>
                  <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">متابعة نشاط وحركة القطيع.</p>
               </div>

               {/* Quote Block */}
               <div className="bg-[#F3E8E8] border border-red-100 rounded-3xl p-6 shadow-sm flex flex-col items-center text-center">
                  <div className="w-16 h-16 bg-white dark:bg-slate-800 rounded-xl border border-gray-100 dark:border-slate-700 flex items-center justify-center mb-4 shadow-sm">
                     {/* Fake Chicken Icon for the quote */}
                     <img src="https://api.iconify.design/twemoji:chicken.svg" alt="Chicken" className="w-10 h-10" />
                  </div>
                  <h4 className="font-extrabold text-[#D32F2F] text-lg mb-2">عاش يا فنان!</h4>
                  <p className="text-gray-600 dark:text-gray-300 text-sm font-medium leading-relaxed italic px-2">
                     "شغلك النهاردة مظبوط.. ركز في التفاصيل الصغيرة هي اللي بتعمل الفرق في الوزن."
                  </p>
               </div>

               {/* Task 4 */}
               <div onClick={() => handleTaskClick('شدة الإضاءة')} className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col items-center text-center relative group cursor-pointer hover:border-gray-300 transition-colors">
                  <div className="absolute top-4 left-4 text-gray-400">
                     <ChevronDown size={20} />
                  </div>
                  <div className="w-14 h-14 rounded-full bg-yellow-50 flex items-center justify-center text-yellow-600 mb-4">
                     <Sun size={24} />
                  </div>
                  <h4 className="font-extrabold text-[#0F172A] text-lg mb-1">شدة الإضاءة</h4>
                  <p className="text-[#D32F2F] text-sm font-bold">المثالي: 30-50 لوكس</p>
               </div>

               {/* Task 5 */}
               <div onClick={() => handleTaskClick('معايرة البيئة')} className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col items-center text-center relative group cursor-pointer hover:border-gray-300 transition-colors">
                  <div className="absolute top-4 left-4 text-gray-400">
                     <ChevronDown size={20} />
                  </div>
                  <div className="w-14 h-14 rounded-full bg-green-50 flex items-center justify-center text-green-600 mb-4">
                     <Sliders size={24} />
                  </div>
                  <h4 className="font-extrabold text-[#0F172A] text-lg mb-1">معايرة البيئة</h4>
                  <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">تأكد من دقة الحساسات والأنظمة.</p>
               </div>

            </div>
         </div>

         {/* Bottom Section (Flock Progress) */}
         <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-8 shadow-sm">
            <div className="flex justify-between items-center mb-8">
               <button onClick={() => handleTaskClick('التقرير الكامل')} className="text-[#D32F2F] font-bold text-sm flex items-center gap-1 hover:underline">
                  <ArrowUpRight size={16} /> عرض التقرير الكامل
               </button>
               <h3 className="text-2xl font-extrabold text-[#0F172A]">تطور الدفعة: قطيع أ-102</h3>
            </div>

            <div className="flex gap-12">

               {/* Chart Area */}
               <div className="flex-1 h-[220px] bg-[#F9FAFB] rounded-2xl p-4">
                  <ResponsiveContainer width="100%" height="100%">
                     <BarChart data={chartData} barGap={0} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#6B7280', fontSize: 12, fontWeight: 'bold' }} dy={10} reversed={true} />
                        <Bar dataKey="val" radius={[8, 8, 0, 0]} barSize={50}>
                           {chartData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.name === 'سبت' ? '#B71C1C' : '#E5B4B4'} />
                           ))}
                        </Bar>
                     </BarChart>
                  </ResponsiveContainer>
               </div>

               {/* Stats Area */}
               <div className="w-[200px] flex flex-col justify-center gap-8 pl-4">
                  <div className="flex items-center justify-end gap-4">
                     <div className="text-right">
                        <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">مرحلة النمو</div>
                        <div className="font-extrabold text-[#0F172A]">تسمين يوم 32</div>
                     </div>
                     <div className="w-14 h-14 rounded-full border-4 border-gray-100 dark:border-slate-700 flex items-center justify-center relative">
                        <svg className="absolute inset-0 w-full h-full transform -rotate-90">
                           <circle cx="24" cy="24" r="22" stroke="#D32F2F" strokeWidth="4" fill="none" strokeDasharray="138" strokeDashoffset="34.5" />
                        </svg>
                        <span className="text-xs font-bold text-[#0F172A]">75%</span>
                     </div>
                  </div>

                  <div className="flex items-center justify-end gap-4">
                     <div className="text-right">
                        <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">الكفاءة</div>
                        <div className="font-extrabold text-[#0F172A]">1.62 معامل<br />تحويل</div>
                     </div>
                     <div className="w-14 h-14 rounded-full bg-green-50 flex items-center justify-center text-green-600">
                        <TrendingUp size={24} />
                     </div>
                  </div>
               </div>

            </div>
         </div>

         {/* Modals */}
         {showMortalityModal && (
            <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm">
               <div className="bg-white dark:bg-slate-800 rounded-3xl p-8 w-[400px] shadow-2xl">
                  <div className="flex justify-between items-center mb-6 flex-row-reverse">
                     <h3 className="text-xl font-extrabold text-[#0F172A]">تسجيل حالات النافق</h3>
                     <button onClick={() => setShowMortalityModal(false)} className="text-gray-400 hover:text-gray-700 dark:text-gray-200">
                        <X size={24} />
                     </button>
                  </div>
                  <div className="mb-6 text-right">
                     <label className="block text-sm font-bold text-gray-700 dark:text-gray-200 mb-2">عدد الطيور النافقة اليوم</label>
                     <input
                        type="number"
                        value={mortalityInput}
                        onChange={(e) => setMortalityInput(e.target.value)}
                        className="w-full border border-gray-200 dark:border-slate-700 rounded-xl p-4 text-right focus:border-[#B71C1C] focus:outline-none"
                        placeholder="أدخل العدد (مثال: 5)"
                     />
                  </div>
                  <button onClick={handleMortalitySubmit} className="w-full bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-4 rounded-xl transition-colors">
                     حفظ وتحديث القطيع
                  </button>
               </div>
            </div>
         )}

         {showFeedModal && (
            <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm">
               <div className="bg-white dark:bg-slate-800 rounded-3xl p-8 w-[400px] shadow-2xl">
                  <div className="flex justify-between items-center mb-6 flex-row-reverse">
                     <h3 className="text-xl font-extrabold text-[#0F172A]">تسجيل استهلاك العلف</h3>
                     <button onClick={() => setShowFeedModal(false)} className="text-gray-400 hover:text-gray-700 dark:text-gray-200">
                        <X size={24} />
                     </button>
                  </div>
                  <div className="mb-6 text-right">
                     <label className="block text-sm font-bold text-gray-700 dark:text-gray-200 mb-2">الكمية المستهلكة (بالطن)</label>
                     <input
                        type="number"
                        step="0.01"
                        value={feedInput}
                        onChange={(e) => setFeedInput(e.target.value)}
                        className="w-full border border-gray-200 dark:border-slate-700 rounded-xl p-4 text-right focus:border-[#B71C1C] focus:outline-none"
                        placeholder="أدخل الكمية (مثال: 1.5)"
                     />
                  </div>
                  <button onClick={handleFeedSubmit} className="w-full bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-4 rounded-xl transition-colors">
                     حفظ التحديث
                  </button>
               </div>
            </div>
         )}

         {showTaskModal && (
            <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm p-4">
               <div className="bg-white dark:bg-slate-800 rounded-3xl p-8 w-[500px] max-w-full shadow-2xl text-center flex flex-col max-h-[80vh]">
                  <div className="w-16 h-16 bg-gray-50 dark:bg-slate-900 rounded-full flex items-center justify-center mx-auto mb-4 text-[#D32F2F] border border-gray-100 dark:border-slate-700 shrink-0">
                     <ArrowUpRight size={32} />
                  </div>
                  <h3 className="text-xl font-extrabold text-[#0F172A] mb-4 shrink-0">{activeTask}</h3>
                  
                  <div className="flex-1 overflow-y-auto mb-6 px-2 text-right">
                     {isTaskLoading ? (
                        <div className="flex flex-col items-center justify-center py-8 gap-3">
                           <div className="w-8 h-8 border-4 border-[#B71C1C] border-t-transparent rounded-full animate-spin"></div>
                           <span className="text-sm font-bold text-gray-500">جاري استشارة قاعدة المعرفة...</span>
                        </div>
                     ) : (
                        <div className="text-sm text-gray-600 dark:text-gray-300 whitespace-pre-wrap leading-relaxed font-medium">
                           {taskGuidance}
                        </div>
                     )}
                  </div>

                  <button onClick={() => setShowTaskModal(false)} className="w-full bg-[#0F172A] hover:bg-black text-white font-bold py-3.5 rounded-xl transition-colors text-sm shrink-0">
                     إغلاق
                  </button>
               </div>
            </div>
         )}

      </div>
   );
}
