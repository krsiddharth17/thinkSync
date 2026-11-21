import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { studentApi } from '../api/client';
import {
  BrainCircuit,
  Scale,
  PieChart as PieIcon,
  Percent,
  Binary,
  CheckCircle2,
  TrendingUp,
  Target,
  Sparkles,
  AlertTriangle,
  ArrowRight,
  BookOpen,
  RotateCcw,
  Clock,
  Layers
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  CartesianGrid
} from 'recharts';
import MetricCard from '../components/MetricCard';
import MisconceptionBadge from '../components/MisconceptionBadge';

export default function StudentDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const iconMap = {
    Scale: Scale,
    PieChart: PieIcon,
    Percent: Percent,
    Binary: Binary,
  };

  useEffect(() => {
    async function fetchDashboard() {
      try {
        setLoading(true);
        const res = await studentApi.getDashboard();
        setData(res);
      } catch (err) {
        console.error('Dashboard fetch error:', err);
        setError(err.message || 'Could not load student dashboard');
      } finally {
        setLoading(false);
      }
    }
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 rounded-full border-4 border-indigo-200 border-t-indigo-600 animate-spin" />
        <p className="text-sm font-semibold text-slate-500">Loading your learning profile & ML analytics...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="max-w-md mx-auto my-16 bg-white p-6 rounded-2xl border border-rose-200 text-center space-y-4 shadow-sm">
        <AlertTriangle className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-lg font-bold text-slate-900">Unable to load dashboard</h3>
        <p className="text-xs text-slate-500">{error || 'Please sign in to view your learning records.'}</p>
        <Link
          to="/login"
          className="inline-block px-4 py-2 text-xs font-bold text-white bg-indigo-600 rounded-xl"
        >
          Sign In
        </Link>
      </div>
    );
  }

  const { overview, topics, misconception_distribution, timeline, recent_activity } = data;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Welcome & Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-indigo-900 via-indigo-800 to-purple-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-700/60 border border-indigo-500/40 text-xs font-semibold text-indigo-200">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>Personalized AI Learning Profile</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome back, {data.user_profile?.full_name || 'Student'}!
          </h1>
          <p className="text-xs sm:text-sm text-indigo-200/80 max-w-xl">
            Our Machine Learning diagnostic engine is tracking your solving strategies across 4 mathematics domains.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/topics/linear-equations"
            className="px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-white text-indigo-900 hover:bg-indigo-50 shadow-md transition-all flex items-center gap-2"
          >
            Start Practice
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            to="/concepts"
            className="px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-indigo-800/80 hover:bg-indigo-700 border border-indigo-500/50 text-white transition-all flex items-center gap-2"
          >
            <BookOpen className="w-4 h-4" />
            Guides
          </Link>
        </div>
      </div>

      {/* Adaptive Recommendation Alert (if top bottleneck detected) */}
      {overview.top_bottleneck && overview.top_bottleneck.count >= 2 && (
        <div className="bg-amber-50 border border-amber-300/80 rounded-2xl p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
          <div className="flex items-start gap-3">
            <div className="p-2.5 rounded-xl bg-amber-100 text-amber-800 shrink-0">
              <RotateCcw className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-extrabold uppercase tracking-wider text-amber-800">
                  Adaptive Engine Alert: Recurring Bottleneck
                </span>
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-amber-200 text-amber-900 font-bold">
                  {overview.top_bottleneck.count} Occurrences
                </span>
              </div>
              <p className="text-xs sm:text-sm text-slate-700 font-medium mt-0.5">
                We've noticed repeated <strong className="text-amber-950 font-bold">{overview.top_bottleneck.name}</strong> patterns in your recent work. Revisiting foundational equation balance rules will unlock your next mastery tier.
              </p>
            </div>
          </div>
          <Link
            to="/concepts"
            className="px-4 py-2 rounded-xl text-xs font-bold text-amber-900 bg-amber-200/80 hover:bg-amber-300 border border-amber-400 shrink-0 self-start sm:self-center transition-all"
          >
            Review Concept Guide
          </Link>
        </div>
      )}

      {/* Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <MetricCard
          title="Overall Mastery"
          value={`${overview.average_mastery}%`}
          subtitle="Weighted across all topics"
          icon={Target}
          color="indigo"
          badge={overview.average_mastery >= 75 ? 'Proficient' : 'Developing'}
        />
        <MetricCard
          title="Accuracy Rate"
          value={`${overview.overall_accuracy}%`}
          subtitle={`${overview.correct_attempts} of ${overview.total_attempts} questions correct`}
          icon={CheckCircle2}
          color="emerald"
        />
        <MetricCard
          title="Total Attempts"
          value={overview.total_attempts}
          subtitle="Diagnostics & practice runs"
          icon={TrendingUp}
          color="purple"
        />
        <MetricCard
          title="Primary Bottleneck"
          value={overview.top_bottleneck ? overview.top_bottleneck.name.split(' ')[0] : 'None'}
          subtitle={overview.top_bottleneck ? `${overview.top_bottleneck.count} flagged instances` : 'Great consistency!'}
          icon={AlertTriangle}
          color="amber"
        />
      </div>

      {/* Topic Mastery Progress Cards */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-900">Topic Mastery Progress</h2>
            <p className="text-xs text-slate-500">Track and advance your mathematical foundation across domains</p>
          </div>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {topics.map((t) => {
            const Icon = iconMap[t.icon] || Scale;
            return (
              <div
                key={t.topic_id}
                className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm card-hover-effect flex flex-col justify-between"
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600">
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="text-xs font-bold font-mono px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                      {Math.round(t.mastery_score)}%
                    </span>
                  </div>

                  <div>
                    <h3 className="font-bold text-slate-900 text-base">{t.topic_name}</h3>
                    <p className="text-xs text-slate-500 mt-0.5">
                      {t.attempts_count} attempts • {t.accuracy}% accuracy
                    </p>
                  </div>

                  {/* Progress bar */}
                  <div className="space-y-1">
                    <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                      <div
                        className="h-2 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 transition-all duration-500"
                        style={{ width: `${Math.max(5, t.mastery_score)}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="mt-5 pt-4 border-t border-slate-100">
                  <Link
                    to={`/topics/${t.topic_slug}`}
                    className="w-full py-2 rounded-xl text-xs font-bold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 flex items-center justify-center gap-1.5 transition-colors"
                  >
                    Practice Diagnostic
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Analytics Charts Section (Recharts) */}
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Misconception Frequency Bar Chart */}
        <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-base text-slate-900">
                Cognitive Misconception Distribution
              </h3>
              <p className="text-xs text-slate-500">
                Machine learning classified error categories across all attempts
              </p>
            </div>
            <span className="text-xs font-semibold px-2 py-1 rounded bg-indigo-50 text-indigo-700 border border-indigo-200">
              Scikit-Learn Model
            </span>
          </div>

          <div className="h-64 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={misconception_distribution.filter((d) => d.count > 0)}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" horizontal vertical={false} stroke="#f1f5f9" />
                <XAxis type="number" allowDecimals={false} stroke="#94a3b8" fontSize={11} />
                <YAxis
                  dataKey="name"
                  type="category"
                  stroke="#64748b"
                  fontSize={10}
                  width={110}
                  tickFormatter={(val) => (val.length > 18 ? `${val.slice(0, 16)}..` : val)}
                />
                <Tooltip
                  formatter={(value) => [`${value} instances`, 'Occurrences']}
                  contentStyle={{ backgroundColor: '#1e293b', color: '#fff', borderRadius: '8px', fontSize: '12px' }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[11px] text-slate-500 italic text-center">
            *Shows error categories isolated by the trained classifier from your intermediate step notations.
          </p>
        </div>

        {/* Learning Progress Over Time */}
        <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-base text-slate-900">
                Learning Trajectory Over Time
              </h3>
              <p className="text-xs text-slate-500">
                Cumulative accuracy and problem solving progression
              </p>
            </div>
            <span className="text-xs font-semibold px-2 py-1 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
              Adaptive Curve
            </span>
          </div>

          <div className="h-64 w-full pt-4">
            {timeline.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={timeline} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="accGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="attempt_number" stroke="#94a3b8" fontSize={11} label={{ value: 'Attempt #', position: 'insideBottom', offset: -2 }} />
                  <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={11} tickFormatter={(v) => `${v}%`} />
                  <Tooltip
                    formatter={(val) => [`${val}%`, 'Cumulative Accuracy']}
                    contentStyle={{ backgroundColor: '#1e293b', color: '#fff', borderRadius: '8px', fontSize: '12px' }}
                  />
                  <Area
                    type="monotone"
                    dataKey="cumulative_accuracy"
                    stroke="#10b981"
                    strokeWidth={2.5}
                    fillOpacity={1}
                    fill="url(#accGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                No attempt timeline data available yet.
              </div>
            )}
          </div>
          <p className="text-[11px] text-slate-500 italic text-center">
            *Chronological trajectory of attempts showing continuous improvement through targeted feedback.
          </p>
        </div>
      </div>

      {/* Recent Diagnostic Activity Stream */}
      <div className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm space-y-5">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-900">Recent Diagnostic Evaluations</h3>
            <p className="text-xs text-slate-500">
              Detailed step inspections and Socratic feedback from your latest problem attempts
            </p>
          </div>
        </div>

        <div className="space-y-3">
          {recent_activity.length > 0 ? (
            recent_activity.map((item) => (
              <div
                key={item.attempt_id}
                className="p-4 rounded-2xl border border-slate-100 hover:border-slate-200 bg-slate-50/60 space-y-2 transition-colors"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold px-2 py-0.5 rounded bg-indigo-100 text-indigo-800">
                      {item.topic_name}
                    </span>
                    <span className="text-xs text-slate-400 font-mono flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {item.created_at}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MisconceptionBadge
                      category={item.predicted_misconception}
                      showConfidence
                      confidence={item.ml_confidence / 100}
                      size="sm"
                    />
                  </div>
                </div>

                <div className="text-xs font-mono font-medium text-slate-800">
                  Q: {item.question_text}
                </div>

                <div className="grid sm:grid-cols-2 gap-2 text-xs bg-white p-3 rounded-xl border border-slate-200/80">
                  <div>
                    <span className="text-slate-400 font-semibold block text-[10px] uppercase">
                      Your Submitted Answer:
                    </span>
                    <span className="font-mono font-bold text-slate-800">{item.student_answer}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 font-semibold block text-[10px] uppercase">
                      Intermediate Steps Provided:
                    </span>
                    <span className="font-mono text-slate-700 whitespace-pre-line text-[11px]">
                      {item.intermediate_steps || 'None entered'}
                    </span>
                  </div>
                </div>

                {item.feedback?.mistake_analysis && (
                  <div className="text-xs bg-indigo-50/70 border border-indigo-100 p-3 rounded-xl text-indigo-950 space-y-1">
                    <p className="font-bold flex items-center gap-1.5 text-indigo-900">
                      <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                      AI Socratic Feedback:
                    </p>
                    <p className="text-slate-700">{item.feedback.mistake_analysis}</p>
                    {item.feedback.socratic_hint && (
                      <p className="text-indigo-800 font-medium pt-1">
                        💡 Hint for next time: {item.feedback.socratic_hint}
                      </p>
                    )}
                  </div>
                )}
              </div>
            ))
          ) : (
            <p className="text-xs text-slate-400 text-center py-6">No recent assessments completed yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}
