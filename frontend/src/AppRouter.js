// AppRouter.js
import { Routes, Route, Navigate } from 'react-router-dom';
import App from './App';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';

const AppRouter = () => {
   const token = localStorage.getItem('token');
  const isLoggedIn = !!token && token !== 'null' && token !== 'undefined';

  console.log("AppRouter - token:", token);
  console.log("AppRouter - isLoggedIn:", isLoggedIn);
  console.log("AppRouter - current path:", window.location.pathname);

  return (
    <Routes>
      {/* Protected route - only accessible when logged in */}
      <Route
        path="/"
        element={isLoggedIn ? <App /> : <Navigate to="/login" replace />}
      />
      
      {/* Auth routes - only accessible when NOT logged in */}
      <Route
        path="/login"
        element={isLoggedIn ? <Navigate to="/" replace /> : <LoginPage />}
      />
      <Route
        path="/signup"
        element={isLoggedIn ? <Navigate to="/" replace /> : <SignupPage />}
      />
    </Routes>
  );
};

export default AppRouter;
