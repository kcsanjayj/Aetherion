"""
Planner Agent - Decides what type of analysis to perform
"""

from typing import Dict, Any
import re
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class PlannerAgent:
    """Brain of the agentic system - decides the task based on document and query"""
    
    def __init__(self):
        # Document type patterns
        self.task_patterns = {
            "resume_analysis": [
                r"\bresume\b", r"\bcv\b", r"\bcurriculum\b", r"\bexperience\b",
                r"\bskills\b", r"\beducation\b", r"\bqualification\b", r"\bjob\b"
            ],
            "research_summary": [
                r"\bresearch\b", r"\bpaper\b", r"\bstudy\b", r"\babstract\b",
                r"\bmethodology\b", r"\bresults\b", r"\bconclusion\b", r"\bfindings\b"
            ],
            "invoice_analysis": [
                r"\binvoice\b", r"\bbill\b", r"\breceipt\b", r"\bpayment\b",
                r"\bamount\b", r"\bdue\b", r"\bcharge\b", r"\btotal\b"
            ],
            "legal_document": [
                r"\bagreement\b", r"\bcontract\b", r"\blegal\b", r"\blaw\b",
                r"\bterms\b", r"\bconditions\b", r"\bclause\b", r"\bsection\b"
            ]
        }
        
        # 🧠 Smart Query Mode - Intent detection patterns
        self.intent_patterns = {
            "compare": [
                r"\bcompare\b", r"\bcomparison\b", r"\bversus\b", r"\bvs\b",
                r"\bdifference\b", r"\bdifferences\b", r"\bsimilarities\b",
                r"\bcontrast\b", r"\bwhich is better\b", r"\bwhich one\b",
                r"\bhow do.*compare\b", r"\bwhat.*difference\b"
            ],
            "summarize": [
                r"\bsummarize\b", r"\bsummary\b", r"\boverview\b", r"\bbrief\b",
                r"\btldr\b", r"\bmain points\b", r"\bkey takeaways\b",
                r"\bwhat is this about\b", r"\bwhat does it say\b"
            ],
            "extract": [
                r"\bextract\b", r"\bfind\b", r"\bget\b", r"\bwhat is\b",
                r"\bwhat are\b", r"\blist\b", r"\bshow me\b", r"\bwhere is\b",
                r"\bwhen is\b", r"\bwho is\b", r"\bhow much\b", r"\bhow many\b"
            ],
            "analyze": [
                r"\banalyze\b", r"\banalysis\b", r"\bevaluate\b", r"\bassess\b",
                r"\breview\b", r"\bcritique\b", r"\binterpret\b", r"\bexplain\b",
                r"\bwhy\b", r"\bhow\b", r"\bwhat does this mean\b"
            ]
        }
    
    def _detect_intent(self, query: str) -> str:
        """🧠 Smart Query Mode - Detect query intent"""
        query_lower = query.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    logger.info(f"🧠 Intent detected: {intent}")
                    return intent
        
        return "query"  # Default intent
    
    def plan(self, query: str, doc_preview: str) -> Dict[str, Any]:
        """Plan the task based on query and document preview with Smart Query Mode"""
        try:
            # 🧠 Step 1: Detect query intent (Smart Query Mode)
            intent = self._detect_intent(query)
            
            # Step 2: Detect document type
            doc_type = self._detect_document_type(doc_preview)
            
            # Step 3: Combine intent + doc_type for smart strategy
            if intent == "compare":
                task_type = "comparison_analysis"
                strategy = "structured_comparison"
                confidence = 0.9
            elif intent == "summarize":
                if doc_type == "resume":
                    task_type = "resume_summary"
                    strategy = "executive_summary"
                elif doc_type == "research":
                    task_type = "research_summary"
                    strategy = "abstract_key_findings"
                else:
                    task_type = "general_summary"
                    strategy = "comprehensive_overview"
                confidence = 0.9
            elif intent == "extract":
                task_type = "information_extraction"
                strategy = "targeted_extraction"
                confidence = 0.85
            elif intent == "analyze":
                task_type = "deep_analysis"
                strategy = "critical_analysis"
                confidence = 0.85
            # Document-specific fallbacks
            elif doc_type == "resume":
                task_type = "resume_analysis"
                strategy = "extract_skills_experience"
                confidence = 0.8
            elif doc_type == "research":
                task_type = "research_summary"
                strategy = "abstract_key_findings"
                confidence = 0.8
            elif doc_type == "invoice":
                task_type = "invoice_analysis"
                strategy = "extract_amounts_dates"
                confidence = 0.8
            elif doc_type == "legal":
                task_type = "legal_document"
                strategy = "extract_clauses_obligations"
                confidence = 0.8
            else:
                task_type = "general_qa"
                strategy = "contextual_answer"
                confidence = 0.6
            
            logger.info(f"🧠 Smart Query | Intent: {intent} | Task: {task_type} | Strategy: {strategy}")
            
            return {
                "task_type": task_type,
                "strategy": strategy,
                "confidence": confidence,
                "document_type": doc_type,
                "query_intent": intent  # 🧠 New: Include detected intent
            }
            
        except Exception as e:
            logger.error(f"Planning error: {e}")
            return {
                "task_type": "general_qa",
                "strategy": "fallback",
                "confidence": 0.3,
                "document_type": "unknown",
                "query_intent": "query"
            }
    
    def _detect_document_type(self, doc_preview: str) -> str:
        """Detect document type from preview"""
        if not doc_preview:
            return "unknown"
        
        preview_lower = doc_preview.lower()
        
        resume_keywords = ["experience", "education", "skills", "resume", "cv"]
        if sum(1 for kw in resume_keywords if kw in preview_lower) >= 2:
            return "resume"
        
        research_keywords = ["abstract", "methodology", "results", "conclusion"]
        if sum(1 for kw in research_keywords if kw in preview_lower) >= 2:
            return "research"
        
        invoice_keywords = ["invoice", "bill", "amount", "payment", "total"]
        if sum(1 for kw in invoice_keywords if kw in preview_lower) >= 2:
            return "invoice"
        
        legal_keywords = ["agreement", "contract", "clause", "terms", "conditions"]
        if sum(1 for kw in legal_keywords if kw in preview_lower) >= 2:
            return "legal"
        
        return "unknown"
