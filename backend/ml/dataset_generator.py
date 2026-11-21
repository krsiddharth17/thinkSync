"""
thinkSync AI - ML Dataset Generator
Generates a realistic, diverse, multi-topic labeled dataset for training the Misconception Detection Engine.
Each entry mirrors authentic student behaviors, intermediate step notations, common algebra/arithmetic slips,
and misconceptions across Linear Equations, Fractions, Percentages, and Basic Algebra.
"""

import csv
import os
import random

# Set fixed seed for perfect reproducibility
random.seed(42)

MISCONCEPTION_CATEGORIES = [
    "inverse_operation_error",
    "sign_error",
    "arithmetic_calculation_error",
    "multiplication_division_error",
    "conceptual_misunderstanding",
    "fraction_operation_error",
    "correct",
]

def generate_base_templates():
    templates = []

    # =========================================================================
    # 1. LINEAR EQUATIONS
    # =========================================================================
    # Inverse operation errors
    templates.extend([
        {
            "topic": "linear_equations",
            "question": "Solve for x: 2x + 7 = 19",
            "correct_answer": "6",
            "student_answer": "13",
            "steps": "2x = 19 + 7\n2x = 26\nx = 13",
            "approach": "isolate_variable",
            "label": "inverse_operation_error",
            "notes": "Added 7 instead of subtracting 7 from both sides"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: 3x + 12 = 33",
            "correct_answer": "7",
            "student_answer": "15",
            "steps": "3x = 33 + 12\n3x = 45\nx = 45 / 3 = 15",
            "approach": "isolate_variable",
            "label": "inverse_operation_error",
            "notes": "Added 12 to 33 instead of subtracting"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: x - 9 = 14",
            "correct_answer": "23",
            "student_answer": "5",
            "steps": "x = 14 - 9\nx = 5",
            "approach": "isolate_variable",
            "label": "inverse_operation_error",
            "notes": "Subtracted 9 instead of adding 9 to undo minus 9"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: 4x = 28",
            "correct_answer": "7",
            "student_answer": "112",
            "steps": "x = 28 * 4\nx = 112",
            "approach": "isolate_variable",
            "label": "inverse_operation_error",
            "notes": "Multiplied by 4 instead of dividing by 4 to undo multiplication"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: x / 5 = 6",
            "correct_answer": "30",
            "student_answer": "1.2",
            "steps": "x = 6 / 5\nx = 1.2",
            "approach": "isolate_variable",
            "label": "inverse_operation_error",
            "notes": "Divided by 5 instead of multiplying by 5 to isolate x"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: 5x - 8 = 22",
            "correct_answer": "6",
            "student_answer": "2.8",
            "steps": "5x = 22 - 8\n5x = 14\nx = 14/5 = 2.8",
            "approach": "isolate_variable",
            "label": "inverse_operation_error",
            "notes": "Subtracted 8 from 22 instead of adding 8"
        },
        # Sign errors
        {
            "topic": "linear_equations",
            "question": "Solve for x: -3x = 21",
            "correct_answer": "-7",
            "student_answer": "7",
            "steps": "x = 21 / 3\nx = 7",
            "approach": "isolate_variable",
            "label": "sign_error",
            "notes": "Dropped negative sign when dividing by -3"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: -(2x - 6) = 14",
            "correct_answer": "-4",
            "student_answer": "10",
            "steps": "-2x - 6 = 14\n-2x = 20\nx = 10",
            "approach": "expand_brackets",
            "label": "sign_error",
            "notes": "Failed to distribute negative to -6, making it -6 instead of +6, and dropped negative sign on x"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: 10 - 2x = 4",
            "correct_answer": "3",
            "student_answer": "-3",
            "steps": "-2x = 4 - 10\n-2x = -6\nx = -3",
            "approach": "isolate_variable",
            "label": "sign_error",
            "notes": "Divided -6 by -2 and ended up with negative result instead of positive"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: -4x - 5 = 15",
            "correct_answer": "-5",
            "student_answer": "5",
            "steps": "-4x = 20\nx = 20 / 4 = 5",
            "approach": "isolate_variable",
            "label": "sign_error",
            "notes": "Forgot to keep negative when dividing 20 by -4"
        },
        # Arithmetic calculation errors
        {
            "topic": "linear_equations",
            "question": "Solve for x: 3x + 14 = 32",
            "correct_answer": "6",
            "student_answer": "5.67",
            "steps": "3x = 32 - 14\n3x = 17\nx = 17 / 3",
            "approach": "isolate_variable",
            "label": "arithmetic_calculation_error",
            "notes": "Correct algebra steps but calculated 32 - 14 = 17 instead of 18"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: 4x + 15 = 47",
            "correct_answer": "8",
            "student_answer": "7.75",
            "steps": "4x = 47 - 15\n4x = 31\nx = 31/4",
            "approach": "isolate_variable",
            "label": "arithmetic_calculation_error",
            "notes": "Subtracted 47 - 15 and got 31 instead of 32"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: 6x - 7 = 41",
            "correct_answer": "8",
            "student_answer": "7.83",
            "steps": "6x = 41 + 7\n6x = 47\nx = 47/6",
            "approach": "isolate_variable",
            "label": "arithmetic_calculation_error",
            "notes": "41 + 7 miscalculated as 47 instead of 48"
        },
        # Multiplication / Division errors
        {
            "topic": "linear_equations",
            "question": "Solve for x: 6x = 3",
            "correct_answer": "0.5",
            "student_answer": "2",
            "steps": "x = 6 / 3\nx = 2",
            "approach": "isolate_variable",
            "label": "multiplication_division_error",
            "notes": "Inverted numerator and denominator: divided 6/3 instead of 3/6"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: 8x = 2",
            "correct_answer": "0.25",
            "student_answer": "4",
            "steps": "x = 8 / 2 = 4",
            "approach": "isolate_variable",
            "label": "multiplication_division_error",
            "notes": "Divided coefficient by right side (8/2) instead of right side by coefficient (2/8)"
        },
        # Conceptual misunderstanding
        {
            "topic": "linear_equations",
            "question": "Solve for x: 4x + 5 = 29",
            "correct_answer": "6",
            "student_answer": "3.22",
            "steps": "4x + 5 = 9x\n9x = 29\nx = 29/9",
            "approach": "combine_terms",
            "label": "conceptual_misunderstanding",
            "notes": "Combined unlike terms 4x and 5 to get 9x"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: 2x + 3 = 11",
            "correct_answer": "4",
            "student_answer": "2.2",
            "steps": "5x = 11\nx = 11 / 5 = 2.2",
            "approach": "combine_terms",
            "label": "conceptual_misunderstanding",
            "notes": "Added constant 3 into variable coefficient 2x to make 5x"
        },
        # Correct linear equations
        {
            "topic": "linear_equations",
            "question": "Solve for x: 3x + 8 = 29",
            "correct_answer": "7",
            "student_answer": "7",
            "steps": "3x = 29 - 8\n3x = 21\nx = 21 / 3\nx = 7",
            "approach": "isolate_variable",
            "label": "correct",
            "notes": "Perfect execution of two-step linear equation"
        },
        {
            "topic": "linear_equations",
            "question": "Solve for x: 5x - 4 = 26",
            "correct_answer": "6",
            "student_answer": "6",
            "steps": "5x = 26 + 4\n5x = 30\nx = 30 / 5\nx = 6",
            "approach": "isolate_variable",
            "label": "correct",
            "notes": "Correct inverse addition and division"
        },

        # =========================================================================
        # 2. FRACTIONS
        # =========================================================================
        # Fraction operation errors
        {
            "topic": "fractions",
            "question": "Evaluate: 1/3 + 1/4",
            "correct_answer": "7/12",
            "student_answer": "2/7",
            "steps": "(1 + 1) / (3 + 4) = 2/7",
            "approach": "direct_addition",
            "label": "fraction_operation_error",
            "notes": "Added numerators and added denominators across directly"
        },
        {
            "topic": "fractions",
            "question": "Evaluate: 2/5 + 1/3",
            "correct_answer": "11/15",
            "student_answer": "3/8",
            "steps": "2 + 1 = 3, 5 + 3 = 8 so 3/8",
            "approach": "direct_addition",
            "label": "fraction_operation_error",
            "notes": "Added numerators and denominators directly"
        },
        {
            "topic": "fractions",
            "question": "Evaluate: 3/4 - 1/2",
            "correct_answer": "1/4",
            "student_answer": "2/2",
            "steps": "(3 - 1) / (4 - 2) = 2/2 = 1",
            "approach": "direct_subtraction",
            "label": "fraction_operation_error",
            "notes": "Subtracted numerators and subtracted denominators directly"
        },
        {
            "topic": "fractions",
            "question": "Evaluate: 2/3 divided by 3/4",
            "correct_answer": "8/9",
            "student_answer": "6/12",
            "steps": "(2 * 3) / (3 * 4) = 6/12 = 1/2",
            "approach": "direct_multiplication",
            "label": "fraction_operation_error",
            "notes": "Multiplied fractions straight across without inverting the divisor"
        },
        {
            "topic": "fractions",
            "question": "Evaluate: 3/5 divided by 2/7",
            "correct_answer": "21/10",
            "student_answer": "6/35",
            "steps": "3 * 2 / 5 * 7 = 6/35",
            "approach": "direct_multiplication",
            "label": "fraction_operation_error",
            "notes": "Multiplied straight across instead of multiplying by the reciprocal"
        },
        {
            "topic": "fractions",
            "question": "Evaluate: 1/2 + 2/3",
            "correct_answer": "7/6",
            "student_answer": "3/5",
            "steps": "1 + 2 over 2 + 3 = 3/5",
            "approach": "direct_addition",
            "label": "fraction_operation_error",
            "notes": "Direct addition of tops and bottoms"
        },
        # Arithmetic calculation errors in fractions
        {
            "topic": "fractions",
            "question": "Evaluate: 2/5 + 1/4",
            "correct_answer": "13/20",
            "student_answer": "12/20",
            "steps": "Common denominator is 20\n(8 + 5) / 20 = 12/20",
            "approach": "common_denominator",
            "label": "arithmetic_calculation_error",
            "notes": "Calculated 8 + 5 = 12 instead of 13"
        },
        {
            "topic": "fractions",
            "question": "Evaluate: 5/6 - 1/4",
            "correct_answer": "7/12",
            "student_answer": "8/12",
            "steps": "10/12 - 3/12 = 8/12",
            "approach": "common_denominator",
            "label": "arithmetic_calculation_error",
            "notes": "Subtracted 10 - 3 = 8 instead of 7"
        },
        # Correct fraction operations
        {
            "topic": "fractions",
            "question": "Evaluate: 1/3 + 2/5",
            "correct_answer": "11/15",
            "student_answer": "11/15",
            "steps": "LCM of 3 and 5 is 15\n5/15 + 6/15 = 11/15",
            "approach": "common_denominator",
            "label": "correct",
            "notes": "Correct common denominator and numerator sum"
        },
        {
            "topic": "fractions",
            "question": "Evaluate: 3/4 * 2/5",
            "correct_answer": "3/10",
            "student_answer": "3/10",
            "steps": "(3 * 2) / (4 * 5) = 6/20 = 3/10",
            "approach": "multiply_across",
            "label": "correct",
            "notes": "Multiplied numerators and denominators and simplified"
        },
        {
            "topic": "fractions",
            "question": "Evaluate: 4/7 divided by 2/3",
            "correct_answer": "6/7",
            "student_answer": "6/7",
            "steps": "4/7 * 3/2 = 12/14 = 6/7",
            "approach": "invert_and_multiply",
            "label": "correct",
            "notes": "Inverted second fraction and multiplied"
        },

        # =========================================================================
        # 3. PERCENTAGES
        # =========================================================================
        # Conceptual misunderstanding in percentages
        {
            "topic": "percentages",
            "question": "What is 20% of 80?",
            "correct_answer": "16",
            "student_answer": "60",
            "steps": "80 - 20 = 60",
            "approach": "subtraction",
            "label": "conceptual_misunderstanding",
            "notes": "Subtracted the percentage number 20 from 80 like a dollar amount"
        },
        {
            "topic": "percentages",
            "question": "What is 15% of 60?",
            "correct_answer": "9",
            "student_answer": "45",
            "steps": "60 - 15 = 45",
            "approach": "subtraction",
            "label": "conceptual_misunderstanding",
            "notes": "Treated percent as direct subtraction"
        },
        {
            "topic": "percentages",
            "question": "A shirt costs $50 with a 20% discount. What is the sale price?",
            "correct_answer": "40",
            "student_answer": "30",
            "steps": "50 - 20 = 30",
            "approach": "direct_subtraction",
            "label": "conceptual_misunderstanding",
            "notes": "Deducted 20 directly from 50 instead of calculating 20% of 50 = 10"
        },
        {
            "topic": "percentages",
            "question": "Convert 3/5 into a percentage.",
            "correct_answer": "60%",
            "student_answer": "35%",
            "steps": "Put 3 and 5 together = 35%",
            "approach": "concatenation",
            "label": "conceptual_misunderstanding",
            "notes": "Concatenated numerator and denominator"
        },
        # Multiplication / Division error in percentages
        {
            "topic": "percentages",
            "question": "What is 25% of 160?",
            "correct_answer": "40",
            "student_answer": "4000",
            "steps": "160 * 25 = 4000",
            "approach": "multiply_without_dividing_100",
            "label": "multiplication_division_error",
            "notes": "Multiplied by 25 but forgot to divide by 100 or convert to 0.25"
        },
        {
            "topic": "percentages",
            "question": "What is 30% of 90?",
            "correct_answer": "27",
            "student_answer": "2700",
            "steps": "90 * 30 = 2700",
            "approach": "multiply_without_dividing_100",
            "label": "multiplication_division_error",
            "notes": "Omitted division by 100"
        },
        {
            "topic": "percentages",
            "question": "What percentage of 50 is 15?",
            "correct_answer": "30%",
            "student_answer": "3.33%",
            "steps": "50 / 15 = 3.33",
            "approach": "inverted_ratio",
            "label": "multiplication_division_error",
            "notes": "Divided total by part (50/15) instead of part by total (15/50)"
        },
        # Arithmetic calculation errors in percentages
        {
            "topic": "percentages",
            "question": "What is 15% of 80?",
            "correct_answer": "12",
            "student_answer": "14",
            "steps": "0.15 * 80 = 14",
            "approach": "decimal_multiplication",
            "label": "arithmetic_calculation_error",
            "notes": "Calculated 0.15 * 80 as 14 instead of 12"
        },
        {
            "topic": "percentages",
            "question": "What is 7% of 200?",
            "correct_answer": "14",
            "student_answer": "16",
            "steps": "7 * 2 = 16",
            "approach": "mental_math",
            "label": "arithmetic_calculation_error",
            "notes": "Simple times table mistake: 7 * 2 = 16 instead of 14"
        },
        # Correct percentage problems
        {
            "topic": "percentages",
            "question": "What is 25% of 80?",
            "correct_answer": "20",
            "student_answer": "20",
            "steps": "25/100 * 80 = 1/4 * 80 = 20",
            "approach": "fraction_conversion",
            "label": "correct",
            "notes": "Converted 25% to 1/4 and multiplied correctly"
        },
        {
            "topic": "percentages",
            "question": "What is 15% of 40?",
            "correct_answer": "6",
            "student_answer": "6",
            "steps": "10% is 4, 5% is 2, 4 + 2 = 6",
            "approach": "benchmark_fractions",
            "label": "correct",
            "notes": "Accurate benchmark percentage addition"
        },

        # =========================================================================
        # 4. BASIC ALGEBRA
        # =========================================================================
        # Conceptual misunderstanding (unlike terms, exponent misinterpretations)
        {
            "topic": "basic_algebra",
            "question": "Simplify: 3x + 4y + 2x",
            "correct_answer": "5x + 4y",
            "student_answer": "9xy",
            "steps": "3 + 4 + 2 = 9 so 9xy",
            "approach": "combine_all_terms",
            "label": "conceptual_misunderstanding",
            "notes": "Combined distinct variable terms 3x, 4y, and 2x into a single product"
        },
        {
            "topic": "basic_algebra",
            "question": "Simplify: 5a + 2b - 3a",
            "correct_answer": "2a + 2b",
            "student_answer": "4ab",
            "steps": "5a + 2b = 7ab, 7ab - 3a = 4ab",
            "approach": "combine_all_terms",
            "label": "conceptual_misunderstanding",
            "notes": "Treated variables as additive scalars together"
        },
        {
            "topic": "basic_algebra",
            "question": "Evaluate: x^2 when x = 5",
            "correct_answer": "25",
            "student_answer": "10",
            "steps": "5 * 2 = 10",
            "approach": "multiply_by_power",
            "label": "conceptual_misunderstanding",
            "notes": "Confused exponent power with multiplication by 2"
        },
        {
            "topic": "basic_algebra",
            "question": "Evaluate: 2 + 3 * 4",
            "correct_answer": "14",
            "student_answer": "20",
            "steps": "2 + 3 = 5, 5 * 4 = 20",
            "approach": "left_to_right",
            "label": "conceptual_misunderstanding",
            "notes": "Violated order of operations (PEMDAS) by adding before multiplying"
        },
        # Sign errors in algebra
        {
            "topic": "basic_algebra",
            "question": "Expand: -2(3x - 4)",
            "correct_answer": "-6x + 8",
            "student_answer": "-6x - 8",
            "steps": "-2 * 3x = -6x\n-2 * 4 = -8\nResult: -6x - 8",
            "approach": "distributive_property",
            "label": "sign_error",
            "notes": "Multiplied negative by negative (-2 * -4) and got negative 8 instead of positive 8"
        },
        {
            "topic": "basic_algebra",
            "question": "Simplify: 4 - (x - 3)",
            "correct_answer": "7 - x",
            "student_answer": "1 - x",
            "steps": "4 - x - 3 = 1 - x",
            "approach": "distribute_negative",
            "label": "sign_error",
            "notes": "Did not distribute minus sign to the -3"
        },
        {
            "topic": "basic_algebra",
            "question": "Evaluate: -3^2",
            "correct_answer": "-9",
            "student_answer": "9",
            "steps": "(-3) * (-3) = 9",
            "approach": "bracket_assumption",
            "label": "sign_error",
            "notes": "Assumed brackets around base, squaring negative"
        },
        # Arithmetic calculation errors in algebra
        {
            "topic": "basic_algebra",
            "question": "Simplify: 7x + 8x - 3x",
            "correct_answer": "12x",
            "student_answer": "11x",
            "steps": "7 + 8 = 14, 14 - 3 = 11x",
            "approach": "combine_like_terms",
            "label": "arithmetic_calculation_error",
            "notes": "Miscalculated 7 + 8 as 14 instead of 15"
        },
        {
            "topic": "basic_algebra",
            "question": "Evaluate: 4x + 7 when x = 6",
            "correct_answer": "31",
            "student_answer": "29",
            "steps": "4 * 6 = 22\n22 + 7 = 29",
            "approach": "substitution",
            "label": "arithmetic_calculation_error",
            "notes": "Calculated 4 * 6 = 22 instead of 24"
        },
        # Correct basic algebra
        {
            "topic": "basic_algebra",
            "question": "Simplify: 4x + 7 + 2x - 3",
            "correct_answer": "6x + 4",
            "student_answer": "6x + 4",
            "steps": "4x + 2x = 6x\n7 - 3 = 4\nAnswer: 6x + 4",
            "approach": "combine_like_terms",
            "label": "correct",
            "notes": "Correct grouping of like variable terms and constants"
        },
        {
            "topic": "basic_algebra",
            "question": "Expand: 3(2x - 5)",
            "correct_answer": "6x - 15",
            "student_answer": "6x - 15",
            "steps": "3 * 2x - 3 * 5 = 6x - 15",
            "approach": "distributive_property",
            "label": "correct",
            "notes": "Accurate distribution across both terms"
        },
    ])

    return templates

