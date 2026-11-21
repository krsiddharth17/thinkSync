import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { topicsApi, assessmentApi } from '../api/client';
import {
  BrainCircuit,
  Sparkles,
  ArrowRight,
  RotateCcw,
  Lightbulb,
  CheckCircle2,
  XCircle,
  HelpCircle,
  BookOpen,
  ChevronRight,
  Scale,
  Percent,
  PieChart as PieIcon,
  Binary,
  Clock,
  Layers,
  X
} from 'lucide-react';
import MisconceptionBadge from '../components/MisconceptionBadge';

export default function TopicAssessmentPage() {
  const { slug } = useParams();
  const navigate = useNavigate();

  const [topic, setTopic] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  // Form input state
  const [studentAnswer, setStudentAnswer] = useState('');
  const [intermediateSteps, setIntermediateSteps] = useState('');
  const [selectedApproach, setSelectedApproach] = useState('standard');
  const [timeTaken, setTimeTaken] = useState(30);

  // Result & Hint state
  const [result, setResult] = useState(null);
  const [activeHint, setActiveHint] = useState(null);
  const [hintLoading, setHintLoading] = useState(false);
  const [conceptModalOpen, setConceptModalOpen] = useState(false);

  useEffect(() => {
    async function fetchTopicAndQuestions() {
      try {
        setLoading(true);
        const [tData, qData] = await Promise.all([
          topicsApi.get(slug),
          topicsApi.getQuestions(slug),
        ]);
        setTopic(tData);
        setQuestions(qData);
        if (qData.length > 0 && qData[0].approach_options?.length > 0) {
          setSelectedApproach(qData[0].approach_options[0]);
        }
      } catch (err) {
        console.error('Failed to load topic questions:', err);
        setError(err.message || 'Error loading topic questions');
      } finally {
        setLoading(false);
      }
    }
    fetchTopicAndQuestions();
  }, [slug]);

  const currentQ = questions[currentIdx];

  const handleNext = () => {
    if (currentIdx < questions.length - 1) {
      const nextIdx = currentIdx + 1;
      setCurrentIdx(nextIdx);
      resetForm(nextIdx);
    }
  };

  const handlePrev = () => {
    if (currentIdx > 0) {
      const prevIdx = currentIdx - 1;
      setCurrentIdx(prevIdx);
      resetForm(prevIdx);
    }
  };

  const resetForm = (idx = currentIdx) => {
    setStudentAnswer('');
    setIntermediateSteps('');
    setResult(null);
    setActiveHint(null);
    const targetQ = questions[idx];
    if (targetQ && targetQ.approach_options?.length > 0) {
      setSelectedApproach(targetQ.approach_options[0]);
    } else {
      setSelectedApproach('standard');
    }
  };

  const handleInsertSymbol = (sym) => {
    setIntermediateSteps((prev) => prev + sym);
  };

  const handleRequestHint = async (level = 1) => {
    if (!currentQ) return;
    try {
      setHintLoading(true);
      const hintRes = await assessmentApi.requestHint({
        question_id: currentQ.id,
        student_current_steps: intermediateSteps,
        hint_level: level,
      });
      setActiveHint(hintRes);
    } catch (err) {
      console.warn('Hint request error:', err);
    } finally {
      setHintLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!currentQ || !studentAnswer.trim()) return;

    setSubmitting(true);
    setError('');
    try {
      const evalResult = await assessmentApi.evaluate({
        question_id: currentQ.id,
        student_answer: studentAnswer.trim(),
        intermediate_steps: intermediateSteps.trim(),
        approach_selected: selectedApproach,
        time_taken_seconds: timeTaken,
      });
      setResult(evalResult);
    } catch (err) {
      console.error('Evaluation error:', err);
      setError(err.message || 'Failed to evaluate submission.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
        <p className="text-xs font-semibold text-slate-500">Preparing diagnostic assessment environment...</p>
      </div>
    );
  }

  if (error && !currentQ) {
    return (
      <div className="max-w-md mx-auto my-16 bg-white p-6 rounded-2xl border border-rose-200 text-center space-y-4">
        <p className="text-sm text-rose-600 font-semibold">{error}</p>
        <Link to="/student-dashboard" className="inline-block text-xs font-bold text-indigo-600">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Header & Breadcrumb */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-500">
            <Link to="/student-dashboard" className="hover:text-indigo-600">
              Student Dashboard
            </Link>
            <ChevronRight className="w-3.5 h-3.5" />
            <span className="text-indigo-600 font-bold">{topic?.name}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            {topic?.name} Diagnostic Assessment
          </h1>
        </div>

        <button
          onClick={() => setConceptModalOpen(true)}
          className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 shadow-sm transition-all self-start sm:self-center"
        >
          <BookOpen className="w-4 h-4" />
          Review Concept Guide
        </button>
      </div>

      {/* Progress & Pagination Bar */}
      <div className="flex items-center justify-between bg-white px-5 py-3 rounded-2xl border border-slate-200 shadow-sm text-xs font-medium text-slate-600">
        <div className="flex items-center gap-2">
          <span>Question {currentIdx + 1} of {questions.length}</span>
          <span className="capitalize px-2 py-0.5 rounded-full text-[11px] font-bold bg-slate-100 text-slate-700">
            Difficulty: {currentQ?.difficulty}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handlePrev}
            disabled={currentIdx === 0}
            className="px-3 py-1 rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <button
            onClick={handleNext}
            disabled={currentIdx === questions.length - 1}
            className="px-3 py-1 rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>

      {/* Main Diagnostic Workspace */}
      <div className="grid lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Question & Problem Solving Input */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-6">
            {/* Question Text Box */}
            <div className="space-y-2">
              <span className="text-[11px] font-extrabold uppercase tracking-wider text-indigo-600">
                Problem Statement:
              </span>
              <div className="p-4 rounded-2xl bg-indigo-50/60 border border-indigo-100 text-slate-900 text-lg sm:text-xl font-bold font-mono">
                {currentQ?.question_text}
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Approach Selector */}
              {currentQ?.approach_options?.length > 0 && (
                <div className="space-y-2">
                  <label className="block text-xs font-bold text-slate-700 uppercase">
                    How do you plan to solve this? (Select Approach)
                  </label>
                  <select
                    value={selectedApproach}
                    onChange={(e) => setSelectedApproach(e.target.value)}
                    className="w-full px-3.5 py-2.5 text-xs sm:text-sm font-medium rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:outline-none bg-slate-50"
                  >
                    {currentQ.approach_options.map((opt, i) => (
                      <option key={i} value={opt}>
                        {opt}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {/* Intermediate Steps Editor */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="block text-xs font-bold text-slate-700 uppercase">
                    Intermediate Solving Steps (Required for AI Diagnosis)
                  </label>
                  <span className="text-[11px] text-slate-400 font-medium">Show line-by-line math</span>
                </div>

                {/* Math helper toolbar */}
                <div className="flex flex-wrap items-center gap-1.5 pb-1">
                  <span className="text-[10px] font-semibold text-slate-400 uppercase mr-1">Insert:</span>
                  {['+', '-', '*', '/', '=', 'x', '1/2', '->'].map((sym) => (
                    <button
                      key={sym}
                      type="button"
                      onClick={() => handleInsertSymbol(` ${sym} `)}
                      className="px-2 py-1 rounded bg-slate-100 hover:bg-slate-200 font-mono text-xs font-bold text-slate-700"
                    >
                      {sym}
                    </button>
                  ))}
                </div>

                <textarea
                  value={intermediateSteps}
                  onChange={(e) => setIntermediateSteps(e.target.value)}
                  rows={4}
                  placeholder="e.g.&#10;2x = 19 - 7&#10;2x = 12&#10;x = 6"
                  className="w-full text-xs sm:text-sm font-mono p-3.5 rounded-2xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:outline-none bg-slate-50 leading-relaxed"
                />
              </div>

              {/* Final Answer Input */}
              <div className="space-y-2">
                <label className="block text-xs font-bold text-slate-700 uppercase">
                  Your Final Answer
                </label>
                <input
                  type="text"
                  required
                  value={studentAnswer}
                  onChange={(e) => setStudentAnswer(e.target.value)}
                  placeholder="e.g. 6 or 7/12"
                  className="w-full px-4 py-3 text-base font-mono font-bold rounded-2xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:outline-none bg-slate-50"
                />
              </div>

              {/* Actions */}
              <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
                <div className="flex items-center gap-2 w-full sm:w-auto">
                  <button
                    type="button"
                    onClick={() => handleRequestHint(1)}
                    disabled={hintLoading}
                    className="flex-1 sm:flex-none px-3.5 py-2.5 rounded-xl border border-amber-300 bg-amber-50 hover:bg-amber-100 text-amber-900 text-xs font-bold flex items-center justify-center gap-1.5 transition-colors"
                  >
                    <Lightbulb className="w-3.5 h-3.5 text-amber-600" />
                    {hintLoading ? 'Thinking...' : 'Get Socratic Hint'}
                  </button>
                  <button
                    type="button"
                    onClick={() => resetForm()}
                    className="p-2.5 rounded-xl border border-slate-200 hover:bg-slate-100 text-slate-500 transition-colors"
                    title="Clear inputs"
                  >
                    <RotateCcw className="w-4 h-4" />
                  </button>
                </div>

                <button
                  type="submit"
                  disabled={submitting || !studentAnswer.trim()}
                  className="w-full sm:w-auto px-6 py-3 rounded-xl font-bold text-xs sm:text-sm text-white bg-indigo-600 hover:bg-indigo-700 shadow-md shadow-indigo-500/20 disabled:opacity-40 transition-all flex items-center justify-center gap-2"
                >
                  <BrainCircuit className="w-4 h-4" />
                  {submitting ? 'Analyzing Steps...' : 'Submit for AI Diagnosis'}
                </button>
              </div>
            </form>

            {/* Socratic Hint Box (if requested) */}
            {activeHint && (
              <div className="bg-amber-50/80 border border-amber-200 rounded-2xl p-4 text-xs text-amber-950 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold flex items-center gap-1 text-amber-900">
                    <Lightbulb className="w-4 h-4 text-amber-600" />
                    {activeHint.hint_title}
                  </span>
                  <span className="text-[10px] text-amber-700 font-semibold uppercase">Non-Spoiler Guidance</span>
                </div>
                <p className="text-slate-700 leading-relaxed">{activeHint.hint_text}</p>
                {activeHint.question_hint && (
                  <p className="text-amber-900 font-medium bg-amber-100/60 p-2 rounded-lg">
                    💡 Topic Note: {activeHint.question_hint}
                  </p>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Instant ML & Socratic Tutor Diagnostic Panel */}
        <div className="lg:col-span-5 space-y-6">
          {result ? (
            <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-7 shadow-lg space-y-6">
              {/* Correctness Header */}
              <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                <div className="flex items-center gap-2.5">
                  {result.is_correct ? (
                    <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
                      <CheckCircle2 className="w-5 h-5" />
                    </div>
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center">
                      <XCircle className="w-5 h-5" />
                    </div>
                  )}
                  <div>
                    <h3 className="font-bold text-base text-slate-900">
                      {result.is_correct ? 'Correct Solution!' : 'Misconception Detected'}
                    </h3>
                    <p className="text-[11px] text-slate-500">
                      {result.is_correct
                        ? 'Accurate steps and mathematical reasoning.'
                        : 'Identified by trained Machine Learning pipeline.'}
                    </p>
                  </div>
                </div>

                <MisconceptionBadge
                  category={result.predicted_misconception}
                  showConfidence
                  confidence={result.ml_confidence}
                  size="sm"
                />
              </div>

              {/* Machine Learning Model Diagnostics Box */}
              <div className="bg-slate-50 rounded-2xl border border-slate-200/80 p-4 space-y-3">
                <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                  <span className="flex items-center gap-1.5">
                    <BrainCircuit className="w-4 h-4 text-indigo-600" />
                    ML Classifier Confidence
                  </span>
                  <span className="font-mono font-bold text-indigo-700">
                    {Math.round(result.ml_confidence * 100)}%
                  </span>
                </div>

                <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-2 rounded-full ${
                      result.is_correct ? 'bg-emerald-500' : 'bg-amber-500'
                    }`}
                    style={{ width: `${Math.min(100, Math.round(result.ml_confidence * 100))}%` }}
                  />
                </div>

                {/* Probability Distribution mini bars */}
                {result.class_probabilities && (
                  <div className="pt-2 border-t border-slate-200/60 space-y-1.5">
                    <span className="text-[10px] font-bold text-slate-400 uppercase block">
                      Candidate Probability Distribution:
                    </span>
                    {Object.entries(result.class_probabilities)
                      .slice(0, 3)
                      .map(([cls, prob]) => (
                        <div key={cls} className="flex items-center justify-between text-[11px] text-slate-600">
                          <span className="truncate max-w-[180px]">{cls.replace(/_/g, ' ')}</span>
                          <span className="font-mono text-slate-500">{Math.round(prob * 100)}%</span>
                        </div>
                      ))}
                  </div>
                )}
              </div>

              {/* AI Socratic Tutor Card */}
              <div className="bg-gradient-to-br from-indigo-50/70 to-purple-50/60 rounded-2xl border border-indigo-200 p-5 space-y-3.5 text-xs">
                <div className="flex items-center gap-1.5 font-bold text-indigo-950 text-sm">
                  <Sparkles className="w-4 h-4 text-amber-500" />
                  <span>Personal AI Tutor Guidance</span>
                </div>

                {/* 1. Mistake Analysis */}
                <div className="space-y-1">
                  <span className="font-bold text-indigo-900 block text-[11px] uppercase">
                    Step Analysis:
                  </span>
                  <p className="text-slate-700 leading-relaxed">
                    {result.ai_feedback?.mistake_analysis}
                  </p>
                </div>

                {/* 2. Conceptual Explanation */}
                <div className="space-y-1 pt-1 border-t border-indigo-100">
                  <span className="font-bold text-indigo-900 block text-[11px] uppercase">
                    Underlying Mathematical Principle:
                  </span>
                  <p className="text-slate-700 leading-relaxed">
                    {result.ai_feedback?.conceptual_explanation}
                  </p>
                </div>

                {/* 3. Socratic Hint */}
                {result.ai_feedback?.socratic_hint && (
                  <div className="bg-white/80 p-3 rounded-xl border border-indigo-100 space-y-1">
                    <span className="font-bold text-indigo-900 block text-[10px] uppercase">
                      💡 Guided Socratic Hint:
                    </span>
                    <p className="text-indigo-950 font-medium">
                      {result.ai_feedback.socratic_hint}
                    </p>
                  </div>
                )}

                {/* 4. Encouragement */}
                <p className="text-[11px] text-indigo-800 font-medium italic pt-1">
                  "{result.ai_feedback?.encouragement}"
                </p>
              </div>

              {/* Adaptive Recommendation */}
              {result.adaptive_recommendation && (
                <div className="bg-slate-50 rounded-2xl border border-slate-200 p-3.5 text-xs text-slate-700 space-y-1">
                  <span className="font-bold text-slate-900 text-[11px] uppercase block">
                    Adaptive Engine Update:
                  </span>
                  <p>{result.adaptive_recommendation.message}</p>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center gap-3 pt-2">
                {!result.is_correct ? (
                  <button
                    onClick={() => setResult(null)}
                    className="flex-1 py-2.5 rounded-xl text-xs font-bold bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 transition-colors"
                  >
                    Try Solving Again
                  </button>
                ) : (
                  <button
                    onClick={handleNext}
                    disabled={currentIdx === questions.length - 1}
                    className="flex-1 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white shadow transition-colors flex items-center justify-center gap-1.5"
                  >
                    Next Question
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-3xl border border-slate-200/80 p-8 shadow-sm flex flex-col items-center justify-center text-center space-y-4 min-h-[380px]">
              <div className="w-14 h-14 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600">
                <BrainCircuit className="w-8 h-8 text-indigo-500 animate-pulse" />
              </div>
              <div className="space-y-1 max-w-xs">
                <h3 className="font-bold text-slate-900 text-base">Awaiting Your Steps</h3>
                <p className="text-xs text-slate-500">
                  Write down your calculation steps and final answer on the left. The ML model will analyze your cognitive approach in real time.
                </p>
              </div>
              <div className="text-[11px] text-indigo-600 font-semibold bg-indigo-50 px-3 py-1.5 rounded-full border border-indigo-100">
                Cognitive Diagnostic Ready
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Concept Guide Modal */}
      {conceptModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[85vh] overflow-y-auto p-6 sm:p-8 space-y-6 shadow-2xl relative">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-indigo-600" />
                <h3 className="text-xl font-bold text-slate-900">
                  {topic?.name} Concept Guide
                </h3>
              </div>
              <button
                onClick={() => setConceptModalOpen(false)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="prose prose-sm max-w-none text-slate-700 space-y-4 leading-relaxed font-sans">
              <div className="whitespace-pre-line text-xs sm:text-sm">
                {topic?.concept_guide || 'Concept guide coming soon.'}
              </div>
            </div>

            <div className="pt-4 border-t border-slate-100 flex justify-end">
              <button
                onClick={() => setConceptModalOpen(false)}
                className="px-5 py-2.5 rounded-xl font-bold text-xs text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Got it, Return to Practice
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
