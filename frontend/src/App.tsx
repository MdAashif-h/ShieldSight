import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ScrollToTop } from './components/ScrollToTop';
import { LoginForm } from './components/auth/LoginForm';
import { SignupForm } from './components/auth/SignupForm';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { MainLayout } from './components/layout/MainLayout'; // ✅ USE THIS
import { LandingPage } from './pages/LandingPage';
import { AboutPage } from './pages/AboutPage';
import { ContactPage } from './pages/ContactPage';
import { Dashboard } from './pages/Dashboard';
import { Analyze } from './pages/Analyze';
import { Batch } from './pages/Batch';
import { History } from './pages/History';
import { Profile } from './pages/Profile';
import { Settings } from './pages/Settings';
import { Help } from './pages/Help';
import { EmailScan } from './pages/EmailScan';
import { QRScanner } from './components/scanner/QRScanner';
import { DocumentScanner } from './components/scanner/DocumentScanner';
import { ErrorBoundary } from './components/ErrorBoundary';
import { OfflineDetector } from './components/OfflineDetector';
import { ToastContainer } from './components/ui/Toast';

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <ScrollToTop />
        <OfflineDetector />
        <ToastContainer />

        <Routes>
          {/* ================= PUBLIC ROUTES ================= */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/signup" element={<SignupForm />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />

          {/* ================= PROTECTED ROUTES ================= */}
          <Route
            path="/app"
            element={
              <ProtectedRoute>
                <MainLayout /> {/* ✅ ONLY ONE LAYOUT */}
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/app/dashboard" replace />} />

            <Route path="dashboard" element={<Dashboard />} />
            <Route path="analyze" element={<Analyze />} />
            <Route path="batch" element={<Batch />} />
            <Route path="history" element={<History />} />
            <Route path="profile" element={<Profile />} />
            <Route path="settings" element={<Settings />} />
            <Route path="help" element={<Help />} />

            {/* Scanner Pages */}
            <Route path="email-scan" element={<EmailScan />} />
            <Route path="qr-scanner" element={<QRScanner />} />
            <Route path="document-scanner" element={<DocumentScanner />} />
          </Route>

          {/* ================= 404 ================= */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
