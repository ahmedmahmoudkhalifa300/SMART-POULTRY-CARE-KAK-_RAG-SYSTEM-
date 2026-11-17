import { useNavigate } from 'react-router-dom';
import { TrendingUp, AlertTriangle, Syringe, FileText } from 'lucide-react';
import { useNotifications } from '../context/NotificationContext';

export default function SmartBanner({ healthIndex, mortalityRate, hoverCardClass }) {
   const navigate = useNavigate();
   const { alerts } = useNotifications();

   // Determine texts based on health
   let bannerTitle = "";
   let bannerText = "";
   if (healthIndex >= 90) {
      bannerTitle = "كله تمام يا فنان.. الكتاكيت زي الفل النهاردة!";
      bannerText = `بناءً على بيانات القطيع، سحب العلف مستقر والنفوق عند ${mortalityRate}%. الذكاء الاصطناعي بيأكد إن صحة القطيع ممتازة، استمر على نفس الأداء.`;
   } else if (healthIndex >= 80) {
      bannerTitle = "الأمور مستقرة، بس خلي بالك!";
      bannerText = `مؤشر الصحة ${healthIndex}%. معدل النفوق (${mortalityRate}%) في الحدود الآمنة، لكن يُفضل مراجعة السجلات لتجنب أي إجهاد.`;
   } else {
      bannerTitle = "تحذير عاجل: القطيع في خطر!";
      bannerText = `مؤشر الصحة انخفض إلى ${healthIndex}%. نسبة النفوق (${mortalityRate}%) مرتفعة جداً. الذكاء الاصطناعي يوصي بالتدخل السريع للتشخيص.`;
   }

   // Determine Smart CTA based on alerts
   const hasCriticalAlert = alerts.some(a => a.type === 'critical');
   const hasVaccineAlert = alerts.some(a => a.id === 'vaccine-alert');

   let primaryAction = {
      label: 'التقرير اليومي',
      icon: <FileText size={16} />,
      path: '/daily',
      color: 'bg-[#B71C1C] hover:bg-[#991616]'
   };

   if (hasCriticalAlert) {
      primaryAction = {
         label: 'التشخيص الذكي',
         icon: <AlertTriangle size={16} />,
         path: '/diagnostics',
         color: 'bg-[#B71C1C] hover:bg-[#991616]'
      };
   } else if (hasVaccineAlert) {
      primaryAction = {
         label: 'تفاصيل التحصين',
         icon: <Syringe size={16} />,
         path: '/vaccinations',
         color: 'bg-green-600 hover:bg-green-700'
      };
   }

   return (
      <div className={`flex-1 bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl shadow-sm p-8 flex flex-col justify-between ${hoverCardClass}`}>
         <div>
            <div className="flex items-center gap-3 mb-6">
               <span className={`${healthIndex >= 90 ? 'bg-green-600' : healthIndex >= 80 ? 'bg-yellow-600' : 'bg-[#B71C1C]'} text-white text-xs font-bold px-4 py-1.5 rounded-full transition-colors`}>نظرة يومية</span>
               <span className="text-gray-500 dark:text-gray-400 text-sm font-bold">{new Date().toLocaleDateString('ar-EG')}</span>
            </div>
            
            <h2 className="text-2xl font-extrabold text-[#0F172A] mb-3">{bannerTitle}</h2>
            <p className="text-gray-600 dark:text-gray-300 text-sm font-medium leading-relaxed max-w-3xl">
               {bannerText}
            </p>
         </div>
         
         <div className="flex items-center gap-4 justify-end mt-4">
            <button 
               onClick={() => navigate('/history')}
               className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:bg-slate-900 font-bold px-6 py-2.5 rounded-xl shadow-sm transition-colors text-sm"
            >
               السجل التاريخي
            </button>
            <button 
               onClick={() => navigate(primaryAction.path)}
               className={`${primaryAction.color} text-white font-bold px-6 py-2.5 rounded-xl shadow-sm transition-colors flex items-center gap-2 text-sm`}
            >
               <span>{primaryAction.label}</span>
               {primaryAction.icon}
            </button>
         </div>
      </div>
   );
}
