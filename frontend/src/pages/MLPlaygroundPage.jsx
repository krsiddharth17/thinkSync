import React, { useState, useEffect } from 'react';
import { mlApi } from '../api/client';
import {
  Cpu,
  BrainCircuit,
  BarChart2,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  ArrowRight,
  Layers,
  Database,
  ShieldCheck,
  Play
} from 'lucide-react';
import MetricCard from '../components/MetricCard';
import MisconceptionBadge from '../components/MisconceptionBadge';

const PRESET_EXAMPLES = [
  {
    name: 'Linear Equations: Inverse Operation Error',
    topic: 'linear_equations',
    question: 'Solve for x: 3x + 12 = 33',
    correct_answer: '7',
    student_answer: '15',
    steps: '3x = 33 + 12\n3x = 45\nx = 45 / 3 = 15',
    approach: 'isolate_variable',
  },
  {
    name: 'Fractions: Direct Denominator Addition',
    topic: 'fractions',
    question: 'Evaluate: 1/3 + 1/4',
    correct_answer: '7/12',
    student_answer: '2/7',
    steps: '(1 + 1) / (3 + 4) = 2/7',
    approach: 'direct_addition',
  },
  {
    name: 'Basic Algebra: Sign Distribution Error',
    topic: 'basic_algebra',
    question: 'Expand: -2(3x - 4)',
    correct_answer: '-6x + 8',
    student_answer: '-6x - 8',
    steps: '-2 * 3x = -6x\n-2 * 4 = -8\nResult: -6x - 8',
    approach: 'distributive_property',
  },
  {
    name: 'Percentages: Flat Dollar Subtraction Trap',
    topic: 'percentages',
    question: 'What is 20% of 80?',
    correct_answer: '16',
    student_answer: '60',
    steps: '80 - 20 = 60',
    approach: 'subtraction',
  },
  {
    name: 'Linear Equations: Inverted Division Ratio',
    topic: 'linear_equations',
    question: 'Solve for x: 6x = 3',
    correct_answer: '0.5',
    student_answer: '2',
    steps: 'x = 6 / 3 = 2',
    approach: 'isolate_variable',
  },
  {
    name: 'Basic Algebra: Unlike Term Fusion',
    topic: 'basic_algebra',
    question: 'Solve for x: 4x + 5 = 29',
    correct_answer: '6',
    student_answer: '3.22',
    steps: '4x + 5 = 9x\n9x = 29\nx = 29/9',
    approach: 'combine_terms',
  },
];