def generate_augmented_dataset(target_size=850):
    """
    Expands base templates into a diverse dataset with natural language student variations,
    different number scales, typos, step formatting styles, and behavioral noise.
    """
    base_templates = generate_base_templates()
    dataset = []

    # Add all base templates first
    for item in base_templates:
        dataset.append(dict(item))

    # Variation phrases and step styles
    step_styles = [
        "step 1: {s1} -> step 2: {s2}",
        "First {s1}, then {s2}",
        "{s1}\n{s2}",
        "{s1}; {s2}",
        "I did {s1} which gave {s2}",
        "{s1} => {s2} => done"
    ]

    approaches_by_label = {
        "inverse_operation_error": ["isolate_variable", "inverse_operations", "moving_terms", "balancing_equation"],
        "sign_error": ["distribute_negative", "isolate_variable", "expanding_brackets", "integer_rules"],
        "arithmetic_calculation_error": ["mental_math", "scratch_calculation", "standard_algorithm", "combining_terms"],
        "multiplication_division_error": ["division_rule", "cross_multiply", "reciprocal_multiply", "fraction_multiplication"],
        "conceptual_misunderstanding": ["combine_all_terms", "pemdas_left_to_right", "exponent_multiplication", "direct_subtraction"],
        "fraction_operation_error": ["direct_addition", "direct_subtraction", "cross_multiplication", "straight_across"],
        "correct": ["step_by_step_algebra", "common_denominator", "distributive_property", "order_of_operations"]
    }

    # Generate synthetic variations across categories
    while len(dataset) < target_size:
        base = random.choice(base_templates)
        label = base["label"]
        topic = base["topic"]

        # Generate numerical variations with matching misconception logic
        if topic == "linear_equations":
            a = random.randint(2, 9)
            x_val = random.randint(2, 12)
            c = random.randint(3, 25)
            # ax + c = b
            b = a * x_val + c
            q_text = f"Solve for x: {a}x + {c} = {b}"
            corr_ans = str(x_val)

            if label == "inverse_operation_error":
                # Adds c instead of subtracting
                wrong_step1 = f"{a}x = {b} + {c} = {b + c}"
                wrong_ans = f"{(b + c) / a:.2f}".rstrip("0").rstrip(".")
                steps_txt = f"{a}x = {b} + {c}\n{a}x = {b + c}\nx = {wrong_ans}"
            elif label == "sign_error":
                # Solves ax - c = b but flips sign
                q_text = f"Solve for x: -{a}x = {a * x_val}"
                corr_ans = str(-x_val)
                wrong_ans = str(x_val)
                steps_txt = f"x = {a * x_val} / {a}\nx = {wrong_ans}"
            elif label == "arithmetic_calculation_error":
                slip = random.choice([-2, -1, 1, 2])
                wrong_diff = (b - c) + slip
                wrong_ans = f"{wrong_diff / a:.2f}".rstrip("0").rstrip(".")
                steps_txt = f"{a}x = {b} - {c}\n{a}x = {wrong_diff}\nx = {wrong_ans}"
            elif label == "multiplication_division_error":
                # Inverted division
                q_text = f"Solve for x: {a}x = {c}"
                corr_ans = f"{c / a:.2f}".rstrip("0").rstrip(".")
                wrong_ans = f"{a / c:.2f}".rstrip("0").rstrip(".")
                steps_txt = f"x = {a} / {c} = {wrong_ans}"
            elif label == "conceptual_misunderstanding":
                # Combines ax + c as (a+c)x
                wrong_coeff = a + c
                wrong_ans = f"{b / wrong_coeff:.2f}".rstrip("0").rstrip(".")
                steps_txt = f"{a}x + {c} = {wrong_coeff}x\n{wrong_coeff}x = {b}\nx = {wrong_ans}"
            else: # correct
                steps_txt = f"{a}x = {b} - {c}\n{a}x = {b - c}\nx = {b - c} / {a}\nx = {corr_ans}"
                wrong_ans = corr_ans

        elif topic == "fractions":
            d1 = random.choice([2, 3, 4, 5, 6])
            d2 = random.choice([3, 4, 5, 7])
            if d1 == d2:
                d2 += 1
            n1 = random.randint(1, d1 - 1)
            n2 = random.randint(1, d2 - 1)

            q_text = f"Evaluate: {n1}/{d1} + {n2}/{d2}"
            import math
            lcm = (d1 * d2) // math.gcd(d1, d2)
            num_sum = n1 * (lcm // d1) + n2 * (lcm // d2)
            g = math.gcd(num_sum, lcm)
            corr_ans = f"{num_sum // g}/{lcm // g}" if lcm // g != 1 else str(num_sum // g)

            if label == "fraction_operation_error":
                # Direct addition of tops and bottoms
                wrong_ans = f"{n1 + n2}/{d1 + d2}"
                steps_txt = f"({n1} + {n2}) / ({d1} + {d2}) = {wrong_ans}"
            elif label == "arithmetic_calculation_error":
                wrong_num = num_sum + random.choice([-1, 1, 2])
                wrong_ans = f"{wrong_num}/{lcm}"
                steps_txt = f"Common denominator is {lcm}\n({n1 * (lcm // d1)} + {n2 * (lcm // d2)}) / {lcm} = {wrong_ans}"
            elif label == "multiplication_division_error":
                # Cross multiplied across plus
                wrong_ans = f"{n1 * d2}/{d1 * n2}"
                steps_txt = f"Cross multiplied {n1}*{d2} / {d1}*{n2} = {wrong_ans}"
            elif label == "sign_error":
                wrong_ans = f"-{corr_ans}"
                steps_txt = f"Got negative fraction by mistake: -{corr_ans}"
            elif label == "conceptual_misunderstanding":
                wrong_ans = f"{n1 + n2}"
                steps_txt = f"Added tops: {n1} + {n2} = {wrong_ans}, dropped denominators"
            else: # correct
                wrong_ans = corr_ans
                steps_txt = f"Common denominator is {lcm}\n{n1*(lcm//d1)}/{lcm} + {n2*(lcm//d2)}/{lcm} = {corr_ans}"

        elif topic == "percentages":
            pct = random.choice([10, 15, 20, 25, 30, 40, 50, 75])
            base_num = random.choice([40, 60, 80, 100, 120, 160, 200, 250])
            calc_val = (pct * base_num) / 100
            corr_ans = f"{calc_val:.0f}" if calc_val.is_integer() else f"{calc_val:.1f}"
            q_text = f"What is {pct}% of {base_num}?"

            if label == "conceptual_misunderstanding":
                # Subtraction
                wrong_ans = str(base_num - pct)
                steps_txt = f"{base_num} - {pct} = {wrong_ans}"
            elif label == "multiplication_division_error":
                # Multiplied without dividing 100
                wrong_ans = str(pct * base_num)
                steps_txt = f"{base_num} * {pct} = {wrong_ans}"
            elif label == "arithmetic_calculation_error":
                slip = random.choice([-3, -2, 2, 4])
                wrong_ans = str(int(calc_val) + slip)
                steps_txt = f"{pct}/100 * {base_num} = {wrong_ans}"
            elif label == "sign_error":
                wrong_ans = f"-{corr_ans}"
                steps_txt = f"Applied negative sign: -{corr_ans}"
            elif label == "inverse_operation_error":
                wrong_ans = f"{(base_num / pct):.2f}"
                steps_txt = f"Divided base by percent: {base_num} / {pct} = {wrong_ans}"
            else: # correct
                wrong_ans = corr_ans
                steps_txt = f"({pct} / 100) * {base_num} = {corr_ans}"

        else: # basic_algebra
            k1 = random.randint(2, 6)
            k2 = random.randint(2, 6)
            c1 = random.randint(1, 9)
            c2 = random.randint(1, 9)
            q_text = f"Simplify: {k1}x + {c1} + {k2}x - {c2}"
            corr_ans = f"{k1 + k2}x + {c1 - c2}" if c1 >= c2 else f"{k1 + k2}x - {c2 - c1}"

            if label == "conceptual_misunderstanding":
                # Combines everything into single product
                wrong_ans = f"{k1 + c1 + k2 - c2}x"
                steps_txt = f"{k1} + {c1} + {k2} - {c2} = {wrong_ans}"
            elif label == "sign_error":
                # Drops or flips minus sign
                wrong_ans = f"{k1 + k2}x + {c1 + c2}"
                steps_txt = f"Added all constants ignoring minus: {c1} + {c2} = {c1 + c2}"
            elif label == "arithmetic_calculation_error":
                slip = random.choice([-2, 1, 2])
                wrong_ans = f"{k1 + k2 + slip}x + {c1 - c2}"
                steps_txt = f"{k1}x + {k2}x = {k1 + k2 + slip}x, {c1} - {c2} = {c1 - c2}"
            elif label == "multiplication_division_error":
                wrong_ans = f"{k1 * k2}x + {c1 - c2}"
                steps_txt = f"Multiplied coefficients: {k1} * {k2} = {k1 * k2}x"
            else: # correct
                wrong_ans = corr_ans
                steps_txt = f"Group like terms: ({k1} + {k2})x + ({c1} - {c2}) = {corr_ans}"

        chosen_approach = random.choice(approaches_by_label.get(label, ["standard"]))

        entry = {
            "topic": topic,
            "question": q_text,
            "correct_answer": corr_ans,
            "student_answer": wrong_ans,
            "steps": steps_txt,
            "approach": chosen_approach,
            "label": label,
            "notes": f"Synthetic variation with {label} logic"
        }
        dataset.append(entry)

    random.shuffle(dataset)
    return dataset

def save_dataset_csv(filepath="backend/ml/dataset.csv", target_size=900):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    dataset = generate_augmented_dataset(target_size=target_size)
    fieldnames = ["topic", "question", "correct_answer", "student_answer", "steps", "approach", "label", "notes"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in dataset:
            writer.writerow(row)

    print(f"[Dataset Generator] Successfully generated {len(dataset)} labeled samples saved to {filepath}")
    # Print label distribution
    from collections import Counter
    counts = Counter(r["label"] for r in dataset)
    print("[Dataset Generator] Class distribution:")
    for k, v in counts.items():
        print(f"  - {k}: {v} samples ({v / len(dataset) * 100:.1f}%)")

if __name__ == "__main__":
    save_dataset_csv()
