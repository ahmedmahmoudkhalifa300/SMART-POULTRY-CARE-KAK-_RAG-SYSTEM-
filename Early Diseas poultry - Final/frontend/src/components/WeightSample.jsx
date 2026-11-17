import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { Weight, Plus, Trash2, TrendingUp } from 'lucide-react';

export default function WeightSample({ cycleAge, onWeightDataChange }) {
  const [samples, setSamples] = useState(() => {
    const saved = localStorage.getItem('weightSamples');
    return saved ? JSON.parse(saved) : [];
  });
  
  const [sampleCount, setSampleCount] = useState('');
  const [sampleWeight, setSampleWeight] = useState('');
  const [showForm, setShowForm] = useState(false);

  // حفظ العينات في localStorage عند التغيير
  useEffect(() => {
    localStorage.setItem('weightSamples', JSON.stringify(samples));
    calculateActualWeight();
  }, [samples]);

  // المعادلة القياسية: W(t) = 9.51 * t^1.567
  const standardWeight = cycleAge > 0 ? (9.51 * Math.pow(cycleAge, 1.567)).toFixed(2) : 0;

  // حساب متوسط الوزن الفعلي
  const calculateActualWeight = () => {
    if (samples.length === 0) {
      onWeightDataChange?.({ actualWeight: 0, standardWeight, variance: 0 });
      return;
    }

    const totalWeight = samples.reduce((sum, s) => sum + s.weight, 0);
    const totalCount = samples.reduce((sum, s) => sum + s.count, 0);
    const actualWeight = totalCount > 0 ? (totalWeight / totalCount).toFixed(2) : 0;
    const variance = ((actualWeight - standardWeight) / standardWeight * 100).toFixed(1);

    onWeightDataChange?.({ 
      actualWeight: parseFloat(actualWeight), 
      standardWeight: parseFloat(standardWeight), 
      variance: parseFloat(variance),
      sampleCount: totalCount 
    });
  };

  // إضافة عينة وزن جديدة
  const addSample = () => {
    if (!sampleCount || !sampleWeight || sampleCount <= 0 || sampleWeight <= 0) {
      toast.error('الرجاء إدخال أرقام صحيحة');
      return;
    }

    const newSample = {
      id: Date.now(),
      count: parseInt(sampleCount),
      weight: parseFloat(sampleWeight),
    };

    setSamples([...samples, newSample]);
    setSampleCount('');
    setSampleWeight('');
    setShowForm(false);
  };

  // حذف عينة
  const removeSample = (id) => {
    setSamples(samples.filter(s => s.id !== id));
  };

  // حساب إجمالي الفراخ والوزن
  const totalCount = samples.reduce((sum, s) => sum + s.count, 0);
  const totalWeight = samples.reduce((sum, s) => sum + s.weight, 0);
  const actualWeight = totalCount > 0 ? (totalWeight / totalCount).toFixed(2) : 0;
  const variance = standardWeight > 0 ? ((actualWeight - standardWeight) / standardWeight * 100).toFixed(1) : 0;

  // تحديد اللون بناءً على الفرق
  const getStatusColor = () => {
    if (totalCount === 0) return 'text-gray-400';
    const varNum = parseFloat(variance);
    if (varNum >= -5 && varNum <= 5) return 'text-green-600';
    if (varNum > 5 && varNum <= 15) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getStatusBg = () => {
    if (totalCount === 0) return 'bg-gray-50';
    const varNum = parseFloat(variance);
    if (varNum >= -5 && varNum <= 5) return 'bg-green-50';
    if (varNum > 5 && varNum <= 15) return 'bg-yellow-50';
    return 'bg-red-50';
  };

  const getStatusText = () => {
    if (totalCount === 0) return 'بانتظار البيانات';
    const varNum = parseFloat(variance);
    if (varNum >= -5 && varNum <= 5) return '✓ ممتاز - الوزن مطابق';
    if (varNum > 5 && varNum <= 15) return '⚠ تحذير - وزن أعلى من المتوقع';
    return '✗ حرج - وزن أقل من المتوقع';
  };

  return (
    <div className="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-3xl p-8 shadow-sm">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-[#B71C1C] hover:bg-[#991616] text-white font-bold px-4 py-2 rounded-xl flex items-center gap-2 transition-colors text-sm"
        >
          <Plus size={16} />
          <span>إضافة عينة وزن</span>
        </button>
        <div className="flex items-center gap-3">
          <Weight size={24} className="text-indigo-600" />
          <h3 className="font-bold text-lg text-[#0F172A]">عينة الوزن</h3>
        </div>
      </div>

      {/* Form to Add Sample */}
      {showForm && (
        <div className="bg-blue-50 dark:bg-slate-900 border border-blue-100 dark:border-slate-700 rounded-xl p-6 mb-6">
          <div className="flex gap-4 mb-4">
            <div className="flex-1">
              <label className="block text-sm font-bold text-[#0F172A] mb-2">عدد الفراخ</label>
              <input
                type="number"
                value={sampleCount}
                onChange={(e) => setSampleCount(e.target.value)}
                placeholder="مثلاً: 10"
                className="w-full border border-gray-200 dark:border-slate-700 rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-[#B71C1C]"
              />
            </div>
            <div className="flex-1">
              <label className="block text-sm font-bold text-[#0F172A] mb-2">الوزن الإجمالي (جرام)</label>
              <input
                type="number"
                value={sampleWeight}
                onChange={(e) => setSampleWeight(e.target.value)}
                placeholder="مثلاً: 180"
                className="w-full border border-gray-200 dark:border-slate-700 rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-[#B71C1C]"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={addSample}
              className="flex-1 bg-[#B71C1C] hover:bg-[#991616] text-white font-bold py-2 rounded-lg transition-colors"
            >
              حفظ
            </button>
            <button
              onClick={() => setShowForm(false)}
              className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 font-bold py-2 rounded-lg transition-colors"
            >
              إلغاء
            </button>
          </div>
        </div>
      )}

      {/* Samples List */}
      {samples.length > 0 && (
        <div className="mb-6 border-b border-gray-100 dark:border-slate-700 pb-6">
          <div className="grid gap-3">
            {samples.map((sample) => (
              <div key={sample.id} className="flex justify-between items-center bg-gray-50 dark:bg-slate-900 p-4 rounded-lg">
                <button
                  onClick={() => removeSample(sample.id)}
                  className="text-red-600 hover:text-red-700 transition-colors"
                >
                  <Trash2 size={18} />
                </button>
                <div className="text-center flex-1">
                  <div className="text-sm text-gray-500 dark:text-gray-400">متوسط الوزن</div>
                  <div className="font-bold text-[#0F172A]">{(sample.weight / sample.count).toFixed(2)} جم</div>
                </div>
                <div className="text-center flex-1">
                  <div className="text-sm text-gray-500 dark:text-gray-400">الوزن الإجمالي</div>
                  <div className="font-bold text-[#0F172A]">{sample.weight} جم</div>
                </div>
                <div className="text-center flex-1">
                  <div className="text-sm text-gray-500 dark:text-gray-400">عدد الفراخ</div>
                  <div className="font-bold text-[#0F172A]">{sample.count}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Summary Card */}
      <div className={`${getStatusBg()} border border-gray-200 dark:border-slate-700 rounded-2xl p-6`}>
        <div className="grid grid-cols-4 gap-4 mb-6">
          {/* Actual Weight */}
          <div className="text-center">
            <div className="text-xs text-gray-600 dark:text-gray-400 font-bold mb-1">الوزن الفعلي</div>
            <div className="text-2xl font-extrabold text-[#0F172A]">
              {totalCount > 0 ? actualWeight : '0.00'}
              <span className="text-sm font-bold text-gray-500"> جم</span>
            </div>
            <div className="text-[10px] text-gray-500 dark:text-gray-400 font-bold mt-1">
              من {totalCount} فرخة
            </div>
          </div>

          {/* Standard Weight */}
          <div className="text-center">
            <div className="text-xs text-gray-600 dark:text-gray-400 font-bold mb-1">الوزن القياسي</div>
            <div className="text-2xl font-extrabold text-[#0F172A]">
              {standardWeight}
              <span className="text-sm font-bold text-gray-500"> جم</span>
            </div>
            <div className="text-[10px] text-gray-500 dark:text-gray-400 font-bold mt-1">
              اليوم {cycleAge}
            </div>
          </div>

          {/* Difference */}
          <div className="text-center">
            <div className="text-xs text-gray-600 dark:text-gray-400 font-bold mb-1">الفرق</div>
            <div className={`text-2xl font-extrabold ${getStatusColor()}`}>
              {totalCount > 0 ? (actualWeight - standardWeight).toFixed(2) : '0.00'}
              <span className="text-sm font-bold"> جم</span>
            </div>
            <div className="text-[10px] text-gray-500 dark:text-gray-400 font-bold mt-1">
              {totalCount > 0 ? variance : '0'}%
            </div>
          </div>

          {/* Status */}
          <div className="flex flex-col items-center justify-center">
            <TrendingUp size={24} className={getStatusColor()} />
            <div className={`text-xs font-bold mt-2 text-center ${getStatusColor()}`}>
              {getStatusText()}
            </div>
          </div>
        </div>

        {/* Alert Message */}
        {totalCount > 0 && (
          <div className="text-sm text-center font-medium text-gray-700 dark:text-gray-200">
            {variance > 5 && variance <= 15 && '⚠️ الفراخ أثقل قليلاً من المتوقع - قد تكون التغذية جيدة جداً'}
            {variance > 15 && '❌ الفراخ أخف من المتوقع - تحتاج لمتابعة التغذية والصحة'}
            {variance >= -5 && variance <= 5 && '✓ الفراخ تتطور بشكل طبيعي وممتاز'}
            {variance < -5 && '⚠️ الفراخ أخف قليلاً من المتوقع - راقب الأداء'}
          </div>
        )}
      </div>
    </div>
  );
}