export default function MLPlaygroundPage() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  // Playground input state
  const [topic, setTopic] = useState('linear_equations');
  const [question, setQuestion] = useState('Solve for x: 2x + 7 = 19');
  const [correctAnswer, setCorrectAnswer] = useState('6');
  const [studentAnswer, setStudentAnswer] = useState('13');
  const [steps, setSteps] = useState('2x = 19 + 7\n2x = 26\nx = 13');
  const [approach, setApproach] = useState('isolate_variable');

  // Prediction output
  const [predResult, setPredResult] = useState(null);
  const [evaluating, setEvaluating] = useState(false);

  useEffect(() => {
    async function loadMetrics() {
      try {
        setLoading(true);
        const data = await mlApi.getMetrics();
        setMetrics(data);
      } catch (err) {
        console.error('Failed to load ML metrics:', err);
      } finally {
        setLoading(false);
      }
    }
    loadMetrics();
  }, []);

  const handleApplyPreset = (preset) => {
    setTopic(preset.topic);
    setQuestion(preset.question);
    setCorrectAnswer(preset.correct_answer);
    setStudentAnswer(preset.student_answer);
    setSteps(preset.steps);
    setApproach(preset.approach);
    setPredResult(null);
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setEvaluating(true);
    try {
      const res = await mlApi.predict({
        topic,
        question,
        correct_answer: correctAnswer,
        student_answer: studentAnswer,
        steps,
        approach,
      });
      setPredResult(res);
    } catch (err) {
      console.error('Prediction failed:', err);
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Page Header */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-3">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-xs font-bold text-indigo-700">
          <Cpu className="w-3.5 h-3.5" />
          <span>Machine Learning Architecture & Evaluation Studio</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Misconception Classifier Metrics & Live Sandbox
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 max-w-3xl leading-relaxed">
          An authentic, trained Scikit-learn classification engine combining TF-IDF n-grams with 9 mathematical domain & behavioral features to categorize student misconceptions independently from LLMs.
        </p>
      </div>

      {/* Model Performance Cards */}
      {metrics && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          <MetricCard
            title="Model Accuracy"
            value={`${metrics.performance.accuracy_percent}%`}
            subtitle="Stratified Holdout Test Set"
            icon={CheckCircle2}
            color="emerald"
            badge="Scikit-Learn"
          />
          <MetricCard
            title="Macro F1-Score"
            value={metrics.performance.macro_f1}
            subtitle="Balanced across all 7 classes"
            icon={BrainCircuit}
            color="indigo"
          />
          <MetricCard
            title="Macro Precision"
            value={metrics.performance.macro_precision}
            subtitle="Low false-positive rate"
            icon={ShieldCheck}
            color="purple"
          />
          <MetricCard
            title="Dataset Size"
            value={`${metrics.sample_counts.total_dataset_size}`}
            subtitle={`${metrics.sample_counts.training_samples} train / ${metrics.sample_counts.test_samples} test`}
            icon={Database}
            color="sky"
          />
        </div>
      )}

      {/* Interactive Live ML Playground Studio */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-5">
          <div>
            <h2 className="text-xl font-bold text-slate-900">Live ML Inference Sandbox</h2>
            <p className="text-xs text-slate-500">
              Test any custom equation, student steps, and response to watch the classifier calculate real-time probabilities.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-slate-400 uppercase">Presets:</span>
            <select
              onChange={(e) => {
                const idx = parseInt(e.target.value);
                if (!isNaN(idx)) handleApplyPreset(PRESET_EXAMPLES[idx]);
              }}
              className="text-xs font-medium px-3 py-1.5 rounded-xl border border-slate-300 bg-slate-50 text-slate-800 focus:outline-none"
            >
              <option value="">Select a benchmark preset...</option>
              {PRESET_EXAMPLES.map((ex, i) => (
                <option key={i} value={i}>
                  {ex.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <form onSubmit={handlePredict} className="grid lg:grid-cols-12 gap-8 items-start">
          {/* Inputs */}
          <div className="lg:col-span-7 space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Topic Domain
                </label>
                <select
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="w-full text-xs font-medium px-3 py-2 rounded-xl border border-slate-300 bg-slate-50"
                >
                  <option value="linear_equations">Linear Equations</option>
                  <option value="fractions">Fractions</option>
                  <option value="percentages">Percentages</option>
                  <option value="basic_algebra">Basic Algebra</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Student Approach
                </label>
                <input
                  type="text"
                  value={approach}
                  onChange={(e) => setApproach(e.target.value)}
                  className="w-full text-xs font-mono px-3 py-2 rounded-xl border border-slate-300 bg-slate-50"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Question Statement
              </label>
              <input
                type="text"
                required
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="w-full text-xs font-mono font-bold px-3 py-2 rounded-xl border border-slate-300 bg-slate-50"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Correct Answer
                </label>
                <input
                  type="text"
                  required
                  value={correctAnswer}
                  onChange={(e) => setCorrectAnswer(e.target.value)}
                  className="w-full text-xs font-mono font-bold px-3 py-2 rounded-xl border border-slate-300 bg-slate-50 text-emerald-700"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Student Submitted Answer
                </label>
                <input
                  type="text"
                  required
                  value={studentAnswer}
                  onChange={(e) => setStudentAnswer(e.target.value)}
                  className="w-full text-xs font-mono font-bold px-3 py-2 rounded-xl border border-slate-300 bg-slate-50 text-rose-700"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Student Intermediate Calculation Steps
              </label>
              <textarea
                rows={4}
                value={steps}
                onChange={(e) => setSteps(e.target.value)}
                className="w-full text-xs font-mono p-3 rounded-xl border border-slate-300 bg-slate-50 leading-relaxed"
                placeholder="Line by line steps..."
              />
            </div>

            <button
              type="submit"
              disabled={evaluating}
              className="px-6 py-3 rounded-xl font-bold text-xs sm:text-sm text-white bg-indigo-600 hover:bg-indigo-700 shadow-md shadow-indigo-500/20 flex items-center justify-center gap-2 transition-all w-full sm:w-auto"
            >
              <Play className="w-4 h-4 fill-white" />
              {evaluating ? 'Running Model...' : 'Execute Misconception Classifier'}
            </button>
          </div>

          {/* Model Output Panel */}
          <div className="lg:col-span-5 bg-slate-50 rounded-2xl border border-slate-200 p-6 space-y-5">
            <div className="flex items-center justify-between border-b border-slate-200/80 pb-3">
              <span className="text-xs font-extrabold uppercase tracking-wider text-slate-500">
                Inference Results
              </span>
              <span className="text-[11px] font-mono text-indigo-600 font-bold">
                Latency: ~8ms
              </span>
            </div>

            {predResult ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-500 font-semibold">Predicted Category:</span>
                  <MisconceptionBadge
                    category={predResult.predicted_misconception}
                    showConfidence
                    confidence={predResult.confidence}
                  />
                </div>

                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs font-semibold text-slate-700">
                    <span>Classification Confidence:</span>
                    <span className="font-mono text-indigo-700 font-bold">
                      {Math.round(predResult.confidence * 100)}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                    <div
                      className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${Math.round(predResult.confidence * 100)}%` }}
                    />
                  </div>
                </div>

                <div className="bg-white rounded-xl border border-slate-200 p-3.5 space-y-1.5 text-xs">
                  <span className="font-bold text-slate-900 block">Cognitive Root Cause:</span>
                  <p className="text-slate-600 leading-relaxed">
                    {predResult.metadata?.description || predResult.reason}
                  </p>
                  <p className="text-indigo-800 font-semibold text-[11px] pt-1 border-t border-slate-100">
                    Prerequisite Target: {predResult.metadata?.prerequisite_concept}
                  </p>
                </div>

                {/* Probability distribution breakdown */}
                <div className="space-y-2 pt-2 border-t border-slate-200">
                  <span className="text-[10px] font-bold text-slate-500 uppercase block">
                    Full Class Probabilities:
                  </span>
                  {Object.entries(predResult.class_probabilities || {}).map(([cls, p]) => (
                    <div key={cls} className="space-y-1">
                      <div className="flex justify-between text-[11px] text-slate-600 font-medium">
                        <span className="truncate max-w-[200px]">{cls.replace(/_/g, ' ')}</span>
                        <span className="font-mono text-slate-700 font-bold">{Math.round(p * 100)}%</span>
                      </div>
                      <div className="w-full bg-slate-200 rounded-full h-1">
                        <div
                          className={`h-1 rounded-full ${
                            cls === predResult.predicted_misconception ? 'bg-indigo-600' : 'bg-slate-400'
                          }`}
                          style={{ width: `${Math.round(p * 100)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-slate-400 space-y-2">
                <BrainCircuit className="w-10 h-10 text-slate-300 mx-auto" />
                <p className="text-xs">
                  Select a preset or click "Execute Misconception Classifier" to inspect model predictions.
                </p>
              </div>
            )}
          </div>
        </form>
      </div>

      {/* Confusion Matrix & Classification Report */}
      {metrics && (
        <div className="grid lg:grid-cols-12 gap-8 items-start">
          {/* Confusion Matrix Table */}
          <div className="lg:col-span-7 bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Test Holdout Confusion Matrix (N = {metrics.sample_counts.test_samples})
                </h3>
                <p className="text-xs text-slate-500">
                  Actual classes (rows) vs. Model predictions (columns)
                </p>
              </div>
            </div>

            <div className="overflow-x-auto pt-2">
              <table className="w-full text-center text-[11px]">
                <thead>
                  <tr className="text-slate-400 text-[10px] uppercase font-semibold">
                    <th className="text-left py-2 px-2">True \ Pred</th>
                    {metrics.confusion_matrix.labels.map((lbl, idx) => (
                      <th key={idx} className="py-2 px-1 max-w-[70px] truncate" title={lbl}>
                        C{idx + 1}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono">
                  {metrics.confusion_matrix.matrix.map((row, rIdx) => (
                    <tr key={rIdx}>
                      <td
                        className="text-left font-sans font-semibold text-slate-700 py-2 px-2 max-w-[130px] truncate"
                        title={metrics.confusion_matrix.labels[rIdx]}
                      >
                        C{rIdx + 1}: {metrics.confusion_matrix.labels[rIdx].replace(/_/g, ' ').slice(0, 16)}..
                      </td>
                      {row.map((val, cIdx) => {
                        const isDiag = rIdx === cIdx;
                        const cellColor =
                          isDiag && val > 0
                            ? 'bg-emerald-50 text-emerald-800 font-bold border border-emerald-200'
                            : val > 0
                            ? 'bg-rose-50 text-rose-800 font-bold'
                            : 'text-slate-300';
                        return (
                          <td key={cIdx} className={`py-2 px-1 rounded ${cellColor}`}>
                            {val}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="pt-2 text-[10px] text-slate-400 font-mono">
              *Diagonal cells represent true positives (correctly classified misconceptions).
            </div>
          </div>

          {/* Per-Class Metrics */}
          <div className="lg:col-span-5 bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-slate-900">Per-Class Performance</h3>
            <div className="space-y-2.5">
              {Object.entries(metrics.per_class_metrics).map(([cls, met]) => (
                <div key={cls} className="p-3 rounded-xl border border-slate-100 bg-slate-50/70 space-y-1">
                  <div className="flex items-center justify-between text-xs font-bold text-slate-800">
                    <span className="truncate max-w-[200px]">{cls.replace(/_/g, ' ')}</span>
                    <span className="font-mono text-indigo-600">F1: {met.f1_score}</span>
                  </div>
                  <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono">
                    <span>Prec: {met.precision}</span>
                    <span>Recall: {met.recall}</span>
                    <span>Support: {met.support}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
