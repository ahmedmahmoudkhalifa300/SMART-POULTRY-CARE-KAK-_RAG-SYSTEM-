import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Bell } from 'lucide-react';

export default function SelectProduction() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col min-h-screen bg-[#F9FAFB]" dir="rtl">
      {/* Header */}
      <div className="p-6 flex justify-between items-center max-w-7xl mx-auto w-full">
        <div className="flex items-center gap-4">
           <div className="w-10 h-10 bg-gray-200 rounded-full overflow-hidden border border-gray-300">
               <img src="https://i.pravatar.cc/150?img=11" alt="User" />
           </div>
           <button className="text-gray-600 hover:text-gray-900 transition-colors">
               <Bell size={20} />
           </button>
        </div>
        <div className="font-bold text-3xl text-[#B71C1C]">PoultryAI</div>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center px-4 -mt-10">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-[#0F172A] mb-4">اختر نوع الإنتاج</h1>
          <p className="text-gray-500 dark:text-gray-400 text-lg">اختر مجال عملك لمعايرة مساعد الذكاء الاصطناعي لتحقيق العائد الأمثل ومراقبة صحة القطيع.</p>
        </div>

        <div className="flex flex-col md:flex-row gap-6 max-w-4xl w-full justify-center">
          
          {/* Broiler Card */}
          <div className="flex-1 bg-white dark:bg-slate-800 border border-gray-200 hover:border-[#B71C1C] hover:shadow-lg rounded-[32px] p-8 transition-all relative overflow-hidden group cursor-pointer flex flex-col min-h-[350px]"
               onClick={() => navigate('/onboarding')}
          >
            <div className="flex justify-between items-start mb-6">
               <div className="flex-1"></div>
               <span className="bg-red-50 text-[#B71C1C] text-xs font-bold px-4 py-1.5 rounded-full flex items-center gap-2">
                 جاهز للبدء <div className="w-2 h-2 bg-[#B71C1C] rounded-full"></div>
               </span>
            </div>
            
            <div className="text-center mb-4 flex-1 flex flex-col justify-center">
              <h2 className="text-4xl font-extrabold text-[#0F172A] mb-4">تسمين</h2>
              <p className="text-gray-500 dark:text-gray-400 text-base leading-relaxed max-w-xs mx-auto">
                محسّن لإنتاج اللحوم. مراقبة فورية لمنحنيات النمو، ومعدلات تحويل الأعلاف (FCR)، ومعايير الراحة الحرارية لزيادة دورات الإنتاج.
              </p>
            </div>

            <div className="flex justify-center mt-6">
              <button className="text-[#B71C1C] font-bold text-lg flex items-center gap-2 group-hover:gap-3 transition-all">
                إعداد سير العمل
                <span className="text-xl">←</span>
              </button>
            </div>
          </div>

          {/* Layer Card (Disabled) */}
          <div className="flex-1 bg-[#F1F3F5] dark:bg-slate-800/50 border border-transparent rounded-[32px] p-8 relative flex flex-col min-h-[350px]">
            <div className="flex justify-between items-start mb-6 w-full">
               <span className="bg-white/60 text-gray-500 text-xs font-bold px-4 py-1.5 rounded-full">
                 المرحلة الثانية
               </span>
               <span className="bg-gray-200 text-gray-500 text-xs font-bold px-4 py-1.5 rounded-full">
                 قريباً
               </span>
            </div>
            
            <div className="text-center mb-4 flex-1 flex flex-col justify-center">
              <h2 className="text-4xl font-extrabold text-gray-400 mb-4">بياض</h2>
              <p className="text-gray-400 text-base leading-relaxed max-w-xs mx-auto">
                مخصص لدورات إنتاج البيض. تحليلات تنبؤية لمعدلات وضع البيض، وتتبع جودة البيض، وإدارة دورة الحياة الممتدة للمزارع الكبيرة.
              </p>
            </div>

            <div className="flex justify-center mt-6 items-center gap-2 text-gray-400 font-bold">
               <Lock size={16} />
               قادم في الربع الرابع ٢٠٢٤
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
