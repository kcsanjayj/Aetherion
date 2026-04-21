"""
Critic Agent - Self-Evaluation
Self-checks responses for quality - Forces regeneration for weak responses
"""

from typing import Dict, Any
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class CriticAgent:
    """Self-checks responses for quality - Forces regeneration for weak responses"""
    
    def __init__(self):
        self.generic_phrases = [
            "i don't have", "no information", "not mentioned", "not specified",
            "cannot determine", "unable to", "no specific", "not provided",
            "no details", "generic response", "template"
        ]
        self.min_response_length = 120
    
    def critique(self, answer: str, context: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Critique and validate the generated response"""
        try:
            score = 0.0
            issues = []
            
            # Immediate check: Generic or short
            if "generic" in answer.lower() or len(answer) < 120:
                return {
                    "is_valid": False,
                    "score": 0.0,
                    "issues": ["Generic/short response"],
                    "force_regenerate": True
                }
            
            # Check for generic phrases
            generic_count = 0
            for phrase in self.generic_phrases:
                if phrase.lower() in answer.lower():
                    generic_count += 1
                    issues.append(f"Generic: '{phrase}'")
            
            if generic_count == 0:
                score += 0.3
            
            # Check length
            if len(answer) >= self.min_response_length:
                score += 0.2
            else:
                issues.append(f"Too short: {len(answer)} chars")
            
            # Check structure
            has_summary = "Summary:" in answer or "📄" in answer
            has_points = "Key Points:" in answer or "•" in answer or "📌" in answer
            
            if has_summary and has_points:
                score += 0.2
            
            # Check grounding
            context_words = set(context.lower().split()[:200])
            answer_words = set(answer.lower().split())
            overlap = len(context_words.intersection(answer_words))
            
            if overlap > 10:
                score += 0.1
            
            is_valid = score >= 0.6
            
            if not is_valid:
                logger.warning(f"🔍 Critic: {issues}")
            else:
                logger.info("🔍 Critic: Validated ✓")
            
            return {
                "is_valid": is_valid,
                "score": score,
                "issues": issues,
                "force_regenerate": not is_valid
            }
            
        except Exception as e:
            logger.error(f"Critic error: {e}")
            return {"is_valid": False, "score": 0.0, "issues": [str(e)], "force_regenerate": True}
