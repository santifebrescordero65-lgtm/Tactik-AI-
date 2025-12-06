"""
TACTIK AI - LLM Integration Module
Real avatar responses powered by OpenAI/Anthropic
"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from dotenv import load_dotenv
load_dotenv()


class LLMIntegration:
    """
    LLM Integration for TACTIK AI Avatar Simulation

    Generates high-fidelity avatar responses based on DNA profiles
    Calculates EIS, HCA, and DNA alignment scores
    """

    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        self.openai_client = None
        self.anthropic_client = None

        # Initialize clients
        if OPENAI_AVAILABLE and self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
            self.default_provider = "openai"
        elif ANTHROPIC_AVAILABLE and self.anthropic_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_key)
            self.default_provider = "anthropic"
        else:
            self.default_provider = None

    def is_configured(self) -> bool:
        """Check if LLM is configured"""
        return self.openai_client is not None or self.anthropic_client is not None

    def generate_avatar_response(
        self,
        avatar_dna,
        user_message: str,
        session_context,
        attempt: int = 1
    ) -> str:
        """
        Generate avatar response using LLM

        Args:
            avatar_dna: AvatarDNA object with complete profile
            user_message: User's message/question
            session_context: SessionContext with conversation history
            attempt: Attempt number (for regeneration)

        Returns:
            Avatar's response as string
        """
        if not self.is_configured():
            return f"[LLM not configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY]\n\nWould respond to: {user_message[:100]}..."

        # Build system prompt from DNA
        system_prompt = self._build_system_prompt(avatar_dna)

        # Build conversation history
        messages = self._build_conversation_history(session_context, user_message)

        # Generate response
        if self.default_provider == "openai":
            return self._generate_openai(system_prompt, messages, attempt)
        elif self.default_provider == "anthropic":
            return self._generate_anthropic(system_prompt, messages, attempt)
        else:
            return "[No LLM provider available]"

    def _build_system_prompt(self, avatar_dna) -> str:
        """
        Build system prompt from Avatar DNA

        This is the core of high-fidelity simulation - translating DNA into AI instructions
        """

        # Extract verified sources
        source_summary = avatar_dna.get_source_summary()
        coverage, breakdown = avatar_dna.calculate_source_coverage()

        # Build comprehensive prompt
        prompt = f"""You are simulating {avatar_dna.avatar_name}, {avatar_dna.role}.

This is a HIGH-FIDELITY STRATEGIC SIMULATION for preparation and rehearsal, not a casual chat.

Your responses must reflect this person's authentic:
- Thinking patterns
- Decision-making style
- Communication style
- Priorities and constraints
- Environmental pressures

═══════════════════════════════════════════════════════════════════
AVATAR DNA PROFILE
═══════════════════════════════════════════════════════════════════

ROLE & ENVIRONMENT:
{avatar_dna.role}
Environment: {avatar_dna.environment}

VALIDATED INFLUENCES (from verified sources):
"""

        # Add verified influences
        for influence in avatar_dna.influences.get("verified", [])[:5]:
            prompt += f"• {influence.get('influence', '')} (Impact: {influence.get('impact', 'unknown')})\n"

        prompt += "\nINFERRED INFLUENCES (speculative):\n"
        for influence in avatar_dna.influences.get("inferred", [])[:3]:
            prompt += f"• {influence.get('influence', '')} - {influence.get('rationale', '')}\n"

        prompt += f"""
VERIFIED THOUGHT PATTERNS:
"""
        for thought in avatar_dna.thoughts.get("verified", [])[:5]:
            prompt += f"• {thought.get('thought', '')}\n"

        prompt += f"""
BEHAVIORAL PATTERNS (documented):
"""
        for behavior in avatar_dna.behavioral_pattern.get("verified", [])[:5]:
            prompt += f"• {behavior.get('behavior', '')} - Context: {behavior.get('context', '')}\n"

        prompt += f"""
DECISION STYLE:
"""
        for style in avatar_dna.decision_style.get("verified", [])[:3]:
            prompt += f"• {style.get('style', '')}\n"

        prompt += f"""
COMMUNICATION STYLE:
"""
        for comm in avatar_dna.communication_style.get("verified", [])[:3]:
            prompt += f"• {comm.get('style', '')}\n"

        prompt += f"""
PRIORITIES:
"""
        for priority in avatar_dna.priorities.get("verified", [])[:5]:
            prompt += f"{priority.get('priority', '')}\n"

        prompt += f"""
