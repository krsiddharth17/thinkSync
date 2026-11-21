"""
thinkSync AI - Comprehensive Seed Data
Seeds default users (students & teachers), 4 core math topics with markdown concept guides,
a rich question bank with diagnostic distractors and multi-step solutions,
and realistic historical attempts for immediate college demo visualisations.
"""

import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import User, Topic, Question, AssessmentAttempt, StudentTopicMastery
from .auth import hash_password

def seed_database(db: Session):
    # Check if already seeded
    if db.query(Topic).first() is not None:
        print("[Seed Data] Database already seeded. Skipping.")
        return

    print("[Seed Data] Seeding thinkSync AI database...")

    # 1. Create Users
    student1 = User(
        username="alex_student",
        email="alex@thinksync.edu",
        hashed_password=hash_password("student123"),
        role="student",
        full_name="Alex Rivera",
        grade="Grade 9"
    )
    student2 = User(
        username="maya_student",
        email="maya@thinksync.edu",
        hashed_password=hash_password("student123"),
        role="student",
        full_name="Maya Chen",
        grade="Grade 10"
    )
    student3 = User(
        username="leo_student",
        email="leo@thinksync.edu",
        hashed_password=hash_password("student123"),
        role="student",
        full_name="Leo Patel",
        grade="Grade 9"
    )
    teacher = User(
        username="sarah_teacher",
        email="sarah.miller@thinksync.edu",
        hashed_password=hash_password("teacher123"),
        role="teacher",
        full_name="Prof. Sarah Miller",
        grade="Mathematics Dept"
    )

    db.add_all([student1, student2, student3, teacher])
    db.flush()

    # 2. Create Topics with Rich Concept Guides
    topic_le = Topic(
        name="Linear Equations",
        slug="linear-equations",
        description="Master single-variable linear equations, equation balancing, and inverse operations.",
        icon="Scale",
        difficulty_levels="Easy,Medium,Hard",
        concept_guide=r"""### Linear Equations Concept Guide

An equation represents a **balance**. The equals sign ($=$) declares that the quantity on the left side has the exact same value as the quantity on the right side.

#### 1. The Principle of Inverse Operations
To isolate a variable, apply the **opposite operation** to both sides:
- To undo addition ($+b$), **subtract** $b$ from both sides.
- To undo subtraction ($-b$), **add** $b$ to both sides.
- To undo multiplication ($\times a$), **divide** both sides by $a$.
- To undo division ($\div a$), **multiply** both sides by $a$.

#### 2. Common Pitfalls to Avoid
- **Operation Reversal:** Adding a constant to both sides when it is already positive on one side.
- **Dropping Negatives:** In $-3x = 12$, dividing by $-3$ gives $x = -4$, not $+4$.
- **Unlike Terms:** Never combine $3x + 5$ into $8x$. They are fundamentally different terms.
"""
    )

    topic_fr = Topic(
        name="Fractions",
        slug="fractions",
        description="Understand fraction arithmetic, common denominators, and reciprocal multiplication.",
        icon="PieChart",
        difficulty_levels="Easy,Medium,Hard",
        concept_guide=r"""### Fractions Concept Guide

A fraction $\frac{a}{b}$ represents $a$ equal parts out of a total of $b$ parts that make up a whole.

#### 1. Addition & Subtraction (Common Denominator Rule)
You **cannot** add or subtract fractions until the slice sizes (denominators) match!
$$\frac{1}{3} + \frac{1}{4} = \frac{4}{12} + \frac{3}{12} = \frac{7}{12}$$
*Never add denominators directly:* $\frac{1}{3} + \frac{1}{4} \neq \frac{2}{7}$.

#### 2. Multiplication & Division
- **Multiplication:** Multiply straight across: $\frac{a}{b} \times \frac{c}{d} = \frac{a \times c}{b \times d}$.
- **Division (Keep, Change, Flip):** $\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \times \frac{d}{c}$.
"""
    )

    topic_pct = Topic(
        name="Percentages",
        slug="percentages",
        description="Grasp percentage proportions, discounts, markups, and fractional conversions.",
        icon="Percent",
        difficulty_levels="Easy,Medium,Hard",
        concept_guide=r"""### Percentages Concept Guide

"Percent" literally means "per hundred" (from Latin *per centum*). $25\%$ means $25$ out of $100$, or $\frac{25}{100} = 0.25$.

#### 1. Finding a Percent of a Number
To calculate $P\%$ of $N$:
$$\text{Amount} = \frac{P}{100} \times N = 0.0P \times N$$
Example: $20\%$ of $80 = 0.20 \times 80 = 16$.

#### 2. Common Pitfalls
- **Direct Subtraction:** For a $20\%$ discount on $80, the price is not $80 - 20 = 60$. It is $80 - (0.20 \times 80) = 80 - 16 = 64$.
- **Percentage of Total:** Part divided by Whole $\times 100\%$.
"""
    )

    topic_alg = Topic(
        name="Basic Algebra",
        slug="basic-algebra",
        description="Simplify algebraic expressions, combine like terms, and apply distributive properties.",
        icon="Binary",
        difficulty_levels="Easy,Medium,Hard",
        concept_guide="""### Basic Algebra Concept Guide

Algebra is the language of mathematical generalization, using symbols to represent changing or unknown values.

#### 1. Combining Like Terms
Only terms that have the **exact same variable raised to the exact same power** can be combined:
- $3x + 5x = 8x$ (Like terms)
- $3x + 4y$ cannot be simplified (Unlike terms)
- $2x^2 + 3x$ cannot be simplified (Different exponents)

#### 2. Distributive Property & Signs
$$a(b + c) = ab + ac$$
$$-2(3x - 4) = (-2)(3x) - (-2)(4) = -6x + 8$$
*Pay careful attention to negative distribution:* $-(-4) = +4$.
"""
    )

    db.add_all([topic_le, topic_fr, topic_pct, topic_alg])
    db.flush()

    # 3. Create Questions
    questions = [
        # --- LINEAR EQUATIONS ---
        Question(
            topic_id=topic_le.id,
            question_text="Solve for x: 2x + 7 = 19",
            correct_answer="6",
            step_by_step_solution="1. Subtract 7 from both sides: 2x = 19 - 7 => 2x = 12.\n2. Divide both sides by 2: x = 12 / 2 => x = 6.",
            explanation="To isolate x, we first undo the addition of 7 by subtracting 7 from both sides, then undo the multiplication by 2 by dividing both sides by 2.",
            difficulty="easy",
            approach_options=json.dumps(["Isolate variable using inverse operations", "Guess and check numbers", "Direct arithmetic on right side"]),
            hint_1="Look at the +7 on the left side. What is the opposite operation of adding 7?",
            hint_2="Subtract 7 from both sides: 2x = 12. Now what is 12 divided by 2?",
            common_misconceptions=json.dumps(["Adding 7 to 19 instead of subtracting (gives 26/2 = 13)", "Combining 2x + 7 into 9x"])
        ),
        Question(
            topic_id=topic_le.id,
            question_text="Solve for x: 3x - 8 = 16",
            correct_answer="8",
            step_by_step_solution="1. Add 8 to both sides: 3x = 16 + 8 => 3x = 24.\n2. Divide both sides by 3: x = 24 / 3 => x = 8.",
            explanation="The inverse of subtracting 8 is adding 8. Once added, 3x = 24, so dividing by 3 yields x = 8.",
            difficulty="easy",
            approach_options=json.dumps(["Isolate variable using inverse operations", "Subtract 8 from right side", "Combine terms"]),
            hint_1="Undo the -8 by adding 8 to both sides.",
            hint_2="3x = 24. What times 3 gives 24?",
            common_misconceptions=json.dumps(["Subtracted 8 from 16 (gives 8/3)", "Sign error when moving 8"])
        ),
        Question(
            topic_id=topic_le.id,
            question_text="Solve for x: -4x + 6 = -14",
            correct_answer="5",
            step_by_step_solution="1. Subtract 6 from both sides: -4x = -14 - 6 => -4x = -20.\n2. Divide both sides by -4: x = -20 / -4 => x = 5.",
            explanation="Subtracting 6 from -14 gives -20. Dividing negative 20 by negative 4 yields positive 5.",
            difficulty="medium",
            approach_options=json.dumps(["Isolate variable with negative coefficient", "Move x to the right side", "Guess and check"]),
            hint_1="Subtract 6 from both sides first. Remember: -14 - 6 becomes more negative.",
            hint_2="-4x = -20. When you divide a negative number by another negative number, the result is positive.",
            common_misconceptions=json.dumps(["Keeping negative sign in final answer (giving -5)", "Incorrect integer subtraction (-14 - 6 = -8)"])
        ),
        Question(
            topic_id=topic_le.id,
            question_text="Solve for x: 5(x - 3) = 2x + 9",
            correct_answer="8",
            step_by_step_solution="1. Expand brackets: 5x - 15 = 2x + 9.\n2. Subtract 2x from both sides: 3x - 15 = 9.\n3. Add 15 to both sides: 3x = 24.\n4. Divide by 3: x = 8.",
            explanation="First distribute 5 across (x - 3) to get 5x - 15. Group variable terms on one side and constant terms on the other.",
            difficulty="hard",
            approach_options=json.dumps(["Distribute then group like terms", "Divide by 5 first", "Guess and check"]),
            hint_1="Start by expanding 5(x - 3) using the distributive property.",
            hint_2="You should have 5x - 15 = 2x + 9. Move 2x to the left side.",
            common_misconceptions=json.dumps(["Failed to multiply 5 by -3 (writing 5x - 3)", "Sign error when moving -15"])
        ),

        # --- FRACTIONS ---
        Question(
            topic_id=topic_fr.id,
            question_text="Evaluate: 1/3 + 1/4",
            correct_answer="7/12",
            step_by_step_solution="1. Find common denominator: LCM(3, 4) = 12.\n2. Convert fractions: 1/3 = 4/12 and 1/4 = 3/12.\n3. Add numerators: 4/12 + 3/12 = 7/12.",
            explanation="Because the denominators are different, we convert both fractions to 12ths before adding.",
            difficulty="easy",
            approach_options=json.dumps(["Find common denominator", "Direct addition of tops and bottoms", "Convert to decimals"]),
            hint_1="What is the smallest number that both 3 and 4 divide into evenly?",
            hint_2="The common denominator is 12. Convert 1/3 into ?/12 and 1/4 into ?/12.",
            common_misconceptions=json.dumps(["Adding tops and bottoms directly (gives 2/7)", "Multiplying denominators instead of adding numerators"])
        ),
        Question(
            topic_id=topic_fr.id,
            question_text="Evaluate: 2/5 + 3/10",
            correct_answer="7/10",
            step_by_step_solution="1. Common denominator is 10.\n2. Convert 2/5 to 4/10.\n3. Add: 4/10 + 3/10 = 7/10.",
            explanation="5 divides into 10, so 10 is the LCD. 2/5 = 4/10, plus 3/10 equals 7/10.",
            difficulty="easy",
            approach_options=json.dumps(["Find common denominator", "Direct addition", "Cross multiplication"]),
            hint_1="Notice that 10 is a multiple of 5. You only need to convert 2/5.",
            hint_2="2/5 is equivalent to 4/10. Now add 4/10 + 3/10.",
            common_misconceptions=json.dumps(["Adding directly to get 5/15 = 1/3", "Arithmetic slip in conversion"])
        ),
        Question(
            topic_id=topic_fr.id,
            question_text="Evaluate: 2/3 divided by 4/5",
            correct_answer="5/6",
            step_by_step_solution="1. Keep, Change, Flip: 2/3 * 5/4.\n2. Multiply numerators and denominators: (2 * 5) / (3 * 4) = 10/12.\n3. Simplify by dividing by 2: 5/6.",
            explanation="Dividing by a fraction is the same as multiplying by its reciprocal (flip the second fraction).",
            difficulty="medium",
            approach_options=json.dumps(["Keep Change Flip (reciprocal)", "Divide numerators and denominators directly", "Cross multiply"]),
            hint_1="Remember the division rule for fractions: Keep the first fraction, change divide to multiply, and flip the second fraction.",
            hint_2="Calculate (2/3) * (5/4) = 10/12. Don't forget to simplify to lowest terms!",
            common_misconceptions=json.dumps(["Multiplying straight across without flipping (gives 8/15)", "Flipping the first fraction instead of the second"])
        ),
        Question(
            topic_id=topic_fr.id,
            question_text="Evaluate: (3/4 - 1/3) * 6/5",
            correct_answer="1/2",
            step_by_step_solution="1. Subtract inside parentheses: 3/4 - 1/3 = 9/12 - 4/12 = 5/12.\n2. Multiply: (5/12) * (6/5) = 30/60.\n3. Simplify: 30/60 = 1/2.",
            explanation="Following order of operations, evaluate the subtraction inside the brackets first using a common denominator of 12, then multiply by 6/5.",
            difficulty="hard",
            approach_options=json.dumps(["PEMDAS brackets first then multiply", "Distribute 6/5 into brackets", "Direct calculation"]),
            hint_1="Solve the parentheses first: 3/4 - 1/3 using LCD 12.",
            hint_2="You should get 5/12. Now multiply 5/12 by 6/5. Notice how 5 cancels with 5!",
            common_misconceptions=json.dumps(["Direct subtraction inside brackets (gives 2/1)", "Calculation error in fraction multiplication"])
        ),

        # --- PERCENTAGES ---
        Question(
            topic_id=topic_pct.id,
            question_text="What is 20% of 80?",
            correct_answer="16",
            step_by_step_solution="1. Convert 20% to decimal: 20/100 = 0.20.\n2. Multiply: 0.20 * 80 = 16.",
            explanation="20% means 20 per 100, or 1/5. One fifth of 80 is 16.",
            difficulty="easy",
            approach_options=json.dumps(["Convert to decimal and multiply", "Direct subtraction 80 - 20", "Convert to fraction 1/5"]),
            hint_1="20% is equal to 0.20 or 1/5.",
            hint_2="Multiply 80 by 0.2, or divide 80 by 5.",
            common_misconceptions=json.dumps(["Subtracting 20 from 80 (gives 60)", "Multiplying without dividing 100 (gives 1600)"])
        ),
        Question(
            topic_id=topic_pct.id,
            question_text="A jacket originally priced at $60 is on sale for 25% off. What is the sale price?",
            correct_answer="45",
            step_by_step_solution="1. Calculate discount: 25% of 60 = 0.25 * 60 = 15.\n2. Subtract discount from original price: 60 - 15 = 45.",
            explanation="A 25% discount means paying 75% of the original price. 0.75 * 60 = $45.",
            difficulty="medium",
            approach_options=json.dumps(["Find discount amount then subtract", "Subtract 25 directly from 60", "Multiply by 0.75"]),
            hint_1="First find what 25% of 60 is (hint: 25% is 1/4).",
            hint_2="1/4 of 60 is 15. Now subtract 15 from the original 60.",
            common_misconceptions=json.dumps(["Directly subtracting percent number (60 - 25 = 35)", "Giving the discount amount ($15) instead of sale price"])
        ),
        Question(
            topic_id=topic_pct.id,
            question_text="If a student scored 36 out of 45 on an exam, what is their percentage score?",
            correct_answer="80%",
            step_by_step_solution="1. Set up fraction: 36 / 45.\n2. Simplify: 36 / 45 = 4 / 5.\n3. Convert to percentage: (4 / 5) * 100 = 80%.",
            explanation="Divide the score by the total possible points and multiply by 100 to get the percentage.",
            difficulty="medium",
            approach_options=json.dumps(["Divide part by whole and multiply by 100", "Divide whole by part", "Cross multiplication"]),
            hint_1="Divide 36 by 45 to get the decimal score.",
            hint_2="36 / 45 simplifies to 4/5. What is 4/5 as a percentage?",
            common_misconceptions=json.dumps(["Inverting the ratio (45 / 36 = 1.25)", "Arithmetic slip in division"])
        ),

        # --- BASIC ALGEBRA ---
        Question(
            topic_id=topic_alg.id,
            question_text="Simplify: 3x + 4y + 5x - 2y",
            correct_answer="8x + 2y",
            step_by_step_solution="1. Group like terms: (3x + 5x) + (4y - 2y).\n2. Combine x terms: 3x + 5x = 8x.\n3. Combine y terms: 4y - 2y = 2y.\n4. Final simplified expression: 8x + 2y.",
            explanation="Only terms with the same variable can be combined together.",
            difficulty="easy",
            approach_options=json.dumps(["Combine like terms separately", "Combine all numbers into one product", "Subtract variables"]),
            hint_1="Group the terms with 'x' together, and the terms with 'y' together.",
            hint_2="What is 3x + 5x? And what is 4y - 2y?",
            common_misconceptions=json.dumps(["Combining everything into 10xy", "Sign error with -2y"])
        ),
        Question(
            topic_id=topic_alg.id,
            question_text="Expand and simplify: -3(2x - 5)",
            correct_answer="-6x + 15",
            step_by_step_solution="1. Distribute -3 to 2x: (-3) * (2x) = -6x.\n2. Distribute -3 to -5: (-3) * (-5) = +15.\n3. Combine: -6x + 15.",
            explanation="When distributing a negative number across parentheses, both terms inside change sign.",
            difficulty="medium",
            approach_options=json.dumps(["Distributive property with sign rules", "Multiply without negative", "Add terms inside brackets"]),
            hint_1="Multiply -3 by both 2x and -5.",
            hint_2="Remember: negative times negative equals positive! What is (-3) * (-5)?",
            common_misconceptions=json.dumps(["Forgetting to change sign of -5 (writing -6x - 15)", "Dropping negative on -6x"])
        ),
        Question(
            topic_id=topic_alg.id,
            question_text="Simplify completely: 2(3a + 4b) - 3(a - 2b)",
            correct_answer="3a + 14b",
            step_by_step_solution="1. Expand first bracket: 2 * 3a + 2 * 4b = 6a + 8b.\n2. Expand second bracket: -3 * a - 3 * (-2b) = -3a + 6b.\n3. Combine like terms: (6a - 3a) + (8b + 6b) = 3a + 14b.",
            explanation="Carefully expand both terms, watching the double negative in -3 * (-2b) which becomes +6b, then combine like terms.",
            difficulty="hard",
            approach_options=json.dumps(["Expand both brackets and combine like terms", "Subtract brackets first", "Factor out coefficients"]),
            hint_1="Expand 2(3a + 4b) first, then expand -3(a - 2b).",
            hint_2="Watch out for -3 * (-2b)! That becomes +6b. Then combine with 8b.",
            common_misconceptions=json.dumps(["Distributing -3 to -2b as -6b (giving 2b)", "Combining unlike terms a and b"])
        )
    ]

    db.add_all(questions)
    db.flush()

    # 4. Create Realistic Historical Attempts for Alex Rivera
    # Alex struggles with inverse operations and sign errors occasionally
    past_attempts = [
        # Attempt 1 on LE Q1: Made inverse operation error
        AssessmentAttempt(
            user_id=student1.id,
            question_id=questions[0].id,
            student_answer="13",
            intermediate_steps="2x = 19 + 7\n2x = 26\nx = 13",
            approach_selected="Isolate variable using inverse operations",
            is_correct=False,
            predicted_misconception="inverse_operation_error",
            ml_confidence=0.88,
            class_probabilities=json.dumps({"inverse_operation_error": 0.88, "arithmetic_calculation_error": 0.06}),
            ai_feedback=json.dumps({
                "mistake_analysis": "Added 7 to 19 instead of subtracting 7.",
                "conceptual_explanation": "In an equation, undoing +7 requires subtracting 7 from both sides.",
                "socratic_hint": "Try subtracting 7 from 19.",
                "encouragement": "Good effort! Check your inverse operation."
            }),
            time_taken_seconds=42,
            created_at=datetime.utcnow() - timedelta(days=3)
        ),
        # Attempt 2 on LE Q1: Retried and got it right!
        AssessmentAttempt(
            user_id=student1.id,
            question_id=questions[0].id,
            student_answer="6",
            intermediate_steps="2x = 19 - 7\n2x = 12\nx = 6",
            approach_selected="Isolate variable using inverse operations",
            is_correct=True,
            predicted_misconception="correct",
            ml_confidence=0.96,
            class_probabilities=json.dumps({"correct": 0.96}),
            ai_feedback=json.dumps({
                "mistake_analysis": "None",
                "conceptual_explanation": "Mastered inverse operations on two-step linear equations.",
                "socratic_hint": "Ready for harder challenges!",
                "encouragement": "Brilliant improvement!"
            }),
            time_taken_seconds=28,
            created_at=datetime.utcnow() - timedelta(days=3, hours=-1)
        ),
        # Attempt 3 on Fractions Q1: Made direct addition misconception
        AssessmentAttempt(
            user_id=student1.id,
            question_id=questions[4].id,
            student_answer="2/7",
            intermediate_steps="(1 + 1) / (3 + 4) = 2/7",
            approach_selected="Direct addition of tops and bottoms",
            is_correct=False,
            predicted_misconception="fraction_operation_error",
            ml_confidence=0.94,
            class_probabilities=json.dumps({"fraction_operation_error": 0.94, "conceptual_misunderstanding": 0.04}),
            ai_feedback=json.dumps({
                "mistake_analysis": "Directly added denominators 3 and 4.",
                "conceptual_explanation": "Fractions require a common denominator before adding.",
                "socratic_hint": "Find the LCM of 3 and 4 (it's 12).",
                "encouragement": "Very common misconception. You can fix this!"
            }),
            time_taken_seconds=35,
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
        # Attempt 4 on Percentages Q1: Made direct subtraction misconception
        AssessmentAttempt(
            user_id=student1.id,
            question_id=questions[8].id,
            student_answer="60",
            intermediate_steps="80 - 20 = 60",
            approach_selected="Direct subtraction 80 - 20",
            is_correct=False,
            predicted_misconception="conceptual_misunderstanding",
            ml_confidence=0.91,
            class_probabilities=json.dumps({"conceptual_misunderstanding": 0.91}),
            ai_feedback=json.dumps({
                "mistake_analysis": "Subtracted 20 like a flat dollar amount.",
                "conceptual_explanation": "Percent means per 100. 20% of 80 is 0.20 * 80.",
                "socratic_hint": "Calculate 0.20 * 80.",
                "encouragement": "Keep going! You're building solid mathematical intuition."
            }),
            time_taken_seconds=25,
            created_at=datetime.utcnow() - timedelta(days=1)
        ),
        # Attempt 5 on Basic Algebra Q2: Made sign error
        AssessmentAttempt(
            user_id=student1.id,
            question_id=questions[12].id,
            student_answer="-6x - 15",
            intermediate_steps="-3 * 2x = -6x\n-3 * 5 = -15",
            approach_selected="Distributive property with sign rules",
            is_correct=False,
            predicted_misconception="sign_error",
            ml_confidence=0.89,
            class_probabilities=json.dumps({"sign_error": 0.89}),
            ai_feedback=json.dumps({
                "mistake_analysis": "Multiplied -3 by -5 and got -15 instead of +15.",
                "conceptual_explanation": "Negative times negative yields a positive value.",
                "socratic_hint": "Watch out for the double negative in -3 * (-5).",
                "encouragement": "Almost perfect! Just remember (-)(-) = (+)."
            }),
            time_taken_seconds=39,
            created_at=datetime.utcnow() - timedelta(hours=5)
        )
    ]
    db.add_all(past_attempts)

    # 5. Seed Student Masteries
    mastery_le = StudentTopicMastery(
        user_id=student1.id,
        topic_id=topic_le.id,
        mastery_score=68.5,
        attempts_count=4,
        correct_count=3,
        recurring_misconceptions=json.dumps({"inverse_operation_error": 1}),
        last_practiced=datetime.utcnow() - timedelta(days=1)
    )
    mastery_fr = StudentTopicMastery(
        user_id=student1.id,
        topic_id=topic_fr.id,
        mastery_score=45.0,
        attempts_count=3,
        correct_count=1,
        recurring_misconceptions=json.dumps({"fraction_operation_error": 2}),
        last_practiced=datetime.utcnow() - timedelta(days=2)
    )
    mastery_pct = StudentTopicMastery(
        user_id=student1.id,
        topic_id=topic_pct.id,
        mastery_score=52.0,
        attempts_count=2,
        correct_count=1,
        recurring_misconceptions=json.dumps({"conceptual_misunderstanding": 1}),
        last_practiced=datetime.utcnow() - timedelta(days=1)
    )
    mastery_alg = StudentTopicMastery(
        user_id=student1.id,
        topic_id=topic_alg.id,
        mastery_score=60.0,
        attempts_count=3,
        correct_count=2,
        recurring_misconceptions=json.dumps({"sign_error": 1}),
        last_practiced=datetime.utcnow() - timedelta(hours=5)
    )

    db.add_all([mastery_le, mastery_fr, mastery_pct, mastery_alg])

    # Also seed attempts for Maya and Leo so Teacher Dashboard has multi-student distribution
    db.add_all([
        AssessmentAttempt(
            user_id=student2.id,
            question_id=questions[0].id,
            student_answer="6",
            intermediate_steps="2x = 12\nx = 6",
            is_correct=True,
            predicted_misconception="correct",
            ml_confidence=0.98,
            class_probabilities="{}",
            ai_feedback="{}",
            time_taken_seconds=20,
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
        AssessmentAttempt(
            user_id=student3.id,
            question_id=questions[4].id,
            student_answer="2/7",
            intermediate_steps="1/3 + 1/4 = 2/7",
            is_correct=False,
            predicted_misconception="fraction_operation_error",
            ml_confidence=0.95,
            class_probabilities="{}",
            ai_feedback="{}",
            time_taken_seconds=45,
            created_at=datetime.utcnow() - timedelta(days=1)
        )
    ])

    db.commit()
    print("[Seed Data] Database seeded successfully with 4 topics, 14 questions, 4 users, and analytics records!")

if __name__ == "__main__":
    from .database import engine, Base, SessionLocal
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()
