# src/api/services/paste_detector.py

def detect_paste_burst(paste_events):
    for event in paste_events:
        if event.length > 200:
            return {
                "flag": True,
                "confidence": 0.95,
                "evidence": f"Pasted {event.length} chars in 1 sec"
            }
    return {
        "flag": False,
        "confidence": 0.2
    }
