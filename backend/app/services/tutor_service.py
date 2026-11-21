"""
thinkSync AI - Personal AI Tutor Service
Integrates Gemini API for personalized, encouraging Socratic explanations and remediation questions.
Includes an expert pedagogical fallback engine when API keys are absent or network is unavailable.
"""

import os
import json
import logging
import httpx
from ..config import settings

logger = logging.getLogger("thinksync.tutor")

# Pedagogical fallback templates by misconception category
FALLBACK_PEDAGOGY = {
    "inverse_operation_error": {
        "analysis_template": "It looks like an inverse operation was flipped! Specifically, when moving a term across the equals sign, the opposite operation is required (addition undoes subtraction, and division undoes multiplication).",
        "concept": "Think of an equation like a balanced playground see-saw. Whatever you do to one side, you must do the exact same operation to the other side to keep it balanced. If a number is currently added (+), we subtract it (-); if a number is multiplying (×), we divide it (÷).",
        "hint": "Identify the operation currently attached to the variable. Ask yourself: 'What is the exact opposite operation needed to undo this?' Apply that opposite operation to both sides.",
        "remedial_question": "Quick check: In the equation 3x + 4 = 19, what is the very first step you should do to both sides?",
        "encouragement": "You are on the right track! Recognizing which operation to undo is one of the most common hurdles in algebra, and you're getting closer with each try."
    },
    "sign_error": {
        "analysis_template": "A sign slip occurred during the calculation. Pay special attention to negative signs when multiplying, dividing, or distributing across parentheses.",
        "concept": "Remember the integer sign rules: multiplying or dividing two negatives produces a positive (- × - = +), while a negative combined with a positive yields a negative (- × + = -). When distributing a negative outside brackets, every term inside changes sign.",
        "hint": "Check the negative sign in your intermediate line. Did you distribute the minus sign to EVERY term inside the parentheses, or keep the negative when dividing?",
        "remedial_question": "Quick check: What is -4 multiplied by (x - 3)? Be sure to expand both terms carefully.",
        "encouragement": "Sign errors happen even to professional mathematicians! A quick double-check of each '-' sign will make your algebra rock-solid."
    },
    "arithmetic_calculation_error": {
        "analysis_template": "Your algebraic setup and problem-solving method were actually spot on! The mistake came from a slight arithmetic calculation slip in the mental math.",
        "concept": "Algebra is two things: logic (the steps) and arithmetic (the computations). Your logic was sound! Separating scratch arithmetic from equation balancing helps catch minor slips.",
        "hint": "Take a look at your intermediate arithmetic step. Double-check your addition/subtraction or times table result on scratch paper.",
        "remedial_question": "Quick check: Double-check 32 - 14 on scratch paper. What value do you get?",
        "encouragement": "Great mathematical thinking! Your conceptual steps were completely right. Just give your scratch math one quick scan before submitting."
    },
    "multiplication_division_error": {
        "analysis_template": "There was an inversion in multiplication or division. In particular, be careful with the order: dividing by a fraction means multiplying by its reciprocal (flipping it), not dividing straight across.",
        "concept": "When you have ax = b, x = b / a (right side divided by coefficient). If a is a fraction like 2/3, dividing by 2/3 is identical to multiplying by 3/2. Always flip the divisor, never the dividend.",
        "hint": "Check which number was in the numerator and which was in the denominator. When dividing fractions: Keep, Change, Flip!",
        "remedial_question": "Quick check: What is 6 divided by (2/3)? Try multiplying 6 by the flipped fraction.",
        "encouragement": "Fractions and reciprocals can be tricky to visualize, but once you master Keep-Change-Flip, these become second nature!"
    },
    "conceptual_misunderstanding": {
        "analysis_template": "A core conceptual misunderstanding occurred here. For instance, unlike terms (like 3x and 5) cannot be added together into 8x because they represent different quantities.",
        "concept": "Variables and constants are like apples and oranges. You can add 3 apples and 2 apples to get 5 apples (3x + 2x = 5x), but 3 apples plus 4 dollars (3x + 4) cannot become 7 of anything! They must stay separate.",
        "hint": "Identify which terms have variables and which terms are plain numbers. Only combine terms that share the exact same variable.",
        "remedial_question": "Quick check: Can you simplify 4x + 3 + 2x? Group the x terms together and keep the 3 separate.",
        "encouragement": "Learning algebra is like learning a new language. Once you see why like terms stick together, everything clicks into place!"
    },
    "fraction_operation_error": {
        "analysis_template": "It looks like the numerators and denominators were added or subtracted directly across. Fractions can only be added or subtracted when they share a common denominator.",
        "concept": "Imagine a pizza cut into 3 giant slices and another cut into 4 smaller slices. 1 slice of the first + 1 slice of the second is not 2 slices of a 7-slice pizza! We must first cut both into equal-sized 12th-slices before adding.",
        "hint": "Find the Least Common Denominator (LCD) for both denominators first. Convert both fractions, then only add the numerators while keeping the common denominator.",
        "remedial_question": "Quick check: What is the Least Common Multiple (LCM) of 3 and 4?",
        "encouragement": "Fraction operations are the foundation of high-level math. Getting the common denominator right is your superpower here!"
    },
    "correct": {
        "analysis_template": "Outstanding work! You solved this problem with accurate steps and sound mathematical logic.",
        "concept": "Your solution demonstrates clear mastery of this topic.",
        "hint": "Ready for the next challenge? Try an intermediate or advanced problem to continue leveling up!",
        "remedial_question": "Would you like to try a timed or multi-step challenge in this topic?",
        "encouragement": "Fantastic job! Your method was clean and your answer is 100% correct. Keep up this momentum!"
    },
    "uncertain_insufficient_evidence": {
        "analysis_template": "We noticed you submitted an answer without detailed intermediate calculation steps.",
        "concept": "Showing your steps isn't just about getting credit—it lets our AI see your thinking so we can guide you if you hit a stumbling block.",
        "hint": "Try writing out step 1 and step 2 of how you approached the equation, even if you are not 100% sure.",
        "remedial_question": "Try solving again: write down what you do to both sides first.",
        "encouragement": "Don't worry about being wrong! Even an incomplete attempt with steps helps us help you succeed."
    }
}

