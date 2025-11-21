import os
def generate_match_summary(candidate_text, jd_text, score):
    # Lightweight summary generator to avoid mandatory cloud calls.
    # If OPENAI_API_KEY is present, user can replace this with a proper LangChain LLM chain.
    score_pct = round(float(score)*100,2) if score is not None else 0.0
    summary = f"""Fit score: {score_pct}%
Top skills (extracted): {', '.join(sorted(set(candidate_text.split()[:10])) ) }
Strengths: strong domain knowledge; quick learner.
Risks: may lack exact tool experience; needs interview to validate.
Recommended next step: Technical phone screen."""
    return summary
