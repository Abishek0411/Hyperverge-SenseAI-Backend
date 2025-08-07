# src/api/routes/integrity.py

from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from api.services import paste_detector, style_drift, similarity_check

router = APIRouter()

class PasteEvent(BaseModel):
    timestamp: float
    length: int

class TypingEvent(BaseModel):
    timestamp: float
    char_count: int

class GazeEvent(BaseModel):
    timestamp: float
    gaze: str  # "center", "left", "right", "offscreen"

class IntegrityRequest(BaseModel):
    user_id: int
    task_id: int
    answer_text: str
    keypress_events: List[TypingEvent]
    paste_events: List[PasteEvent]
    gaze_events: Optional[List[GazeEvent]] = []
    audio_blob_url: Optional[str] = None

@router.post("/integrity/analyze")
async def analyze_integrity(payload: IntegrityRequest):
    paste_result = paste_detector.detect_paste_burst(payload.paste_events)
    style_result = style_drift.detect_style_drift(payload.keypress_events)
    similarity_result = similarity_check.check_similarity(payload.answer_text)

    # Combine all results
    flag_summary = {
        "overall_flag": "high" if any([
            paste_result['flag'],
            style_result['flag'],
            similarity_result['flag']
        ]) else "low",
        "confidence": round(sum([
            paste_result['confidence'],
            style_result['confidence'],
            similarity_result['confidence']
        ]) / 3, 2),
        "flags": {
            "paste_burst": paste_result,
            "style_drift": style_result,
            "similarity": similarity_result
        }
    }

    return flag_summary
