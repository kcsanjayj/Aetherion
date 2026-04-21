"""
Agents - Consolidated Agent Components
All agent classes in one professional file
"""

from typing import Dict, Any, List, Optional
import re
import time
from backend.utils.logger import setup_logger
from backend.core.llm import LLMClient

# Import from separate files
from backend.agents.planner_agent import PlannerAgent
from backend.agents.critic_agent import CriticAgent

logger = setup_logger(__name__)


# =============================================================================
# 1. PLANNER AGENT - Imported from planner_agent.py
# =============================================================================

# PlannerAgent imported from backend.agents.planner_agent


# =============================================================================
# 2. REASONING AGENT - LLM Core
# =============================================================================

class ReasoningAgent:
    """Core LLM agent that generates responses based on context and task"""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.task_prompts = {
            "resume_analysis": """You are analyzing a resume/CV. Extract and present:
1. Professional Summary (2-3 sentences)
2. Key Points (4-6 bullets): Experience, skills, education, achievements, expertise, leadership

Use ONLY the resume content provided.""",
            
            "research_summary": """You are analyzing a research paper. Extract and present:
1. Research Summary (2-3 sentences)
2. Key Points (4-6 bullets): Objective, methodology, findings, conclusions, implications, limitations

Use ONLY the research paper content provided.""",
            
            "invoice_analysis": """You are analyzing an invoice/bill. Extract and present:
1. Invoice Summary (2-3 sentences)
2. Key Points (4-6 bullets): Invoice number, vendor, items, total amount, payment terms, due date

Use ONLY the invoice content provided.""",
            
            "legal_document": """You are analyzing a legal document. Extract and present:
1. Document Summary (2-3 sentences)
2. Key Points (4-6 bullets): Document type, parties, obligations, terms, duration, clauses

Use ONLY the legal document content provided.""",
            
            "general_summary": """You are analyzing a document. Extract and present:
1. Document Summary (2-3 sentences)
2. Key Points (4-6 bullets): Purpose, important info, key details, features, context, implications

Use ONLY the document content provided."""
        }
    
    async def reason(self, context: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response based on context and task"""
        try:
            start_time = time.time()
            
            task_type = task.get("task_type", "general_summary")
            base_prompt = self.task_prompts.get(task_type, self.task_prompts["general_summary"])
            
            prompt = f"""{base_prompt}

DOCUMENT CONTENT:
{context[:4000]}

Return your response in this format:

📄 Summary:
<2-3 sentence summary>

📌 Key Points:
• <Point 1>
• <Point 2>
• <Point 3>
• <Point 4>
• <Point 5>
• <Point 6>"""
            
            logger.info(f"🧠 Generating response for: {task_type}")
            response = await self.llm_client.generate_response(
                prompt=prompt, temperature=0.3, max_tokens=1500
            )
            
            return {
                "answer": response.strip(),
                "task_type": task_type,
                "confidence": task.get("confidence", 0.5),
                "processing_time": time.time() - start_time,
                "agent_trace": {"agent": "reasoning", "task": task_type}
            }
            
        except Exception as e:
            logger.error(f"Reasoning error: {e}")
            return {
                "answer": f"Error: {str(e)}",
                "task_type": task.get("task_type", "unknown"),
                "confidence": 0.0,
                "error": str(e)
            }


# =============================================================================
# 3. CRITIC AGENT - Imported from critic_agent.py
# =============================================================================

# CriticAgent imported from backend.agents.critic_agent


# =============================================================================
# 4. RETRY AGENT - Autonomy
# =============================================================================

class RetryAgent:
    """Handles intelligent retries with different strategies"""
    
    def __init__(self):
        self.reasoning_agent = ReasoningAgent()
        self.retry_strategies = ["broader_query", "full_document", "different_prompt", "minimal_summary"]
        self.max_retries = 2
    
    async def retry_if_needed(
        self, 
        is_valid: bool, 
        original_query: str,
        context: str, 
        task: Dict[str, Any],
        retrieved_docs: List[Dict[str, Any]],
        full_text: Optional[str] = None,
        force_regenerate: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Retry with different strategies if response is invalid"""
        
        if is_valid and not force_regenerate:
            return None
        
        logger.info("🔄 Starting retry...")
        
        # Check for weak context
        if self._is_weak_context(context, retrieved_docs) and full_text:
            context = full_text[:4000]
        
        for attempt in range(self.max_retries):
            strategy = self.retry_strategies[attempt]
            logger.info(f"🔄 Retry {attempt + 1}: {strategy}")
            
            try:
                if strategy == "broader_query":
                    new_context = self._retry_with_broader_query(retrieved_docs)
                elif strategy == "full_document" and full_text:
                    new_context = full_text[:4000]
                else:
                    new_context = context[:2000]
                    task = {"task_type": "general_summary", "strategy": "minimal"}
                
                response = await self.reasoning_agent.reason(new_context, task)
                response["agent_trace"]["retry_attempt"] = attempt + 1
                response["agent_trace"]["retry_strategy"] = strategy
                
                return response
                
            except Exception as e:
                logger.error(f"🔄 Retry {attempt + 1} failed: {e}")
                continue
        
        logger.error("🔄 All retries failed")
        return None
    
    def _is_weak_context(self, context: str, retrieved_docs: List[Dict[str, Any]]) -> bool:
        """Check if context is weak"""
        if len(context) < 500 or len(retrieved_docs) < 3:
            return True
        return False
    
    def _retry_with_broader_query(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Use more documents"""
        more_docs = retrieved_docs[:10] if len(retrieved_docs) > 6 else retrieved_docs
        return "\n\n".join([doc.get('content', '') for doc in more_docs])


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "PlannerAgent",
    "ReasoningAgent", 
    "CriticAgent",
    "RetryAgent"
]