CONSTRAINTS:
{json.dumps(avatar_dna.constraints, indent=2)}

═══════════════════════════════════════════════════════════════════
VALIDATION METRICS
═══════════════════════════════════════════════════════════════════

DNA Source Coverage: {coverage*100:.1f}%
Total Ground Truth Sources: {source_summary['total_sources']}
Cross-Verified Sources: {source_summary['cross_verified']}

Component Coverage:
• Influences: {breakdown.get('influences', 0)*100:.1f}%
• Thoughts: {breakdown.get('thoughts', 0)*100:.1f}%
• Behavioral Patterns: {breakdown.get('behavioral_pattern', 0)*100:.1f}%
• Decision Style: {breakdown.get('decision_style', 0)*100:.1f}%
• Communication: {breakdown.get('communication_style', 0)*100:.1f}%

═══════════════════════════════════════════════════════════════════
SIMULATION GUIDELINES
═══════════════════════════════════════════════════════════════════

1. AUTHENTICITY FIRST
   - Stay true to documented patterns and verified sources
   - When uncertain, acknowledge limitations honestly
   - Don't fabricate positions or statements

2. STRATEGIC DEPTH
   - Consider constraints, priorities, and environmental pressures
   - Respond with the strategic depth expected of this role
   - Balance ideals with practical realities

3. APPROPRIATE TONE
   - Match the communication style documented above
   - Adapt formality to the relationship and context
   - Show emotional intelligence where appropriate

4. DNA ALIGNMENT
   - Every response should align with the verified DNA profile
   - Reference specific influences when they shape your thinking
   - Acknowledge when inferred patterns are speculative

5. EMPATHY PAUSE PROTOCOL
   - If asked about topics outside your documented expertise: acknowledge uncertainty
   - If emotional/sensitive topics arise: show appropriate care
   - If contradictions appear in your DNA: surface them honestly

LANGUAGE: {avatar_dna.language}

