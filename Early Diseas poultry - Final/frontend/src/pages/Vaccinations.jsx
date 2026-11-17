import { useState, useEffect } from 'react';
import { Download, Plus, CheckCircle, Hourglass, Clock, AlertTriangle, Syringe, Box, RefreshCw, FileText, Bot, X } from 'lucide-react';

const initialVaccines = [
  { id: 1, name: 'مرض نيوكاسل (ND) - كلون 30', supervisor: 'د. سارة جنكينز', details: 'دفعة# 12,000 • ND2408-A جرعة', date: '12 أكتوبر 2023 | 05:30 صباحاً', status: 'completed' },
  { id: 2, name: 'التهاب الشعب الهوائية المعدي (IB)', supervisor: 'فريق البيطرة المساعد', details: 'يجب اتخاذ التدابير الوقائية القياسية. يطبق عن طريق الرش في جميع العنابر النشطة.', date: 'خلال يومين', status: 'upcoming', dose: '0.2 مل/طائر', target: 'عنبر 01 - 12', method: 'تحت الجلد' },
  { id: 3, name: 'إنفلونزا الطيور (H5N1)', supervisor: 'الطبيب المناوب', details: 'مجدول للدفعة الجديدة', date: 'بعد 14 يوماً من الآن', status: 'scheduled' }
];

