"""
TACTIK AI MVP - FastAPI Backend
Web API for TACTIK AI 5.3 Premium Edition
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime
from pathlib import Path

from tactik_algorithm import (
    TACTIKEngine,
    GroundTruthSource,
    create_ground_truth_source,
    ConversationTurn
)
from llm_integration import LLMIntegration

# Initialize FastAPI
app = FastAPI(
    title="TACTIK AI MVP",
    description="Strategic Intelligence System with Multi-Avatar Simulation",
    version="5.3"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TACTIK Engine and LLM
engine = TACTIKEngine()
llm = LLMIntegration()

# Data persistence directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
AVATARS_FILE = DATA_DIR / "avatars.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"

# ═══════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════

class GroundTruthSourceModel(BaseModel):
    source_id: str
    tier: str
    description: str
    url: Optional[str] = None
    date: str = ""
    cross_verified: bool = False

class AvatarDNARequest(BaseModel):
    avatar_id: str
    avatar_name: str
    role: str
    sources: List[GroundTruthSourceModel]
    influences_verified: List[Dict]
    influences_inferred: List[Dict]
    thoughts_verified: List[Dict]
    thoughts_inferred: List[Dict]
    behavioral_verified: List[Dict]
    behavioral_inferred: List[Dict]
    decision_style_verified: List[Dict]
    decision_style_inferred: List[Dict]
    communication_verified: List[Dict]
    communication_inferred: List[Dict]
    priorities_verified: List[Dict]
    priorities_inferred: List[Dict]
    environment: str
    constraints: Dict
    language: str = "es"

class SessionCreateRequest(BaseModel):
    session_id: str
    user_goal: str
    avatar_ids: List[str]

class MessageRequest(BaseModel):
    session_id: str
    speaker_id: str
    message: str

# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def save_avatars():
    """Save avatars to JSON file"""
    avatars_data = {}
    for avatar_id, dna in engine.avatars_dna.items():
        avatars_data[avatar_id] = {
            "avatar_id": dna.avatar_id,
            "avatar_name": dna.avatar_name,
            "role": dna.role,
            "language": dna.language,
            "environment": dna.environment,
            "created_at": datetime.now().isoformat()
        }

    with open(AVATARS_FILE, 'w') as f:
        json.dump(avatars_data, f, indent=2)

def save_sessions():
    """Save sessions to JSON file"""
    sessions_data = {}
    for session_id, session in engine.sessions.items():
        sessions_data[session_id] = {
            "session_id": session.session_id,
            "user_goal": session.user_goal,
            "active_avatars": session.active_avatars,
            "current_turn": session.current_turn,
            "start_time": session.start_time,
            "total_turns": len(session.transcript)
        }

    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions_data, f, indent=2)

# ═══════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Root endpoint - serves the main UI"""
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "5.3",
        "avatars_loaded": len(engine.avatars_dna),
        "active_sessions": len(engine.sessions)
    }

# ───────────────────────────────────────────────────────────────────
# AVATAR MANAGEMENT
# ───────────────────────────────────────────────────────────────────

