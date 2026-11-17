import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { Download, Plus, TrendingUp, TrendingDown, Wallet, Bot, FileText, ShoppingCart, Tag, Activity, X, Trash2 } from 'lucide-react';
import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const chartData = [
   { name: 'يناير', revenues: 0, expenses: 0 },
   { name: 'فبراير', revenues: 0, expenses: 0 },
   { name: 'مارس', revenues: 0, expenses: 0 },
   { name: 'أبريل', revenues: 0, expenses: 0 },
   { name: 'مايو', revenues: 0, expenses: 0 },
];

export default function Financials() {
   const [transactions, setTransactions] = useState(() => {
      const saved = localStorage.getItem('financialTransactions');
      return saved ? JSON.parse(saved) : [];
   });
   const [transactionType, setTransactionType] = useState('income');
   const [transactionCategory, setTransactionCategory] = useState('إيرادات مبيعات');
   const [transactionAmount, setTransactionAmount] = useState('');

   useEffect(() => {
      localStorage.setItem('financialTransactions', JSON.stringify(transactions));
   }, [transactions]);

   const totalExpenses = transactions
      .filter((transaction) => transaction.type === 'expense')
      .reduce((sum, transaction) => sum + transaction.amount, 0);
   const totalRevenues = transactions
      .filter((transaction) => transaction.type === 'income')
      .reduce((sum, transaction) => sum + transaction.amount, 0);

   const birdCost = transactions.filter(t => t.category === 'الكتاكيت الأساسية' && t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);
   const feedCost = transactions.filter(t => t.category === 'إمدادات الأعلاف' && t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);
   const medicineCost = transactions.filter(t => t.category === 'الأدوية واللقاحات' && t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);
   const logisticsCost = transactions.filter(t => t.category === 'الخدمات اللوجستية' && t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);
   const maintenanceCost = transactions.filter(t => t.category === 'الصيانة' && t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);

  const netProfit = totalRevenues - totalExpenses;
  const profitMargin = totalRevenues > 0 ? ((netProfit / totalRevenues) * 100).toFixed(1) : 0;

   const dynamicChartData = [...chartData];
   dynamicChartData[4] = { name: 'مايو (حالي)', revenues: Math.floor(totalRevenues), expenses: Math.floor(totalExpenses) };

  const [showTransactionModal, setShowTransactionModal] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);

  // Dynamic AI Insight string
  let aiInsightString = "أضف بعض المعاملات ليتمكن الذكاء الاصطناعي من تقديم رؤى مالية.";
  if (totalExpenses > 0) {
    const expensesMap = {
      'الأعلاف': feedCost,
      'الكتاكيت': birdCost,
      'الأدوية': medicineCost,
      'اللوجستيات': logisticsCost,
      'الصيانة': maintenanceCost
    };
    let highestExpense = Object.keys(expensesMap).reduce((a, b) => expensesMap[a] > expensesMap[b] ? a : b);
    let highestValue = expensesMap[highestExpense];
    let percentage = ((highestValue / totalExpenses) * 100).toFixed(0);
    aiInsightString = `تستحوذ ${highestExpense} على نسبة ${percentage}% من مصروفاتك الإجمالية. حاول تقليل الهدر أو البحث عن موردين بأسعار أفضل لزيادة هامش الربح.`;
  }

   const handleTransactionSubmit = () => {
      const amount = parseFloat(transactionAmount);
      if (!amount || amount <= 0) return;

      setTransactions((currentTransactions) => [
         ...currentTransactions,
         {
            id: Date.now(),
            entity: transactionType === 'income' ? 'إيراد جديد' : 'مصروف جديد',
            subEntity: 'تمت الإضافة يدويًا',
            category: transactionCategory,
            date: new Date().toLocaleDateString('ar-EG'),
            status: 'مكتمل',
            amount,
            type: transactionType,
         },
      ]);
      setTransactionAmount('');
      setShowTransactionModal(false);
   };

   const handleDeleteTransaction = (id) => {
      setTransactions((currentTransactions) => currentTransactions.filter(t => t.id !== id));
   };

   // Update categories when type changes
   useEffect(() => {
      if (transactionType === 'income') {
         setTransactionCategory('إيرادات مبيعات');
      } else {
         setTransactionCategory('إمدادات الأعلاف');
      }
   }, [transactionType]);

  return (
    <>
      <div className="flex flex-col gap-6 h-full pb-8 max-w-[1200px] mx-auto w-full">
      {/* Header */}
      <div className="flex justify-between items-center mb-2">
        <div className="flex gap-3">
          <button onClick={() => setShowTransactionModal(true)} className="bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-2.5 px-6 rounded-xl shadow-sm flex items-center gap-2 transition-colors text-sm">
             <Plus size={18}/> إضافة معاملة
          </button>
          <button onClick={() => setShowExportModal(true)} className="bg-white dark:bg-slate-800 hover:bg-gray-50 dark:bg-slate-900 text-[#B71C1C] font-bold py-2.5 px-6 rounded-xl border-2 border-[#B71C1C] shadow-sm flex items-center gap-2 transition-colors text-sm">
             <Download size={18}/> تصدير PDF
          </button>
        </div>
        <div className="text-right">
          <h1 className="text-[32px] font-bold text-[#0F172A] mb-2">الإدارة المالية</h1>
          <p className="text-gray-500 dark:text-gray-400 text-sm">تتبع الأرباح والمصروفات لمزرعة الدواجن في الوقت الفعلي.</p>
        </div>
      </div>

      {/* Top Cards */}
      <div className="grid grid-cols-3 gap-6">
        {/* Net Profit Margin */}
        <div className="bg-[#0F172A] text-white rounded-3xl p-6 shadow-sm relative overflow-hidden flex flex-col justify-between">
           <div className="flex justify-between items-start mb-6">
              <div className="bg-[#1E293B] px-3 py-1 rounded-full text-xs font-bold text-gray-300">
                {profitMargin > 0 ? '+' : ''}{profitMargin}%
              </div>
              <div className="w-10 h-10 bg-[#B71C1C] rounded-xl flex items-center justify-center">
                 <Wallet size={20} className="text-white" />
              </div>
           </div>
           <div className="text-right">
              <p className="text-gray-300 text-sm font-bold mb-1">هامش صافي الربح</p>
              <h2 className="text-4xl font-extrabold">${netProfit.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</h2>
           </div>
        </div>

        {/* Total Expenses */}
        <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col justify-between">
           <div className="flex justify-between items-start mb-6">
              <div className="bg-[#FEF2F2] px-3 py-1 rounded-full text-xs font-bold text-[#B71C1C]">
                -4.2%
              </div>
              <div className="w-10 h-10 bg-[#FEF2F2] rounded-xl flex items-center justify-center">
                 <TrendingDown size={20} className="text-[#B71C1C]" />
              </div>
           </div>
           <div className="text-right">
              <p className="text-gray-500 dark:text-gray-400 text-sm font-bold mb-1">إجمالي المصاريف (الحالية)</p>
              <h2 className="text-4xl font-extrabold text-[#0F172A]">${totalExpenses.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</h2>
           </div>
        </div>

        {/* Total Revenue */}
        <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col justify-between">
           <div className="flex justify-between items-start mb-6">
              <div className="bg-[#EFF6FF] px-3 py-1 rounded-full text-xs font-bold text-blue-600">
                +12.5%
              </div>
              <div className="w-10 h-10 bg-[#EFF6FF] rounded-xl flex items-center justify-center">
                 <TrendingUp size={20} className="text-blue-600" />
              </div>
           </div>
           <div className="text-right">
              <p className="text-gray-500 dark:text-gray-400 text-sm font-bold mb-1">الإيرادات المتوقعة</p>
              <h2 className="text-4xl font-extrabold text-[#0F172A]">${totalRevenues.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</h2>
           </div>
        </div>
      </div>

      {/* Middle Section (Chart + Expenses Distribution) */}
      <div className="flex gap-6">
        {/* Left Column (Expenses & AI) */}
        <div className="w-[320px] flex flex-col gap-6">
           <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm text-right">
              <h3 className="font-bold text-lg text-[#0F172A] mb-8">توزيع المصروفات</h3>
              
              <div className="space-y-6">
                 <div>
                    <div className="flex justify-between items-center mb-2">
                       <span className="font-bold text-[#0F172A] text-sm">${feedCost.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0})}</span>
                       <span className="text-sm font-bold text-gray-600 dark:text-gray-300 flex items-center gap-2">
                          إمدادات الأعلاف <span className="w-2 h-2 rounded-full bg-[#B71C1C]"></span>
                       </span>
                    </div>
                    <div className="h-2 w-full bg-gray-100 dark:bg-slate-700 rounded-full overflow-hidden flex justify-end">
                       <div className="h-full bg-[#B71C1C]" style={{width: `${totalExpenses ? (feedCost / totalExpenses * 100) : 0}%`}}></div>
                    </div>
                 </div>

                 <div>
                    <div className="flex justify-between items-center mb-2">
                       <span className="font-bold text-[#0F172A] text-sm">${birdCost.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0})}</span>
                       <span className="text-sm font-bold text-gray-600 dark:text-gray-300 flex items-center gap-2">
                          الكتاكيت الأساسية <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                       </span>
                    </div>
                    <div className="h-2 w-full bg-gray-100 dark:bg-slate-700 rounded-full overflow-hidden flex justify-end">
                       <div className="h-full bg-blue-500" style={{width: `${totalExpenses ? (birdCost / totalExpenses * 100) : 0}%`}}></div>
                    </div>
                 </div>

                 <div>
                    <div className="flex justify-between items-center mb-2">
                       <span className="font-bold text-[#0F172A] text-sm">${medicineCost.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0})}</span>
                       <span className="text-sm font-bold text-gray-600 dark:text-gray-300 flex items-center gap-2">
                          الأدوية واللقاحات <span className="w-2 h-2 rounded-full bg-pink-400"></span>
                       </span>
                    </div>
                    <div className="h-2 w-full bg-gray-100 dark:bg-slate-700 rounded-full overflow-hidden flex justify-end">
                       <div className="h-full bg-pink-400" style={{width: `${totalExpenses ? (medicineCost / totalExpenses * 100) : 0}%`}}></div>
                    </div>
                 </div>

                 <div>
                    <div className="flex justify-between items-center mb-2">
                       <span className="font-bold text-[#0F172A] text-sm">${logisticsCost.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0})}</span>
                       <span className="text-sm font-bold text-gray-600 dark:text-gray-300 flex items-center gap-2">
                          الخدمات اللوجستية <span className="w-2 h-2 rounded-full bg-gray-600"></span>
                       </span>
                    </div>
                    <div className="h-2 w-full bg-gray-100 dark:bg-slate-700 rounded-full overflow-hidden flex justify-end">
                       <div className="h-full bg-gray-600" style={{width: `${totalExpenses ? (logisticsCost / totalExpenses * 100) : 0}%`}}></div>
                    </div>
                 </div>

                 <div>
                    <div className="flex justify-between items-center mb-2">
                       <span className="font-bold text-[#0F172A] text-sm">${maintenanceCost.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0})}</span>
                       <span className="text-sm font-bold text-gray-600 dark:text-gray-300 flex items-center gap-2">
                          الصيانة <span className="w-2 h-2 rounded-full bg-gray-300"></span>
                       </span>
                    </div>
                    <div className="h-2 w-full bg-gray-100 dark:bg-slate-700 rounded-full overflow-hidden flex justify-end">
                       <div className="h-full bg-gray-300" style={{width: `${totalExpenses ? (maintenanceCost / totalExpenses * 100) : 0}%`}}></div>
                    </div>
                 </div>
              </div>

              <div className="mt-8 bg-[#FEF2F2] rounded-2xl p-5 border border-red-50 relative">
                 <div className="flex items-center gap-2 text-[#B71C1C] font-bold text-sm mb-3 justify-end">
                    رؤى الذكاء الاصطناعي <Bot size={18}/>
                 </div>
                 <p className="text-sm text-[#B71C1C] font-medium leading-relaxed text-right">
                    {aiInsightString}
                 </p>
              </div>
           </div>
        </div>

        {/* Chart */}
        <div className="flex-1 bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm flex flex-col">
           <div className="flex justify-between items-center mb-8">
              <div className="flex items-center gap-6">
                 <div className="flex items-center gap-2 text-sm font-bold text-gray-600 dark:text-gray-300">
                    الإيرادات <span className="w-3 h-3 rounded-full bg-[#B71C1C]"></span>
                 </div>
                 <div className="flex items-center gap-2 text-sm font-bold text-gray-600 dark:text-gray-300">
                    المصاريف <span className="w-3 h-3 rounded-full bg-gray-500"></span>
                 </div>
              </div>
              <h3 className="font-bold text-lg text-[#0F172A]">الأداء المالي</h3>
           </div>
           
           <div className="flex-1 w-full min-h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                 <BarChart data={dynamicChartData} barGap={8} margin={{top: 10, right: 0, left: 0, bottom: 0}}>
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#6B7280', fontSize: 12, fontWeight: 'bold'}} dy={10} reversed={true}/>
                    <Tooltip cursor={{fill: '#F9FAFB'}} contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)', textAlign: 'right', direction: 'rtl'}} />
                    <Bar dataKey="revenues" fill="#B71C1C" radius={[4,4,0,0]} barSize={40} name="الإيرادات" />
                    <Bar dataKey="expenses" fill="#6B7280" radius={[4,4,0,0]} barSize={40} name="المصاريف" />
                 </BarChart>
              </ResponsiveContainer>
           </div>
        </div>
      </div>

      {/* Transactions List */}
      <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-6 shadow-sm">
         <div className="flex justify-between items-center mb-8">
            <button className="w-10 h-10 bg-[#B71C1C] hover:bg-[#991616] text-white rounded-full flex items-center justify-center shadow-sm transition-colors">
               <Plus size={20}/>
            </button>
            <h3 className="font-bold text-lg text-[#0F172A]">سجل المعاملات</h3>
         </div>

         <div className="w-full">
            <div className="flex justify-between items-center text-xs font-bold text-gray-400 border-b border-gray-100 dark:border-slate-700 pb-4 mb-4 text-right px-4">
               <div className="w-[15%] text-left">المبلغ</div>
               <div className="w-[15%]">الحالة</div>
               <div className="w-[20%]">التاريخ</div>
               <div className="w-[15%]">الفئة</div>
               <div className="w-[35%] pr-4">الجهة / النوع</div>
            </div>

            <div className="flex flex-col gap-2">
               {transactions.map((tr) => (
                  <div key={tr.id} className="flex justify-between items-center p-4 rounded-2xl hover:bg-gray-50 dark:bg-slate-900 transition-colors text-sm font-bold text-right border border-transparent hover:border-gray-100 dark:border-slate-700">
                     <div className={`w-[15%] text-left text-lg ${tr.type === 'income' ? 'text-green-600' : 'text-[#B71C1C]'}`}>
                        {tr.type === 'income' ? '+' : '-'}${tr.amount.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                     </div>
                     <div className="w-[15%] flex items-center gap-2 text-[#0F172A] justify-end">
                        {tr.status} <span className="w-1.5 h-1.5 rounded-full bg-[#B71C1C]"></span>
                     </div>
                     <div className="w-[20%] text-gray-500 dark:text-gray-400">
                        {tr.date}
                     </div>
                     <div className="w-[15%]">
                        <span className={`px-3 py-1.5 rounded-lg text-xs font-bold ${
                           tr.category === 'إيرادات' ? 'bg-red-50 text-[#B71C1C]' :
                           tr.category === 'إمدادات الأعلاف' ? 'bg-blue-50 text-blue-600' : 'bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-gray-300'
                        }`}>
                           {tr.category}
                        </span>
                     </div>
                     <div className="w-[35%] flex justify-end items-center gap-4">
                        <button onClick={() => handleDeleteTransaction(tr.id)} className="text-gray-400 hover:text-red-500 transition-colors p-2 rounded-full hover:bg-red-50">
                           <Trash2 size={16} />
                        </button>
                        <div className="text-right">
                           <div className="text-[#0F172A] text-[15px]">{tr.entity}</div>
                           <div className="text-gray-400 text-xs mt-0.5">{tr.subEntity}</div>
                        </div>
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                           tr.type === 'income' ? 'bg-blue-50 text-blue-600' :
                           tr.category === 'إمدادات الأعلاف' ? 'bg-red-50 text-[#B71C1C]' : 'bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-gray-300'
                        }`}>
                           {tr.type === 'income' ? <Tag size={16} /> : <ShoppingCart size={16} />}
                        </div>
                     </div>
                  </div>
               ))}
            </div>
         </div>
         <div className="text-center mt-6">
            <button className="text-[#B71C1C] font-bold text-sm">عرض جميع السجلات ↓</button>
         </div>
      </div>
    </div>

      {/* Modals */}
      {showTransactionModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm">
          <div className="bg-white dark:bg-slate-800 rounded-3xl p-8 w-[400px] shadow-2xl">
            <div className="flex justify-between items-center mb-6 flex-row-reverse">
              <h3 className="text-xl font-extrabold text-[#0F172A]">إضافة معاملة جديدة</h3>
              <button onClick={() => setShowTransactionModal(false)} className="text-gray-400 hover:text-gray-700 dark:text-gray-200">
                <X size={24} />
              </button>
            </div>
            <div className="mb-4 text-right">
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-200 mb-2">نوع المعاملة</label>
                     <select value={transactionType} onChange={(event) => setTransactionType(event.target.value)} className="w-full border border-gray-200 dark:border-slate-700 rounded-xl p-4 text-right focus:border-[#B71C1C] focus:outline-none bg-white dark:bg-slate-800">
                        <option value="income">إيرادات</option>
                        <option value="expense">مصروفات</option>
              </select>
            </div>
            <div className="mb-4 text-right">
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-200 mb-2">الفئة</label>
                     <select value={transactionCategory} onChange={(event) => setTransactionCategory(event.target.value)} className="w-full border border-gray-200 dark:border-slate-700 rounded-xl p-4 text-right focus:border-[#B71C1C] focus:outline-none bg-white dark:bg-slate-800">
                        {transactionType === 'income' ? (
                           <>
                              <option value="إيرادات مبيعات">إيرادات مبيعات</option>
                              <option value="مبيعات بيض">مبيعات بيض</option>
                              <option value="إيرادات أخرى">إيرادات أخرى</option>
                           </>
                        ) : (
                           <>
                              <option value="إمدادات الأعلاف">إمدادات الأعلاف</option>
                              <option value="الكتاكيت الأساسية">الكتاكيت الأساسية</option>
                              <option value="الأدوية واللقاحات">الأدوية واللقاحات</option>
                              <option value="الخدمات اللوجستية">الخدمات اللوجستية</option>
                              <option value="الصيانة">الصيانة</option>
                           </>
                        )}
              </select>
            </div>
            <div className="mb-6 text-right">
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-200 mb-2">المبلغ</label>
                     <input
                type="number" 
                        value={transactionAmount}
                        onChange={(event) => setTransactionAmount(event.target.value)}
                className="w-full border border-gray-200 dark:border-slate-700 rounded-xl p-4 text-right focus:border-[#B71C1C] focus:outline-none"
                placeholder="أدخل المبلغ..."
              />
            </div>
                  <button onClick={handleTransactionSubmit} className="w-full bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-4 rounded-xl transition-colors">
              حفظ المعاملة
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
            <h3 className="text-xl font-extrabold text-[#0F172A] mb-2">تصدير التقرير المالي</h3>
            <p className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-6">سيتم تجهيز التقرير المالي بصيغة PDF لقطيعك الحالي وتنزيله على جهازك.</p>
            <div className="flex gap-3">
              <button onClick={() => setShowExportModal(false)} className="flex-1 bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-200 font-bold py-3.5 rounded-xl transition-colors text-sm">
                إلغاء
              </button>
              <button onClick={() => {
                toast.success("جاري تجهيز وتنزيل التقرير...");
                setShowExportModal(false);
              }} className="flex-1 bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-3.5 rounded-xl transition-colors text-sm">
                تأكيد التنزيل
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
