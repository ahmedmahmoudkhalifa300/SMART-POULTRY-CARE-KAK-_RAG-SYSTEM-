import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { NotificationProvider } from './context/NotificationContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Diagnostics from './pages/Diagnostics';
import Dashboard from './pages/Dashboard';
import Vaccinations from './pages/Vaccinations';
import Auth from './pages/Auth';
import SelectProduction from './pages/SelectProduction';
import Onboarding from './pages/Onboarding';
import DailyManagement from './pages/DailyManagement';
import History from './pages/History';
import Financials from './pages/Financials';
import SmartAssistant from './pages/SmartAssistant';

function App() {
  return (
    <BrowserRouter>
      <NotificationProvider>
        <Toaster position="bottom-right" reverseOrder={false} />
        <Routes>
        <Route path="/" element={<Auth />} />
        
        {/* Protected Routes */}
        <Route element={<ProtectedRoute />}>
           <Route path="/select-production" element={<SelectProduction />} />
           <Route path="/onboarding" element={<Onboarding />} />
           <Route element={<Layout />}>
             <Route path="dashboard" element={<Dashboard />} />
             <Route path="diagnostics" element={<Diagnostics />} />
             <Route path="vaccinations" element={<Vaccinations />} />
             <Route path="daily" element={<DailyManagement />} />
             <Route path="assistant" element={<SmartAssistant />} />
             <Route path="history" element={<History />} />
             <Route path="financials" element={<Financials />} />
             {/* Fallbacks for other mock routes */}
             <Route path="*" element={<div className="text-center mt-20"><h2 className="text-2xl font-bold">قريباً</h2><p className="text-muted">هذه الصفحة قيد التطوير</p></div>} />
           </Route>
        </Route>
      </Routes>
      </NotificationProvider>
    </BrowserRouter>
  );
}

export default App;