You are {avatar_dna.avatar_name}. Respond as this person would, with their authentic voice, priorities, and strategic thinking.
"""

        return prompt

    def _build_conversation_history(self, session_context, current_message: str) -> List[Dict]:
        """Build conversation history for context"""
        messages = []

        # Add recent turns (last 10)
        for turn in session_context.transcript[-10:]:
            if turn.speaker_id == "user":
                messages.append({"role": "user", "content": turn.message})
            else:
                messages.append({"role": "assistant", "content": turn.message})

        # Add current message
        messages.append({"role": "user", "content": current_message})

        return messages

    def _generate_openai(self, system_prompt: str, messages: List[Dict], attempt: int) -> str:
        """Generate response using OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # Use GPT-4o for best quality
                messages=[
                    {"role": "system", "content": system_prompt}
                ] + messages,
                temperature=0.7 if attempt == 1 else 0.5,  # Lower temp on retry
                max_tokens=800
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"[OpenAI Error: {str(e)}]"

    def _generate_anthropic(self, system_prompt: str, messages: List[Dict], attempt: int) -> str:
        """Generate response using Anthropic Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                system=system_prompt,
                messages=messages,
                temperature=0.7 if attempt == 1 else 0.5
            )

            return response.content[0].text

        except Exception as e:
            return f"[Anthropic Error: {str(e)}]"

    def calculate_response_metrics(self, response: str, avatar_dna) -> Dict[str, float]:
        """
        Calculate EIS, HCA, and DNA scores for response

        In production: Would use semantic analysis
        For MVP: Simplified heuristic-based scoring

        Returns:
            {eis_score, hca_score, dna_score}
        """

        # EIS (Emotional Intelligence Score)
        eis_score = self._calculate_eis(response)

        # HCA (Human-Centered Approach Score)
        hca_score = self._calculate_hca(response)

        # DNA Alignment Score
        dna_score = self._calculate_dna_alignment(response, avatar_dna)

        return {
            "eis_score": eis_score,
            "hca_score": hca_score,
            "dna_score": dna_score
        }

    def _calculate_eis(self, response: str) -> float:
        """
        Calculate Emotional Intelligence Score

        Factors:
        - Empathy indicators (understanding, acknowledgment)
        - Emotional awareness
        - Appropriate tone
        """
        score = 0.7  # Base score

        # Positive indicators
        empathy_markers = [
            "understand", "appreciate", "recognize", "acknowledge",
            "perspective", "concern", "consider", "feel"
        ]

        response_lower = response.lower()
        for marker in empathy_markers:
            if marker in response_lower:
                score += 0.02

        # Check for appropriate length (too short = low EI)
        if len(response) < 100:
            score -= 0.1

        # Check for question marks (engagement)
        if "?" in response:
            score += 0.05

        return min(1.0, max(0.0, score))

    def _calculate_hca(self, response: str) -> float:
        """
        Calculate Human-Centered Approach Score

        Factors:
        - Practical value
        - Actionable insights
        - Respect for agency
        """
        score = 0.75  # Base score

        # Positive indicators
        hca_markers = [
            "you", "your", "could", "might", "consider",
            "option", "approach", "strategy", "solution"
        ]

        response_lower = response.lower()
        for marker in hca_markers:
            if marker in response_lower:
                score += 0.02

        # Check for structured thinking (bullet points, numbers)
        if "•" in response or any(str(i) + "." in response for i in range(1, 6)):
            score += 0.05

        return min(1.0, max(0.0, score))

    def _calculate_dna_alignment(self, response: str, avatar_dna) -> float:
        """
        Calculate DNA Alignment Score

        How well does the response align with avatar DNA?

        Factors:
        - Reference to documented priorities
        - Consistency with decision style
        - Alignment with constraints
        """
        score = 0.8  # Base score (assume good alignment if LLM followed prompt)

        # Check if response references constraints
        response_lower = response.lower()
        for constraint_type, constraint_desc in avatar_dna.constraints.items():
            if isinstance(constraint_desc, str) and any(
                word in response_lower
                for word in constraint_desc.lower().split()[:5]
            ):
                score += 0.03

        # Check language consistency
        if avatar_dna.language == "es":
            # Simple heuristic: Spanish uses more "de", "la", "el"
            spanish_markers = response_lower.count("de ") + response_lower.count("la ") + response_lower.count("el ")
            if spanish_markers > 5:
                score += 0.05

        # Penalize if too generic
        if len(response) < 150:
            score -= 0.1

        return min(1.0, max(0.0, score))


# ═══════════════════════════════════════════════════════════════════
# TESTING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def test_llm_integration():
    """Test LLM integration with sample avatar"""
    from tactik_algorithm import TACTIKEngine, create_ground_truth_source

    engine = TACTIKEngine()
    llm = LLMIntegration()

    if not llm.is_configured():
        print("❌ LLM not configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        return

    print(f"✅ LLM configured with provider: {llm.default_provider}")

    # Create simple test avatar
    sources = [
        create_ground_truth_source(
            source_id="test_001",
            tier="tier_1_primary",
            description="Test source",
            date="2024-01-01"
        )
    ]

    dna = engine.build_avatar_dna(
        avatar_id="test_avatar",
        avatar_name="Test Avatar",
        role="Strategic Advisor",
        sources=sources,
        influences_verified=[{"influence": "Data-driven decision making", "source_id": "test_001", "impact": "high"}],
        influences_inferred=[],
        thoughts_verified=[{"thought": "Strategic thinking is essential", "source_id": "test_001"}],
        thoughts_inferred=[],
        behavioral_verified=[{"behavior": "Analytical approach", "source_id": "test_001", "context": "Problem solving"}],
        behavioral_inferred=[],
        decision_style_verified=[{"style": "Evidence-based", "source_id": "test_001"}],
        decision_style_inferred=[],
        communication_verified=[{"style": "Clear and concise", "source_id": "test_001"}],
        communication_inferred=[],
        priorities_verified=[{"priority": "1. Strategic clarity", "source_id": "test_001"}],
        priorities_inferred=[],
        environment="Professional consulting",
        constraints={"time": "Limited availability"},
        language="en"
    )

    # Create session
    session = engine.create_multi_avatar_session(
        session_id="test_session",
        user_goal="Test LLM integration",
        avatar_ids=["test_avatar"]
    )

    # Generate response
    test_message = "What is your approach to strategic planning?"
    response = llm.generate_avatar_response(dna, test_message, session)

    print("\n" + "="*70)
    print("TEST RESPONSE:")
    print("="*70)
    print(response)
    print("="*70)

    # Calculate metrics
    metrics = llm.calculate_response_metrics(response, dna)
    print(f"\nMETRICS:")
    print(f"  EIS Score: {metrics['eis_score']:.2f}")
    print(f"  HCA Score: {metrics['hca_score']:.2f}")
    print(f"  DNA Score: {metrics['dna_score']:.2f}")


if __name__ == "__main__":
    test_llm_integration()
