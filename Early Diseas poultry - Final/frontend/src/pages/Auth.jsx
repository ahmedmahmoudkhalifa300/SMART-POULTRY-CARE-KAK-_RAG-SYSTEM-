import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Auth() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Check if already logged in
  useEffect(() => {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
       // Check if they already have a flock
       const flockId = localStorage.getItem('currentFlockId');
       if (flockId) {
          navigate('/dashboard', { replace: true });
       } else {
          navigate('/select-production', { replace: true });
       }
    }
  }, [navigate]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const users = JSON.parse(localStorage.getItem('registeredUsers')) || [];

    if (!isLogin) {
      // Signup Logic
      if (password !== confirmPassword) {
        setError('كلمات المرور غير متطابقة!');
        return;
      }
      
      const userExists = users.find(u => u.email === email);
      if (userExists) {
        setError('هذا البريد الإلكتروني مسجل بالفعل!');
        return;
      }

      const newUser = { fullName, email, password };
      users.push(newUser);
      localStorage.setItem('registeredUsers', JSON.stringify(users));
      
      setSuccess('تم إنشاء الحساب بنجاح! يرجى تسجيل الدخول.');
      setIsLogin(true);
      setPassword('');
      setConfirmPassword('');
    } else {
      // Login Logic
      const user = users.find(u => u.email === email && u.password === password);
      
      if (!user) {
        setError('البريد الإلكتروني أو كلمة المرور غير صحيحة!');
        return;
      }

      // Successful Login
      localStorage.setItem('currentUser', JSON.stringify(user));
      
      // Restore user's specific appData if it exists
      if (user.appData) {
          Object.keys(user.appData).forEach(key => {
              if (user.appData[key] !== null && user.appData[key] !== undefined) {
                  localStorage.setItem(key, user.appData[key]);
              }
          });
      }

      const flockId = localStorage.getItem('currentFlockId');
      if (flockId) {
         navigate('/dashboard');
      } else {
         navigate('/select-production');
      }
    }
  };

  return (
    <div className="flex min-h-screen bg-[#F9FAFB] items-center justify-center p-4" dir="rtl">
      {/* Center - Form */}
      <div className="w-full max-w-md bg-white dark:bg-slate-800 p-10 md:p-12 shadow-sm border border-gray-100 dark:border-slate-700 rounded-3xl">
        <div className="text-right mb-8 text-center">
          <div className="font-bold text-3xl flex items-center justify-center bg-[#B71C1C] text-white rounded-lg p-2 px-3 w-16 mx-auto mb-6">
            KAK
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-[#0F172A] mb-3">
            {isLogin ? 'تسجيل الدخول إلى حسابك' : 'أنشئ حساب KAK الخاص بك'}
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm">
            {isLogin ? 'مرحباً بعودتك إلى KAK لإدارة الدواجن بذكاء.' : 'ابدأ في إدارة أصول الدواجن بذكاء أكبر اليوم.'}
          </p>
        </div>

        {error && <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm font-bold text-center mb-4">{error}</div>}
        {success && <div className="bg-green-50 text-green-600 p-3 rounded-lg text-sm font-bold text-center mb-4">{success}</div>}

        <form onSubmit={handleSubmit} className="flex flex-col gap-5 text-right">
          {!isLogin && (
            <div>
              <label className="block text-sm font-bold text-[#0F172A] mb-2">الاسم بالكامل *</label>
              <div className="relative">
                 <input 
                    type="text" 
                    placeholder="مثال: محمد أحمد" 
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="w-full p-3 border border-gray-200 dark:border-slate-700 rounded-lg text-[#0F172A] bg-white dark:bg-slate-800 focus:outline-none focus:border-[#B71C1C]" 
                    required 
                 />
              </div>
              <p className="text-[#B71C1C] text-xs mt-2">سيتم استخدام اسمك للترحيب بك في لوحة التحكم الخاصة بك.</p>
            </div>
          )}

          <div>
            <label className="block text-sm font-bold text-[#0F172A] mb-2">البريد الإلكتروني</label>
            <input 
               type="email" 
               placeholder="john@farm-tech.com" 
               value={email}
               onChange={(e) => setEmail(e.target.value)}
               className="w-full p-3 border border-gray-200 dark:border-slate-700 rounded-lg text-left" 
               dir="ltr" 
               required 
            />
          </div>

          <div className={isLogin ? "" : "flex gap-4"}>
            <div className={isLogin ? "w-full" : "w-1/2"}>
              <label className="block text-sm font-bold text-[#0F172A] mb-2">كلمة المرور</label>
              <input 
                 type="password" 
                 placeholder="••••••••" 
                 value={password}
                 onChange={(e) => setPassword(e.target.value)}
                 className="w-full p-3 border border-gray-200 dark:border-slate-700 rounded-lg text-left" 
                 dir="ltr" 
                 required 
              />
            </div>
            {!isLogin && (
              <div className="w-1/2">
                <label className="block text-sm font-bold text-[#0F172A] mb-2">تأكيد كلمة المرور</label>
                <input 
                   type="password" 
                   placeholder="••••••••" 
                   value={confirmPassword}
                   onChange={(e) => setConfirmPassword(e.target.value)}
                   className="w-full p-3 border border-gray-200 dark:border-slate-700 rounded-lg text-left" 
                   dir="ltr" 
                   required 
                />
              </div>
            )}
          </div>

          {!isLogin ? (
            <div className="flex items-center gap-2 justify-start my-2 text-sm text-gray-500 dark:text-gray-400">
              <input type="checkbox" className="w-4 h-4 accent-[#B71C1C] rounded border-gray-300" required />
              <span>أوافق على <span className="text-[#B71C1C] font-semibold">شروط الخدمة</span> و <span className="text-[#B71C1C] font-semibold">سياسة الخصوصية</span> لشركة KAK.</span>
            </div>
          ) : (
            <div className="flex items-center gap-2 justify-start my-2 text-sm text-gray-500 dark:text-gray-400">
              <input type="checkbox" className="w-4 h-4 accent-[#B71C1C] rounded border-gray-300" />
              <span>تذكرني</span>
            </div>
          )}

          <button type="submit" className="w-full py-4 text-white text-lg font-bold rounded-xl mt-4 flex justify-center items-center gap-3 transition-colors hover:bg-[#991616]" style={{backgroundColor: '#B71C1C'}}>
             <span>{isLogin ? 'تسجيل الدخول' : 'إنشاء حساب KAK'}</span>
             <span>←</span>
          </button>
        </form>

        <div className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">
          {isLogin ? 'ليس لديك حساب؟ ' : 'لديك حساب بالفعل؟ '}
          <button onClick={(e) => { 
             e.preventDefault(); 
             setIsLogin(!isLogin); 
             setError('');
             setSuccess('');
          }} className="text-[#B71C1C] font-bold bg-transparent border-none cursor-pointer p-0 underline">
            {isLogin ? 'إنشاء حساب جديد' : 'تسجيل دخول'}
          </button>
        </div>

      </div>
    </div>
  );
}
