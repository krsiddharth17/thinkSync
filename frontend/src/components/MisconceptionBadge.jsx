import React from 'react';
import {
  AlertTriangle,
  RotateCcw,
  Plus,
  Minus,
  Calculator,
  Divide,
  PieChart,
  CheckCircle2,
  HelpCircle
} from 'lucide-react';

const BADGE_CONFIG = {
  inverse_operation_error: {
    label: 'Inverse Operation Error',
    bg: 'bg-amber-50 text-amber-800 border-amber-200',
    dot: 'bg-amber-500',
    icon: RotateCcw,
    desc: 'Flipped addition/subtraction or multiplication/division during equation balancing.',
  },
  sign_error: {
    label: 'Sign / Integer Error',
    bg: 'bg-rose-50 text-rose-800 border-rose-200',
    dot: 'bg-rose-500',
    icon: Plus,
    desc: 'Dropped negative sign or misapplied negative multiplication/distribution.',
  },
  arithmetic_calculation_error: {
    label: 'Arithmetic Calculation Slip',
    bg: 'bg-blue-50 text-blue-800 border-blue-200',
    dot: 'bg-blue-500',
    icon: Calculator,
    desc: 'Correct conceptual steps, but minor mental math or times-table slip.',
  },
  multiplication_division_error: {
    label: 'Mult / Div Inversion',
    bg: 'bg-purple-50 text-purple-800 border-purple-200',
    dot: 'bg-purple-500',
    icon: Divide,
    desc: 'Inverted numerator/denominator order or failed reciprocal multiplication.',
  },
  conceptual_misunderstanding: {
    label: 'Conceptual Misunderstanding',
    bg: 'bg-red-50 text-red-800 border-red-200',
    dot: 'bg-red-500',
    icon: AlertTriangle,
    desc: 'Combined unlike terms or misinterpreted foundational rules.',
  },
  fraction_operation_error: {
    label: 'Fraction Operation Error',
    bg: 'bg-teal-50 text-teal-800 border-teal-200',
    dot: 'bg-teal-500',
    icon: PieChart,
    desc: 'Direct addition/subtraction of denominators without finding common LCM.',
  },
  correct: {
    label: 'Correct Solution',
    bg: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    dot: 'bg-emerald-500',
    icon: CheckCircle2,
    desc: 'Solid understanding and accurate intermediate steps.',
  },
  uncertain_insufficient_evidence: {
    label: 'Uncertain / Steps Needed',
    bg: 'bg-slate-100 text-slate-700 border-slate-200',
    dot: 'bg-slate-400',
    icon: HelpCircle,
    desc: 'Incomplete or uninformative steps to pinpoint a single misconception.',
  },
};

export default function MisconceptionBadge({ category, showConfidence, confidence, size = 'md' }) {
  const config = BADGE_CONFIG[category] || {
    label: category ? category.replace(/_/g, ' ') : 'General',
    bg: 'bg-slate-100 text-slate-700 border-slate-200',
    dot: 'bg-slate-400',
    icon: HelpCircle,
    desc: 'Diagnosed pattern',
  };

  const Icon = config.icon;
  const isSm = size === 'sm';

  return (
    <div
      title={config.desc}
      className={`inline-flex items-center gap-1.5 rounded-full border font-medium ${
        config.bg
      } ${isSm ? 'px-2.5 py-0.5 text-xs' : 'px-3 py-1 text-xs sm:text-sm'}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${config.dot}`} />
      <Icon className={isSm ? 'w-3 h-3' : 'w-3.5 h-3.5'} />
      <span>{config.label}</span>
      {showConfidence && confidence !== undefined && (
        <span className="ml-1 opacity-75 font-mono text-[11px]">
          ({Math.round(confidence * 100)}%)
        </span>
      )}
    </div>
  );
}
