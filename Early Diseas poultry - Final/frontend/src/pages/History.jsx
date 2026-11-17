import { useState, useEffect } from 'react';
import { History as HistoryIcon, Search, FileText, ChevronLeft, CheckCircle, Syringe, Wallet, TrendingUp, TrendingDown, Filter } from 'lucide-react';

export default function History() {
  const [allRecords, setAllRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('الكل');

  useEffect(() => {
    const fetchUnifiedHistory = async () => {
      let unified = [];
      
      // 1. Fetch AI Predictions
      try {
        const response = await fetch('http://localhost:8000/predictions');
        if (response.ok) {
          const data = await response.json();
          const formattedRecords = data.map((item) => ({
            id: `pred-${item.id}`,
            realTimestamp: new Date(item.timestamp).getTime(),
            type: "تشخيص طبي",
            desc: `تحليل عينة - نتيجة: ${item.predicted_disease === 'Healthy' ? 'سليم' : item.predicted_disease === 'Coccidiosis' ? 'كوكسيديا' : item.predicted_disease === 'Salmonella' ? 'سالمونيلا' : item.predicted_disease === 'New Castle Disease' ? 'نيوكاسل' : item.predicted_disease}`,
            date: new Date(item.timestamp).toLocaleDateString('ar-EG'),
            icon: <FileText size={18}/>,
            color: item.predicted_disease === 'Healthy' ? 'green' : 'red'
          }));
          unified = [...unified, ...formattedRecords];
        }
      } catch (error) {
        console.error("Failed to load predictions", error);
      }

      // 2. Fetch Financials
      const financialSaved = localStorage.getItem('financialTransactions');
      if (financialSaved) {
         const transactions = JSON.parse(financialSaved);
         const formattedFinancials = transactions.map(t => ({
            id: `fin-${t.id}`,
            realTimestamp: t.id,
            type: t.type === 'income' ? 'إيراد مالي' : 'مصروف مالي',
            desc: `${t.category} - ${t.amount}$`,
            date: t.date,
            icon: t.type === 'income' ? <TrendingUp size={18}/> : <TrendingDown size={18}/>,
            color: t.type === 'income' ? 'blue' : 'red'
         }));
         unified = [...unified, ...formattedFinancials];
      }

      // 3. Fetch Vaccinations
      const vaccinesSaved = localStorage.getItem('vaccinationData');
      if (vaccinesSaved) {
         const vaccines = JSON.parse(vaccinesSaved);
         const completedVaccines = vaccines.filter(v => v.status === 'completed');
         const formattedVaccines = completedVaccines.map(v => ({
            id: `vac-${v.id}`,
            realTimestamp: v.id,
            type: 'تطعيم مكتمل',
            desc: v.name,
            date: v.date.split(' | ')[0],
            icon: <Syringe size={18}/>,
            color: 'purple'
         }));
         unified = [...unified, ...formattedVaccines];
      }

      // Sort all by timestamp descending
      unified.sort((a, b) => b.realTimestamp - a.realTimestamp);

      setAllRecords(unified);
      setLoading(false);
    };

    fetchUnifiedHistory();
  }, []);

  const filteredRecords = allRecords.filter(record => {
     const matchesSearch = record.desc.includes(searchTerm) || record.type.includes(searchTerm);
     const matchesFilter = filterType === 'الكل' || 
                           (filterType === 'تشخيصات' && record.type.includes('تشخيص')) ||
                           (filterType === 'ماليات' && record.type.includes('مالي')) ||
                           (filterType === 'تطعيمات' && record.type.includes('تطعيم'));
     return matchesSearch && matchesFilter;
  });

  return (
    <div className="flex flex-col gap-6 h-full pb-8 max-w-5xl mx-auto w-full">
      <div className="flex justify-between items-center mb-2 flex-row-reverse">
        <div className="text-right">
          <h1 className="text-[32px] font-bold text-[#0F172A] mb-2">السجل التاريخي الموحد</h1>
          <p className="text-gray-500 dark:text-gray-400 text-sm">راجع جميع الأنشطة، التشخيصات، والمعاملات لمزرعتك.</p>
        </div>
        <div className="relative w-72">
           <Search className="absolute right-3 top-2.5 text-gray-400" size={18} />
           <input 
              type="text" 
              placeholder="ابحث في التشخيصات، الماليات..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl py-2 pr-10 pl-4 text-sm focus:outline-none focus:border-[#B71C1C] shadow-sm text-right"
           />
        </div>
      </div>

      <div className="flex gap-2 justify-end mb-2">
         {['الكل', 'تشخيصات', 'ماليات', 'تطعيمات'].map(type => (
            <button 
               key={type}
               onClick={() => setFilterType(type)}
               className={`px-4 py-2 rounded-lg text-sm font-bold transition-colors ${filterType === type ? 'bg-[#B71C1C] text-white' : 'bg-white dark:bg-slate-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-900'}`}
            >
               {type}
            </button>
         ))}
      </div>

      <div className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-3xl shadow-sm overflow-hidden text-right">
         <div className="flex flex-col">
            {loading ? (
              <div className="text-center py-10 text-gray-500 font-bold">جاري تجميع السجلات...</div>
            ) : filteredRecords.length === 0 ? (
              <div className="text-center py-10 text-gray-500 font-bold">لا توجد سجلات تطابق بحثك.</div>
            ) : filteredRecords.map((record, i) => (
               <div key={record.id} className={`flex items-center justify-between p-5 cursor-pointer hover:bg-gray-50 dark:bg-slate-900 transition-colors flex-row-reverse ${i !== filteredRecords.length - 1 ? 'border-b border-gray-100 dark:border-slate-700' : ''}`}>
                  
                  <div className="flex items-center gap-4 flex-row-reverse">
                     <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
                        record.color === 'red' ? 'bg-red-50 text-red-600' :
                        record.color === 'blue' ? 'bg-blue-50 text-blue-600' :
                        record.color === 'green' ? 'bg-green-50 text-green-600' :
                        record.color === 'purple' ? 'bg-purple-50 text-purple-600' :
                        'bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-gray-300'
                     }`}>
                        {record.icon}
                     </div>
                     <div className="text-right">
                        <h4 className="font-bold text-[#0F172A] mb-0.5 text-sm">{record.desc}</h4>
                        <div className="text-xs font-bold text-gray-400">{record.type}</div>
                     </div>
                  </div>

                  <div className="flex items-center gap-6 flex-row-reverse shrink-0">
                     <div className="text-sm font-bold text-gray-500 dark:text-gray-400">
                        {record.date}
                     </div>
                     <ChevronLeft size={20} className="text-gray-300"/>
                  </div>
               </div>
            ))}
         </div>
      </div>
      
      <div className="text-center mt-4">
         <button className="text-[#B71C1C] font-bold text-sm bg-transparent border-none cursor-pointer hover:underline">
            تحميل المزيد من الأرشيف...
         </button>
      </div>
    </div>
  );
}
