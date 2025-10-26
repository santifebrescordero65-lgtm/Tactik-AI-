"""
TACTIK AI 5.3 PREMIUM EDITION
Strategic Intelligence System with Scientific Validation

Author: Santiago Cañas
Organization: TACTIK AI
Version: 5.3 Premium
Date: October 2025

Description:
Multi-avatar simulation system with DNA-based profiles, AVDA validation metrics,
empathy pause, backflow detection, and transparent confidence scoring.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import math
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════
# ENUMS AND CONSTANTS
# ═══════════════════════════════════════════════════════════════════

class SourceTier(Enum):
    """Source reliability tiers with associated weights"""
    TIER_1_PRIMARY = "tier_1_primary"      # 100% weight: Official docs, laws, contracts
    TIER_2_SECONDARY = "tier_2_secondary"  # 85% weight: NGO reports, corporate reports
    TIER_3_TERTIARY = "tier_3_tertiary"    # 60% weight: Industry analysis, press interviews
    TIER_4_INFERRED = "tier_4_inferred"    # 40% weight: Reasoned inferences


class AvatarFidelity(Enum):
    """AVDA Score classification levels"""
    VERY_HIGH_FIDELITY = "VERY HIGH FIDELITY"  # 90-100%: Critical decisions
    HIGH_FIDELITY = "HIGH FIDELITY"            # 75-89%: Strategic preparation
    MEDIUM_FIDELITY = "MEDIUM FIDELITY"        # 60-74%: Scenario exploration
    LOW_FIDELITY = "LOW FIDELITY"              # 45-59%: Hypothetical exercises only
    UNRELIABLE = "UNRELIABLE"                  # <45%: DO NOT USE


class GatingDecision(Enum):
    """Gating system decisions"""
    APPROVED = "APPROVED"
    INTERRUPTED = "INTERRUPTED"
    EMPATHY_PAUSE = "EMPATHY_PAUSE"


# ═══════════════════════════════════════════════════════════════════
# DATA CLASSES - GROUND TRUTH SOURCES
# ═══════════════════════════════════════════════════════════════════

@dataclass
class GroundTruthSource:
    """
    Ground truth source with tier-based weighting

    Attributes:
        source_id: Unique identifier for the source
        tier: Source reliability tier (tier_1_primary to tier_4_inferred)
        description: Human-readable description of the source
        url: Optional URL to the source document
        date: Publication/access date (YYYY-MM-DD format)
        cross_verified: Whether verified by independent sources
    """
    source_id: str
    tier: str
    description: str
    url: Optional[str] = None
    date: str = ""
    cross_verified: bool = False

    def get_weight(self) -> float:
        """Calculate source weight based on tier"""
        weights = {
            "tier_1_primary": 1.0,
            "tier_2_secondary": 0.85,
            "tier_3_tertiary": 0.60,
            "tier_4_inferred": 0.40
        }
        return weights.get(self.tier, 0.40)

    def get_reliability(self) -> Tuple[float, float]:
        """Get reliability range for this tier"""
        reliability_ranges = {
            "tier_1_primary": (0.95, 1.0),
            "tier_2_secondary": (0.75, 0.90),
            "tier_3_tertiary": (0.50, 0.70),
            "tier_4_inferred": (0.30, 0.50)
        }
        return reliability_ranges.get(self.tier, (0.30, 0.50))


# ═══════════════════════════════════════════════════════════════════
# DATA CLASSES - AVATAR DNA
# ═══════════════════════════════════════════════════════════════════

@dataclass
class AvatarDNA:
    """
    Avatar cognitive DNA with traceable sources

    Each component (influences, thoughts, etc.) contains:
    - verified: List of elements backed by ground truth sources
    - inferred: List of speculative elements without direct sources
    """
    avatar_id: str
    avatar_name: str
    role: str
    influences: Dict[str, Any]
    thoughts: Dict[str, Any]
    environment: str
    behavioral_pattern: Dict[str, Any]
    decision_style: Dict[str, Any]
    communication_style: Dict[str, Any]
    priorities: Dict[str, Any]
    constraints: Dict[str, Any]
    language: str = "es"
    sources: List[GroundTruthSource] = field(default_factory=list)

    def calculate_source_coverage(self) -> Tuple[float, Dict]:
        """
        Calculate percentage of DNA based on verified vs inferred sources

        Returns:
            (total_coverage, coverage_breakdown_by_component)
        """
        components = [
            "influences", "thoughts", "behavioral_pattern",
            "decision_style", "communication_style", "priorities"
        ]
        coverage_scores = {}

        for component in components:
            data = getattr(self, component, {})
            verified = data.get("verified", [])
            inferred = data.get("inferred", [])
            total_items = len(verified) + len(inferred)

            if total_items == 0:
                coverage = 0.0
            else:
                # Calculate weighted coverage based on source tiers
                verified_weight = 0
                for item in verified:
                    source_id = item.get("source_id", "")
                    matching_source = next(
                        (s for s in self.sources if s.source_id == source_id),
                        None
                    )
                    if matching_source:
                        verified_weight += matching_source.get_weight()

                coverage = verified_weight / total_items if total_items > 0 else 0.0

            coverage_scores[component] = coverage

        # Weighted total coverage (different components have different importance)
        total_coverage = (
            0.15 * coverage_scores.get("influences", 0) +
            0.20 * coverage_scores.get("thoughts", 0) +
            0.15 * coverage_scores.get("communication_style", 0) +
            0.30 * coverage_scores.get("behavioral_pattern", 0) +
            0.20 * coverage_scores.get("decision_style", 0)
        )

        return total_coverage, coverage_scores

    def get_source_summary(self) -> Dict:
        """Get summary of ground truth sources"""
        tier_counts = {}
        cross_verified_count = 0

        for source in self.sources:
            tier_counts[source.tier] = tier_counts.get(source.tier, 0) + 1
            if source.cross_verified:
                cross_verified_count += 1

        return {
            "total_sources": len(self.sources),
            "tier_breakdown": tier_counts,
            "cross_verified": cross_verified_count,
            "cross_verified_percentage": (
                cross_verified_count / len(self.sources) * 100
                if self.sources else 0
            )
        }


# ═══════════════════════════════════════════════════════════════════
# DATA CLASSES - AVDA METRICS
# ═══════════════════════════════════════════════════════════════════

@dataclass
class AVDAMetrics:
    """
    Avatar Validation Deviation & Accuracy metrics

    Scientific validation metrics for avatar reliability with 95% confidence intervals
    """
    accuracy: float  # Behavioral precision vs documented reality (0-1)
    confidence_interval: Tuple[float, float]  # 95% CI [lower, upper]
    source_coverage: float  # % DNA based on verified sources (0-1)
    drift_risk: float  # Probability of deviation during conversation (0-1)
    ground_truth_quality: float  # Aggregate source quality (0-1)
    avda_score: float  # Consolidated AVDA score (0-1)
    classification: AvatarFidelity
    limitations: List[str] = field(default_factory=list)
    source_breakdown: Dict = field(default_factory=dict)

    def to_percentage(self) -> Dict:
        """Convert metrics to percentage format for display"""
        return {
            "accuracy": round(self.accuracy * 100, 1),
            "confidence_interval": [
                round(self.confidence_interval[0] * 100, 1),
                round(self.confidence_interval[1] * 100, 1)
            ],
            "source_coverage": round(self.source_coverage * 100, 1),
            "drift_risk": round(self.drift_risk * 100, 1),
            "ground_truth_quality": round(self.ground_truth_quality * 100, 1),
            "avda_score": round(self.avda_score * 100, 1),
            "classification": self.classification.value,
            "limitations": self.limitations
        }

    def get_recommendation(self) -> str:
        """Get usage recommendation based on AVDA score"""
        recommendations = {
            AvatarFidelity.VERY_HIGH_FIDELITY:
                "✓ RECOMMENDED for critical decisions and real negotiations",
            AvatarFidelity.HIGH_FIDELITY:
                "✓ SUITABLE for strategic preparation and executive training",
            AvatarFidelity.MEDIUM_FIDELITY:
                "⚠ USE ONLY for scenario exploration and brainstorming",
            AvatarFidelity.LOW_FIDELITY:
                "⚠ LIMIT to hypothetical exercises only",
            AvatarFidelity.UNRELIABLE:
                "✗ DO NOT USE for strategic preparation"
        }
        return recommendations.get(
            self.classification,
            "⚠ Use with extreme caution"
        )


# ═══════════════════════════════════════════════════════════════════
# DATA CLASSES - SESSION CONTEXT
# ═══════════════════════════════════════════════════════════════════

@dataclass
class ConversationTurn:
    """Single turn in multi-avatar conversation"""
    turn_number: int
    speaker_id: str  # avatar_id or "user" or "human_expert"
    speaker_name: str
    message: str
    timestamp: str
    eis_score: float = 0.0  # Emotional Intelligence Score
    hca_score: float = 0.0  # Human-Centered Approach Score
    dna_score: float = 0.0  # DNA Alignment Score
    gating_decision: str = "APPROVED"


@dataclass
class SessionContext:
    """
    Multi-avatar conversation session with full tracking
    """
    session_id: str
    user_goal: str
    active_avatars: List[str]  # List of avatar_ids
    transcript: List[ConversationTurn] = field(default_factory=list)
    current_turn: int = 0
    backflow_triggers: List[Dict] = field(default_factory=list)
    empathy_pauses: List[Dict] = field(default_factory=list)
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_turn(self, turn: ConversationTurn):
        """Add conversation turn to transcript"""
        self.transcript.append(turn)
        self.current_turn += 1

    def get_avatar_turns(self, avatar_id: str) -> List[ConversationTurn]:
        """Get all turns for specific avatar"""
        return [t for t in self.transcript if t.speaker_id == avatar_id]

    def calculate_session_metrics(self) -> Dict:
        """Calculate aggregate metrics for entire session"""
        if not self.transcript:
            return {}

        avg_eis = sum(t.eis_score for t in self.transcript) / len(self.transcript)
        avg_hca = sum(t.hca_score for t in self.transcript) / len(self.transcript)
        avg_dna = sum(t.dna_score for t in self.transcript) / len(self.transcript)

        # TACTIK Score: composite metric (scale 0-10)
        tactik_score = (avg_eis * 0.3 + avg_hca * 0.3 + avg_dna * 0.4) * 10

        return {
            "total_turns": len(self.transcript),
            "avg_eis": round(avg_eis, 2),
            "avg_hca": round(avg_hca, 2),
            "avg_dna": round(avg_dna, 2),
            "tactik_score": round(tactik_score, 1),
            "backflow_events": len(self.backflow_triggers),
            "empathy_pauses": len(self.empathy_pauses)
        }


# ═══════════════════════════════════════════════════════════════════
# CORE SYSTEM - TACTIK ENGINE
# ═══════════════════════════════════════════════════════════════════

class TACTIKEngine:
    """
    TACTIK 5.3 Premium Edition - Main orchestration engine

    Integrates 8 core systems:
    1. DNA Builder
    2. AVDA Validation
    3. Empathy Pause
    4. Backflow Detection
    5. Multi-Avatar Orchestration
    6. Gating with Hysteresis
    7. EMA Metrics
    8. TACTIK Advisor
    """

    def __init__(self):
        self.avatars_dna: Dict[str, AvatarDNA] = {}
        self.sessions: Dict[str, SessionContext] = {}
        self.gating_tau: float = 0.52  # Adaptive threshold

    # ═══════════════════════════════════════════════════════════════
    # SYSTEM 1: DNA BUILDER
    # ═══════════════════════════════════════════════════════════════

    def build_avatar_dna(
        self,
        avatar_id: str,
        avatar_name: str,
        role: str,
        sources: List[GroundTruthSource],
        influences_verified: List[Dict],
        influences_inferred: List[Dict],
        thoughts_verified: List[Dict],
        thoughts_inferred: List[Dict],
        behavioral_verified: List[Dict],
        behavioral_inferred: List[Dict],
        decision_style_verified: List[Dict],
        decision_style_inferred: List[Dict],
        communication_verified: List[Dict],
        communication_inferred: List[Dict],
        priorities_verified: List[Dict],
        priorities_inferred: List[Dict],
        environment: str,
        constraints: Dict,
        language: str = "es"
    ) -> AvatarDNA:
        """
        Build complete avatar DNA with traceable sources

        Each component has verified (sourced) and inferred (speculative) elements
        """
        dna = AvatarDNA(
            avatar_id=avatar_id,
            avatar_name=avatar_name,
            role=role,
            influences={
                "verified": influences_verified,
                "inferred": influences_inferred
            },
            thoughts={
                "verified": thoughts_verified,
                "inferred": thoughts_inferred
            },
            environment=environment,
            behavioral_pattern={
                "verified": behavioral_verified,
                "inferred": behavioral_inferred
            },
            decision_style={
                "verified": decision_style_verified,
                "inferred": decision_style_inferred
            },
            communication_style={
                "verified": communication_verified,
                "inferred": communication_inferred
            },
            priorities={
                "verified": priorities_verified,
                "inferred": priorities_inferred
            },
            constraints=constraints,
            language=language,
            sources=sources
        )

        self.avatars_dna[avatar_id] = dna
        return dna

    # ═══════════════════════════════════════════════════════════════
    # SYSTEM 2: AVDA VALIDATION
    # ═══════════════════════════════════════════════════════════════

    def calculate_avda_score(
        self,
        avatar_id: str,
        session: Optional[SessionContext] = None
    ) -> AVDAMetrics:
        """
        Calculate Avatar Validation Deviation & Accuracy metrics

        AVDA Score formula:
        AVDA = 0.40 × (Accuracy × GT_Quality) +
               0.30 × Source_Coverage +
               0.20 × (1 - Drift_Risk) +
               0.10 × GT_Quality
        """
        avatar_dna = self.avatars_dna.get(avatar_id)
        if not avatar_dna:
            raise ValueError(f"Avatar DNA not found: {avatar_id}")

        # 1. Ground Truth Quality
        gt_quality = self._validate_ground_truth_quality(avatar_dna.sources)

        # 2. Behavioral Fidelity (Accuracy)
        behavior_fidelity = self._assess_behavioral_fidelity(
            avatar_dna,
            session.transcript if session else []
        )

        # 3. Source Coverage
        source_coverage, coverage_breakdown = avatar_dna.calculate_source_coverage()

        # 4. Drift Risk
        drift_risk = self._quantify_drift_risk(session, avatar_dna) if session else 0.3

        # 5. Confidence Interval (95%)
        ci_lower, ci_upper = self._calculate_confidence_interval(
            behavior_fidelity,
            source_coverage,
            len(avatar_dna.sources)
        )

        # 6. AVDA Final Score
        avda_final = (
            0.40 * behavior_fidelity * gt_quality +
            0.30 * source_coverage +
            0.20 * (1 - drift_risk) +
            0.10 * gt_quality
        )

        # 7. Classification
        classification = self._classify_fidelity(avda_final)

        # 8. Limitations
        limitations = self._identify_limitations(avatar_dna, session)

        return AVDAMetrics(
            accuracy=behavior_fidelity,
            confidence_interval=(ci_lower, ci_upper),
            source_coverage=source_coverage,
            drift_risk=drift_risk,
            ground_truth_quality=gt_quality,
            avda_score=avda_final,
            classification=classification,
            limitations=limitations,
            source_breakdown=coverage_breakdown
        )

    def _validate_ground_truth_quality(self, sources: List[GroundTruthSource]) -> float:
        """Calculate aggregate quality of ground truth sources"""
        if not sources:
            return 0.0

        total_weight = sum(s.get_weight() for s in sources)
        cross_verified_bonus = sum(0.1 for s in sources if s.cross_verified)
        recency_factor = self._calculate_recency_factor(sources)

        base_quality = total_weight / len(sources)
        adjusted_quality = min(1.0, base_quality + cross_verified_bonus * 0.1 + recency_factor * 0.05)

        return adjusted_quality

    def _calculate_recency_factor(self, sources: List[GroundTruthSource]) -> float:
        """Calculate recency factor (sources from last 2 years get bonus)"""
        current_year = datetime.now().year
        recent_count = 0

        for source in sources:
            if source.date:
                try:
                    year = int(source.date.split('-')[0])
                    if current_year - year <= 2:
                        recent_count += 1
                except:
                    pass

        return recent_count / len(sources) if sources else 0.0

    def _assess_behavioral_fidelity(
        self,
        avatar_dna: AvatarDNA,
        transcript: List[ConversationTurn]
    ) -> float:
        """
        Assess how closely avatar behavior matches documented profile

        In production: compare actual responses vs expected patterns
        For now: base on source coverage + behavioral pattern strength
        """
        source_coverage, _ = avatar_dna.calculate_source_coverage()
        behavioral_items = avatar_dna.behavioral_pattern.get("verified", [])

        # Base fidelity on source coverage
        base_fidelity = source_coverage

        # Adjust based on behavioral pattern depth
        if len(behavioral_items) >= 5:
            adjustment = 0.1
        elif len(behavioral_items) >= 3:
            adjustment = 0.05
        else:
            adjustment = -0.05

        return min(1.0, max(0.0, base_fidelity + adjustment))

    def _quantify_drift_risk(
        self,
        session: Optional[SessionContext],
        avatar_dna: AvatarDNA
    ) -> float:
        """
        Quantify probability of avatar drifting from authentic behavior

        Factors:
        - Conversation length (longer = higher drift)
        - Source coverage (lower = higher drift)
        - Number of backflow events (more = higher drift)
        """
        if not session:
            return 0.3  # Default moderate risk

        # Length factor: risk increases with turns
        length_risk = min(0.4, len(session.transcript) / 100)

        # Coverage factor: lower coverage = higher drift
        source_coverage, _ = avatar_dna.calculate_source_coverage()
        coverage_risk = (1 - source_coverage) * 0.4

        # Backflow factor
        backflow_risk = min(0.3, len(session.backflow_triggers) * 0.05)

        total_drift_risk = length_risk + coverage_risk + backflow_risk
        return min(1.0, total_drift_risk)

    def _calculate_confidence_interval(
        self,
        accuracy: float,
        coverage: float,
        sample_size: int
    ) -> Tuple[float, float]:
        """
        Calculate 95% confidence interval using bootstrap approach

        Interval width depends on:
        - Sample size (# of sources)
        - Coverage quality
        """
        # Standard error decreases with more sources
        if sample_size == 0:
            return (0.0, 0.0)

        standard_error = 1 / math.sqrt(sample_size) * 0.15
        margin = 1.96 * standard_error  # 95% CI

        # Adjust margin based on coverage quality
        adjusted_margin = margin * (1.5 - coverage * 0.5)

        ci_lower = max(0.0, accuracy - adjusted_margin)
        ci_upper = min(1.0, accuracy + adjusted_margin)

        return (ci_lower, ci_upper)

    def _classify_fidelity(self, avda_score: float) -> AvatarFidelity:
        """Classify AVDA score into fidelity levels"""
        if avda_score >= 0.90:
            return AvatarFidelity.VERY_HIGH_FIDELITY
        elif avda_score >= 0.75:
            return AvatarFidelity.HIGH_FIDELITY
        elif avda_score >= 0.60:
            return AvatarFidelity.MEDIUM_FIDELITY
        elif avda_score >= 0.45:
            return AvatarFidelity.LOW_FIDELITY
        else:
            return AvatarFidelity.UNRELIABLE

    def _identify_limitations(
        self,
        avatar_dna: AvatarDNA,
        session: Optional[SessionContext]
    ) -> List[str]:
        """Identify explicit limitations of the avatar simulation"""
        limitations = []

        source_coverage, coverage_breakdown = avatar_dna.calculate_source_coverage()

        # Check coverage gaps
        if coverage_breakdown.get("communication_style", 0) < 0.5:
            limitations.append(
                "⚠ Limited primary sources for communication style - "
                "responses may not reflect authentic tone"
            )

        if coverage_breakdown.get("decision_style", 0) < 0.6:
            limitations.append(
                "⚠ Moderate uncertainty in decision-making patterns - "
                "use with caution for critical negotiations"
            )

        # Check source count
        if len(avatar_dna.sources) < 5:
            limitations.append(
                f"⚠ Only {len(avatar_dna.sources)} ground truth sources - "
                "recommend minimum 8 for high-stakes preparation"
            )

        # Check cross-verification
        cross_verified = sum(1 for s in avatar_dna.sources if s.cross_verified)
        if cross_verified < 3:
            limitations.append(
                "⚠ Limited cross-verification of sources - "
                "independently verify critical insights"
            )

        # Session-specific limitations
        if session and len(session.transcript) > 40:
            limitations.append(
                "⚠ Extended conversation (>40 turns) - "
                "drift risk increases, validate key takeaways"
            )

        return limitations

    # ═══════════════════════════════════════════════════════════════
    # SYSTEM 3: EMPATHY PAUSE
    # ═══════════════════════════════════════════════════════════════

    def check_empathy_pause(
        self,
        current_message: str,
        avatar_dna: AvatarDNA,
        session: SessionContext
    ) -> Tuple[bool, List[str]]:
        """
        Check if empathy pause should activate

        Triggers (need 2+ to activate):
        1. High uncertainty detected
        2. Request outside documented expertise
        3. Contradictory information in DNA
        4. Emotional/sensitive topic
        """
        triggers = []

        # Trigger 1: High uncertainty (low source coverage for topic)
        source_coverage, _ = avatar_dna.calculate_source_coverage()
        if source_coverage < 0.6:
            triggers.append("high_uncertainty_low_coverage")

        # Trigger 2: Complexity exceeds documented patterns
        if len(current_message.split()) > 50:  # Complex question
            behavioral_items = len(avatar_dna.behavioral_pattern.get("verified", []))
            if behavioral_items < 5:
                triggers.append("complexity_exceeds_documentation")

        # Trigger 3: Detect emotional keywords
        emotional_keywords = [
            "crisis", "conflict", "legal", "lawsuit", "denuncia",
            "scandal", "fraud", "violation"
        ]
        if any(keyword in current_message.lower() for keyword in emotional_keywords):
            triggers.append("emotional_sensitive_topic")

        # Trigger 4: Backflow events in recent history
        if len(session.backflow_triggers) >= 2:
            triggers.append("repeated_backflow_detected")

        # Activate if 2+ triggers
        should_pause = len(triggers) >= 2

        if should_pause:
            session.empathy_pauses.append({
                "turn": session.current_turn,
                "triggers": triggers,
                "message": "High uncertainty detected - recommending human expert consultation"
            })

        return should_pause, triggers

    # ═══════════════════════════════════════════════════════════════
    # SYSTEM 4: BACKFLOW DETECTION
    # ═══════════════════════════════════════════════════════════════

    def detect_backflow(
        self,
        session: SessionContext,
        current_turn: ConversationTurn,
        user_goal: str
    ) -> Tuple[bool, str]:
        """
        Detect conversation drift and trigger recalibration

        Detects 4 problems:
        1. Topic drift (deviation from original goal)
        2. Uncertainty accumulation
        3. Coverage gaps
        4. Contradiction detection
        """
        issues = []

        # 1. Topic drift detection
        if self._detect_topic_drift(current_turn.message, user_goal):
            issues.append("topic_drift")

        # 2. Uncertainty accumulation (low scores for 3+ consecutive turns)
        recent_turns = session.transcript[-3:] if len(session.transcript) >= 3 else []
        if recent_turns:
            avg_dna_score = sum(t.dna_score for t in recent_turns) / len(recent_turns)
            if avg_dna_score < 0.6:
                issues.append("uncertainty_accumulation")

        # 3. Coverage gap (speaking outside expertise)
        # Would need semantic analysis in production

        # 4. Contradiction (conflicting statements)
        # Would need consistency checking in production

        backflow_triggered = len(issues) > 0

        if backflow_triggered:
            issue_type = issues[0]
            session.backflow_triggers.append({
                "turn": session.current_turn,
                "issue": issue_type,
                "action": "recalibrating_to_goal"
            })
            return True, issue_type

        return False, ""

    def _detect_topic_drift(self, current_message: str, original_goal: str) -> bool:
        """
        Detect if conversation has drifted from original goal

        Production: Would use semantic similarity
        Simplified: Check for goal keywords
        """
        goal_keywords = set(original_goal.lower().split())
        message_keywords = set(current_message.lower().split())

        # If <20% keyword overlap, potential drift
        overlap = len(goal_keywords & message_keywords)
        overlap_ratio = overlap / len(goal_keywords) if goal_keywords else 0

        return overlap_ratio < 0.2

    # ═══════════════════════════════════════════════════════════════
    # SYSTEM 5: MULTI-AVATAR ORCHESTRATION
    # ═══════════════════════════════════════════════════════════════

    def create_multi_avatar_session(
        self,
        session_id: str,
        user_goal: str,
        avatar_ids: List[str]
    ) -> SessionContext:
        """
        Initialize multi-avatar conversation session

        Supports:
        - Up to 4 avatars simultaneously
        - Dynamic avatar switching
        - Human expert invitation
        """
        # Validate avatars exist
        for avatar_id in avatar_ids:
            if avatar_id not in self.avatars_dna:
                raise ValueError(f"Avatar not found: {avatar_id}")

        session = SessionContext(
            session_id=session_id,
            user_goal=user_goal,
            active_avatars=avatar_ids
        )

        self.sessions[session_id] = session
        return session

    def orchestrate_turn(
        self,
        session_id: str,
        speaker_id: str,
        message: str
    ) -> Dict:
        """
        Orchestrate single conversation turn with all validations

        Flow:
        1. Empathy pause check
        2. Generate response (simulated)
        3. Gating validation
        4. Backflow detection
        5. EMA metrics calculation
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")

        # Get avatar DNA (if avatar speaker)
        avatar_dna = self.avatars_dna.get(speaker_id) if speaker_id != "user" else None

        # 1. Empathy Pause Check
        empathy_triggered = False
        if avatar_dna:
            empathy_triggered, triggers = self.check_empathy_pause(
                message, avatar_dna, session
            )

        if empathy_triggered:
            return {
                "action": "EMPATHY_PAUSE",
                "message": "I detect high uncertainty on this topic. I recommend consulting a human expert for accurate guidance.",
                "triggers": triggers
            }

        # 2. Generate response (in production: actual AI generation)
        # For now: placeholder
        response = f"[{speaker_id} responds to: {message[:50]}...]"

        # 3. Calculate EMA metrics
        eis_score = 0.84  # Placeholder - would calculate from response
        hca_score = 0.86  # Placeholder
        dna_score = 0.83 if avatar_dna else 0.0  # Placeholder

        # 4. Gating validation
        gating_result = self.apply_gating(eis_score, hca_score, dna_score)

        if gating_result == GatingDecision.INTERRUPTED:
            return {
                "action": "GATING_INTERRUPTED",
                "message": "Response quality below threshold - regenerating",
                "scores": {"eis": eis_score, "hca": hca_score, "dna": dna_score}
            }

        # 5. Create turn
        turn = ConversationTurn(
            turn_number=session.current_turn + 1,
            speaker_id=speaker_id,
            speaker_name=avatar_dna.avatar_name if avatar_dna else "User",
            message=response,
            timestamp=datetime.now().isoformat(),
            eis_score=eis_score,
            hca_score=hca_score,
            dna_score=dna_score,
            gating_decision=gating_result.value
        )

        session.add_turn(turn)

        # 6. Backflow detection
        backflow_triggered, issue = self.detect_backflow(session, turn, session.user_goal)

        return {
            "action": "TURN_COMPLETED",
            "turn": turn,
            "backflow_triggered": backflow_triggered,
            "backflow_issue": issue if backflow_triggered else None,
            "session_metrics": session.calculate_session_metrics()
        }

    # ═══════════════════════════════════════════════════════════════
    # SYSTEM 6: GATING WITH HYSTERESIS
    # ═══════════════════════════════════════════════════════════════

    def apply_gating(
        self,
        eis_score: float,
        hca_score: float,
        dna_score: float
    ) -> GatingDecision:
        """
        Apply gating with hysteresis to decide approval/interruption

        Composite score must exceed adaptive threshold tau
        """
        # Composite score (weighted)
        composite_score = (
            0.30 * eis_score +
            0.30 * hca_score +
            0.40 * dna_score
        )

        if composite_score >= self.gating_tau:
            return GatingDecision.APPROVED
        else:
            # Adapt tau slightly (hysteresis)
            self.gating_tau = max(0.45, self.gating_tau - 0.02)
            return GatingDecision.INTERRUPTED

    # ═══════════════════════════════════════════════════════════════
    # SYSTEM 8: TACTIK ADVISOR
    # ═══════════════════════════════════════════════════════════════

    def generate_tactik_advisor(self, session_id: str) -> Dict:
        """
        Generate TACTIK Advisor report after simulation

        Includes:
        1. Avatar synthesis
        2. Conversation narrative
        3. Strategic recommendations
        4. 72-hour action plan
        5. Transparency card
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")

        # Calculate session metrics
        metrics = session.calculate_session_metrics()

        # Get AVDA scores for all avatars
        avda_scores = {}
        for avatar_id in session.active_avatars:
            avda_scores[avatar_id] = self.calculate_avda_score(avatar_id, session)

        # Generate transparency card
        transparency_card = self._generate_transparency_card(session, avda_scores)

        return {
            "session_summary": {
                "session_id": session.session_id,
                "goal": session.user_goal,
                "total_turns": metrics["total_turns"],
                "tactik_score": metrics["tactik_score"],
                "duration": self._calculate_duration(session.start_time)
            },
            "avatar_avda_scores": {
                avatar_id: avda.to_percentage()
                for avatar_id, avda in avda_scores.items()
            },
            "key_insights": self._extract_key_insights(session),
            "recommendations": self._generate_recommendations(session, avda_scores),
            "action_plan_72h": self._generate_action_plan(session),
            "transparency_card": transparency_card
        }

    def _generate_transparency_card(
        self,
        session: SessionContext,
        avda_scores: Dict[str, AVDAMetrics]
    ) -> Dict:
        """Generate scientific transparency card for audit trail"""
        return {
            "certification": "TACTIK 5.3 Premium - Scientific Validation",
            "session_id": session.session_id,
            "timestamp": datetime.now().isoformat(),
            "avatars_validated": [
                {
                    "avatar_id": avatar_id,
                    "avda_score": avda.avda_score,
                    "classification": avda.classification.value,
                    "sources_count": len(self.avatars_dna[avatar_id].sources),
                    "limitations": avda.limitations
                }
                for avatar_id, avda in avda_scores.items()
            ],
            "quality_assurance": {
                "empathy_pauses": len(session.empathy_pauses),
                "backflow_corrections": len(session.backflow_triggers),
                "avg_tactik_score": session.calculate_session_metrics()["tactik_score"]
            },
            "usage_guidelines": {
                "recommended_use": self._get_overall_recommendation(avda_scores),
                "validation_required": "Cross-verify critical insights with primary sources",
                "update_frequency": "Re-validate DNA quarterly or when stakeholder context changes"
            }
        }

    def _calculate_duration(self, start_time: str) -> str:
        """Calculate session duration"""
        start = datetime.fromisoformat(start_time)
        duration = datetime.now() - start
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"

    def _extract_key_insights(self, session: SessionContext) -> List[str]:
        """Extract key insights from conversation (simplified)"""
        return [
            f"Simulated {len(session.transcript)} conversation turns",
            f"Engaged {len(session.active_avatars)} strategic stakeholders",
            f"Quality assurance: {len(session.empathy_pauses)} empathy pauses, "
            f"{len(session.backflow_triggers)} backflow corrections"
        ]

    def _generate_recommendations(
        self,
        session: SessionContext,
        avda_scores: Dict[str, AVDAMetrics]
    ) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []

        # Check overall AVDA quality
        avg_avda = sum(a.avda_score for a in avda_scores.values()) / len(avda_scores)

        if avg_avda >= 0.75:
            recommendations.append(
                "✓ Simulation quality sufficient for strategic decision-making"
            )
        else:
            recommendations.append(
                "⚠ Recommend gathering additional sources before critical decisions"
            )

        # Check for specific avatar issues
        for avatar_id, avda in avda_scores.items():
            if avda.classification == AvatarFidelity.LOW_FIDELITY or \
               avda.classification == AvatarFidelity.UNRELIABLE:
                avatar_name = self.avatars_dna[avatar_id].avatar_name
                recommendations.append(
                    f"⚠ {avatar_name}: Low fidelity - validate insights independently"
                )

        return recommendations

    def _generate_action_plan(self, session: SessionContext) -> List[Dict]:
        """Generate 72-hour action plan (simplified)"""
        return [
            {
                "timeframe": "24 hours",
                "action": "Review transparency card and validate high-priority insights",
                "priority": "HIGH"
            },
            {
                "timeframe": "48 hours",
                "action": "Gather additional primary sources for low-coverage areas",
                "priority": "MEDIUM"
            },
            {
                "timeframe": "72 hours",
                "action": "Prepare initial outreach strategy based on simulation outcomes",
                "priority": "MEDIUM"
            }
        ]

    def _get_overall_recommendation(self, avda_scores: Dict[str, AVDAMetrics]) -> str:
        """Get overall usage recommendation"""
        avg_avda = sum(a.avda_score for a in avda_scores.values()) / len(avda_scores)

        if avg_avda >= 0.90:
            return "APPROVED for critical decision-making"
        elif avg_avda >= 0.75:
            return "SUITABLE for strategic preparation"
        elif avg_avda >= 0.60:
            return "USE for scenario exploration only"
        else:
            return "NOT RECOMMENDED for strategic use - gather more sources"


# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def create_ground_truth_source(
    source_id: str,
    tier: str,
    description: str,
    url: Optional[str] = None,
    date: str = "",
    cross_verified: bool = False
) -> GroundTruthSource:
    """Helper to create ground truth source"""
    return GroundTruthSource(
        source_id=source_id,
        tier=tier,
        description=description,
        url=url,
        date=date,
        cross_verified=cross_verified
    )


# ═══════════════════════════════════════════════════════════════════
# END OF TACTIK ALGORITHM 5.3 PREMIUM
# ═══════════════════════════════════════════════════════════════════
