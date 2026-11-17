import { createContext, useContext, useState, useEffect } from 'react';
import { HeartCrack, AlertTriangle, Info, CheckCircle } from 'lucide-react';

const NotificationContext = createContext();

export function NotificationProvider({ children }) {
   const [alerts, setAlerts] = useState([]);
   const [unreadCount, setUnreadCount] = useState(0);

   const evaluateAlerts = () => {
      const isEnabled = localStorage.getItem('alerts') !== 'false';
      if (!isEnabled) {
         setAlerts([]);
         setUnreadCount(0);
         return;
      }

      // Load data for evaluation
      const initialFlockSize = parseInt(localStorage.getItem('flockSize') || '42500', 10);
      const totalMortality = parseInt(localStorage.getItem('manualMortality') || '0', 10);
      const mortalityRate = initialFlockSize > 0 ? ((totalMortality / initialFlockSize) * 100).toFixed(1) : 0;

      const financialTransactions = JSON.parse(localStorage.getItem('financialTransactions') || '[]');
      const totalFinancialRevenues = financialTransactions
         .filter(t => t.type === 'income')
         .reduce((sum, t) => sum + Number(t.amount), 0);
      const totalFinancialExpenses = financialTransactions
         .filter(t => t.type === 'expense')
         .reduce((sum, t) => sum + Number(t.amount), 0);

      const vaccinations = JSON.parse(localStorage.getItem('vaccinationData') || '[]');
      const upcomingVaccine = vaccinations.find(v => v.status === 'upcoming' || v.status === 'scheduled');

      // Generate alerts
      let newAlerts = [];
      if (mortalityRate > 1.5) {
         newAlerts.push({
            id: 'mortality-alert',
            type: 'critical',
            title: 'ارتفاع نسبة النفوق!',
            time: 'عاجل',
            text: `نسبة النفوق وصلت ${mortalityRate}%. يرجى التحقق من العنابر وطلب استشارة بيطرية فوراً.`,
            iconType: 'critical'
         });
      }
      if (totalFinancialExpenses > totalFinancialRevenues && totalFinancialExpenses > 0) {
         newAlerts.push({
            id: 'finance-alert',
            type: 'warning',
            title: 'عجز مالي مؤقت',
            time: 'تحديث اليوم',
            text: `مصروفاتك ($${totalFinancialExpenses}) تجاوزت إيراداتك. راجع بند "الأعلاف واللقاحات" لتقليل الهدر.`,
            iconType: 'warning'
         });
      }
      if (upcomingVaccine) {
         newAlerts.push({
            id: 'vaccine-alert',
            type: 'info',
            title: 'ميعاد تحصين قادم',
            time: upcomingVaccine.date,
            text: `تحصين "${upcomingVaccine.name}" مطلوب قريباً. يرجى تجهيز الجرعات المطلوبة.`,
            iconType: 'info'
         });
      }

      if (newAlerts.length === 0) {
         newAlerts.push({
            id: 'all-clear',
            type: 'success',
            title: 'الوضع آمن',
            time: 'الآن',
            text: 'لا توجد أي تنبيهات عاجلة. جميع المؤشرات الحيوية والمالية في وضعها الطبيعي.',
            iconType: 'success'
         });
      }

      // Check against dismissed/read alerts from localStorage
      const readAlerts = JSON.parse(localStorage.getItem('readAlerts') || '[]');
      const finalAlerts = newAlerts.map(a => ({
         ...a,
         isRead: readAlerts.includes(a.id)
      }));

      setAlerts(finalAlerts);
      setUnreadCount(finalAlerts.filter(a => !a.isRead && a.type !== 'success').length);
   };

   useEffect(() => {
      evaluateAlerts();
      const handleStorageChange = () => evaluateAlerts();
      window.addEventListener('storage', handleStorageChange);
      window.addEventListener('farm-data-updated', handleStorageChange);
      return () => {
         window.removeEventListener('storage', handleStorageChange);
         window.removeEventListener('farm-data-updated', handleStorageChange);
      };
   }, []);

   const markAsRead = (id) => {
      const readAlerts = JSON.parse(localStorage.getItem('readAlerts') || '[]');
      if (!readAlerts.includes(id)) {
         readAlerts.push(id);
         localStorage.setItem('readAlerts', JSON.stringify(readAlerts));
         evaluateAlerts();
      }
   };

   const markAllAsRead = () => {
      const allIds = alerts.map(a => a.id);
      localStorage.setItem('readAlerts', JSON.stringify(allIds));
      evaluateAlerts();
   };

   return (
      <NotificationContext.Provider value={{ alerts, unreadCount, markAsRead, markAllAsRead }}>
         {children}
      </NotificationContext.Provider>
   );
}

export function useNotifications() {
   return useContext(NotificationContext);
}
