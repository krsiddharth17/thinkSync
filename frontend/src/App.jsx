import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import StudentDashboard from './pages/StudentDashboard';
import TopicAssessmentPage from './pages/TopicAssessmentPage';
import TeacherDashboard from './pages/TeacherDashboard';
import MLPlaygroundPage from './pages/MLPlaygroundPage';
import ConceptsPage from './pages/ConceptsPage';

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 selection:bg-indigo-500 selection:text-white">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/student-dashboard" element={<StudentDashboard />} />
              <Route path="/topics/:slug" element={<TopicAssessmentPage />} />
              <Route path="/teacher-dashboard" element={<TeacherDashboard />} />
              <Route path="/ml-playground" element={<MLPlaygroundPage />} />
              <Route path="/concepts" element={<ConceptsPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}
