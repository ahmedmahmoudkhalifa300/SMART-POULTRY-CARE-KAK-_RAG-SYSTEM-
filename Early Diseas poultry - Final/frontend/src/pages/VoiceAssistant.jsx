import { Mic, Activity, CheckCircle } from 'lucide-react';

export default function VoiceAssistant() {
  return (
    <div className="flex flex-col gap-6 h-full pb-8 max-w-4xl mx-auto w-full">
      <div>
        <h1 className="text-[32px] font-bold text-[#0F172A] mb-2">المساعد الصوتي (KAK Voice)</h1>
        <p className="text-gray-500 dark:text-gray-400 text-sm">تحدث مع مساعدك الذكي لتسجيل الملاحظات اليومية والحصول على تقارير فورية.</p>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-3xl shadow-sm p-10 relative overflow-hidden">
         {/* Background pulse effect */}
         <div className="absolute inset-0 flex items-center justify-center opacity-5">
            <div className="w-[500px] h-[500px] bg-[#B71C1C] rounded-full filter blur-3xl"></div>
         </div>

         <div className="relative z-10 flex flex-col items-center">
            <div className="w-32 h-32 bg-[#FEF2F2] rounded-full flex items-center justify-center text-[#B71C1C] mb-8 cursor-pointer hover:scale-105 transition-transform shadow-lg border-4 border-white">
               <Mic size={48} />
            </div>
            
            <h2 className="text-2xl font-bold text-[#0F172A] mb-3">أنا أستمع...</h2>
            <p className="text-gray-500 dark:text-gray-400 text-center max-w-md leading-relaxed mb-10">
               يمكنك قول: "سجل نفوق ٥ طيور اليوم في العنبر أ" أو "ما هو معدل استهلاك العلف هذا الأسبوع؟"
            </p>

            <div className="w-full max-w-lg bg-gray-50 dark:bg-slate-900 p-5 rounded-2xl border border-gray-100 dark:border-slate-700 flex items-start gap-4">
               <Activity className="text-[#B71C1C] mt-1" size={24} />
               <div>
                  <h4 className="font-bold text-[#0F172A] mb-1">تحديثات تم تسجيلها مؤخراً</h4>
                  <ul className="text-sm text-gray-600 dark:text-gray-300 flex flex-col gap-2 mt-3">
                     <li className="flex items-center gap-2"><CheckCircle size={14} className="text-green-500"/> تم تسجيل استهلاك ٥٠ كجم علف (اليوم ١٠:٠٠ ص)</li>
                     <li className="flex items-center gap-2"><CheckCircle size={14} className="text-green-500"/> تم إضافة ملاحظة: انخفاض ملحوظ في نشاط القطيع (أمس)</li>
                  </ul>
               </div>
            </div>
         </div>
      </div>
    </div>
  );
}
