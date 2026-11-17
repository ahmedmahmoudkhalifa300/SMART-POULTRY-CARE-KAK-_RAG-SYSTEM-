import { useState, useRef } from 'react';
import toast from 'react-hot-toast';
import { Upload, X, CheckCircle, AlertTriangle, Share2, Download, UploadCloud, User } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Diagnostics() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  
  const [showReportModal, setShowReportModal] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);
  const fileInputRef = useRef(null);
  
  const navigate = useNavigate();
  
  // States for Additional Symptoms Card
  const [selectedAdditionalSymptoms, setSelectedAdditionalSymptoms] = useState([]);
  
  // States for Follow-up Symptoms Card
  const [followUpSymptoms, setFollowUpSymptoms] = useState([]);
  const [followUpNotes, setFollowUpNotes] = useState('');

  const toggleAdditionalSymptom = (symptom) => {
    setSelectedAdditionalSymptoms(prev => 
      prev.includes(symptom) ? prev.filter(s => s !== symptom) : [...prev, symptom]
    );
  };

  const handleUpdateDiagnosis = () => {
    if (selectedAdditionalSymptoms.length > 0) {
      navigate('/assistant', { state: { symptoms: selectedAdditionalSymptoms, source: 'diagnostics_additional' } });
    } else {
      toast.error('يرجى اختيار عرض واحد على الأقل');
    }
  };

  const toggleFollowUpSymptom = (symptom) => {
    setFollowUpSymptoms(prev => 
      prev.includes(symptom) ? prev.filter(s => s !== symptom) : [...prev, symptom]
    );
  };

  const handleFollowUpSubmit = () => {
    if (followUpSymptoms.length > 0 || followUpNotes.trim() !== '') {
      navigate('/assistant', { state: { symptoms: followUpSymptoms, notes: followUpNotes, source: 'diagnostics_followup' } });
    } else {
      toast.error('يرجى اختيار أعراض أو كتابة ملاحظات أولاً');
    }
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setLoading(true);

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://localhost:8000/predict', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();
        setResult({
          predicted_disease: data.predicted_disease || 'غير معروف',
          confidence_score: data.confidence_score ? (data.confidence_score * 100).toFixed(1) : '0.0'
        });
      } catch (error) {
        console.error("Error predicting:", error);
        toast.error("فشل في الاتصال بالخادم. يرجى التأكد من تشغيل الباك إند.");
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="flex gap-8 h-full items-start max-w-[1200px] mx-auto w-full pb-8">
      {/* Right Column: Upload & Symptoms */}
      <div className="flex-1 flex flex-col gap-6">
        <div className="mb-2 text-right">
           <div className="flex items-center justify-end relative w-full mb-10">
              <div className="w-full h-10 border border-gray-200 dark:border-slate-700 rounded-full flex items-center bg-gray-50 dark:bg-slate-900 px-4">
                 <SearchIcon />
                 <span className="text-gray-400 text-sm mr-2">ابحث في سجل التشخيصات...</span>
              </div>
           </div>
           
           <h1 className="text-4xl font-extrabold text-[#0F172A] mb-4 text-center">تشخيص أمراض الدواجن</h1>
           <p className="text-gray-500 dark:text-gray-400 text-center mb-10">يرجى تحميل صورة للفضلات للحصول على تحليل دقيق.</p>
        </div>

        {/* Upload Box */}
        <div 
           className="bg-white dark:bg-slate-800 rounded-3xl border border-gray-200 dark:border-slate-700 flex flex-col items-center justify-center py-16 px-6 cursor-pointer hover:bg-gray-50 dark:bg-slate-900 transition relative shadow-sm"
           onClick={() => fileInputRef.current?.click()}
        >
          <div className="absolute inset-4 border-2 border-dashed border-gray-200 dark:border-slate-700 rounded-2xl pointer-events-none"></div>
          <input type="file" accept="image/*" className="hidden" ref={fileInputRef} onChange={handleFileChange} />
          
          {loading ? (
             <div className="flex flex-col items-center z-10">
                <div className="w-12 h-12 border-4 border-[#B71C1C] border-t-transparent rounded-full animate-spin mb-4"></div>
                <h3 className="text-xl font-bold text-[#0F172A]">جاري التحليل...</h3>
             </div>
          ) : preview ? (
             <div className="flex flex-col items-center z-10">
                <img src={preview} alt="Preview" className="w-48 h-48 object-cover rounded-2xl mb-4 border-4 border-white shadow-sm" />
                <button className="bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-200 px-8 py-2.5 rounded-full font-bold shadow-sm hover:bg-gray-300" onClick={() => fileInputRef.current?.click()}>
                   تغيير الصورة
                </button>
             </div>
          ) : (
             <>
               <div className="w-16 h-16 bg-[#FEF2F2] text-[#B71C1C] rounded-full flex items-center justify-center mb-6 z-10">
                  <UploadCloud size={32} />
               </div>
               <h3 className="text-xl font-bold text-[#0F172A] mb-3 z-10">من فضلك قم بتحميل صورة للفضلات.</h3>
               <p className="text-gray-500 dark:text-gray-400 text-center mb-6 max-w-sm text-sm leading-relaxed z-10">
                  الذكاء الاصطناعي يتعرف بتشخيص أحسن لو الصور واضحة ومن كذا زاوية.
               </p>
               <button className="bg-[#B71C1C] text-white px-8 py-2.5 rounded-full font-bold z-10 shadow-sm" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>
                  اختار الملفات
               </button>
             </>
          )}
        </div>

        {/* Symptoms Form (محتاجين معلومات أكتر) */}
        <div className="bg-[#FEF2F2] rounded-3xl p-8 border border-red-100 shadow-sm text-right mt-4">
          <div className="flex items-center justify-end gap-2 text-[#B71C1C] font-bold text-xl mb-3">
            محتاجين معلومات أكتر <AlertTriangle size={24} />
          </div>
          <p className="text-gray-600 dark:text-gray-300 text-sm mb-8 leading-relaxed font-medium">
             درجة التأكد من الصورة منخفضة. من فضلك دخل الأعراض اللي شايفها يدوياً عشان نساعدك أحسن.
          </p>
          
          <h4 className="font-bold text-[#0F172A] mb-4 text-xs">أعراض إضافية لاحظتها؟</h4>
          <div className="grid grid-cols-2 gap-4 mb-8">
             {['تنفس صعب', 'إفرازات من الأنف', 'هزة في الرأس', 'انخفاض إنتاج البيض', 'عطش شديد'].map((symptom, idx) => (
               <label key={idx} className="flex items-center justify-end gap-3 bg-white dark:bg-slate-800 py-3 px-4 rounded-xl border border-gray-200 dark:border-slate-700 cursor-pointer shadow-sm text-sm font-medium text-gray-700 dark:text-gray-200">
                  <span>{symptom}</span>
                  <input 
                     type="checkbox" 
                     className="w-4 h-4 accent-[#B71C1C]" 
                     checked={selectedAdditionalSymptoms.includes(symptom)}
                     onChange={() => toggleAdditionalSymptom(symptom)}
                  />
               </label>
             ))}
          </div>
          <button 
            onClick={handleUpdateDiagnosis}
            className="bg-[#B71C1C] hover:bg-[#991616] text-white font-bold w-full py-4 rounded-xl shadow-sm transition-colors text-sm"
          >
            تحديث التشخيص بالأعراض
          </button>
        </div>

        {/* Symptoms Tracker */}
        <div className="bg-white dark:bg-slate-800 rounded-3xl p-8 border border-gray-200 dark:border-slate-700 shadow-sm text-right mt-4">
          <div className="flex items-center justify-end gap-3 font-bold text-xl text-[#0F172A] mb-6">
            متابعة الأعراض
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#B71C1C" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          </div>
          <div className="mb-6">
            <h4 className="font-bold text-xs text-gray-700 dark:text-gray-200 mb-4">اختار الأعراض اللي شايفها</h4>
            <div className="flex flex-wrap justify-end gap-3">
               {['إسهال', 'خمول', 'تدلي متقدم', 'ورم في العين', 'ريش منكوش', 'فقدان شهية'].map(tag => (
                  <button 
                     key={tag}
                     onClick={() => toggleFollowUpSymptom(tag)}
                     className={`px-5 py-2.5 rounded-full text-xs font-bold border cursor-pointer transition-colors ${
                        followUpSymptoms.includes(tag) 
                        ? 'bg-[#B71C1C] text-white border-[#B71C1C]' 
                        : 'bg-white dark:bg-slate-800 text-gray-500 dark:text-gray-400 border-gray-200 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-700'
                     }`}
                  >
                    {tag}
                  </button>
               ))}
            </div>
          </div>
          <div>
            <h4 className="font-bold text-xs text-gray-700 dark:text-gray-200 mb-3">ملاحظات تانية؟</h4>
            <textarea 
               value={followUpNotes}
               onChange={(e) => setFollowUpNotes(e.target.value)}
               className="w-full bg-[#F9FAFB] border border-gray-200 dark:border-slate-700 rounded-xl p-5 text-sm focus:outline-none focus:border-[#B71C1C] min-h-[120px]" 
               rows="3" 
               placeholder="لو فيه أي حاجة تانية غريبة لاحظتها اكتبها هنا..."
            ></textarea>
          </div>
          <div className="mt-6">
            <button 
              onClick={handleFollowUpSubmit}
              className="bg-[#0F172A] hover:bg-black text-white font-bold w-full py-4 rounded-xl shadow-sm transition-colors text-sm"
            >
              إرسال الأعراض للمساعد الذكي
            </button>
          </div>
        </div>
      </div>

      {/* Left Column: Results & Widgets */}
      <div className="w-[340px] flex flex-col gap-6 mt-[92px]">
        
        {/* Result Card */}
        {result && (() => {
           const isHealthy = result.predicted_disease === 'Healthy';
           const bgMain = isHealthy ? 'bg-green-600' : 'bg-[#B71C1C]';
           const textMain = isHealthy ? 'text-green-600' : 'text-[#B71C1C]';
           const borderMain = isHealthy ? 'border-green-600' : 'border-[#B71C1C]';
           const bgLight = isHealthy ? 'bg-green-50' : 'bg-[#FEF2F2]';

           return (
           <div className={`bg-white dark:bg-slate-800 rounded-3xl overflow-hidden shadow-sm border ${borderMain}`}>
              <div className={`${bgMain} text-white p-4 flex justify-between items-center font-bold`}>
                 <div dir="ltr" className="text-sm">الدقة: {result.confidence_score}%</div>
                 <div className="flex items-center gap-2 text-sm">
                   تم التشخيص بنجاح <CheckCircle size={18}/>
                 </div>
              </div>
              
              <div className="p-6 pb-8 text-right">
                 <div className="flex justify-between items-start mb-6 flex-row-reverse">
                    <div className="text-right flex-1">
                       <p className="text-[10px] text-gray-500 dark:text-gray-400 mb-1 font-bold">التشخيص المحتمل..</p>
                       <h2 className={`text-3xl font-extrabold ${textMain} mb-1`}>{isHealthy ? 'سليم' : result.predicted_disease === 'Coccidiosis' ? 'كوكسيديا' : result.predicted_disease === 'Salmonella' ? 'سالمونيلا' : result.predicted_disease === 'New Castle Disease' ? 'نيوكاسل' : result.predicted_disease}</h2>
                       <h3 className={`text-lg font-bold ${textMain}`}>({result.predicted_disease})</h3>
                    </div>
                    <div className="w-16 h-16 rounded-full border-4 border-gray-100 dark:border-slate-700 overflow-hidden ml-4">
                       {preview ? (
                          <img src={preview} alt="Dropping" className="w-full h-full object-cover" />
                       ) : (
                          <img src="https://images.unsplash.com/photo-1590424744257-f827be95bb49?w=100&q=80" alt="Dropping" className="w-full h-full object-cover" />
                       )}
                    </div>
                 </div>

                 <div className={`${bgLight} p-5 rounded-2xl mb-4 text-right`}>
                    <h4 className={`font-bold ${textMain} mb-2 text-sm`}>{isHealthy ? 'الرعاية الموصى بها..' : 'العلاج الموصى به..'}</h4>
                    <p className="text-xs text-gray-700 dark:text-gray-200 leading-relaxed font-bold">
                      {isHealthy ? 'طيرك سليم وبصحة جيدة! استمر في تقديم العلف والمياه النظيفة مع الحفاظ على التهوية الجيدة.' : 'استخدم "أمپروليوم" في مياه الشرب فوراً للقطيع بأكمله. واعزل الطيور المصابة بشدة بمفردها.'}
                    </p>
                 </div>

                 {!isHealthy && (
                 <div className="flex gap-3 mb-8">
                    <div className="bg-gray-50 dark:bg-slate-900 p-3 rounded-2xl flex-1 text-center">
                       <div className="text-[10px] text-gray-500 dark:text-gray-400 mb-1 font-bold">المدة</div>
                       <div className="font-bold text-xs text-[#0F172A]">5 - 7 أيام متتالية</div>
                    </div>
                    <div className="bg-gray-50 dark:bg-slate-900 p-3 rounded-2xl flex-1 text-center">
                       <div className="text-[10px] text-gray-500 dark:text-gray-400 mb-1 font-bold">الجرعة</div>
                       <div className="font-bold text-xs text-[#0F172A] leading-tight">تركيز 9.6% - 1 سم<br/>لكل لتر ماء</div>
                    </div>
                 </div>
                 )}

                 <div className={`mb-8 border-t border-gray-100 dark:border-slate-700 pt-6 ${isHealthy ? 'mt-8' : ''}`}>
                    <h4 className="font-bold text-xs mb-4 text-[#0F172A]">كيف تحمي قطيعك مستقبلاً؟</h4>
                    <ul className="text-xs text-gray-600 dark:text-gray-300 flex flex-col gap-4 font-bold">
                       <li className="flex items-start justify-end gap-2">
                          <span>حافظ على جفاف ونظافة الفرشة</span>
                          <CheckCircle size={14} className={`${textMain} mt-0.5 shrink-0`}/> 
                       </li>
                       <li className="flex items-start justify-end gap-2">
                          <span>تجنب الازدحام الزائد في العنبر</span>
                          <CheckCircle size={14} className={`${textMain} mt-0.5 shrink-0`}/> 
                       </li>
                    </ul>
                 </div>

                 <div className="flex gap-3 mt-4 border-t border-gray-100 dark:border-slate-700 pt-6">
                    <button onClick={() => setShowShareModal(true)} className="p-3 border border-gray-200 dark:border-slate-700 rounded-xl text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:bg-slate-900 shadow-sm flex items-center justify-center">
                       <Share2 size={20}/>
                    </button>
                    <button onClick={() => setShowReportModal(true)} className={`${bgMain} hover:opacity-90 text-white font-bold flex-1 py-3.5 rounded-xl shadow-sm transition-colors text-sm`}>
                       تحميل تقرير الحالة
                    </button>
                 </div>
              </div>
           </div>
           );
        })()}

        {/* Quote Widget */}
        <div className="bg-[#F3E8E8] rounded-3xl p-8 relative overflow-hidden text-center shadow-sm">
           <h3 className="text-2xl font-bold text-[#B71C1C] mb-4 leading-snug">"أنا عيني على<br/>مزرعتك!"</h3>
           <p className="text-sm text-gray-600 dark:text-gray-300 italic font-medium leading-relaxed mb-12">
             "هذه الحالة تتطلب اهتماماً فورياً ولكنها قابلة للعلاج. تأكد من ضبط مستويات الرطوبة، فالبيئة الرطبة هي المحفز الأول لهذا المرض."
           </p>
           
           {/* Custom App Logo block - mimicking the VITALHEN block but with KAK */}
           <div className="absolute bottom-6 right-6 left-6 bg-white dark:bg-slate-800 py-3 rounded-2xl shadow-sm flex flex-col items-center justify-center">
              <div className="text-[#B71C1C] flex flex-col items-center gap-1">
                 <div className="w-8 h-8 rounded-full border-2 border-[#B71C1C] flex items-center justify-center font-black">
                   K
                 </div>
                 <span className="font-bold text-[10px] tracking-widest">KAK AI</span>
              </div>
           </div>
        </div>

        {/* Team Widget */}
        <div className="bg-gray-200 dark:bg-slate-700 rounded-3xl p-6 shadow-sm">
           <div className="flex justify-between items-center mb-6">
              <span className="bg-green-600 text-white text-[10px] px-3 py-1 rounded-full font-bold">فريق الخبراء</span>
              <h3 className="font-bold text-lg text-[#0F172A]">فريقنا</h3>
           </div>
           
           <div className="flex flex-col gap-3">
             <div className="bg-white dark:bg-slate-800 p-3 rounded-2xl flex items-center justify-between border border-gray-100 dark:border-slate-700 shadow-sm">
                <button className="bg-[#B71C1C] text-white text-xs font-bold px-4 py-1.5 rounded-lg">تواصل</button>
                <div className="flex items-center gap-3">
                   <div className="text-right">
                      <div className="font-bold text-sm text-[#0F172A]">د. سارة محمود</div>
                      <div className="text-[10px] text-[#B71C1C] font-bold">استشارية أمراض دواجن</div>
                   </div>
                   <div className="w-10 h-10 rounded-full bg-gray-100 dark:bg-slate-700 flex items-center justify-center text-gray-400 border border-gray-200 dark:border-slate-700 overflow-hidden">
                     <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&q=80" alt="Sarah" className="w-full h-full object-cover" />
                   </div>
                </div>
             </div>
             <div className="bg-white dark:bg-slate-800 p-3 rounded-2xl flex items-center justify-between border border-gray-100 dark:border-slate-700 shadow-sm">
                <button className="bg-[#B71C1C] text-white text-xs font-bold px-4 py-1.5 rounded-lg">تواصل</button>
                <div className="flex items-center gap-3">
                   <div className="text-right">
                      <div className="font-bold text-sm text-[#0F172A]">م. أحمد علي</div>
                      <div className="text-[10px] text-[#B71C1C] font-bold">خبير نظم الإنتاج الداجني</div>
                   </div>
                   <div className="w-10 h-10 rounded-full bg-gray-100 dark:bg-slate-700 flex items-center justify-center text-gray-400 border border-gray-200 dark:border-slate-700 overflow-hidden">
                     <img src="https://images.unsplash.com/photo-1560250097-0b93528c311a?w=100&q=80" alt="Ahmed" className="w-full h-full object-cover" />
                   </div>
                </div>
             </div>
           </div>
        </div>

      </div>

      {/* Modals */}
      {showReportModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm">
          <div className="bg-white dark:bg-slate-800 rounded-3xl p-8 w-[400px] shadow-2xl text-center">
            <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4 text-[#B71C1C]">
               <Download size={32} />
            </div>
            <h3 className="text-xl font-extrabold text-[#0F172A] mb-2">تحميل تقرير الحالة</h3>
            <p className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-6">سيتم إنشاء وتنزيل تقرير مفصل عن الحالة وبروتوكول العلاج بصيغة PDF.</p>
            <div className="flex gap-3">
              <button onClick={() => setShowReportModal(false)} className="flex-1 bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-200 font-bold py-3.5 rounded-xl transition-colors text-sm">
                إلغاء
              </button>
              <button onClick={() => {
                toast.success("جاري إنشاء التقرير والتنزيل...");
                setShowReportModal(false);
              }} className="flex-1 bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-3.5 rounded-xl transition-colors text-sm">
                تنزيل التقرير
              </button>
            </div>
          </div>
        </div>
      )}

      {showShareModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm">
          <div className="bg-white dark:bg-slate-800 rounded-3xl p-8 w-[400px] shadow-2xl text-center">
            <div className="w-16 h-16 bg-gray-50 dark:bg-slate-900 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-600 dark:text-gray-300">
               <Share2 size={32} />
            </div>
            <h3 className="text-xl font-extrabold text-[#0F172A] mb-2">مشاركة التشخيص</h3>
            <p className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-6">شارك نتيجة التشخيص وخطة العلاج مع الطبيب البيطري أو فريقك.</p>
            <div className="flex flex-col gap-3">
              <button onClick={() => {
                toast.success("تم نسخ الرابط!");
                setShowShareModal(false);
              }} className="w-full bg-[#0F172A] hover:bg-black text-white font-bold py-3.5 rounded-xl transition-colors text-sm">
                نسخ الرابط
              </button>
              <button onClick={() => setShowShareModal(false)} className="w-full bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-200 font-bold py-3.5 rounded-xl transition-colors text-sm">
                إغلاق
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

function SearchIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
  );
}
