import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { teacherApi } from '../api/client';
import {
  Users,
  BrainCircuit,
  AlertTriangle,
  CheckCircle2,
  TrendingUp,
  Cpu,
  GraduationCap,
  Sparkles,
  ArrowRight,
  ShieldAlert,
  Search,
  Filter,
  BarChart3
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell
} from 'recharts';
import MetricCard from '../components/MetricCard';
import MisconceptionBadge from '../components/MisconceptionBadge';

export default function TeacherDashboard() {
  const { user, isTeacher, quickSwitch } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterInterventionOnly, setFilterInterventionOnly] = useState(false);

  useEffect(() => {
    async function fetchTeacherData() {
      try {
        setLoading(true);
        // If not logged in as teacher, attempt quickSwitch or fetch
        let res;
        try {
          res = await teacherApi.getDashboard();
        } catch (authErr) {
          // Auto switch to teacher demo if unauthorized
          await quickSwitch('teacher');
          res = await teacherApi.getDashboard();
        }
        setData(res);
      } catch (err) {
        console.error('Failed to load teacher dashboard:', err);
        setError(err.message || 'Could not load teacher dashboard');
      } finally {
        setLoading(false);
      }
    }
    fetchTeacherData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
        <p className="text-xs font-semibold text-slate-500">Aggregating classroom cognitive analytics & ML data...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="max-w-md mx-auto my-16 bg-white p-6 rounded-2xl border border-rose-200 text-center space-y-4">
        <AlertTriangle className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-lg font-bold text-slate-900">Teacher Portal Access Required</h3>
        <p className="text-xs text-slate-500">{error || 'Please sign in with a teacher account.'}</p>
        <button
          onClick={() => quickSwitch('teacher').then(() => window.location.reload())}
          className="px-4 py-2 text-xs font-bold text-white bg-indigo-600 rounded-xl"
        >
          Sign In as Demo Teacher
        </button>
      </div>
    );
  }

  const { overview, misconception_distribution, topics_difficulty, students, recent_stream } = data;

  const filteredStudents = students.filter((s) => {
    const matchesSearch =
      s.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.top_bottleneck.toLowerCase().includes(searchTerm.toLowerCase());
    if (filterInterventionOnly) {
      return matchesSearch && s.needs_intervention;
    }
    return matchesSearch;
  });

  const barColors = ['#6366f1', '#f59e0b', '#ec4899', '#14b8a6', '#8b5cf6', '#ef4444'];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Teacher Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm">
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-50 border border-purple-200 text-xs font-bold text-purple-700">
            <GraduationCap className="w-3.5 h-3.5" />
            <span>Teacher & Administrator Cognitive Command Center</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Classroom Learning & Bottleneck Analytics
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
            Real-time cognitive diagnostics aggregated across all student intermediate solving attempts.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/ml-playground"
            className="px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 transition-all flex items-center gap-2"
          >
            <Cpu className="w-4 h-4 text-indigo-600" />
            Inspect ML Classifier
          </Link>
        </div>
      </div>

      {/* Classroom Overview Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <MetricCard
          title="Active Students"
          value={overview.total_students}
          subtitle="Enrolled learners"
          icon={Users}
          color="indigo"
        />
        <MetricCard
          title="Class Average Mastery"
          value={`${overview.average_mastery}%`}
          subtitle="Across all math topics"
          icon={TrendingUp}
          color="emerald"
        />
        <MetricCard
          title="Diagnostic Attempts"
          value={overview.total_assessments}
          subtitle={`${overview.class_accuracy}% overall accuracy`}
          icon={CheckCircle2}
          color="purple"
        />
        <MetricCard
          title="Top Class Bottleneck"
          value={overview.top_recurring_misconception.split(' ')[0]}
          subtitle="Most common error pattern"
          icon={AlertTriangle}
          color="amber"
          badge="High Priority"
        />
      </div>

      {/* Analytics Charts (Classroom Misconception Breakdown & Topic Difficulty) */}
      <div className="grid lg:grid-cols-12 gap-8">
        {/* Class Misconception Distribution Chart */}
        <div className="lg:col-span-7 bg-white rounded-3xl border border-slate-200 p-6 sm:p-7 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-base text-slate-900">
                Classroom Misconception Frequency
              </h3>
              <p className="text-xs text-slate-500">
                Which mathematical traps are confusing the most students?
              </p>
            </div>
            <span className="text-xs font-semibold px-2 py-1 rounded bg-slate-100 text-slate-700">
              Aggregated from Steps
            </span>
          </div>

          <div className="h-64 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={misconception_distribution}
                margin={{ top: 10, right: 20, left: 0, bottom: 25 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis
                  dataKey="name"
                  stroke="#94a3b8"
                  fontSize={10}
                  interval={0}
                  angle={-15}
                  textAnchor="end"
                />
                <YAxis allowDecimals={false} stroke="#94a3b8" fontSize={11} />
                <Tooltip
                  formatter={(val, name, props) => [
                    `${val} occurrences (${props.payload.percentage}% of mistakes)`,
                    'Frequency',
                  ]}
                  contentStyle={{ backgroundColor: '#1e293b', color: '#fff', borderRadius: '8px', fontSize: '12px' }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {misconception_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={barColors[index % barColors.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[11px] text-slate-500 text-center italic">
            *Identified by our trained Scikit-learn Classifier from student intermediate steps.
          </p>
        </div>

        {/* Concept Difficulty & Error Rates */}
        <div className="lg:col-span-5 bg-white rounded-3xl border border-slate-200 p-6 sm:p-7 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-base text-slate-900">
                Topics Ranked by Difficulty
              </h3>
              <p className="text-xs text-slate-500">
                Highest error rates requiring teacher review
              </p>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            {topics_difficulty.map((t, idx) => (
              <div
                key={t.topic_id}
                className="p-3.5 rounded-2xl border border-slate-100 bg-slate-50/70 space-y-2"
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-slate-900">{t.name}</span>
                  <span className="font-mono font-bold text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                    {t.error_rate}% Error Rate
                  </span>
                </div>

                <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
                  <div
                    className="h-1.5 rounded-full bg-rose-500"
                    style={{ width: `${Math.min(100, t.error_rate)}%` }}
                  />
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-500">
                  <span>{t.total_attempts} student attempts</span>
                  <span className="font-medium text-amber-700">
                    Primary trap: {t.primary_misconception}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Student Roster & Teacher Intervention Alerts Table */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-5">
          <div>
            <h3 className="text-xl font-bold text-slate-900">
              Student Diagnostic Roster & Intervention Alerts
            </h3>
            <p className="text-xs text-slate-500">
              Personalized cognitive profiling identifies students who need targeted instruction before falling behind
            </p>
          </div>

          {/* Search and filters */}
          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search student or bottleneck..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-slate-50 w-48 sm:w-64"
              />
            </div>
            <button
              onClick={() => setFilterInterventionOnly(!filterInterventionOnly)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-colors ${
                filterInterventionOnly
                  ? 'bg-rose-50 text-rose-700 border-rose-300'
                  : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
              }`}
            >
              {filterInterventionOnly ? 'Showing Interventions' : 'All Students'}
            </button>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-b border-slate-200">
              <tr>
                <th className="py-3 px-4">Student</th>
                <th className="py-3 px-4">Grade</th>
                <th className="py-3 px-4">Attempts</th>
                <th className="py-3 px-4">Avg Mastery</th>
                <th className="py-3 px-4">Primary Misconception</th>
                <th className="py-3 px-4">Intervention Status</th>
                <th className="py-3 px-4">Recommended Teacher Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredStudents.map((s) => (
                <tr key={s.student_id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3.5 px-4">
                    <div className="font-bold text-slate-900">{s.full_name}</div>
                    <div className="text-[10px] text-slate-400 font-mono">@{s.username}</div>
                  </td>
                  <td className="py-3.5 px-4 font-medium text-slate-600">{s.grade}</td>
                  <td className="py-3.5 px-4 font-mono font-semibold text-slate-700">
                    {s.total_attempts} ({s.accuracy}%)
                  </td>
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-slate-800">{s.average_mastery}%</span>
                      <div className="w-16 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                        <div
                          className="h-1.5 rounded-full bg-indigo-600"
                          style={{ width: `${Math.min(100, s.average_mastery)}%` }}
                        />
                      </div>
                    </div>
                  </td>
                  <td className="py-3.5 px-4">
                    {s.top_bottleneck !== 'None detected' ? (
                      <span className="inline-block px-2 py-1 rounded bg-amber-50 text-amber-900 border border-amber-200 font-semibold text-[11px]">
                        {s.top_bottleneck} ({s.bottleneck_count}x)
                      </span>
                    ) : (
                      <span className="text-slate-400">None detected</span>
                    )}
                  </td>
                  <td className="py-3.5 px-4">
                    {s.needs_intervention ? (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rose-50 text-rose-700 border border-rose-200">
                        <ShieldAlert className="w-3 h-3 text-rose-500" />
                        Needs Review
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                        <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                        On Track
                      </span>
                    )}
                  </td>
                  <td className="py-3.5 px-4 text-slate-700 font-medium">
                    {s.intervention_action}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Live Classroom Submissions Stream */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-900">Live Classroom Diagnostics Stream</h3>
            <p className="text-xs text-slate-500">Real-time incoming submissions and classifier outputs</p>
          </div>
          <span className="text-xs font-mono font-bold text-emerald-600 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            Live Feed
          </span>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {recent_stream.slice(0, 6).map((item) => (
            <div
              key={item.attempt_id}
              className="p-4 rounded-2xl border border-slate-100 bg-slate-50/70 space-y-2 text-xs"
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-900">{item.student_name}</span>
                <span className="text-[10px] text-slate-400 font-mono">{item.created_at}</span>
              </div>
              <p className="font-mono text-slate-600 truncate">{item.question_text}</p>
              <div className="flex items-center justify-between pt-1 border-t border-slate-200/60">
                <span className="font-bold font-mono text-slate-800">Ans: {item.student_answer}</span>
                <MisconceptionBadge category={item.predicted_misconception} size="sm" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