export default function Vaccinations() {
  const [showReportModal, setShowReportModal] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);

  const [vaccinations, setVaccinations] = useState(() => {
     const saved = localStorage.getItem('vaccinationData');
     return saved ? JSON.parse(saved) : initialVaccines;
  });

  const [newVaccineName, setNewVaccineName] = useState('تطعيم جديد');
  const [newVaccineDetails, setNewVaccineDetails] = useState('');

  useEffect(() => {
     localStorage.setItem('vaccinationData', JSON.stringify(vaccinations));
  }, [vaccinations]);

  const handleSaveReport = () => {
    if(!newVaccineDetails) return;
    const newVaccine = {
       id: Date.now(),
       name: newVaccineName,
       supervisor: 'الطبيب المناوب',
       details: newVaccineDetails,
       date: new Date().toLocaleDateString('ar-EG'),
       status: 'scheduled'
    };
    setVaccinations([newVaccine, ...vaccinations]);
    setShowReportModal(false);
    setNewVaccineDetails('');
  };

  const handleCompleteVaccine = (id) => {
     setVaccinations(vaccinations.map(v => 
        v.id === id ? { ...v, status: 'completed', date: new Date().toLocaleDateString('ar-EG') } : v
     ));
  };

  const completedCount = vaccinations.filter(v => v.status === 'completed').length;
  const completionRate = Math.round((completedCount / (vaccinations.length || 1)) * 100);

  const upcomingVaccine = vaccinations.find(v => v.status === 'upcoming') || vaccinations.find(v => v.status === 'scheduled') || {
      name: 'لا توجد تطعيمات قادمة', date: '---', details: 'الجدول الزمني نظيف حالياً.', dose: '-', target: '-', method: '-'
  };

  return (
    <div className="flex flex-col gap-6 h-full pb-8 max-w-[1200px] mx-auto w-full">
      {/* Header */}
      <div className="flex justify-between items-center mb-2">
        <div className="flex gap-3">
          <button onClick={() => setShowReportModal(true)} className="bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-2.5 px-6 rounded-xl shadow-sm flex items-center gap-2 transition-colors text-sm">
             <Plus size={18}/> تقرير جديد
          </button>
          <button onClick={() => setShowExportModal(true)} className="bg-white dark:bg-slate-800 hover:bg-gray-50 dark:bg-slate-900 text-[#B71C1C] font-bold py-2.5 px-6 rounded-xl border-2 border-[#B71C1C] shadow-sm flex items-center gap-2 transition-colors text-sm">
             <Download size={18}/> تصدير
          </button>
        </div>
        <div className="text-right">
          <h1 className="text-[32px] font-bold text-[#0F172A] mb-2">سجل التطعيمات</h1>
          <p className="text-gray-500 dark:text-gray-400 text-sm">مجمع KAK للدواجن • دفعة 24-12,000 • B طائر</p>
        </div>
      </div>

      {/* Main Alert Card */}
      <div className="bg-white dark:bg-slate-800 border-2 border-red-100 rounded-3xl p-8 relative shadow-sm">
         <div className="absolute top-6 left-6 bg-[#FEF2F2] text-[#B71C1C] px-3 py-1.5 rounded-full text-xs font-bold flex items-center gap-2">
            التنبيهات نشطة <BellIcon />
         </div>
         <div className="text-right max-w-2xl ml-auto">
            <h4 className="text-[#B71C1C] font-bold text-sm mb-2">التطعيم القادم</h4>
            <div className="flex items-center justify-end gap-4 mb-4">
               <h2 className="text-4xl font-extrabold text-[#B71C1C]">{upcomingVaccine.date}</h2>
               <h2 className="text-3xl font-bold text-[#0F172A]">{upcomingVaccine.name}</h2>
            </div>
            <p className="text-gray-600 dark:text-gray-300 font-medium mb-8">
               {upcomingVaccine.details}
            </p>
            
            <div className="flex justify-end gap-12 mb-8">
               <div className="text-center">
                  <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">الجرعة</div>
                  <div className="font-bold text-[#0F172A]">{upcomingVaccine.dose || '-'}</div>
               </div>
               <div className="text-center">
                  <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">نطاق العنابر</div>
                  <div className="font-bold text-[#0F172A]">{upcomingVaccine.target || '-'}</div>
               </div>
               <div className="text-center">
                  <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">الطريقة</div>
                  <div className="font-bold text-[#0F172A]">{upcomingVaccine.method || '-'}</div>
               </div>
            </div>

            <div className="flex items-center gap-4 justify-end">
               <div className="h-3 bg-gray-100 dark:bg-slate-700 rounded-full w-64 overflow-hidden flex justify-end">
                  <div className="bg-[#B71C1C] h-full" style={{width: '85%'}}></div>
               </div>
               <span className="text-[#B71C1C] font-bold text-sm">85% جاهز</span>
            </div>
         </div>
      </div>

      <div className="flex gap-6">
        {/* Left Column */}
        <div className="w-[320px] flex flex-col gap-6">
           {/* Completion Rate */}
           <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm relative text-right flex flex-col justify-between h-[140px]">
              <div className="absolute top-6 left-6 bg-blue-50 text-blue-600 px-3 py-1 rounded-lg text-xs font-bold">هذا الشهر</div>
              <div className="absolute top-6 right-6 w-10 h-10 bg-gray-50 dark:bg-slate-900 rounded-xl flex items-center justify-center text-gray-500 dark:text-gray-400">
                 <CheckCircle size={20} />
              </div>
              <div className="mt-auto">
                 <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">معدل الإنجاز</div>
                 <div className="flex items-center justify-end gap-3">
                    <span className="text-green-500 font-bold text-sm bg-green-50 px-2 py-0.5 rounded-lg flex items-center">نشط</span>
                    <h2 className="text-4xl font-extrabold text-[#0F172A]">{completionRate}%</h2>
                 </div>
              </div>
           </div>

           {/* Vaccine Inventory */}
           <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm relative text-right flex flex-col justify-between h-[140px]">
              <div className="absolute top-6 right-6 w-10 h-10 bg-red-50 rounded-xl flex items-center justify-center text-[#B71C1C]">
                 <Box size={20} />
              </div>
              <div className="mt-auto">
                 <div className="text-xs text-gray-500 dark:text-gray-400 font-bold mb-1">مخزون اللقاحات</div>
                 <div className="flex items-center justify-end gap-3 mb-2">
                    <span className="text-gray-500 dark:text-gray-400 font-bold text-sm">جرعات منخفضة</span>
                    <h2 className="text-4xl font-extrabold text-[#0F172A]">14</h2>
                 </div>
                 <button className="text-[#B71C1C] font-bold text-xs flex items-center justify-end w-full gap-1">
                    طلب إمدادات ‹
                 </button>
              </div>
           </div>

           {/* Recent Log */}
           <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm text-right">
              <div className="flex justify-between items-center mb-6">
                 <button className="text-[#B71C1C] font-bold text-xs">عرض الكل</button>
                 <h3 className="font-bold text-lg text-[#0F172A]">السجل الأخير</h3>
              </div>
              <div className="flex flex-col gap-6">
                 {vaccinations.filter(v => v.status === 'completed').slice(0, 3).map(v => (
                    <div key={`log-${v.id}`} className="flex items-center justify-between">
                       <div className="text-xs text-gray-400 shrink-0">{v.date}</div>
                       <div className="flex items-center gap-3 w-full justify-end">
                          <div className="text-right">
                             <div className="font-bold text-[#0F172A] text-sm truncate">{v.name}</div>
                             <div className="text-xs text-gray-500 dark:text-gray-400 max-w-[150px] truncate">{v.details}</div>
                          </div>
                          <div className="w-8 h-8 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center shrink-0"><FileText size={14}/></div>
                       </div>
                    </div>
                 ))}
                 {vaccinations.filter(v => v.status === 'completed').length === 0 && (
                     <div className="text-sm text-gray-400 text-center py-4">لا توجد سجلات مكتملة.</div>
                 )}
              </div>
           </div>

           {/* AI Alerts */}
           <div className="bg-[#0F172A] rounded-3xl p-6 shadow-sm text-right text-white relative">
              <div className="flex items-center gap-2 justify-end mb-4 text-sm font-bold opacity-80">
                 تنبيهات الذكاء الاصطناعي <Bot size={16} />
              </div>
              <h3 className="text-xl font-bold mb-3">تنبيه التوقيت الأمثل</h3>
              <p className="text-xs text-gray-300 font-medium leading-relaxed mb-6">
                 بناءً على مستويات الرطوبة الحالية (82%)، يوصي الذكاء الاصطناعي بتقديم موعد رش لقاح IB غداً إلى الساعة 05:00 صباحاً لضمان أقصى قدر من الامتصاص قبل ذروة حرارة الشمس.
              </p>
              <button className="bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-3 w-full rounded-xl transition-colors text-sm">
                 تطبيق التوصية
              </button>
           </div>
        </div>

        {/* Middle Column (Timeline) */}
        <div className="flex-1 bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col">
           <div className="flex justify-between items-center mb-8">
              <div className="flex items-center gap-3">
                 <div className="text-xs font-bold text-gray-600 dark:text-gray-300">الأسبوع 12-24</div>
                 <div className="bg-[#B71C1C] text-white px-3 py-1 rounded-lg text-xs font-bold">الأسبوع 12-0</div>
              </div>
              <h3 className="font-bold text-lg text-[#0F172A]">الجدول النشط</h3>
           </div>

           <div className="relative flex-1 mt-4 ml-6">
              {/* Vertical line right aligned */}
              <div className="absolute right-[23px] top-4 bottom-8 w-[2px] bg-red-100"></div>

              <div className="flex flex-col gap-10 h-full relative">
                 
                 {vaccinations.map(v => (
                    <div key={`timeline-${v.id}`} className="flex gap-6 items-start justify-end w-full">
                       {v.status === 'completed' && (
                          <div className="w-[85%] bg-[#F9FAFB] border border-gray-100 dark:border-slate-700 rounded-2xl p-6 text-right">
                             <div className="flex justify-between items-start mb-4">
                                <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold">مكتمل</span>
                                <div>
                                   <h4 className="font-bold text-lg text-[#0F172A]">{v.name}</h4>
                                   <p className="text-xs text-gray-500 dark:text-gray-400">بإشراف: {v.supervisor}</p>
                                </div>
                             </div>
                             <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-xl p-4 flex justify-between items-center">
                                <div className="text-right w-full pr-2">
                                   <div className="text-xs text-gray-400 mb-1">{v.details}</div>
                                   <div className="font-bold text-sm text-[#0F172A]">{v.date}</div>
                                </div>
                             </div>
                          </div>
                       )}

                       {v.status === 'upcoming' && (
                          <div className="w-[85%] bg-white dark:bg-slate-800 border border-[#B71C1C] rounded-2xl p-6 text-right shadow-sm">
                             <div className="flex justify-between items-start mb-4">
                                <span className="bg-red-50 text-[#B71C1C] px-3 py-1 rounded-full text-xs font-bold">قادم</span>
                                <div>
                                   <h4 className="font-bold text-lg text-[#0F172A]">{v.name}</h4>
                                   <p className="text-xs text-gray-500 dark:text-gray-400">المسؤول: {v.supervisor}</p>
                                </div>
                             </div>
                             <p className="text-sm text-gray-600 dark:text-gray-300 font-medium mb-6">
                                {v.details}
                             </p>
                             <div className="flex gap-3 justify-end">
                                <button onClick={() => handleCompleteVaccine(v.id)} className="bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-2.5 px-6 rounded-xl text-sm transition-colors">
                                   تأكيد الإنجاز
                                </button>
                             </div>
                          </div>
                       )}

                       {v.status === 'scheduled' && (
                          <div className="w-[85%] bg-transparent p-4 text-right pr-6">
                             <h4 className="font-bold text-[#0F172A]">{v.name}</h4>
                             <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">مجدول: {v.date}</p>
                             <button onClick={() => handleCompleteVaccine(v.id)} className="text-xs text-[#B71C1C] font-bold hover:underline">
                                تعيين كمكتمل ✅
                             </button>
                          </div>
                       )}

                       <div className="relative z-10 w-12 h-12 bg-white dark:bg-slate-800 flex items-center justify-center mt-4 shrink-0">
                          {v.status === 'completed' && (
                             <div className="w-8 h-8 rounded-full bg-green-500 text-white flex items-center justify-center border-[3px] border-white shadow-sm">
                                <CheckCircle size={16} />
                             </div>
                          )}
                          {v.status === 'upcoming' && (
                             <div className="w-8 h-8 rounded-full bg-[#B71C1C] text-white flex items-center justify-center border-[3px] border-white shadow-sm">
                                <Hourglass size={14} />
                             </div>
                          )}
                          {v.status === 'scheduled' && (
                             <div className="w-8 h-8 rounded-full bg-white dark:bg-slate-800 text-gray-400 flex items-center justify-center border-[3px] border-gray-200 dark:border-slate-700 shadow-sm">
                                <Clock size={16} />
                             </div>
                          )}
                       </div>
                    </div>
                 ))}

              </div>
           </div>
        </div>
      </div>

      {/* Modals */}
      {showReportModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm">
          <div className="bg-white dark:bg-slate-800 rounded-3xl p-8 w-[400px] shadow-2xl">
            <div className="flex justify-between items-center mb-6 flex-row-reverse">
              <h3 className="text-xl font-extrabold text-[#0F172A]">إضافة تقرير جديد</h3>
              <button onClick={() => setShowReportModal(false)} className="text-gray-400 hover:text-gray-700 dark:text-gray-200">
                <X size={24} />
              </button>
            </div>
            <div className="mb-4 text-right">
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-200 mb-2">نوع التقرير</label>
              <select value={newVaccineName} onChange={(e) => setNewVaccineName(e.target.value)} className="w-full border border-gray-200 dark:border-slate-700 rounded-xl p-4 text-right focus:border-[#B71C1C] focus:outline-none bg-white dark:bg-slate-800">
                <option value="تطعيم جديد">تطعيم جديد</option>
                <option value="جرعة معززة">جرعة معززة</option>
                <option value="ملاحظات أخرى">ملاحظات أخرى</option>
              </select>
            </div>
            <div className="mb-6 text-right">
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-200 mb-2">تفاصيل التقرير</label>
              <textarea 
                value={newVaccineDetails}
                onChange={(e) => setNewVaccineDetails(e.target.value)}
                className="w-full border border-gray-200 dark:border-slate-700 rounded-xl p-4 text-right focus:border-[#B71C1C] focus:outline-none"
                placeholder="أدخل التفاصيل هنا..."
                rows="3"
              ></textarea>
            </div>
            <button onClick={handleSaveReport} className="w-full bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-4 rounded-xl transition-colors">
              حفظ التقرير
            </button>
          </div>
        </div>
      )}

      {showExportModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm">
          <div className="bg-white dark:bg-slate-800 rounded-3xl p-8 w-[400px] shadow-2xl text-center">
            <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4 text-[#B71C1C]">
               <Download size={32} />
            </div>
            <h3 className="text-xl font-extrabold text-[#0F172A] mb-2">تصدير سجل التطعيمات</h3>
            <p className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-6">سيتم تجهيز تقرير التطعيمات الشامل بصيغة PDF وتنزيله.</p>
            <div className="flex gap-3">
              <button onClick={() => setShowExportModal(false)} className="flex-1 bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-200 font-bold py-3.5 rounded-xl transition-colors text-sm">
                إلغاء
              </button>
              <button onClick={() => {
                alert("جاري التنزيل...");
                setShowExportModal(false);
              }} className="flex-1 bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-3.5 rounded-xl transition-colors text-sm">
                تأكيد التنزيل
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

function BellIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
  )
}
