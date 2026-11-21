import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  Scale,
  PieChart as PieIcon,
  Percent,
  Binary,
  ArrowRight,
  Lightbulb,
  AlertTriangle,
  CheckCircle2
} from 'lucide-react';

const CONCEPTS_DATA = [
  {
    id: 'linear-equations',
    title: 'Linear Equations & Balancing',
    slug: 'linear-equations',
    icon: Scale,
    summary: 'Mastering single-variable equations, inverse operations, and preserving equality.',
    principles: [
      {
        name: 'The Playground See-Saw Balance Principle',
        desc: 'An equation states that whatever is on the left side has the exact same value as what is on the right side. To preserve balance, any operation applied to one side must be applied equally to the other.'
      },
      {
        name: 'Inverse Operation Table',
        desc: 'Undo addition with subtraction (+c -> -c), undo subtraction with addition (-c -> +c), undo multiplication with division (×a -> ÷a), and undo division with multiplication (÷a -> ×a).'
      }
    ],
    pitfalls: [
      {
        name: 'Operation Reversal Slip',
        desc: 'In 2x + 7 = 19, students frequently add 7 to 19 to get 26 instead of subtracting 7 to get 12.'
      },
      {
        name: 'Dropping Negative Signs',
        desc: 'When solving -3x = 12, dividing by -3 gives -4, not +4. A negative divided by a positive is always negative.'
      }
    ]
  },
  {
    id: 'fractions',
    title: 'Fractions & Proportions',
    slug: 'fractions',
    icon: PieIcon,
    summary: 'Fraction arithmetic, finding common denominators, and reciprocal division rules.',
    principles: [
      {
        name: 'Common Denominator (Equal Slices Rule)',
        desc: 'Fractions represent equal parts of a whole. You cannot add 1/3 and 1/4 directly because thirds and fourths are different slice sizes! Both must be converted to twelfths (4/12 + 3/12 = 7/12).'
      },
      {
        name: 'Fraction Division: Keep, Change, Flip',
        desc: 'Dividing by a fraction is identical to multiplying by its reciprocal. (2/3) ÷ (4/5) becomes (2/3) × (5/4) = 10/12 = 5/6.'
      }
    ],
    pitfalls: [
      {
        name: 'Direct Denominator Addition Trap',
        desc: 'Writing 1/3 + 1/4 = 2/7. Adding across tops and bottoms breaks the fractional unit logic.'
      },
      {
        name: 'Flipping the Wrong Fraction',
        desc: 'In division, you must flip the divisor (the second fraction), never the dividend (the first fraction).'
      }
    ]
  },
  {
    id: 'percentages',
    title: 'Percentages & Conversions',
    slug: 'percentages',
    icon: Percent,
    summary: 'Understanding percent as per hundred, discounts, markups, and proportions.',
    principles: [
      {
        name: 'Percent Means Per Hundred',
        desc: 'P% of N is calculated as (P / 100) × N. For example, 20% of 80 is (20/100) × 80 = 0.20 × 80 = 16.'
      },
      {
        name: 'Discounts and Sale Prices',
        desc: 'A 20% discount on an $80 item means you save $16. The final sale price is $80 - $16 = $64.'
      }
    ],
    pitfalls: [
      {
        name: 'Flat Subtraction Error',
        desc: 'Students often subtract the percent number directly like a dollar amount (e.g. 80 - 20 = 60 instead of 80 - 16 = 64).'
      },
      {
        name: 'Omission of Division by 100',
        desc: 'Calculating 25% of 160 by multiplying 25 × 160 = 4000 and forgetting to divide by 100.'
      }
    ]
  },
  {
    id: 'basic-algebra',
    title: 'Basic Algebra & Term Grouping',
    slug: 'basic-algebra',
    icon: Binary,
    summary: 'Combining like terms, distributive property, and preserving negative signs.',
    principles: [
      {
        name: 'Like Terms Must Share Variable and Exponent',
        desc: 'Terms like 3x and 5x can be added together to form 8x. Terms with different variables (like 3x and 4y) cannot be combined.'
      },
      {
        name: 'Distributive Property with Signs',
        desc: '-2(3x - 4) = (-2)(3x) + (-2)(-4) = -6x + 8. Multiplying two negatives always yields a positive.'
      }
    ],
    pitfalls: [
      {
        name: 'Unlike Term Fusion',
        desc: 'Combining 4x + 5 into 9x. A variable term cannot be added into a constant term.'
      },
      {
        name: 'Negative Sign Non-Distribution',
        desc: 'In -3(2x - 5), failing to multiply -3 by -5, writing -6x - 15 instead of -6x + 15.'
      }
    ]
  }
];

export default function ConceptsPage() {
  const [activeTab, setActiveTab] = useState(CONCEPTS_DATA[0].id);
  const activeConcept = CONCEPTS_DATA.find((c) => c.id === activeTab) || CONCEPTS_DATA[0];
  const Icon = activeConcept.icon;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Header */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-xs font-bold text-indigo-700">
          <BookOpen className="w-3.5 h-3.5" />
          <span>Foundational Mathematical Principles</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Concept Reference & Remediation Library
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 max-w-2xl">
          Review core foundational concepts and common cognitive stumbling blocks to avoid recurring misconception flags.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-2">
        {CONCEPTS_DATA.map((c) => {
          const TabIcon = c.icon;
          const isSelected = activeTab === c.id;
          return (
            <button
              key={c.id}
              onClick={() => setActiveTab(c.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-2xl text-xs sm:text-sm font-bold transition-all ${
                isSelected
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/20'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              <TabIcon className="w-4 h-4" />
              <span>{c.title}</span>
            </button>
          );
        })}
      </div>

      {/* Active Concept Details */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-10 shadow-sm space-y-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600">
              <Icon className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900">{activeConcept.title}</h2>
              <p className="text-xs text-slate-500">{activeConcept.summary}</p>
            </div>
          </div>

          <Link
            to={`/topics/${activeConcept.slug}`}
            className="px-5 py-2.5 rounded-xl font-bold text-xs sm:text-sm text-white bg-indigo-600 hover:bg-indigo-700 shadow-md shadow-indigo-500/20 flex items-center gap-2 transition-all self-start sm:self-center"
          >
            Practice This Topic
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* Core Principles */}
        <div className="space-y-4">
          <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-900 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            Core Foundational Principles
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {activeConcept.principles.map((p, i) => (
              <div key={i} className="p-4 rounded-2xl border border-slate-200/80 bg-slate-50/70 space-y-2">
                <h4 className="font-bold text-slate-900 text-xs sm:text-sm">{p.name}</h4>
                <p className="text-xs text-slate-600 leading-relaxed">{p.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Pitfalls to Avoid */}
        <div className="space-y-4 pt-4 border-t border-slate-100">
          <h3 className="text-sm font-extrabold uppercase tracking-wider text-rose-900 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-500" />
            Common Traps Identified by thinkSync ML
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {activeConcept.pitfalls.map((pit, i) => (
              <div key={i} className="p-4 rounded-2xl border border-rose-200/80 bg-rose-50/50 space-y-2">
                <h4 className="font-bold text-rose-950 text-xs sm:text-sm">{pit.name}</h4>
                <p className="text-xs text-slate-700 leading-relaxed">{pit.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
