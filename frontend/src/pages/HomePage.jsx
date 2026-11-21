import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  BrainCircuit,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Cpu,
  BarChart2,
  Layers,
  Scale,
  PieChart,
  Percent,
  Binary,
  Lightbulb
} from 'lucide-react';
import MisconceptionBadge from '../components/MisconceptionBadge';

export default function HomePage() {
  const { quickSwitch } = useAuth();
  const navigate = useNavigate();

  // Interactive demo state on homepage
  const [demoStep, setDemoStep] = useState("2x = 19 + 7\n2x = 26\nx = 13");
  const [demoAnswer, setDemoAnswer] = useState("13");
  const [demoDiagnosed, setDemoDiagnosed] = useState(false);

  const handleTestDemo = () => {
    setDemoDiagnosed(true);
  };

  const handleStudentLogin = async () => {
    await quickSwitch('student');
    navigate('/student-dashboard');
  };

  const handleTeacherLogin = async () => {
    await quickSwitch('teacher');
    navigate('/teacher-dashboard');
  };

  return (
    <div className="space-y-24 py-8">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-8 pb-12 sm:pt-16 sm:pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs sm:text-sm font-semibold shadow-sm">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span>AIML Capstone Project: Educational Cognitive Diagnostics</span>
          </div>

          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold text-slate-900 tracking-tight max-w-4xl mx-auto leading-[1.1]">
            Don't Just Know You're Wrong.{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-800">
              Understand Why.
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto font-normal leading-relaxed">
            Traditional platforms only check if an answer is correct or incorrect. <strong className="text-slate-800 font-semibold">thinkSync AI</strong> analyzes your intermediate calculation steps using a trained Machine Learning engine to isolate recurring mathematical misconceptions and tutor you Socratically.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <button
              onClick={handleStudentLogin}
              className="px-6 py-3.5 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-700 shadow-md shadow-indigo-500/20 flex items-center gap-2 transition-all hover:scale-[1.02]"
            >
              Launch Student Dashboard
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={handleTeacherLogin}
              className="px-6 py-3.5 rounded-xl font-bold text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 shadow-sm flex items-center gap-2 transition-all hover:scale-[1.02]"
            >
              Explore Teacher & ML Hub
            </button>
          </div>

          {/* Quick specs pill */}
          <div className="flex flex-wrap items-center justify-center gap-6 pt-6 text-xs text-slate-500 font-medium">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Scikit-Learn Random Forest (95.6% Accuracy)
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Gemini Socratic AI Tutoring
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Stateful Adaptive Difficulty Engine
            </span>
          </div>
        </div>
      </section>

      {/* The Core Difference (Traditional vs thinkSync) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-3 mb-12">
          <h2 className="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            The Fundamental Shift in EdTech
          </h2>
          <p className="text-slate-600 max-w-xl mx-auto text-sm sm:text-base">
            Why traditional automated grading fails struggling students, and how cognitive misconception classification fixes it.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 items-stretch">
          {/* Traditional */}
          <div className="bg-white rounded-3xl border border-rose-200/80 p-6 sm:p-8 shadow-sm flex flex-col justify-between">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-bold">
                <XCircle className="w-4 h-4 text-rose-600" />
                Traditional Automated Evaluation
              </div>
              <h3 className="text-xl font-bold text-slate-900">
                Binary Correct / Incorrect Feedback
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                A student solves <code className="bg-slate-100 px-1 py-0.5 rounded text-indigo-700 font-mono">2x + 7 = 19</code> and submits <code className="bg-slate-100 px-1 py-0.5 rounded text-rose-700 font-mono">x = 13</code>.
              </p>

              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2">
                <div className="flex items-center justify-between text-xs font-semibold text-slate-500">
                  <span>Standard Grader Output:</span>
                  <span className="text-rose-600 font-bold uppercase">Incorrect (0/10)</span>
                </div>
                <p className="text-xs text-rose-800 bg-rose-50 border border-rose-200 p-2.5 rounded-lg font-mono">
                  ✗ Incorrect. Correct answer is 6.
                </p>
                <p className="text-xs text-slate-500 italic">
                  Does not explain why the student got 13, does not check steps, and leaves the student frustrated.
                </p>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100 text-xs text-slate-500 flex items-center gap-2">
              <span className="text-rose-500 font-bold">Outcome:</span>
              <span>Student repeats the same mistake without learning the root cause.</span>
            </div>
          </div>

          {/* thinkSync AI */}
          <div className="bg-gradient-to-br from-indigo-50/60 to-purple-50/40 rounded-3xl border border-indigo-200 p-6 sm:p-8 shadow-md shadow-indigo-500/5 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-100 border border-indigo-300 text-indigo-800 text-xs font-bold">
                <BrainCircuit className="w-4 h-4 text-indigo-700" />
                thinkSync AI Cognitive Diagnosis
              </div>
              <h3 className="text-xl font-bold text-slate-900">
                Machine Learning Misconception Identification
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                The ML model inspects intermediate steps <code className="bg-indigo-100/50 px-1 py-0.5 rounded text-indigo-800 font-mono">2x = 19 + 7</code> and classifies the root misconception.
              </p>

              <div className="bg-white border border-indigo-200 rounded-xl p-4 space-y-3 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-600">ML Model Diagnosis:</span>
                  <MisconceptionBadge category="inverse_operation_error" showConfidence confidence={0.88} size="sm" />
                </div>
                <div className="text-xs space-y-1.5 text-slate-700 bg-indigo-50/60 border border-indigo-100 p-3 rounded-lg">
                  <p className="font-semibold text-indigo-900 flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                    AI Tutor Socratic Feedback:
                  </p>
                  <p className="text-slate-600">
                    "You added 7 to 19 instead of subtracting! Remember that an equation is like a balanced see-saw: to undo +7, you must subtract 7 from both sides."
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-indigo-100 text-xs text-indigo-900 font-medium flex items-center gap-2">
              <span className="text-emerald-600 font-bold">Outcome:</span>
              <span>Student fixes the mental gap and difficulty adapts automatically.</span>
            </div>
          </div>
        </div>
      </section>

      {/* Live Interactive Sandbox Preview */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-10 shadow-lg space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-5">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">
                Live Interactive Demonstration
              </span>
              <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mt-1">
                Test the ML Misconception Engine Now
              </h3>
              <p className="text-xs sm:text-sm text-slate-500">
                Question: <span className="font-mono font-semibold text-slate-800">Solve for x: 2x + 7 = 19</span> (Correct answer: 6)
              </p>
            </div>
            <button
              onClick={handleTestDemo}
              className="px-5 py-2.5 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-700 text-sm shadow transition-all self-start sm:self-center"
            >
              Run ML Diagnostics
            </button>
          </div>

          <div className="grid sm:grid-cols-2 gap-6">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-2">
                Simulated Student Intermediate Steps:
              </label>
              <textarea
                value={demoStep}
                onChange={(e) => setDemoStep(e.target.value)}
                rows={4}
                className="w-full text-xs sm:text-sm font-mono p-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:outline-none bg-slate-50"
              />
              <div className="mt-3">
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Student Final Answer:
                </label>
                <input
                  type="text"
                  value={demoAnswer}
                  onChange={(e) => setDemoAnswer(e.target.value)}
                  className="w-full text-sm font-mono p-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:outline-none bg-slate-50"
                />
              </div>
            </div>

            <div className="bg-slate-50 rounded-2xl border border-slate-200 p-5 flex flex-col justify-between">
              {demoDiagnosed ? (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-500">Predicted Misconception:</span>
                    <MisconceptionBadge category="inverse_operation_error" showConfidence confidence={0.88} />
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-xs font-medium text-slate-600">
                      <span>Model Confidence:</span>
                      <span className="font-bold font-mono">88.4%</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                      <div className="bg-amber-500 h-2 rounded-full w-[88%]" />
                    </div>
                  </div>

                  <div className="bg-white border border-slate-200 rounded-xl p-3 text-xs text-slate-700 space-y-1">
                    <p className="font-bold text-slate-900">AI Tutor Analysis:</p>
                    <p className="text-slate-600">
                      The student added 7 to 19 instead of subtracting. They recognized that 7 needed to move, but reversed the inverse operation rule.
                    </p>
                  </div>

                  <p className="text-[11px] text-emerald-700 font-medium">
                    ✓ Adaptive Path: Serving 1 foundational equation balancing question.
                  </p>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-center py-6 text-slate-400 space-y-2">
                  <Cpu className="w-8 h-8 text-slate-300 animate-pulse" />
                  <p className="text-xs">Click "Run ML Diagnostics" above to see the real-time classifier in action.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Topics Covered */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-3 mb-12">
          <h2 className="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Mathematics Diagnostic Topics
          </h2>
          <p className="text-slate-600 max-w-xl mx-auto text-sm sm:text-base">
            Full support across essential foundational mathematical domains with modular expansion architecture.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              title: "Linear Equations",
              slug: "linear-equations",
              icon: Scale,
              color: "amber",
              desc: "Isolating variables, inverse operation balances, multi-step expressions.",
              traps: "Inverse Op Errors, Sign Drops"
            },
            {
              title: "Fractions",
              slug: "fractions",
              icon: PieChart,
              color: "teal",
              desc: "Common denominators, LCD calculation, reciprocal fraction division.",
              traps: "Direct Denominator Addition"
            },
            {
              title: "Percentages",
              slug: "percentages",
              icon: Percent,
              color: "purple",
              desc: "Proportions, discounts, markups, benchmark fraction conversions.",
              traps: "Flat Subtraction Confusion"
            },
            {
              title: "Basic Algebra",
              slug: "basic-algebra",
              icon: Binary,
              color: "indigo",
              desc: "Combining like terms, distributive property, integer exponents.",
              traps: "Unlike Term Fusion (3x+4=7x)"
            }
          ].map((topic, i) => {
            const Icon = topic.icon;
            return (
              <div key={i} className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm card-hover-effect flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600">
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="font-bold text-lg text-slate-900">{topic.title}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{topic.desc}</p>
                </div>
                <div className="mt-6 pt-4 border-t border-slate-100">
                  <span className="text-[11px] font-semibold text-slate-500 block mb-2">
                    Common Misconceptions:
                  </span>
                  <span className="inline-block text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">
                    {topic.traps}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* 4-Step Technical Architecture */}
      <section className="bg-slate-900 text-white rounded-3xl max-w-7xl mx-auto px-6 py-16 sm:p-16">
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-16">
          <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">
            System Architecture
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
            How thinkSync AI Understands Learning Difficulties
          </h2>
          <p className="text-slate-400 text-sm sm:text-base">
            A cohesive pipeline that blends real machine learning classification with generative AI pedagogical tutoring and Bayesian adaptive progression.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {[
            {
              step: "01",
              title: "Step & Approach Capture",
              desc: "Students input intermediate solving lines and select their problem-solving strategy, capturing behavioral cognitive traces."
            },
            {
              step: "02",
              title: "Scikit-Learn ML Engine",
              desc: "TF-IDF n-grams combined with 9 engineered mathematical domain features classify the exact misconception category with 95.6% accuracy."
            },
            {
              step: "03",
              title: "Socratic AI Tutor",
              desc: "Gemini API synthesizes the ML diagnosis into empathetic, non-judgmental explanations, step hints, and parallel practice problems."
            },
            {
              step: "04",
              title: "Adaptive Profiling",
              desc: "The student learning profile updates dynamically. If recurring misconceptions exceed thresholds, foundational scaffolds are automatically deployed."
            }
          ].map((item, i) => (
            <div key={i} className="space-y-3 border-l-2 border-indigo-500/30 pl-4">
              <span className="font-mono text-2xl font-extrabold text-indigo-400">
                {item.step}
              </span>
              <h3 className="font-bold text-lg text-white">{item.title}</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
