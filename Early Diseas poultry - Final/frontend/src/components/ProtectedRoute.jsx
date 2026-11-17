import { Navigate, Outlet } from 'react-router-dom';

export default function ProtectedRoute() {
  const currentUser = localStorage.getItem('currentUser');
  
  // If not logged in, redirect to the Auth page
  if (!currentUser) {
    return <Navigate to="/" replace />;
  }

  // Otherwise, render the child routes (Layout, Dashboard, etc.)
  return <Outlet />;
}
