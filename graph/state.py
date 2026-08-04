from dataclasses import dataclass, field
from typing import List, Dict, Optional
from graph.enums import DebatePhase
from schemas.debate_plan import DebatePlan
# -------------------------------
# Individual Debate Message
# -------------------------------
@dataclass
class DebateMessage:
    speaker: str          # "user" or "ai"
    content: str
# -------------------------------
# Evidence Retrieved via RAG
# -------------------------------
@dataclass
class Evidence:
    source: str
    content: str
    relevance_score: float
# -------------------------------
# Tool Output
# -------------------------------
@dataclass
class ToolOutput:
    tool_name: str
    result: str
# -------------------------------
# Debate Evaluation
# -------------------------------
@dataclass
class DebateScore:
    logic: float = 0.0
    evidence: float = 0.0
    clarity: float = 0.0
    persuasion: float = 0.0
# -------------------------------
# Long-Term User Profile
# -------------------------------
@dataclass
class UserProfile:
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    favorite_topics: List[str] = field(default_factory=list)
    common_fallacies: List[str] = field(default_factory=list)
# -------------------------------
# Main Graph State
# -------------------------------
@dataclass
class DebateState:
    topic: str
    user_stance: str
    ai_stance: str
    current_phase: DebatePhase
    debate_history: List[DebateMessage] = field(default_factory=list)
    retrieved_evidence: List[Evidence] = field(default_factory=list)
    tool_outputs: List[ToolOutput] = field(default_factory=list)
    score: DebateScore = field(default_factory=DebateScore)
    profile: UserProfile = field(default_factory=UserProfile)
    metadata: Dict = field(default_factory=dict)
    plan: DebatePlan | None = None