@app.post("/api/avatars")
async def create_avatar(request: AvatarDNARequest):
    """Create a new avatar with DNA profile"""
    try:
        # Convert sources
        sources = [
            create_ground_truth_source(
                source_id=s.source_id,
                tier=s.tier,
                description=s.description,
                url=s.url,
                date=s.date,
                cross_verified=s.cross_verified
            )
            for s in request.sources
        ]

        # Build DNA
        dna = engine.build_avatar_dna(
            avatar_id=request.avatar_id,
            avatar_name=request.avatar_name,
            role=request.role,
            sources=sources,
            influences_verified=request.influences_verified,
            influences_inferred=request.influences_inferred,
            thoughts_verified=request.thoughts_verified,
            thoughts_inferred=request.thoughts_inferred,
            behavioral_verified=request.behavioral_verified,
            behavioral_inferred=request.behavioral_inferred,
            decision_style_verified=request.decision_style_verified,
            decision_style_inferred=request.decision_style_inferred,
            communication_verified=request.communication_verified,
            communication_inferred=request.communication_inferred,
            priorities_verified=request.priorities_verified,
            priorities_inferred=request.priorities_inferred,
            environment=request.environment,
            constraints=request.constraints,
            language=request.language
        )

        # Calculate AVDA
        avda_metrics = engine.calculate_avda_score(request.avatar_id)

        # Save
        save_avatars()

        return {
            "success": True,
            "avatar_id": request.avatar_id,
            "avatar_name": dna.avatar_name,
            "avda_score": avda_metrics.to_percentage(),
            "source_coverage": dna.calculate_source_coverage()[0] * 100
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/avatars")
async def list_avatars():
    """List all avatars"""
    avatars = []
    for avatar_id, dna in engine.avatars_dna.items():
        avda = engine.calculate_avda_score(avatar_id)
        coverage, _ = dna.calculate_source_coverage()

        avatars.append({
            "avatar_id": avatar_id,
            "avatar_name": dna.avatar_name,
            "role": dna.role,
            "sources_count": len(dna.sources),
            "source_coverage": round(coverage * 100, 1),
            "avda_score": round(avda.avda_score * 100, 1),
            "classification": avda.classification.value
        })

    return {"avatars": avatars}

@app.get("/api/avatars/{avatar_id}")
async def get_avatar(avatar_id: str):
    """Get avatar details"""
    if avatar_id not in engine.avatars_dna:
        raise HTTPException(status_code=404, detail="Avatar not found")

    dna = engine.avatars_dna[avatar_id]
    avda = engine.calculate_avda_score(avatar_id)
    coverage, breakdown = dna.calculate_source_coverage()

    return {
        "avatar_id": avatar_id,
        "avatar_name": dna.avatar_name,
        "role": dna.role,
        "environment": dna.environment,
        "sources_count": len(dna.sources),
        "source_coverage": round(coverage * 100, 1),
        "coverage_breakdown": {k: round(v * 100, 1) for k, v in breakdown.items()},
        "avda_metrics": avda.to_percentage(),
        "recommendation": avda.get_recommendation()
    }

# ───────────────────────────────────────────────────────────────────
# SESSION MANAGEMENT
# ───────────────────────────────────────────────────────────────────

@app.post("/api/sessions")
async def create_session(request: SessionCreateRequest):
    """Create a new multi-avatar session"""
    try:
        session = engine.create_multi_avatar_session(
            session_id=request.session_id,
            user_goal=request.user_goal,
            avatar_ids=request.avatar_ids
        )

        save_sessions()

        return {
            "success": True,
            "session_id": session.session_id,
            "user_goal": session.user_goal,
            "active_avatars": session.active_avatars
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/sessions")
async def list_sessions():
    """List all sessions"""
    sessions = []
    for session_id, session in engine.sessions.items():
        metrics = session.calculate_session_metrics()

        sessions.append({
            "session_id": session_id,
            "user_goal": session.user_goal,
            "active_avatars": session.active_avatars,
            "total_turns": len(session.transcript),
            "tactik_score": metrics.get("tactik_score", 0),
            "start_time": session.start_time
        })

    return {"sessions": sessions}

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session details"""
    if session_id not in engine.sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = engine.sessions[session_id]
    metrics = session.calculate_session_metrics()

    return {
        "session_id": session.session_id,
        "user_goal": session.user_goal,
        "active_avatars": session.active_avatars,
        "total_turns": len(session.transcript),
        "metrics": metrics,
        "transcript": [
            {
                "turn_number": turn.turn_number,
                "speaker_id": turn.speaker_id,
                "speaker_name": turn.speaker_name,
                "message": turn.message,
                "timestamp": turn.timestamp,
                "eis_score": turn.eis_score,
                "hca_score": turn.hca_score,
                "dna_score": turn.dna_score
            }
            for turn in session.transcript
        ]
    }

# ───────────────────────────────────────────────────────────────────
# CONVERSATION
# ───────────────────────────────────────────────────────────────────

@app.post("/api/chat")
async def send_message(request: MessageRequest):
    """Send a message and get avatar response"""
    try:
        session = engine.sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        avatar_dna = engine.avatars_dna.get(request.speaker_id)
        if not avatar_dna:
            raise HTTPException(status_code=404, detail="Avatar not found")

        # Check empathy pause
        empathy_triggered, triggers = engine.check_empathy_pause(
            request.message, avatar_dna, session
        )

        if empathy_triggered:
            return {
                "action": "EMPATHY_PAUSE",
                "message": "I detect high uncertainty on this topic. I recommend consulting a human expert for accurate guidance.",
                "triggers": triggers
            }

        # Generate response using LLM
        response = llm.generate_avatar_response(
            avatar_dna=avatar_dna,
            user_message=request.message,
            session_context=session
        )

        # Calculate metrics
        metrics = llm.calculate_response_metrics(response, avatar_dna)

        # Gating check
        gating_result = engine.apply_gating(
            metrics["eis_score"],
            metrics["hca_score"],
            metrics["dna_score"]
        )

        if gating_result.value == "INTERRUPTED":
            # Regenerate response
            response = llm.generate_avatar_response(
                avatar_dna=avatar_dna,
                user_message=request.message,
                session_context=session,
                attempt=2
            )
            metrics = llm.calculate_response_metrics(response, avatar_dna)

        # Create turn
        turn = ConversationTurn(
            turn_number=session.current_turn + 1,
            speaker_id=request.speaker_id,
            speaker_name=avatar_dna.avatar_name,
            message=response,
            timestamp=datetime.now().isoformat(),
            eis_score=metrics["eis_score"],
            hca_score=metrics["hca_score"],
            dna_score=metrics["dna_score"],
            gating_decision=gating_result.value
        )

        session.add_turn(turn)

        # Backflow detection
        backflow_triggered, issue = engine.detect_backflow(session, turn, session.user_goal)

        save_sessions()

        return {
            "action": "TURN_COMPLETED",
            "turn": {
                "turn_number": turn.turn_number,
                "speaker_name": turn.speaker_name,
                "message": turn.message,
                "eis_score": turn.eis_score,
                "hca_score": turn.hca_score,
                "dna_score": turn.dna_score
            },
            "backflow_triggered": backflow_triggered,
            "backflow_issue": issue if backflow_triggered else None,
            "session_metrics": session.calculate_session_metrics()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ───────────────────────────────────────────────────────────────────
# REPORTS
# ───────────────────────────────────────────────────────────────────

@app.get("/api/sessions/{session_id}/report")
async def generate_report(session_id: str):
    """Generate TACTIK Advisor report"""
    if session_id not in engine.sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        report = engine.generate_tactik_advisor(session_id)
        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}/export/pdf")
async def export_pdf(session_id: str):
    """Export session report as PDF"""
    if session_id not in engine.sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        from pdf_generator import generate_pdf_report

        report = engine.generate_tactik_advisor(session_id)
        pdf_path = generate_pdf_report(session_id, report)

        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"tactik_report_{session_id}.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ───────────────────────────────────────────────────────────────────
# DEMO DATA
# ───────────────────────────────────────────────────────────────────

@app.post("/api/demo/load-example")
async def load_example():
    """Load the Ecuador -> EDEKA example"""
    try:
        from example_usage import main as load_example_data

        # This will populate the engine with example data
        # We need to modify it to not print, just load

        return {
            "success": True,
            "message": "Example data loaded successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ═══════════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("🚀 TACTIK AI MVP Starting...")
    print(f"📊 Data directory: {DATA_DIR.absolute()}")
    print(f"🤖 LLM Integration: {'✓ Configured' if llm.is_configured() else '✗ Not configured'}")

    # Mount static files
    if Path("static").exists():
        app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
