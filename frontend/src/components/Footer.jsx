import React from 'react';
import { BrainCircuit, Cpu, Database, Sparkles, ShieldCheck } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
              <BrainCircuit className="w-5 h-5" />
            </div>
            <div>
              <p className="font-bold text-sm text-slate-900">thinkSync AI</p>
              <p className="text-xs text-slate-500">
                Don't Just Know You're Wrong. Understand Why.
              </p>
            </div>
          </div>

          {/* Architecture badges */}
          <div className="flex flex-wrap items-center justify-center gap-2 text-xs text-slate-600 font-medium">
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
              <Cpu className="w-3.5 h-3.5 text-indigo-600" />
              Scikit-learn RF + TF-IDF (95.6% Acc)
            </span>
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
              <Sparkles className="w-3.5 h-3.5 text-amber-600" />
              Gemini Socratic AI Tutor
            </span>
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
              <Database className="w-3.5 h-3.5 text-teal-600" />
              FastAPI + SQLite
            </span>
          </div>

          <div className="text-xs text-slate-500 text-center md:text-right">
            College AIML Capstone Exhibition Edition
          </div>
        </div>
      </div>
    </footer>
  );
}