def generate_ai_tutor_feedback(
    question_text: str,
    student_answer: str,
    intermediate_steps: str,
    predicted_misconception: str,
    ml_confidence: float,
    topic: str,
    is_correct: bool = False
) -> dict:
    """
    Synchronous pedagogical tutoring response generator.
    Calls Gemini API if configured, otherwise utilizes the expert pedagogical fallback engine.
    """
    if is_correct:
        return FALLBACK_PEDAGOGY["correct"]

    # If Gemini API Key is configured, attempt live LLM call
    if settings.GEMINI_API_KEY:
        try:
            return _call_gemini_api_sync(
                question_text=question_text,
                student_answer=student_answer,
                intermediate_steps=intermediate_steps,
                predicted_misconception=predicted_misconception,
                ml_confidence=ml_confidence,
                topic=topic
            )
        except Exception as e:
            logger.warning(f"Gemini API invocation failed or unavailable: {e}. Utilizing fallback pedagogy.")

    # High-fidelity pedagogical fallback
    base_info = FALLBACK_PEDAGOGY.get(predicted_misconception, FALLBACK_PEDAGOGY["conceptual_misunderstanding"])
    
    # Customise fallback with student's specific answer and question
    analysis = base_info["analysis_template"]
    if student_answer:
        analysis = f"You answered '{student_answer}'. {analysis}"
        
    return {
        "mistake_analysis": analysis,
        "conceptual_explanation": base_info["concept"],
        "socratic_hint": base_info["hint"],
        "remedial_question": base_info["remedial_question"],
        "encouragement": base_info["encouragement"]
    }

def _call_gemini_api_sync(
    question_text: str,
    student_answer: str,
    intermediate_steps: str,
    predicted_misconception: str,
    ml_confidence: float,
    topic: str
) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
    
    system_prompt = (
        "You are the empathetic, expert personal tutor for thinkSync AI. "
        "A student made a mistake on an educational math assessment. "
        "Our Scikit-learn Machine Learning classifier independently analyzed their work and flagged the underlying misconception.\n"
        "Your mission is to guide the student Socratically without shaming them and without revealing the final answer.\n"
        "You MUST respond ONLY with a valid JSON object matching this schema:\n"
        "{\n"
        '  "mistake_analysis": "string describing where the student\'s thought process diverged",\n'
        '  "conceptual_explanation": "string explaining the core math concept in intuitive simple terms",\n'
        '  "socratic_hint": "string with a helpful hint for the next step",\n'
        '  "remedial_question": "string with a similar follow-up problem to practice",\n'
        '  "encouragement": "string with warm, uplifting growth-mindset feedback"\n'
        "}"
    )
    
    user_prompt = (
        f"Topic: {topic}\n"
        f"Original Question: {question_text}\n"
        f"Student Answer: {student_answer}\n"
        f"Student Intermediate Steps: {intermediate_steps or 'None provided'}\n"
        f"ML Classifier Diagnosed Misconception: {predicted_misconception} (Confidence: {ml_confidence:.1%})\n\n"
        "Provide your friendly pedagogical feedback in strict JSON format."
    )
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt + "\n\n" + user_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json"
        }
    }
    
    with httpx.Client(timeout=8.0) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(raw_text)

def generate_step_hint(question_text: str, current_steps: str, hint_level: int = 1) -> dict:
    if hint_level == 1:
        return {
            "hint_level": 1,
            "hint_title": "Getting Started Hint",
            "hint_text": "Identify your target variable. Ask yourself: what numbers or operations are currently grouped with it, and what is the first barrier to peel away?",
            "suggested_action": "Write down what the equation looks like after removing the constant term."
        }
    else:
        return {
            "hint_level": 2,
            "hint_title": "Next Step Hint",
            "hint_text": "Balance check: apply the inverse operation equally to both sides of the equal sign. Keep all terms aligned vertically to avoid arithmetic slips.",
            "suggested_action": "Check your arithmetic on scratchpad before writing your final isolated variable value."
        }
